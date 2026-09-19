from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty


class MessageBubble(BoxLayout):
    message_text = StringProperty("")
    is_me = BooleanProperty(False)
    time = StringProperty("")
