import cv2
import numpy as np

tracker = None
trayectoria = []
inicializado = False


# Recibir los frames del video ya transformado detectar el aruco 0 y despues hacer tracking con este
def tracking(frame, coordenadas, ids):
    global tracker, trayectoria, inicializado

    frame_blank = np.ones_like(frame) * 255

    if coordenadas and 0 in coordenadas:
        coordenada_aruco = coordenadas[0]

        if coordenada_aruco is not None:
            tracker = cv2.TrackerMIL.create()
            bbox = cv2.boundingRect(np.array(coordenada_aruco))
            tracker.init(frame, bbox)
            inicializado = True
            frame, frame_blank = add_trayectoria(bbox, frame, frame_blank)

    elif inicializado and tracker is not None:
        success, bbox = tracker.update(frame)

        if success:
            frame, frame_blank = add_trayectoria(bbox, frame, frame_blank)

    return frame, frame_blank

def reset_trayectoria():
    global trayectoria
    trayectoria = []

def add_trayectoria(bbox, frame, frame_blank):
    global trayectoria

    x, y, w, h = [int(i) for i in bbox]
    centro = (x + w // 2, y + h // 2)
    trayectoria.append(centro)

    # Dibujar trayectoria en frame original
    for i in range(1, len(trayectoria)):
        cv2.line(frame, trayectoria[i - 1], trayectoria[i], (255, 0, 0), 2)
        print("dibujar trayectoria en frame original")

    # Dibujar trayectoria en frame blanco
    for i in range(1, len(trayectoria)):
        cv2.line(frame_blank, trayectoria[i - 1], trayectoria[i], (255, 0, 0), 2)
        print("dibujar trayectoria en frame blanco")

    # Dibujar bbox
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame, frame_blank