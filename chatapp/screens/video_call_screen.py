from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class VideoCallScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = FloatLayout()
        
        layout.add_widget(Label(
            text="[Remote Video Placeholder]",
            font_size="24sp",
            color=(0.8, 0.8, 0.8, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        ))
        
        self.duration_label = Label(
            text="00:00",
            font_size="20sp",
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        layout.add_widget(self.duration_label)
        
        self.caller_label = Label(
            text="",
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "top": 0.85}
        )
        layout.add_widget(self.caller_label)
        
        controls = BoxLayout(
            size_hint_y=None,
            height="100dp",
            padding="20dp",
            spacing="20dp",
            pos_hint={"center_x": 0.5, "y": 0.05}
        )
        
        mute_btn = Button(
            text="Mute",
            font_size="14sp",
            background_color=(0.3, 0.3, 0.3, 1)
        )
        controls.add_widget(mute_btn)
        
        end_call_btn = Button(
            text="End Call",
            font_size="16sp",
            background_color=(0.9, 0.2, 0.2, 1),
            on_release=self._end_call
        )
        controls.add_widget(end_call_btn)
        
        video_btn = Button(
            text="Video",
            font_size="14sp",
            background_color=(0.3, 0.3, 0.3, 1)
        )
        controls.add_widget(video_btn)
        
        speaker_btn = Button(
            text="Speaker",
            font_size="14sp",
            background_color=(0.3, 0.3, 0.3, 1)
        )
        controls.add_widget(speaker_btn)
        
        layout.add_widget(controls)
        self.add_widget(layout)
    
    def on_enter(self):
        app = App.get_running_app()
        self.caller_label.text = app.current_chat
        app.bind(video_call_duration=self._update_duration)
    
    def on_leave(self):
        app = App.get_running_app()
        try:
            app.unbind(video_call_duration=self._update_duration)
        except:
            pass
    
    def _update_duration(self, instance, value):
        self.duration_label.text = value
    
    def _end_call(self, *args):
        App.get_running_app().end_video_call()
