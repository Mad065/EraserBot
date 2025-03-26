import cv2
import numpy as np

# Cargar el diccionario de ArUco
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
PARAMS = cv2.aruco.DetectorParameters()
ultima_transformacion = None  # Guarda la última transformación válida


def detectar_aruco(frame):
    """ Detecta ArUco markers en un frame y devuelve sus coordenadas. """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detector = cv2.aruco.ArucoDetector(ARUCO_DICT, PARAMS)

    # Detectar ArUco markers
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None and len(ids) >= 4:
        coordenadas = {}
        for i in range(len(ids)):
            id_marker = ids[i][0]
            coordenadas[id_marker] = corners[i][0]  # Guarda los 4 puntos del marcador

            # Dibujar los bordes del marcador en la imagen original
            cv2.polylines(frame, [np.int32(corners[i][0])], True, (0, 255, 0), 2)
            centro_x = int(np.mean(corners[i][0][:, 0]))
            centro_y = int(np.mean(corners[i][0][:, 1]))
            cv2.putText(frame, str(id_marker), (centro_x, centro_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return coordenadas, frame, corners

    return None, frame, None


def ordenar_esquinas(coordenadas):
    """ Ordena los 4 puntos de ArUco en el orden:
        [esquina superior izquierda, superior derecha, inferior derecha, inferior izquierda]
    """
    if len(coordenadas) != 4:
        return None

    # Obtener los centros de cada marcador
    centros = {id_marker: np.mean(puntos, axis=0) for id_marker, puntos in coordenadas.items()}

    # Convertir en lista y ordenar por coordenada Y (de arriba a abajo)
    centros_ordenados = sorted(centros.items(), key=lambda x: x[1][1])

    # Las dos primeras son las superiores, las dos últimas son las inferiores
    arriba = sorted(centros_ordenados[:2], key=lambda x: x[1][0])  # Ordenar por X (izq a der)
    abajo = sorted(centros_ordenados[2:], key=lambda x: x[1][0])  # Ordenar por X (izq a der)

    # Obtener los puntos en el orden correcto
    orden_final = [
        coordenadas[arriba[0][0]],  # Superior izquierda
        coordenadas[arriba[1][0]],  # Superior derecha
        coordenadas[abajo[1][0]],  # Inferior derecha
        coordenadas[abajo[0][0]],  # Inferior izquierda
    ]

    return np.array([p[0] for p in orden_final], dtype="float32")


def calcular_transformacion_frontal(pts, nuevo_ancho=600, nuevo_alto=400):
    """ Calcula la matriz de transformación para generar una vista de frente. """
    dst = np.array([
        [0, 0],  # Superior izquierda
        [nuevo_ancho - 1, 0],  # Superior derecha
        [nuevo_ancho - 1, nuevo_alto - 1],  # Inferior derecha
        [0, nuevo_alto - 1]  # Inferior izquierda
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(pts, dst)

    return M, (nuevo_ancho, nuevo_alto)


def transformar_perspectiva(frame, coordenadas, corners):
    """ Aplica la transformación de perspectiva para mostrar una vista de frente. """
    global ultima_transformacion

    if coordenadas is not None and len(coordenadas) == 4:
        pts = ordenar_esquinas(coordenadas)
        if pts is not None:
            M, size = calcular_transformacion_frontal(pts)
            ultima_transformacion = (M, size)  # Guardar transformación válida

    if ultima_transformacion is not None:
        M, size = ultima_transformacion
        transformed = cv2.warpPerspective(frame, M, size)

        # Dibujar los ArUco en la imagen transformada
        if corners is not None:
            for marker in corners:
                puntos_transformados = cv2.perspectiveTransform(marker, M)
                cv2.polylines(transformed, [np.int32(puntos_transformados)], True, (0, 255, 0), 2)

        return transformed

    return None


# Inicializar la captura de video
cap = cv2.VideoCapture(1)  # Cambia a la ruta del video si no usas webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame")
        break

    # Detectar los ArUco markers
    coordenadas, frame_con_aruco, corners = detectar_aruco(frame)

    # Aplicar la transformación de perspectiva
    imagen_transformada = transformar_perspectiva(frame, coordenadas, corners)

    # Mostrar los resultados
    cv2.imshow("Detección de ArUco", frame_con_aruco)

    if imagen_transformada is not None:
        cv2.imshow("Transformación de Perspectiva", imagen_transformada)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
