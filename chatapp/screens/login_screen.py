from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_signup = False
        self.build_ui()
    
    def build_ui(self):
        main_layout = FloatLayout()
        
        # Background
        main_layout.add_widget(Widget())
        
        content = BoxLayout(
            orientation="vertical",
            padding="30dp",
            spacing="15dp",
            size_hint=(0.85, 0.7),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        # Logo
        content.add_widget(Widget(size_hint_y=0.1))
        
        logo = Label(
            text="Jamaa",
            font_size="36sp",
            bold=True,
            color=(0.15, 0.45, 0.75, 1),
            size_hint_y=None,
            height="50dp"
        )
        content.add_widget(logo)
        
        tagline = Label(
            text="Stay Connected with Family & Friends",
            font_size="14sp",
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height="25dp"
        )
        content.add_widget(tagline)
        
        content.add_widget(Widget(size_hint_y=0.05))
        
        # Name Input (signup only)
        self.name_input = TextInput(
            hint_text="Full Name",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"],
            font_size="15sp"
        )
        content.add_widget(self.name_input)
        
        # Email Input
        self.email_input = TextInput(
            hint_text="Email Address",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"],
            font_size="15sp"
        )
        content.add_widget(self.email_input)
        
        # Phone Input (signup only)
        self.phone_input = TextInput(
            hint_text="Phone Number",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"],
            font_size="15sp"
        )
        content.add_widget(self.phone_input)
        
        # Password Input
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"],
            font_size="15sp"
        )
        content.add_widget(self.password_input)
        
        # Login/Signup Button
        self.action_btn = Button(
            text="Login",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height="50dp",
            background_color=(0.15, 0.45, 0.75, 1)
        )
        self.action_btn.bind(on_release=self.do_action)
        content.add_widget(self.action_btn)
        
        # Toggle Login/Signup
        self.toggle_btn = Button(
            text="Don't have an account? Sign Up",
            font_size="13sp",
            size_hint_y=None,
            height="35dp",
            background_color=(0, 0, 0, 0),
            color=(0.15, 0.45, 0.75, 1)
        )
        self.toggle_btn.bind(on_release=self.toggle_mode)
        content.add_widget(self.toggle_btn)
        
        # Status
        self.status_label = Label(
            text="",
            font_size="13sp",
            color=(0.9, 0.3, 0.3, 1),
            size_hint_y=None,
            height="25dp"
        )
        content.add_widget(self.status_label)
        
        main_layout.add_widget(content)
        self.add_widget(main_layout)
        
        # Hide name and phone initially
        self.name_input.opacity = 0
        self.name_input.size_hint_y = 0
        self.name_input.height = 0
        self.phone_input.opacity = 0
        self.phone_input.size_hint_y = 0
        self.phone_input.height = 0
    
    def toggle_mode(self, *args):
        self.is_signup = not self.is_signup
        
        if self.is_signup:
            self.action_btn.text = "Sign Up"
            self.toggle_btn.text = "Already have an account? Login"
            self.name_input.opacity = 1
            self.name_input.size_hint_y = None
            self.name_input.height = 45
            self.phone_input.opacity = 1
            self.phone_input.size_hint_y = None
            self.phone_input.height = 45
        else:
            self.action_btn.text = "Login"
            self.toggle_btn.text = "Don't have an account? Sign Up"
            self.name_input.opacity = 0
            self.name_input.size_hint_y = 0
            self.name_input.height = 0
            self.phone_input.opacity = 0
            self.phone_input.size_hint_y = 0
            self.phone_input.height = 0
    
    def do_action(self, *args):
        app = App.get_running_app()
        
        if self.is_signup:
            success = app.signup(
                name=self.name_input.text,
                email=self.email_input.text,
                phone=self.phone_input.text,
                password=self.password_input.text
            )
        else:
            success = app.login(
                email=self.email_input.text,
                password=self.password_input.text
            )
        
        if not success:
            self.status_label.text = "Please fill in all fields"
        else:
            self.status_label.text = ""


from kivy.uix.widget import Widget
