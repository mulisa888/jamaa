from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class ChatScreen(Screen):
    show_emoji = BooleanProperty(False)
    
    def toggle_emoji(self):
        self.show_emoji = not self.show_emoji
    
    def insert_emoji(self, emoji):
        app = App.get_running_app()
        input_field = self.ids.get("message_input")
        if input_field:
            input_field.text += emoji
    
    def start_voice_recording(self):
        app = App.get_running_app()
        
        if app.is_recording:
            duration = app.stop_recording()
            self._show_voice_note_popup(duration)
        else:
            app.start_recording()
    
    def _show_voice_note_popup(self, duration):
        content = BoxLayout(orientation="vertical", padding="15dp", spacing="10dp")
        
        content.add_widget(Label(
            text=f"Voice Note Recorded",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height="30dp"
        ))
        
        content.add_widget(Label(
            text=f"Duration: {duration}",
            font_size="14sp",
            size_hint_y=None,
            height="25dp"
        ))
        
        btn_layout = BoxLayout(size_hint_y=None, height="45dp", spacing="10dp")
        
        cancel_btn = Button(text="Cancel", font_size="14sp")
        btn_layout.add_widget(cancel_btn)
        
        send_btn = Button(
            text="Send Voice Note",
            font_size="14sp",
            background_color=(0.15, 0.6, 0.35, 1)
        )
        btn_layout.add_widget(send_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title="",
            content=content,
            size_hint=(0.75, 0.35),
            auto_dismiss=False
        )
        
        def send_voice(*args):
            app = App.get_running_app()
            app.send_voice_note("voice_note_" + duration, duration)
            popup.dismiss()
        
        cancel_btn.bind(on_release=popup.dismiss)
        send_btn.bind(on_release=send_voice)
        
        popup.open()
    
    def attach_media(self):
        content = BoxLayout(orientation="vertical", padding="15dp", spacing="10dp")
        
        content.add_widget(Label(
            text="Select Media",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height="30dp"
        ))
        
        btn_layout = BoxLayout(size_hint_y=None, height="120dp", spacing="10dp")
        
        photo_btn = Button(
            text="Photo",
            font_size="14sp",
            background_color=(0.3, 0.55, 0.85, 1)
        )
        btn_layout.add_widget(photo_btn)
        
        video_btn = Button(
            text="Video",
            font_size="14sp",
            background_color=(0.85, 0.35, 0.55, 1)
        )
        btn_layout.add_widget(video_btn)
        
        file_btn = Button(
            text="File",
            font_size="14sp",
            background_color=(0.5, 0.5, 0.5, 1)
        )
        btn_layout.add_widget(file_btn)
        
        content.add_widget(btn_layout)
        
        cancel_btn = Button(
            text="Cancel",
            font_size="14sp",
            size_hint_y=None,
            height="40dp"
        )
        content.add_widget(cancel_btn)
        
        popup = Popup(
            title="",
            content=content,
            size_hint=(0.75, 0.4),
            auto_dismiss=False
        )
        
        def send_photo(*args):
            app = App.get_running_app()
            app.send_media("photo.jpg", "image")
            popup.dismiss()
        
        def send_video(*args):
            app = App.get_running_app()
            app.send_media("video.mp4", "video")
            popup.dismiss()
        
        def send_file(*args):
            app = App.get_running_app()
            app.send_media("document.pdf", "file")
            popup.dismiss()
        
        photo_btn.bind(on_release=send_photo)
        video_btn.bind(on_release=send_video)
        file_btn.bind(on_release=send_file)
        cancel_btn.bind(on_release=popup.dismiss)
        
        popup.open()
