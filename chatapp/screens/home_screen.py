from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class HomeScreen(Screen):
    current_filter = StringProperty("all")
    
    def filter_contacts(self, filter_type):
        self.current_filter = filter_type
        app = App.get_running_app()
        
        if filter_type == "all":
            filtered = app.contacts
        elif filter_type == "family":
            filtered = [c for c in app.contacts if c.get("category") == "family"]
        elif filter_type == "friends":
            filtered = [c for c in app.contacts if c.get("category") == "friends" and not c.get("is_group")]
        elif filter_type == "groups":
            filtered = [c for c in app.contacts if c.get("is_group")]
        else:
            filtered = app.contacts
        
        self.ids.contacts_rv.data = [
            {
                "text": item["name"],
                "secondary_text": item["last_message"],
                "tertiary_text": item["time"],
                "unread": item["unread"],
                "is_group": item.get("is_group", False),
                "category": item.get("category", "friends")
            }
            for item in filtered
        ]
    
    def show_add_menu(self):
        app = App.get_running_app()
        
        content = BoxLayout(orientation="vertical", padding="15dp", spacing="10dp")
        
        content.add_widget(Label(text="Add New", font_size="18sp", bold=True, size_hint_y=None, height="35dp"))
        
        name_input = TextInput(hint_text="Name", multiline=False, size_hint_y=None, height="40dp")
        content.add_widget(name_input)
        
        phone_input = TextInput(hint_text="Phone (optional)", multiline=False, size_hint_y=None, height="40dp")
        content.add_widget(phone_input)
        
        category_input = TextInput(hint_text="Category: family/friends/work", multiline=False, size_hint_y=None, height="40dp")
        content.add_widget(category_input)
        
        btn_layout = BoxLayout(size_hint_y=None, height="45dp", spacing="10dp")
        
        cancel_btn = Button(text="Cancel", font_size="14sp")
        btn_layout.add_widget(cancel_btn)
        
        add_contact_btn = Button(text="Add Contact", font_size="14sp", background_color=(0.2, 0.7, 0.4, 1))
        btn_layout.add_widget(add_contact_btn)
        
        add_group_btn = Button(text="Create Group", font_size="14sp", background_color=(0.2, 0.6, 0.9, 1))
        btn_layout.add_widget(add_group_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(title="", content=content, size_hint=(0.85, 0.6), auto_dismiss=False)
        
        def add_contact(*args):
            name = name_input.text.strip()
            phone = phone_input.text.strip()
            category = category_input.text.strip() or "friends"
            
            if name:
                app.add_contact(name, phone, category)
                popup.dismiss()
        
        def create_group(*args):
            name = name_input.text.strip()
            if name:
                app.create_group(name, [])
                popup.dismiss()
        
        cancel_btn.bind(on_release=popup.dismiss)
        add_contact_btn.bind(on_release=add_contact)
        add_group_btn.bind(on_release=create_group)
        
        popup.open()
