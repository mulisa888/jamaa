from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation="vertical", padding="20dp", spacing="15dp")
        
        # Header
        header = BoxLayout(size_hint_y=None, height="50dp")
        back_btn = Button(text="<", size_hint_x=None, width="40dp", font_size="20sp")
        back_btn.bind(on_release=lambda x: self.go_back())
        header.add_widget(back_btn)
        header.add_widget(Label(text="My Profile", font_size="22sp", bold=True, color=(0.2, 0.6, 0.9, 1)))
        header.add_widget(Widget())
        layout.add_widget(header)
        
        # Avatar
        avatar_layout = BoxLayout(size_hint_y=None, height="120dp")
        avatar_layout.add_widget(Widget())
        self.avatar_label = Label(
            text=App.get_running_app().user_avatar,
            font_size="40sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(100, 100)
        )
        avatar_layout.add_widget(self.avatar_label)
        avatar_layout.add_widget(Widget())
        layout.add_widget(avatar_layout)
        
        # Name
        self.name_input = TextInput(
            hint_text="Your Name",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"],
            font_size="16sp"
        )
        self.name_input.text = App.get_running_app().user_name
        layout.add_widget(self.name_input)
        
        # Email
        self.email_input = TextInput(
            hint_text="Email Address",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"],
            font_size="16sp"
        )
        self.email_input.text = App.get_running_app().user_email
        layout.add_widget(self.email_input)
        
        # Phone
        self.phone_input = TextInput(
            hint_text="Phone Number",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"],
            font_size="16sp"
        )
        self.phone_input.text = App.get_running_app().user_phone
        layout.add_widget(self.phone_input)
        
        # Status
        self.status_input = TextInput(
            hint_text="Your Status",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"],
            font_size="16sp"
        )
        self.status_input.text = App.get_running_app().user_status
        layout.add_widget(self.status_input)
        
        # Save Button
        save_btn = Button(
            text="Save Changes",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height="50dp",
            background_color=(0.2, 0.7, 0.4, 1)
        )
        save_btn.bind(on_release=lambda x: self.save_profile())
        layout.add_widget(save_btn)
        
        # Spacer
        layout.add_widget(Widget())
        
        self.add_widget(layout)
    
    def save_profile(self):
        app = App.get_running_app()
        app.update_profile(
            name=self.name_input.text,
            email=self.email_input.text,
            phone=self.phone_input.text,
            status=self.status_input.text
        )
        self.avatar_label.text = app.user_avatar
        app.import_status = "Profile saved!"
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: setattr(app, 'import_status', ''), 2)
    
    def go_back(self):
        App.get_running_app().go_home()


from kivy.app import App
from kivy.uix.widget import Widget
