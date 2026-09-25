from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.clipboard import Clipboard
from kivy import platform as kivy_platform
import os


class ChatScreen(Screen):
    show_emoji = BooleanProperty(False)
    is_typing = BooleanProperty(False)
    typing_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._selected_msg_index = None

    def on_text_change(self, text):
        was_typing = self.is_typing
        self.is_typing = len(text.strip()) > 0
        self.typing_text = text.strip()

    def toggle_emoji(self):
        self.show_emoji = not self.show_emoji

    def insert_emoji(self, emoji):
        input_field = self.ids.get("message_input")
        if input_field:
            input_field.text += emoji
            input_field.focus = True

    def send_message(self):
        app = App.get_running_app()
        input_field = self.ids.get("message_input")
        if not input_field:
            return
        text = input_field.text.strip()
        if not text:
            return
        if app.send_message(text):
            input_field.text = ""
            self.is_typing = False
            self.typing_text = ""

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
            text="Voice Note Recorded",
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

        def open_photo(*args):
            popup.dismiss()
            self._open_file_chooser("image")

        def open_video(*args):
            popup.dismiss()
            self._open_file_chooser("video")

        def open_file(*args):
            popup.dismiss()
            self._open_file_chooser("file")

        photo_btn.bind(on_release=open_photo)
        video_btn.bind(on_release=open_video)
        file_btn.bind(on_release=open_file)
        cancel_btn.bind(on_release=popup.dismiss)
        popup.open()

    def _open_file_chooser(self, media_type):
        if kivy_platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])

        filters = {
            "image": [("Images", "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp")],
            "video": [("Videos", "*.mp4", "*.avi", "*.mov", "*.mkv", "*.webm")],
            "file": [("All Files", "*.*")]
        }

        try:
            from kivy.uix.filechooser import FileChooserIconView
            from kivy.core.window import Window

            chosen = {"path": None}

            file_layout = BoxLayout(orientation="vertical", spacing="8dp")

            filechooser = FileChooserIconView(
                path=os.path.expanduser("~"),
                filters=filters.get(media_type, filters["file"]),
                size_hint_y=0.85
            )
            file_layout.add_widget(filechooser)

            btn_layout = BoxLayout(size_hint_y=None, height="45dp", spacing="10dp")
            cancel_btn = Button(text="Cancel", font_size="14sp")
            select_btn = Button(
                text="Select",
                font_size="14sp",
                background_color=(0.15, 0.6, 0.35, 1)
            )
            btn_layout.add_widget(cancel_btn)
            btn_layout.add_widget(select_btn)
            file_layout.add_widget(btn_layout)

            popup = Popup(
                title=f"Select {media_type.capitalize()}",
                content=file_layout,
                size_hint=(0.9, 0.8),
                auto_dismiss=False
            )

            def select_file(*args):
                if filechooser.selection:
                    chosen["path"] = filechooser.selection[0]
                popup.dismiss()

            cancel_btn.bind(on_release=popup.dismiss)
            select_btn.bind(on_release=select_file)
            popup.open()

            def process_selection(dt):
                if chosen["path"]:
                    self._process_selected_file(chosen["path"], media_type)

            if chosen["path"]:
                from kivy.clock import Clock
                Clock.schedule_once(process_selection, 0.1)

        except ImportError:
            app = App.get_running_app()
            app.send_media(f"{media_type}_file", media_type)

    def _process_selected_file(self, file_path, media_type):
        app = App.get_running_app()
        ext = os.path.splitext(file_path)[1].lower()
        image_exts = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        video_exts = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}

        if media_type == "image" or ext in image_exts:
            app.send_media(file_path, "image")
        elif media_type == "video" or ext in video_exts:
            app.send_media(file_path, "video")
        else:
            app.send_media(file_path, "file")

    def show_message_actions(self, msg_index, msg_text):
        self._selected_msg_index = msg_index

        content = BoxLayout(orientation="vertical", padding="15dp", spacing="10dp")

        content.add_widget(Label(
            text="Message Actions",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height="30dp"
        ))

        preview = Label(
            text=f'"{msg_text[:50]}{"..." if len(msg_text) > 50 else ""}"',
            font_size="12sp",
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None,
            height="35dp",
            halign="center",
            text_size=(None, None)
        )
        content.add_widget(preview)

        btn_layout = BoxLayout(size_hint_y=None, height="45dp", spacing="10dp")

        copy_btn = Button(
            text="Copy",
            font_size="14sp",
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn_layout.add_widget(copy_btn)

        delete_btn = Button(
            text="Delete",
            font_size="14sp",
            background_color=(0.9, 0.3, 0.3, 1)
        )
        btn_layout.add_widget(delete_btn)

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

        def copy_message(*args):
            try:
                Clipboard.copy(msg_text)
                app = App.get_running_app()
                app.import_status = "Message copied!"
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: setattr(app, 'import_status', ''), 2)
            except Exception:
                pass
            popup.dismiss()

        def delete_message(*args):
            app = App.get_running_app()
            if self._selected_msg_index is not None:
                app.delete_message_by_chat_index(self._selected_msg_index)
            popup.dismiss()

        copy_btn.bind(on_release=copy_message)
        delete_btn.bind(on_release=delete_message)
        cancel_btn.bind(on_release=popup.dismiss)
        popup.open()
