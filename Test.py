import cv2
import Tracking
import Transformation

cap = cv2.VideoCapture(1)
frame_tracking = None
frame_blank = None

if not cap.isOpened():
    print("Error: no se pudo abrir la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame")
        break

    # 1) Detección de todos los ArUco
    coordenadas, frame_aruco, corners, ids = Transformation.detectar_aruco(frame, True)
    cv2.imshow("Deteccion aruco", frame)

    # Inicializa imagen_transformada
    imagen_transformada = None

    # 2) Transformación de perspectiva solo si tenemos al menos 4 esquinas
    if coordenadas:
        imagen_transformada = Transformation.transformar_perspectiva(frame, coordenadas, corners)
        if imagen_transformada is not None and imagen_transformada.size > 0:
            cv2.imshow("Imagen transformada con perspectiva", imagen_transformada)
            print("Transformar perspectiva")
        else:
            print("Error: la transformación de perspectiva falló.")
            imagen_transformada = frame_aruco
    else:
        print("No se detectaron suficientes coordenadas ArUco.")
        imagen_transformada = frame_aruco

    # 3) Detección del ArUco específico en la imagen transformada
    coordenadas_id, frame_con_id, corners_id, ids_id = Transformation.detectar_aruco_id(imagen_transformada, 0, True)
    cv2.imshow("Deteccion aruco con id 0", frame_con_id)

    # 4) Tracking — aquí Tracking.tracking devolverá siempre dos frames válidos
    if coordenadas_id:
        frame_tracking, frame_blank = Tracking.tracking(frame_con_id, coordenadas_id, ids_id)
        cv2.imshow("Tracking con fondo blanco", frame_blank)
        cv2.imshow("Tracking con fondo original", frame_tracking)

    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
