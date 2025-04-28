import cv2
import numpy as np

tracker = None
trayectoria = []
inicializado = False


# Recibir los frames del video ya transformado detectar el aruco 0 y despues hacer tracking con este
def tracking(frame, coordenadas, ids):
    global tracker, trayectoria, inicializado

    if not inicializado:
        # Buscar el ArUco con ID 0
        coordenada_aruco = None
        if ids is not None:
            for i in range(len(ids)):
                if ids[i][0] == 0:
                    coordenada_aruco = coordenadas[i]
                    break

        if coordenada_aruco is not None:
            tracker = cv2.TrackerMIL.create()
            bbox = cv2.boundingRect(np.array(coordenada_aruco))
            tracker.init(frame, bbox)
            inicializado = True

    if inicializado and tracker is not None:
        success, bbox = tracker.update(frame)

        if success:
            x, y, w, h = [int(i) for i in bbox]
            centro = (x + w // 2, y + h // 2)
            trayectoria.append(centro)

            # Dibujar trayectoria
            # TODO Hacer que se dibuje en un panel blanco y devolver frame con video y otro con panel blanco
            for i in range(1, len(trayectoria)):
                cv2.line(frame, trayectoria[i-1], trayectoria[i], (255, 0, 0), 2)
                print("dibujar trayectoria")

            # Dibujar bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame