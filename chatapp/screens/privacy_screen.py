from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.properties import StringProperty
from kivy.app import App


class PrivacyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        main_layout = BoxLayout(orientation="vertical", padding="15dp", spacing="10dp")
        
        # Header
        header = BoxLayout(size_hint_y=None, height="50dp")
        back_btn = Button(text="<", size_hint_x=None, width="40dp", font_size="20sp")
        back_btn.bind(on_release=lambda x: self.go_back())
        header.add_widget(back_btn)
        header.add_widget(Label(text="Privacy & Security", font_size="20sp", bold=True, color=(0.15, 0.45, 0.75, 1)))
        header.add_widget(Widget())
        main_layout.add_widget(header)
        
        # Settings List
        scroll = ScrollView()
        settings_box = BoxLayout(orientation="vertical", size_hint_y=None, height="500dp", spacing="5dp")
        
        # Privacy Section
        settings_box.add_widget(Label(
            text="PRIVACY",
            font_size="13sp",
            bold=True,
            color=(0.15, 0.45, 0.75, 1),
            size_hint_y=None,
            height="30dp",
            halign="left"
        ))
        
        # Online Status
        settings_box.add_widget(self._create_setting(
            "Show Online Status",
            "Let others see when you're online",
            "show_online_status"
        ))
        
        # Last Seen
        settings_box.add_widget(self._create_setting(
            "Show Last Seen",
            "Let others see your last active time",
            "show_last_seen"
        ))
        
        # Read Receipts
        settings_box.add_widget(self._create_setting(
            "Show Read Receipts",
            "Let others know when you've read their messages",
            "show_read_receipts"
        ))
        
        # Profile Photo
        settings_box.add_widget(self._create_setting(
            "Show Profile Photo",
            "Let others see your profile photo",
            "show_profile_photo"
        ))
        
        # Contact Requests
        settings_box.add_widget(self._create_setting(
            "Allow Contact Requests",
            "Let others send you contact requests",
            "allow_contact_requests"
        ))
        
        # Block Unknown
        settings_box.add_widget(self._create_setting(
            "Block Unknown Numbers",
            "Block messages from unknown numbers",
            "block_unknown_numbers"
        ))
        
        # Security Section
        settings_box.add_widget(Label(
            text="SECURITY",
            font_size="13sp",
            bold=True,
            color=(0.15, 0.45, 0.75, 1),
            size_hint_y=None,
            height="30dp",
            halign="left"
        ))
        
        # End-to-End Encryption
        settings_box.add_widget(self._create_setting(
            "End-to-End Encryption",
            "Encrypt all your messages for privacy",
            "encrypted_messages"
        ))
        
        # Two-Factor Authentication
        twofa_layout = BoxLayout(
            size_hint_y=None,
            height="70dp",
            padding=["10dp", "5dp"],
            spacing="10dp"
        )
        
        twofa_info = BoxLayout(orientation="vertical", size_hint_x=0.7)
        twofa_info.add_widget(Label(
            text="Two-Factor Authentication",
            font_size="14sp",
            halign="left",
            text_size=(None, None)
        ))
        twofa_info.add_widget(Label(
            text="Add extra security to your account",
            font_size="11sp",
            color=(0.5, 0.5, 0.5, 1),
            halign="left"
        ))
        twofa_layout.add_widget(twofa_info)
        
        twofa_switch = Switch(
            size_hint_x=0.3,
            active=App.get_running_app().two_factor_enabled
        )
        twofa_switch.bind(active=self._toggle_2fa)
        twofa_layout.add_widget(twofa_switch)
        
        settings_box.add_widget(twofa_layout)
        
        # Blocked Users Section
        settings_box.add_widget(Label(
            text="BLOCKED USERS",
            font_size="13sp",
            bold=True,
            color=(0.15, 0.45, 0.75, 1),
            size_hint_y=None,
            height="30dp",
            halign="left"
        ))
        
        self.blocked_list = BoxLayout(orientation="vertical", size_hint_y=None, height="100dp")
        settings_box.add_widget(self.blocked_list)
        
        # Logout
        settings_box.add_widget(Widget(size_hint_y=None, height="20dp"))
        
        logout_btn = Button(
            text="Logout",
            font_size="14sp",
            size_hint_y=None,
            height="45dp",
            background_color=(0.8, 0.2, 0.2, 1)
        )
        logout_btn.bind(on_release=lambda x: self.logout())
        settings_box.add_widget(logout_btn)
        
        scroll.add_widget(settings_box)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def _create_setting(self, title, description, key):
        app = App.get_running_app()
        
        layout = BoxLayout(
            size_hint_y=None,
            height="70dp",
            padding=["10dp", "5dp"],
            spacing="10dp"
        )
        
        info = BoxLayout(orientation="vertical", size_hint_x=0.7)
        info.add_widget(Label(
            text=title,
            font_size="14sp",
            halign="left",
            text_size=(None, None)
        ))
        info.add_widget(Label(
            text=description,
            font_size="11sp",
            color=(0.5, 0.5, 0.5, 1),
            halign="left"
        ))
        layout.add_widget(info)
        
        switch = Switch(
            size_hint_x=0.3,
            active=app.privacy_settings.get(key, False)
        )
        switch.bind(active=lambda instance, value, k=key: self._update_setting(k, value))
        layout.add_widget(switch)
        
        return layout
    
    def _update_setting(self, key, value):
        app = App.get_running_app()
        app.update_privacy(key, value)
    
    def _toggle_2fa(self, instance, value):
        app = App.get_running_app()
        app.toggle_two_factor(value)
    
    def on_enter(self):
        self.refresh_blocked_list()
    
    def refresh_blocked_list(self):
        app = App.get_running_app()
        self.blocked_list.clear_widgets()
        
        if not app.blocked_users:
            self.blocked_list.add_widget(Label(
                text="No blocked users",
                font_size="12sp",
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height="40dp"
            ))
        
        for user in app.blocked_users:
            item = BoxLayout(size_hint_y=None, height="40dp", padding="5dp", spacing="5dp")
            
            item.add_widget(Label(
                text=user,
                font_size="13sp",
                halign="left"
            ))
            
            unblock_btn = Button(
                text="Unblock",
                font_size="11sp",
                size_hint_x=None,
                width="70dp",
                background_color=(0.15, 0.45, 0.75, 1)
            )
            unblock_btn.bind(on_release=lambda x, name=user: self.unblock_user(name))
            item.add_widget(unblock_btn)
            
            self.blocked_list.add_widget(item)
    
    def unblock_user(self, user_name):
        app = App.get_running_app()
        app.unblock_user(user_name)
        self.refresh_blocked_list()
    
    def logout(self):
        App.get_running_app().logout()
    
    def go_back(self):
        App.get_running_app().go_home()
