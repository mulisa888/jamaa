from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty
from kivy.app import App


class ContactRequestScreen(Screen):
    current_tab = StringProperty("received")
    
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
        header.add_widget(Label(text="Contact Requests", font_size="20sp", bold=True, color=(0.15, 0.45, 0.75, 1)))
        header.add_widget(Widget())
        main_layout.add_widget(header)
        
        # Info
        info = Label(
            text="Manage who can contact you.\nYou control who gets added to your contacts.",
            font_size="13sp",
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height="45dp"
        )
        main_layout.add_widget(info)
        
        # Tabs
        tab_layout = BoxLayout(size_hint_y=None, height="40dp", spacing="8dp")
        
        self.received_btn = Button(text="Received", font_size="13sp")
        self.received_btn.bind(on_release=lambda x: self.set_tab("received"))
        tab_layout.add_widget(self.received_btn)
        
        self.sent_btn = Button(text="Sent", font_size="13sp")
        self.sent_btn.bind(on_release=lambda x: self.set_tab("sent"))
        tab_layout.add_widget(self.sent_btn)
        
        self.new_btn = Button(text="+ New Request", font_size="13sp", background_color=(0.15, 0.45, 0.75, 1))
        self.new_btn.bind(on_release=lambda x: self.set_tab("new"))
        tab_layout.add_widget(self.new_btn)
        
        main_layout.add_widget(tab_layout)
        
        # Content Area
        self.content_area = ScrollView(size_hint_y=1)
        self.content_box = BoxLayout(orientation="vertical", size_hint_y=None, height="300dp")
        self.content_area.add_widget(self.content_box)
        main_layout.add_widget(self.content_area)
        
        # New Request Form (hidden by default)
        self.new_request_form = BoxLayout(orientation="vertical", size_hint_y=None, height="0", spacing="10dp")
        
        self.phone_input = TextInput(
            hint_text="Phone Number",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"]
        )
        self.new_request_form.add_widget(self.phone_input)
        
        self.message_input = TextInput(
            hint_text="Message (optional)",
            multiline=False,
            size_hint_y=None,
            height="45dp",
            padding=["15dp", "12dp"]
        )
        self.new_request_form.add_widget(self.message_input)
        
        send_btn = Button(
            text="Send Request",
            font_size="14sp",
            size_hint_y=None,
            height="45dp",
            background_color=(0.15, 0.45, 0.75, 1)
        )
        send_btn.bind(on_release=lambda x: self.send_request())
        self.new_request_form.add_widget(send_btn)
        
        main_layout.add_widget(self.new_request_form)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.refresh_content()
    
    def set_tab(self, tab):
        self.current_tab = tab
        if tab == "new":
            self.new_request_form.size_hint_y = 1
            self.new_request_form.height = "180dp"
            self.content_area.size_hint_y = 0
            self.content_area.height = 0
        else:
            self.new_request_form.size_hint_y = 0
            self.new_request_form.height = 0
            self.content_area.size_hint_y = 1
            self.content_area.height = "300dp"
            self.refresh_content()
    
    def refresh_content(self):
        app = App.get_running_app()
        self.content_box.clear_widgets()
        
        if self.current_tab == "received":
            requests = [r for r in app.contact_requests if r.get("direction") != "outgoing" and r["status"] == "pending"]
            
            if not requests:
                self.content_box.add_widget(Label(
                    text="No pending requests",
                    font_size="14sp",
                    color=(0.5, 0.5, 0.5, 1),
                    size_hint_y=None,
                    height="60dp"
                ))
            
            for idx, request in enumerate(requests):
                item = BoxLayout(
                    orientation="vertical",
                    size_hint_y=None,
                    height="100dp",
                    padding="10dp",
                    spacing="5dp"
                )
                
                # Canvas background
                item.canvas.before
                
                header = BoxLayout(size_hint_y=None, height="25dp")
                header.add_widget(Label(
                    text=request["from"],
                    font_size="15sp",
                    bold=True,
                    halign="left"
                ))
                header.add_widget(Label(
                    text=request.get("time", ""),
                    font_size="11sp",
                    color=(0.5, 0.5, 0.5, 1)
                ))
                item.add_widget(header)
                
                if request.get("message"):
                    item.add_widget(Label(
                        text=f'"{request["message"]}"',
                        font_size="12sp",
                        color=(0.4, 0.4, 0.4, 1),
                        size_hint_y=None,
                        height="20dp"
                    ))
                
                if request.get("from_phone"):
                    item.add_widget(Label(
                        text=request["from_phone"],
                        font_size="11sp",
                        color=(0.5, 0.5, 0.5, 1),
                        size_hint_y=None,
                        height="18dp"
                    ))
                
                btn_layout = BoxLayout(size_hint_y=None, height="30dp", spacing="8dp")
                
                accept_btn = Button(
                    text="Accept",
                    font_size="12sp",
                    background_color=(0.2, 0.7, 0.4, 1)
                )
                accept_btn.bind(on_release=lambda x, i=app.contact_requests.index(request): self.accept_request(i))
                btn_layout.add_widget(accept_btn)
                
                reject_btn = Button(
                    text="Reject",
                    font_size="12sp",
                    background_color=(0.9, 0.3, 0.3, 1)
                )
                reject_btn.bind(on_release=lambda x, i=app.contact_requests.index(request): self.reject_request(i))
                btn_layout.add_widget(reject_btn)
                
                block_btn = Button(
                    text="Block",
                    font_size="12sp",
                    background_color=(0.5, 0.5, 0.5, 1)
                )
                block_btn.bind(on_release=lambda x, name=request["from"]: self.block_user(name))
                btn_layout.add_widget(block_btn)
                
                item.add_widget(btn_layout)
                self.content_box.add_widget(item)
        
        elif self.current_tab == "sent":
            sent = [r for r in app.contact_requests if r.get("direction") == "outgoing"]
            
            if not sent:
                self.content_box.add_widget(Label(
                    text="No sent requests",
                    font_size="14sp",
                    color=(0.5, 0.5, 0.5, 1),
                    size_hint_y=None,
                    height="60dp"
                ))
            
            for request in sent:
                item = BoxLayout(
                    size_hint_y=None,
                    height="50dp",
                    padding="10dp",
                    spacing="10dp"
                )
                
                item.add_widget(Label(
                    text=f"To: {request.get('to_phone', 'Unknown')}",
                    font_size="14sp",
                    halign="left"
                ))
                
                status_color = (0.2, 0.7, 0.4, 1) if request["status"] == "accepted" else (0.9, 0.3, 0.3, 1) if request["status"] == "rejected" else (0.5, 0.5, 0.5, 1)
                
                item.add_widget(Label(
                    text=request["status"],
                    font_size="12sp",
                    color=status_color,
                    size_hint_x=None,
                    width="80dp"
                ))
                
                self.content_box.add_widget(item)
    
    def send_request(self):
        app = App.get_running_app()
        phone = self.phone_input.text.strip()
        message = self.message_input.text.strip()
        
        if phone:
            app.send_contact_request(phone, message)
            self.phone_input.text = ""
            self.message_input.text = ""
            self.set_tab("sent")
    
    def accept_request(self, index):
        app = App.get_running_app()
        app.accept_contact_request(index)
        self.refresh_content()
    
    def reject_request(self, index):
        app = App.get_running_app()
        app.reject_contact_request(index)
        self.refresh_content()
    
    def block_user(self, user_name):
        app = App.get_running_app()
        app.block_user(user_name)
        self.refresh_content()
    
    def go_back(self):
        App.get_running_app().go_home()
