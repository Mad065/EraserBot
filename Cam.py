import cv2
import numpy as np

esp32 = "http://192.168.1.15:81/stream"

# Cargar el video o la cámara
cap = cv2.VideoCapture(esp32)  # Usar 0 para la cámara predeterminada

M = None  # Matriz de transformación (se calculará solo una vez)
width, height = 400, 600  # Dimensiones deseadas para la hoja transformada


def detectar_circulos(gray):
    """Detecta círculos negros en la imagen (marcas de esquina)."""
    circles = None
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
        param1=50, param2=30, minRadius=5, maxRadius=30
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        return circles[0, :]  # Regresar los círculos detectados

    return []


while True:
    # Leer un frame del video
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame")
        break

    # Solo calcular la transformación una vez
    if M is None:
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar círculos (marcas en esquinas)
        circles = detectar_circulos(gray)

        # Verificar si se detectaron al menos 4 círculos
        if len(circles) >= 4:
            # Ordenar las esquinas en sentido arriba-izquierda, arriba-derecha, abajo-derecha, abajo-izquierda
            sorted_circles = sorted(circles, key=lambda c: (c[1], c[0]))  # Ordenar por Y y luego X
            pts = np.array([c[:2] for c in sorted_circles[:4]], dtype="float32")  # Tomar las primeras 4 coordenadas

            # Puntos de destino para la transformación
            dst = np.array([
                [0, 0],
                [width - 1, 0],
                [width - 1, height - 1],
                [0, height - 1]
            ], dtype="float32")

            # Calcular la matriz de transformación solo una vez
            M = cv2.getPerspectiveTransform(pts, dst)

            # Dibujar los círculos detectados en la imagen
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

    # Si la transformación ya fue calculada, aplicarla directamente
    if M is not None:
        warped = cv2.warpPerspective(frame, M, (width, height))
        cv2.imshow("Hoja Transformada", warped)
    else:
        cv2.imshow("Frame", frame)  # Mostrar frame normal si aún no hay transformación

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
