import cv2
import numpy as np

# Inicializar la cámara
cap = cv2.VideoCapture(0)  # Usar 0 para la cámara predeterminada

# Crear una imagen en blanco para dibujar la trayectoria
trajectory_image = np.ones((480, 640, 3), dtype=np.uint8) * 255  # Fondo blanco

# Lista para almacenar las coordenadas de la trayectoria
trajectory_points = []

while True:
    # Leer un frame del video
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a espacio de color HSV para segmentación por color
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de color para la marca (ajusta estos valores según tu marca)
    lower_color = np.array([25, 50, 50])  # Valores HSV mínimos (verde claro)
    upper_color = np.array([85, 255, 255])  # Valores HSV máximos (verde oscuro)

    # Crear una máscara para la marca
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se detecta al menos un contorno
    if contours:
        # Encontrar el contorno más grande (asumimos que es la marca)
        largest_contour = max(contours, key=cv2.contourArea)

        # Obtener el centro de la marca
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Guardar las coordenadas del centro
            trajectory_points.append((cx, cy))

            # Dibujar un círculo en la posición actual de la marca
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    # Dibujar la trayectoria sobre el fondo blanco
    for i in range(1, len(trajectory_points)):
        cv2.line(trajectory_image, trajectory_points[i - 1], trajectory_points[i], (0, 0, 255), 2)

    # Mostrar el frame original con la marca detectada
    cv2.imshow("Frame", frame)

    # Mostrar la trayectoria sobre el fondo blanco
    cv2.imshow("Trayectoria", trajectory_image)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()