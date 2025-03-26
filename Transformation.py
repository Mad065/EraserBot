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


# Corregir orientacion
def ordenar_esquinas(coordenadas):
    """ Ordena los 4 puntos de ArUco en el orden:
        [esquina superior izquierda, superior derecha, inferior derecha, inferior izquierda]
    """
    if len(coordenadas) != 4:
        return None

    # Inicializamos listas para las coordenadas de las esquinas
    esquina_superior_izquierda = None
    esquina_superior_derecha = None
    esquina_inferior_derecha = None
    esquina_inferior_izquierda = None

    # Iteramos solo sobre los valores (las coordenadas) del diccionario
    for id_marker, puntos in coordenadas.items():
        for punto in puntos:  # puntos es un array con 4 coordenadas
            # Verificar que cada punto sea un arreglo con 2 valores (x, y)
            if isinstance(punto, np.ndarray) and punto.shape[0] == 2:
                x, y = punto[0], punto[1]
            elif isinstance(punto, list) and len(punto) == 2:
                x, y = punto[0], punto[1]
            else:
                print("Error: cada punto debe ser un arreglo con 2 valores (x, y).")
                return None

            # Determinamos las esquinas según las condiciones de los valores de x, y
            if esquina_superior_izquierda is None or (x + y) < (esquina_superior_izquierda[0] + esquina_superior_izquierda[1]):
                esquina_superior_izquierda = (x, y)
            if esquina_superior_derecha is None or (x - y) < (esquina_superior_derecha[0] - esquina_superior_derecha[1]):
                esquina_superior_derecha = (x, y)
            if esquina_inferior_derecha is None or (x + y) > (esquina_inferior_derecha[0] + esquina_inferior_derecha[1]):
                esquina_inferior_derecha = (x, y)
            if esquina_inferior_izquierda is None or (x - y) > (esquina_inferior_izquierda[0] - esquina_inferior_izquierda[1]):
                esquina_inferior_izquierda = (x, y)

    # Devolver las esquinas en el orden correcto
    return np.array([
        esquina_superior_izquierda,  # Superior izquierda
        esquina_superior_derecha,    # Superior derecha
        esquina_inferior_derecha,    # Inferior derecha
        esquina_inferior_izquierda   # Inferior izquierda
    ], dtype="float32")


def distancia(p1, p2):
    """Calcula la distancia Euclidiana entre dos puntos"""
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def calcular_transformacion_frontal(pts, nuevo_ancho=1000, nuevo_alto=800):
    """ Calcula la matriz de transformación para generar una vista de frente, ajustando el tamaño real del marcador y recortando la parte inferior """

    # Obtener las esquinas del marcador
    esquina_superior_izquierda = pts[0]
    esquina_superior_derecha = pts[1]
    esquina_inferior_derecha = pts[2]
    esquina_inferior_izquierda = pts[3]

    # Calcular el ancho y el alto reales del marcador usando la distancia euclidiana
    ancho_real = distancia(esquina_superior_izquierda, esquina_superior_derecha)
    alto_real = distancia(esquina_superior_izquierda, esquina_inferior_izquierda)

    # Ajustar las coordenadas de destino para aplicar la transformación
    dst = np.array([
        [0, 0],  # Superior izquierda
        [ancho_real - 1, 0],  # Superior derecha
        [ancho_real - 1, alto_real - 1],  # Inferior derecha
        [0, alto_real - 1]  # Inferior izquierda
    ], dtype="float32")

    # Calcular la matriz de transformación
    M = cv2.getPerspectiveTransform(pts, dst)

    # Aplicar la transformación de perspectiva (esto se hace afuera de la función principal)
    size = (int(ancho_real), int(alto_real))

    return M, size, (nuevo_ancho, nuevo_alto)


def transformar_perspectiva(frame, coordenadas, corners):
    global ultima_transformacion

    if coordenadas is not None and len(coordenadas) == 4:
        pts = ordenar_esquinas(coordenadas)
        if pts is not None:
            M, size, dimensiones_reales = calcular_transformacion_frontal(pts)
            ultima_transformacion = (M, size)  # Guardar transformación válida
            print(f"Tamaño real del marcador: {dimensiones_reales} (Ancho, Alto)")

    if ultima_transformacion is not None:
        M, size = ultima_transformacion
        transformed = cv2.warpPerspective(frame, M, size)

        # Aplicar la rotación al video completo
        rotated = cv2.transpose(transformed)  # Transponer la imagen para rotarla 90 grados

        return rotated

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
