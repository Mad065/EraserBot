import cv2
import numpy as np
import Tracking
import Transformation
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.clock import Clock

# TODO Custom buttons

# TODO Programar sistema de grabacion

# App kivy
class EraserBotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = None
        self.img = None
        self.cam = None
        self.cap = None
        self.fps = None
        self.fps_button = None
        self.cam_button = None
        self.display = None

    def build(self):
        Window.size = (800, 600)

        self.title = "EraserBot"
        # Widget Image para Visualizar video
        self.img = Image()
        self.cam = 1
        self.cap = cv2.VideoCapture(self.cam)
        self.fps = 30
        self.display = False

        Clock.schedule_interval(self.update_img, 1.0 / self.fps)

        self.build_main_layout()

        return self.main_layout

    def control_start(self):
        # TODO Iniciar a grabar video (se graba con panel blanco y se muestra con video)
        pass

    def control_pause(self):
        # TODO Pausar la grabacion del video
        pass

    def control_stop(self):
        # TODO Detener la grabacion del video
        pass

    def control_capture(self):
        # TODO Hacer una captura del video (se captura con panel blanco)
        pass

    def control_erase(self):
        # TODO Borrar los trazos en el video y en el pizarron
        pass

    def control_display(self):
        self.display = not self.display

        if self.display:
            self.build_display_layout()
        else:
            self.build_main_layout()

    def change_main_layout_display_layout(self):
        pass

    def update_img(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Error al capturar el frame")

            # Detectar los ArUco markers de las esquinas
            coordenadas, frame_con_aruco, corners, ids = Transformation.detectar_aruco(frame)

            # Aplicar la transformación de perspectiva
            imagen_transformada = Transformation.transformar_perspectiva(frame, coordenadas, corners)

            # Volver a detectar los aruco en la imagen ya transformada
            coordenadas, frame_con_aruco, corners, ids = Transformation.detectar_aruco_id(imagen_transformada, 0)

            # Tracking del ArUco
            frame_tracking, frame_blank = Tracking.tracking(frame_con_aruco, coordenadas, ids)

            # Crear una textura
            if self.display:
                texture = Texture.create(size=(frame_blank.shape[1], frame_blank.shape[0]), colorfmt='rgb')
                texture.blit_buffer(frame_blank.flatten(), colorfmt='rgb', bufferfmt='ubyte')
            else:
                texture = Texture.create(size=(frame_tracking.shape[1], frame_tracking.shape[0]), colorfmt='rgb')
                texture.blit_buffer(frame_tracking.flatten(), colorfmt='rgb', bufferfmt='ubyte')


            self.img.texture = texture

    def update_fps(self, fps):
        # Establecer texto en fps_button
        self.fps_button.text = str(fps)
        # Actualizar fps
        self.fps = fps

    def update_cam(self, cam):
        # Establecer texto en cam_button
        self.cam_button.text = str(cam)
        # Actualizar cam  y cap
        self.cam = cam
        self.cap = cv2.VideoCapture(self.cam)

    def build_main_layout(self):
        self.main_layout = BoxLayout(orientation="vertical")
        head_layout = BoxLayout(orientation="horizontal")
        controls_layout = BoxLayout(orientation="horizontal")

        # Elementos para el head
        fps_dropdown = DropDown()
        head_title = Label(text="EraserBot")
        cam_dropdown = DropDown()

        # Añadir opciones al fps_dropdown
        for fps_option in ['30 fps', '60 fps']:
            btn = Button(text=fps_option, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: fps_dropdown.select(btn.text))
            fps_dropdown.add_widget(btn)

        # Botón despliegue fps_button
        self.fps_button = Button(text='Selecciona la cantidad de fps', size_hint=(None, None), size=(200, 50))
        self.fps_button.bind(on_release=fps_dropdown.open)

        fps_dropdown.bind(on_select=lambda instance, value: self.update_fps(fps=value))

        head_layout.add_widget(self.fps_button)

        head_layout.add_widget(head_title)

        # Añadir opciones al cam_dropdown
        for cam_option in [0, 1, 2, 3, 4, 5]:
            btn = Button(text=cam_option, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: cam_dropdown.select(btn.text))
            cam_dropdown.add_widget(btn)

        # Botón despliegue cam_button
        self.cam_button = Button(text='Selecciona una camara', size_hint=(None, None), size=(200, 50))
        self.cam_button.bind(on_release=cam_dropdown.open)

        cam_dropdown.bind(on_select=lambda instance, value: self.update_cam(cam=value))

        head_layout.add_widget(self.cam_button)

        self.main_layout.add_widget(head_layout)

        self.main_layout.add_widget(self.img)

        # Elementos para los controles
        start_button = Button(text="Iniciar", size_hint_y=None, height=40, on_press=self.control_start)
        pause_button = Button(text="Pausar", size_hint_y=None, height=40, on_press=self.control_pause)
        stop_button = Button(text="Detener", size_hint_y=None, height=40, on_press=self.control_stop)
        capture_button = Button(text="Captura", size_hint_y=None, height=40, on_press=self.control_capture)
        erase_button = Button(text="Borrar", size_hint_y=None, height=40, on_press=self.control_erase)
        display_button = Button(text="Presentar", size_hint_y=None, height=40, on_press=self.control_display)

        controls_layout.add_widget(start_button)
        controls_layout.add_widget(pause_button)
        controls_layout.add_widget(stop_button)
        controls_layout.add_widget(capture_button)
        controls_layout.add_widget(erase_button)
        controls_layout.add_widget(display_button)

        self.main_layout.add_widget(controls_layout)

    def build_display_layout(self):
        self.main_layout = BoxLayout(orientation="vertical")
        controls_layout = BoxLayout(orientation="horizontal")

        self.main_layout.add_widget(self.img)

        # Elementos para los controles
        display_button = Button(text="Terminar presentacion", size_hint_y=None, height=40, on_press=self.control_display)

        controls_layout.add_widget(display_button)

        self.main_layout.add_widget(controls_layout)

    def on_stop(self):
        self.cap.release()