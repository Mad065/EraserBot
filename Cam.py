import cv2
import numpy as np

esp32 = "http://192.168.1.15:81/stream"

# Cargar el video o la cámara
cap = cv2.VideoCapture(esp32)  # Usar 0 para la cámara predeterminada

M = None  # Matriz de transformación (se calculará solo una vez)
width, height = 400, 600  # Dimensiones deseadas para la hoja transformada

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

        # Aplicar un desenfoque para reducir el ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detectar bordes con Canny
        edges = cv2.Canny(blurred, 50, 150)

        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            epsilon = 0.02 * cv2.arcLength(largest_contour, True)
            approx = cv2.approxPolyDP(largest_contour, epsilon, True)

            # Verificar si el contorno tiene 4 esquinas (es un cuadrilátero)
            if len(approx) == 4:
                pts = np.array([point[0] for point in approx], dtype="float32")

                # Puntos de destino para la transformación
                dst = np.array([
                    [0, 0],
                    [width - 1, 0],
                    [width - 1, height - 1],
                    [0, height - 1]
                ], dtype="float32")

                # Calcular la matriz de transformación solo una vez
                M = cv2.getPerspectiveTransform(pts, dst)

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
