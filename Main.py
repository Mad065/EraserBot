import asyncio
import cv2
import Connection
import Tracking
import Transformation
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from kivy.clock import Clock

# TODO Custom buttons

# App kivy
class EraserBotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Layout
        self.main_layout = None

        # Buttons
        self.fps_button = None
        self.cam_button = None

        # Video
        self.img = None
        self.frame_tracking = None
        self.frame_blank = None

        # Variables
        self.cam = None
        self.cap = None
        self.fps = None
        self.display = None

        # Recording
        self.recording = None
        self.video_writer = None
        self.filename_input = None

        # Capture
        self.num_capture = None

        # Popup
        self.popup = None

    def build(self):
        Window.size = (800, 600)

        self.title = "EraserBot"
        # Widget Image para Visualizar video
        self.img = Image()
        self.cam = 1
        self.cap = cv2.VideoCapture(self.cam)
        self.fps = 30
        self.display = False
        self.recording = False

        Clock.schedule_interval(self.update_img, 1.0 / self.fps)

        self.build_main_layout()

        return self.main_layout

    def control_start(self):
        if not self.recording:
            fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter('video_guardado.avi', fourcc, self.fps, (int(self.cap.get(3)), int(self.cap.get(4))))
            self.recording = True
            print("Grabación iniciada...")

    def control_pause(self):
        if self.recording:
            self.recording = False

    def control_stop(self):
        if self.recording:
            self.recording = False
            self.show_filename_popup()

    def control_capture(self):
        ret, frame = self.cap.read()
        if ret:
            self.num_capture += 1
            filename = f"capture_{self.num_capture}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Captura guardada como {filename}")

    def control_erase(self):
        # Reiniciar trayectoria guardada
        Tracking.reset_trayectoria()
        # Borrar en pizarron fisico
        asyncio.run(Connection.eraser())

    def control_display(self):
        self.display = not self.display

        if self.display:
            self.build_display_layout()
        else:
            self.build_main_layout()

    def change_main_layout_display_layout(self):
        pass

    def update_img(self, dt):  # ahora acepta dt
        if not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            print("Error al capturar el frame")
            return

        # 1) Detección de todos los ArUco
        coordenadas, frame_aruco, corners, ids = Transformation.detectar_aruco(frame)

        # 2) Transformación de perspectiva solo si tenemos al menos 4 esquinas
        imagen_transformada = None
        if coordenadas:
            imagen_transformada = Transformation.transformar_perspectiva(frame, coordenadas, corners)

        # Si la transformación devolvió None, volvemos a usar el frame con ArUco
        if imagen_transformada is None:
            imagen_transformada = frame_aruco

        # 3) Detección del ArUco específico en la imagen transformada
        coordenadas_id, frame_con_id, corners_id, ids_id = Transformation.detectar_aruco_id(imagen_transformada, 0)

        # 4) Tracking — aquí Tracking.tracking devolverá siempre dos frames válidos
        self.frame_tracking, self.frame_blank = Tracking.tracking(
            frame_con_id, coordenadas_id, ids_id
        )

        # 5) Selección del frame a mostrar
        show_frame = self.frame_blank if self.display else self.frame_tracking

        # 6) Conversión BGR → RGB y subida a la textura de Kivy
        rgb = cv2.cvtColor(show_frame, cv2.COLOR_BGR2RGB)
        texture = Texture.create(size=(rgb.shape[1], rgb.shape[0]), colorfmt='rgb')
        texture.blit_buffer(rgb.flatten(), colorfmt='rgb', bufferfmt='ubyte')
        self.img.texture = texture

        # 7) Si estamos grabando, escribir el frame original (no la textura)
        if self.recording and self.video_writer:
            self.video_writer.write(frame)

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

    def show_filename_popup(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.filename_input = TextInput(hint_text='Nombre del archivo', multiline=False)
        save_button = Button(text="Guardar", size_hint=(1, 0.3))
        layout.add_widget(self.filename_input)
        layout.add_widget(save_button)

        self.popup = Popup(title="Guardar video", content=layout, size_hint=(None, None), size=(400, 200))
        save_button.bind(on_press=self.save_video)
        self.popup.open()

    def save_video(self, instance):
        filename = self.filename_input.text.strip()
        if filename == '':
            filename = 'video_guardado'  # nombre por defecto

        filename += '.mp4'  # Añadir extensión .mp4 si no lo puso

        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

        # Aquí podrías mover/renombrar el archivo temporal, si quieres
        print(f"Video guardado como: {filename}")

        self.popup.dismiss()

    def build_main_layout(self):
        self.main_layout = BoxLayout(orientation="vertical")
        head_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=60)
        controls_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)

        # Título
        head_title = Label(text="EraserBot", size_hint_x=0.4)

        # Dropdown para FPS
        fps_dropdown = DropDown()
        for fps_option in ['30 fps', '60 fps']:
            btn = Button(text=fps_option, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn_instance: fps_dropdown.select(btn_instance.text))
            fps_dropdown.add_widget(btn)

        self.fps_button = Button(text='fps', size_hint=(None, None), size=(200, 50))
        self.fps_button.bind(on_release=fps_dropdown.open)
        fps_dropdown.bind(on_select=lambda instance, value: self.update_fps(fps=value))

        # Dropdown para cámara
        cam_dropdown = DropDown()
        for cam_option in range(6):
            btn = Button(text=str(cam_option), size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn_instance: cam_dropdown.select(btn_instance.text))
            cam_dropdown.add_widget(btn)

        self.cam_button = Button(text='cámara', size_hint=(None, None), size=(200, 50))
        self.cam_button.bind(on_release=cam_dropdown.open)
        cam_dropdown.bind(on_select=lambda instance, value: self.update_cam(cam=value))

        # Agregar widgets al head_layout
        head_layout.add_widget(self.fps_button)
        head_layout.add_widget(head_title)
        head_layout.add_widget(self.cam_button)

        # Agregar head y vista de imagen al layout principal
        self.main_layout.add_widget(head_layout)

        # Asegúrate de tener una propiedad self.img inicializada antes de este método
        self.main_layout.add_widget(self.img)

        # Botones de control
        control_buttons = [
            ("Iniciar", self.control_start),
            ("Pausar", self.control_pause),
            ("Detener", self.control_stop),
            ("Captura", self.control_capture),
            ("Borrar", self.control_erase),
            ("Presentar", self.control_display),
        ]

        for text, callback in control_buttons:
            btn = Button(text=text, size_hint_y=None, height=40)
            btn.bind(on_press=callback)
            controls_layout.add_widget(btn)

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

if __name__ == '__main__':
    EraserBotApp().run()