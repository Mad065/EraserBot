import cv2
import Tracking
import Transformation

cap = cv2.VideoCapture(0)
frame_tracking = None
frame_blank = None
transformation = None

if not cap.isOpened():
    print("Error: no se pudo abrir la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame")
        break

    # 1) Detección de todos los ArUco
    coordenadas, frame_aruco, corners, ids = Transformation.detectar_aruco(frame, False)
    cv2.imshow("Deteccion aruco", frame_aruco)

    # Inicializa imagen_transformada
    imagen_transformada = None

    # 2) Transformación de perspectiva solo si tenemos al menos 4 esquinas
    # Para cambiar perspectiva volver a poner None en transformation
    if coordenadas and transformation is None:
        transformation = Transformation.obtener_perspectiva(coordenadas)
        print("Transformacion establecida")
    elif transformation is None:
        print("Error: no se pudo obtener la perspectiva")


    imagen_transformada = Transformation.aplicar_perspectiva(frame_aruco, transformation)

    if transformation is not None and imagen_transformada is not None:
        cv2.imshow("Imagen transformada", imagen_transformada)
    else:
        print("Error: no se pudo aplicar la perspectiva")
        imagen_transformada = frame_aruco


    # 3) Detección del ArUco específico en la imagen transformada
    coordenadas_id, frame_con_id, corners_id, ids_id = Transformation.detectar_aruco_id(imagen_transformada, 0, True)
    cv2.imshow("Deteccion aruco con id 0", frame_con_id)

    # 4) Tracking — aquí Tracking.tracking devolverá siempre dos frames válidos
    frame_tracking, frame_blank = Tracking.tracking(frame_con_id, coordenadas_id, ids_id)
    cv2.imshow("Tracking con fondo blanco", frame_blank)
    cv2.imshow("Tracking con fondo original", frame_tracking)

    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
