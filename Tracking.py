import cv2
import numpy as np

# Recibir los frames del video ya transformado detectar el aruco 0 y despues hacer tracking con este
def tracking(frame, coordenadas, ids):
    coordenada_aruco = None
    id_aruco = None

    # Obtener el aruco con id 0
    if ids is not None:
        for i in range(len(ids)):
            if ids[i][0] == 0:
                coordenada_aruco = coordenadas[i]
                id_aruco = ids[i][0]
                break

    # Lista para almacenar la trayectoria del objeto
    trayectoria = []

    # Tracking
    if id_aruco == 0 and coordenada_aruco is not None:
        # Crear el tracker
        tracker = cv2.TrackerMIL.create()
        print("crear tracker")

        # Crear un rectángulo delimitador
        bbox = cv2.boundingRect(np.array(coordenada_aruco))

        # Inicializar el tracker
        tracker.init(frame, bbox)

        # Actualizar el tracker
        success, bbox = tracker.update(frame)

        if success:
            x, y, w, h = [int(i) for i in bbox]

            # Guardar el centro del objeto (como coordenada de la trayectoria)
            centro = (x + w // 2, y + h // 2)
            trayectoria.append(centro)

            # Dibujar la trayectoria
            for i in range(1, len(trayectoria)):
                cv2.line(frame, trayectoria[i-1], trayectoria[i], (255, 0, 0), 2)  # Azul, grosor 2

            return frame
        return frame

    return frame