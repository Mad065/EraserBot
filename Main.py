import cv2
import numpy as np
import Tracking
import Transformation

# Inicializar la captura de video
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame")
        break

    # Detectar los ArUco markers
    coordenadas, frame_con_aruco, corners, ids = Transformation.detectar_aruco(frame)

    # Aplicar la transformación de perspectiva
    #imagen_transformada = Transformation.transformar_perspectiva(frame, coordenadas, corners)
    # Resultados deteccion de arUco
    #cv2.imshow("Detección de ArUco", frame_con_aruco)

    # Mostrar la imagen transformada
    #if imagen_transformada is not None:
    #    cv2.imshow("Transformación de Perspectiva", imagen_transformada)

    # Tracking de los arUco
    frame_tracking = Tracking.tracking(frame, coordenadas, ids)

    # Mostrar el frame con el rectángulo y la trayectoria
    cv2.imshow("Tracking", frame_tracking)
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Liberar recursos al finalizar
cap.release()
cv2.destroyAllWindows()