from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty
from kivy.app import App


class InviteScreen(Screen):
    current_chat = StringProperty("")
    invite_mode = StringProperty("person")  # "person" or "group"
    
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
        header.add_widget(Label(text="Invite to Chat", font_size="20sp", bold=True, color=(0.2, 0.6, 0.9, 1)))
        header.add_widget(Widget())
        main_layout.add_widget(header)
        
        # Target Chat Info
        self.target_label = Label(
            text=f"Invite to: {self.current_chat}",
            font_size="14sp",
            size_hint_y=None,
            height="30dp"
        )
        main_layout.add_widget(self.target_label)
        
        # Mode Toggle
        mode_layout = BoxLayout(size_hint_y=None, height="40dp", spacing="10dp")
        person_btn = Button(text="Invite Person", font_size="13sp")
        person_btn.bind(on_release=lambda x: self.set_mode("person"))
        mode_layout.add_widget(person_btn)
        
        group_btn = Button(text="Invite Group", font_size="13sp")
        group_btn.bind(on_release=lambda x: self.set_mode("group"))
        mode_layout.add_widget(group_btn)
        main_layout.add_widget(mode_layout)
        
        # Restriction Info
        self.restriction_label = Label(
            text="",
            font_size="12sp",
            color=(0.9, 0.4, 0.2, 1),
            size_hint_y=None,
            height="25dp"
        )
        main_layout.add_widget(self.restriction_label)
        
        # Search Input
        self.search_input = TextInput(
            hint_text="Search by name...",
            multiline=False,
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.search_input)
        
        # Available Contacts/Groups
        main_layout.add_widget(Label(text="Available:", font_size="13sp", size_hint_y=None, height="25dp", halign="left"))
        
        self.available_list = ScrollView(size_hint_y=1)
        self.available_box = BoxLayout(orientation="vertical", size_hint_y=None, height="200dp")
        self.available_list.add_widget(self.available_box)
        main_layout.add_widget(self.available_list)
        
        # Pending Invites
        main_layout.add_widget(Label(text="Pending Invites:", font_size="13sp", size_hint_y=None, height="25dp", halign="left"))
        
        self.pending_list = ScrollView(size_hint_y=1)
        self.pending_box = BoxLayout(orientation="vertical", size_hint_y=None, height="150dp")
        self.pending_list.add_widget(self.pending_box)
        main_layout.add_widget(self.pending_list)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        app = App.get_running_app()
        self.current_chat = app.current_chat
        self.target_label.text = f"Invite to: {self.current_chat}"
        
        # Check restrictions
        can_invite = app.can_invite_to_chat(self.current_chat)
        can_invite_group = app.can_invite_group_to_chat(self.current_chat)
        
        if not can_invite:
            self.restriction_label.text = "Note: You cannot add members to this chat"
        elif not can_invite_group:
            self.restriction_label.text = "Note: You cannot invite groups to this chat"
        else:
            self.restriction_label.text = ""
        
        self.refresh_available()
        self.refresh_pending()
    
    def set_mode(self, mode):
        self.invite_mode = mode
        self.refresh_available()
    
    def refresh_available(self):
        app = App.get_running_app()
        self.available_box.clear_widgets()
        
        if self.invite_mode == "person":
            contacts = [c for c in app.contacts if not c.get("is_group")]
        else:
            contacts = [c for c in app.contacts if c.get("is_group")]
        
        search = self.search_input.text.lower()
        if search:
            contacts = [c for c in contacts if search in c["name"].lower()]
        
        for contact in contacts:
            item = BoxLayout(size_hint_y=None, height="45dp", padding="5dp", spacing="5dp")
            
            item.add_widget(Label(
                text=contact["name"],
                font_size="14sp",
                halign="left",
                text_size=(None, None)
            ))
            
            if contact["name"] != self.current_chat:
                invite_btn = Button(
                    text="Invite",
                    size_hint_x=None,
                    width="70dp",
                    font_size="12sp",
                    background_color=(0.2, 0.7, 0.4, 1)
                )
                invite_btn.bind(on_release=lambda x, n=contact["name"]: self.send_invite(n))
                item.add_widget(invite_btn)
            else:
                item.add_widget(Label(text="(This chat)", font_size="11sp", size_hint_x=None, width="70dp"))
            
            self.available_box.add_widget(item)
    
    def refresh_pending(self):
        app = App.get_running_app()
        self.pending_box.clear_widgets()
        
        for idx, invite in enumerate(app.pending_invites):
            if invite.get("to_chat") == self.current_chat or invite.get("from") == app.user_name:
                item = BoxLayout(size_hint_y=None, height="45dp", padding="5dp", spacing="5dp")
                
                status_color = (0.2, 0.7, 0.4, 1) if invite["status"] == "accepted" else (0.9, 0.4, 0.2, 1) if invite["status"] == "rejected" else (0.5, 0.5, 0.5, 1)
                
                item.add_widget(Label(
                    text=f"{invite['from']} -> {invite.get('recipient', invite.get('to_chat', ''))}",
                    font_size="12sp",
                    halign="left"
                ))
                
                item.add_widget(Label(
                    text=invite["status"],
                    font_size="11sp",
                    color=status_color,
                    size_hint_x=None,
                    width="60dp"
                ))
                
                if invite["status"] == "pending":
                    if invite.get("to_chat") == self.current_chat:
                        accept_btn = Button(text="Accept", size_hint_x=None, width="60dp", font_size="11sp", background_color=(0.2, 0.7, 0.4, 1))
                        accept_btn.bind(on_release=lambda x, i=idx: self.accept_invite(i))
                        item.add_widget(accept_btn)
                        
                        reject_btn = Button(text="Reject", size_hint_x=None, width="60dp", font_size="11sp", background_color=(0.9, 0.3, 0.3, 1))
                        reject_btn.bind(on_release=lambda x, i=idx: self.reject_invite(i))
                        item.add_widget(reject_btn)
                
                self.pending_box.add_widget(item)
    
    def send_invite(self, recipient_name):
        app = App.get_running_app()
        can_invite = app.can_invite_to_chat(self.current_chat)
        can_invite_group = app.can_invite_group_to_chat(self.current_chat)
        
        if self.invite_mode == "person" and not can_invite:
            app.import_status = "Cannot add members to this chat"
            return
        
        if self.invite_mode == "group" and not can_invite_group:
            app.import_status = "Cannot invite groups to this chat"
            return
        
        if app.send_invite(self.current_chat, recipient_name):
            app.import_status = f"Invite sent to {recipient_name}!"
            self.refresh_pending()
            self.refresh_available()
    
    def accept_invite(self, invite_index):
        app = App.get_running_app()
        if app.accept_invite(invite_index):
            self.refresh_pending()
    
    def reject_invite(self, invite_index):
        app = App.get_running_app()
        if app.reject_invite(invite_index):
            self.refresh_pending()
    
    def go_back(self):
        App.get_running_app().go_home()
