from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty


class ContactItem(BoxLayout):
    contact_name = StringProperty("")
    last_message = StringProperty("")
    msg_time = StringProperty("")
    unread_count = NumericProperty(0)
