from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty
from kivy.app import App


class GroupInteractionScreen(Screen):
    selected_group1 = StringProperty("")
    selected_group2 = StringProperty("")
    interaction_messages = ListProperty([])
    
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
        header.add_widget(Label(text="Group Interactions", font_size="20sp", bold=True, color=(0.2, 0.6, 0.9, 1)))
        header.add_widget(Widget())
        main_layout.add_widget(header)
        
        # Info
        info = Label(
            text="Connect two groups to create a shared chat space.\nMessages will be visible to members of both groups.",
            font_size="13sp",
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height="50dp"
        )
        main_layout.add_widget(info)
        
        # Group 1 Selection
        main_layout.add_widget(Label(text="Select Group 1:", font_size="14sp", size_hint_y=None, height="30dp", halign="left"))
        self.group1_spinner = Spinner(
            text="Choose...",
            size_hint_y=None,
            height="45dp"
        )
        main_layout.add_widget(self.group1_spinner)
        
        # Group 2 Selection
        main_layout.add_widget(Label(text="Select Group 2:", font_size="14sp", size_hint_y=None, height="30dp", halign="left"))
        self.group2_spinner = Spinner(
            text="Choose...",
            size_hint_y=None,
            height="45dp"
        )
        main_layout.add_widget(self.group2_spinner)
        
        # Create Interaction Button
        create_btn = Button(
            text="Create Interaction",
            font_size="14sp",
            size_hint_y=None,
            height="45dp",
            background_color=(0.2, 0.7, 0.4, 1)
        )
        create_btn.bind(on_release=lambda x: self.create_interaction())
        main_layout.add_widget(create_btn)
        
        # Existing Interactions
        main_layout.add_widget(Label(text="Active Interactions:", font_size="14sp", size_hint_y=None, height="30dp", halign="left"))
        
        self.interactions_list = BoxLayout(orientation="vertical", size_hint_y=None, height="150dp")
        main_layout.add_widget(self.interactions_list)
        
        # Shared Chat
        main_layout.add_widget(Label(text="Shared Chat:", font_size="14sp", size_hint_y=None, height="30dp", halign="left"))
        
        self.shared_chat_messages = ScrollView(size_hint_y=1)
        self.messages_box = BoxLayout(orientation="vertical", size_hint_y=None, height="200dp")
        self.shared_chat_messages.add_widget(self.messages_box)
        main_layout.add_widget(self.shared_chat_messages)
        
        # Message Input
        input_layout = BoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        self.message_input = TextInput(
            hint_text="Type a message...",
            multiline=False,
            size_hint_y=None,
            height="40dp"
        )
        input_layout.add_widget(self.message_input)
        
        send_btn = Button(text="Send", size_hint_x=None, width="70dp", font_size="14sp")
        send_btn.bind(on_release=lambda x: self.send_message())
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.refresh_groups()
        self.refresh_interactions()
    
    def refresh_groups(self):
        app = App.get_running_app()
        groups = [g["name"] for g in app.contacts if g.get("is_group")]
        self.group1_spinner.values = groups
        self.group2_spinner.values = groups
    
    def refresh_interactions(self):
        app = App.get_running_app()
        self.interactions_list.clear_widgets()
        
        for interaction in app.group_interactions:
            item = BoxLayout(size_hint_y=None, height="40dp", padding="5dp")
            item.add_widget(Label(
                text=f"{interaction['group1']} <-> {interaction['group2']}",
                font_size="13sp",
                halign="left",
                text_size=self.size
            ))
            
            open_btn = Button(text="Open", size_hint_x=None, width="60dp", font_size="12sp")
            open_btn.bind(on_release=lambda x, i=interaction: self.open_interaction(i))
            item.add_widget(open_btn)
            
            delete_btn = Button(text="X", size_hint_x=None, width="30dp", font_size="12sp", background_color=(0.9, 0.3, 0.3, 1))
            delete_btn.bind(on_release=lambda x, i=interaction: self.delete_interaction(i))
            item.add_widget(delete_btn)
            
            self.interactions_list.add_widget(item)
    
    def create_interaction(self):
        app = App.get_running_app()
        group1 = self.group1_spinner.text
        group2 = self.group2_spinner.text
        
        if group1 == "Choose..." or group2 == "Choose...":
            app.import_status = "Please select both groups"
            return
        
        if group1 == group2:
            app.import_status = "Please select different groups"
            return
        
        if app.create_group_interaction(group1, group2):
            app.import_status = "Interaction created!"
            self.refresh_interactions()
            self.group1_spinner.text = "Choose..."
            self.group2_spinner.text = "Choose..."
        else:
            app.import_status = "Interaction already exists"
    
    def open_interaction(self, interaction):
        self.selected_group1 = interaction["group1"]
        self.selected_group2 = interaction["group2"]
        self.interaction_messages = interaction.get("messages", [])
        self.refresh_messages()
    
    def refresh_messages(self):
        self.messages_box.clear_widgets()
        for msg in self.interaction_messages:
            label = Label(
                text=f"[{msg['sender']}] {msg['text']}\n{msg['time']}",
                font_size="12sp",
                size_hint_y=None,
                height="40dp",
                halign="left",
                text_size=(None, None)
            )
            self.messages_box.add_widget(label)
    
    def send_message(self):
        app = App.get_running_app()
        text = self.message_input.text
        if text and self.selected_group1:
            app.send_group_interaction_message(self.selected_group1, text)
            self.message_input.text = ""
            
            for interaction in app.group_interactions:
                if interaction["group1"] == self.selected_group1 or interaction["group2"] == self.selected_group1:
                    self.interaction_messages = interaction["messages"]
                    break
            self.refresh_messages()
    
    def delete_interaction(self, interaction):
        app = App.get_running_app()
        app.group_interactions.remove(interaction)
        self.refresh_interactions()
    
    def go_back(self):
        App.get_running_app().go_home()


from kivy.uix.spinner import Spinner
