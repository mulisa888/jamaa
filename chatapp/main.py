import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.properties import StringProperty, ListProperty, BooleanProperty, IntegerProperty, DictProperty
from kivy.clock import Clock
from datetime import datetime
import re

from utils.file_io import StorageManager
from utils.encryption import EncryptionManager
from utils.validators import Validator


class JamaaApp(App):
    title = "Jamaa"

    # User Info
    current_user = StringProperty("You")
    user_id = StringProperty("")
    current_chat = StringProperty("")
    is_group_chat = BooleanProperty(False)

    # Profile
    user_name = StringProperty("")
    user_email = StringProperty("")
    user_phone = StringProperty("")
    user_status = StringProperty("Hey there! I am using Jamaa")
    user_avatar = StringProperty("")
    user_password_hash = StringProperty("")
    user_password_salt = StringProperty("")
    is_logged_in = BooleanProperty(False)
    two_factor_enabled = BooleanProperty(False)

    # Privacy Settings
    privacy_settings = DictProperty({
        "show_online_status": True,
        "show_last_seen": True,
        "show_read_receipts": True,
        "allow_contact_requests": True,
        "show_profile_photo": True,
        "block_unknown_numbers": False,
        "encrypted_messages": True
    })

    # Blocked Users
    blocked_users = ListProperty([])

    # Contacts
    contacts = ListProperty([])

    # Messages
    messages = ListProperty([])

    # Voice Notes
    voice_notes = ListProperty([])

    # Media Files
    media_files = ListProperty([])

    # Group interactions
    group_interactions = ListProperty([])

    # Contact Requests
    contact_requests = ListProperty([])

    # Chat restrictions
    chat_restrictions = DictProperty({
        "family": {"can_add_members": True, "can_invite_groups": True, "restrict_message_length": False},
        "friends": {"can_add_members": True, "can_invite_groups": True, "restrict_message_length": False},
        "work": {"can_add_members": False, "can_invite_groups": False, "restrict_message_length": True, "max_length": 500}
    })

    whatsapp_groups = ListProperty([])
    import_status = StringProperty("")
    video_call_active = BooleanProperty(False)
    video_call_duration = StringProperty("00:00")
    notification_count = IntegerProperty(0)

    # Recording state
    is_recording = BooleanProperty(False)
    recording_duration = StringProperty("00:00")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager(data_dir="data")
        self.encryption = EncryptionManager()
        self._call_timer = None
        self._call_seconds = 0
        self._recording_timer = None
        self._recording_seconds = 0
        self._save_timeout = None

    def build(self):
        from kivy.lang import Builder
        Builder.load_file("chat.kv")

        self.screen_manager = ScreenManager(transition=FadeTransition())

        from screens.home_screen import HomeScreen
        from screens.chat_screen import ChatScreen
        from screens.video_call_screen import VideoCallScreen
        from screens.profile_screen import ProfileScreen
        from screens.group_interaction_screen import GroupInteractionScreen
        from screens.contact_request_screen import ContactRequestScreen
        from screens.privacy_screen import PrivacyScreen
        from screens.login_screen import LoginScreen

        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(HomeScreen(name="home"))
        self.screen_manager.add_widget(ChatScreen(name="chat"))
        self.screen_manager.add_widget(VideoCallScreen(name="video_call"))
        self.screen_manager.add_widget(ProfileScreen(name="profile"))
        self.screen_manager.add_widget(GroupInteractionScreen(name="group_interaction"))
        self.screen_manager.add_widget(ContactRequestScreen(name="contact_request"))
        self.screen_manager.add_widget(PrivacyScreen(name="privacy"))

        self._load_saved_state()
        self.update_notification_count()

        return self.screen_manager

    # ─── Persistence ───────────────────────────────────────────

    def _schedule_save(self):
        if self._save_timeout:
            self._save_timeout.cancel()
        self._save_timeout = Clock.schedule_once(lambda dt: self._save_state(), 1.0)

    def _save_state(self):
        if not self.user_id:
            return

        user_data = {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "user_phone": self.user_phone,
            "user_status": self.user_status,
            "user_avatar": self.user_avatar,
            "user_password_hash": self.user_password_hash,
            "user_password_salt": self.user_password_salt,
            "two_factor_enabled": self.two_factor_enabled,
            "privacy_settings": dict(self.privacy_settings),
            "blocked_users": list(self.blocked_users),
            "contacts": list(self.contacts),
            "messages": list(self.messages),
            "voice_notes": list(self.voice_notes),
            "media_files": list(self.media_files),
            "group_interactions": list(self.group_interactions),
            "contact_requests": list(self.contact_requests),
            "chat_restrictions": dict(self.chat_restrictions),
        }
        self.storage.save_user_data(self.user_id, user_data)

    def _load_saved_state(self):
        app_state = self.storage.load_app_state()
        if not app_state:
            return

        last_user_id = app_state.get("last_user_id")
        if not last_user_id:
            return

        user_data = self.storage.load_user_data(last_user_id)
        if not user_data:
            return

        self.user_id = user_data.get("user_id", "")
        self.user_name = user_data.get("user_name", "")
        self.user_email = user_data.get("user_email", "")
        self.user_phone = user_data.get("user_phone", "")
        self.user_status = user_data.get("user_status", "Hey there! I am using Jamaa")
        self.user_avatar = user_data.get("user_avatar", "")
        self.user_password_hash = user_data.get("user_password_hash", "")
        self.user_password_salt = user_data.get("user_password_salt", "")
        self.two_factor_enabled = user_data.get("two_factor_enabled", False)

        if user_data.get("privacy_settings"):
            self.privacy_settings.update(user_data["privacy_settings"])
        if user_data.get("blocked_users"):
            self.blocked_users = user_data["blocked_users"]
        if user_data.get("contacts"):
            self.contacts = user_data["contacts"]
        if user_data.get("messages"):
            self.messages = user_data["messages"]
        if user_data.get("voice_notes"):
            self.voice_notes = user_data["voice_notes"]
        if user_data.get("media_files"):
            self.media_files = user_data["media_files"]
        if user_data.get("group_interactions"):
            self.group_interactions = user_data["group_interactions"]
        if user_data.get("contact_requests"):
            self.contact_requests = user_data["contact_requests"]
        if user_data.get("chat_restrictions"):
            self.chat_restrictions.update(user_data["chat_restrictions"])

    def _clear_saved_state(self):
        app_state = self.storage.load_app_state() or {}
        last_user_id = app_state.get("last_user_id")
        if last_user_id:
            self.storage.delete_file(f"user_{last_user_id}.json")
        self.storage.save_app_state({"last_user_id": None})

    # ─── Auth ──────────────────────────────────────────────────

    def login(self, email, password):
        if not email or not password:
            return False

        app_state = self.storage.load_app_state() or {}
        last_user_id = app_state.get("last_user_id")

        if last_user_id:
            user_data = self.storage.load_user_data(last_user_id)
            if user_data and user_data.get("user_email") == email:
                stored_hash = user_data.get("user_password_hash", "")
                salt = user_data.get("user_password_salt", "")
                if self.encryption.verify_password(password, stored_hash, salt):
                    self._load_saved_state()
                    self.is_logged_in = True
                    self.screen_manager.current = "home"
                    return True
                else:
                    self.import_status = "Invalid password"
                    Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
                    return False

        self.import_status = "Account not found. Please sign up."
        Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
        return False

    def signup(self, name, email, phone, password):
        name_valid, name_err = Validator.validate_name(name)
        if not name_valid:
            self.import_status = name_err
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            return False

        email_valid, email_err = Validator.validate_email(email)
        if not email_valid:
            self.import_status = email_err
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            return False

        pwd_valid, pwd_err = Validator.validate_password(password)
        if not pwd_valid:
            self.import_status = pwd_err
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            return False

        phone_valid, phone_err = Validator.validate_phone(phone)
        if not phone_valid:
            self.import_status = phone_err
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            return False

        pwd_hash, salt = self.encryption.hash_password(password)

        self.user_name = name.strip()
        self.user_email = email.strip()
        self.user_phone = phone.strip()
        self.user_password_hash = pwd_hash
        self.user_password_salt = salt
        self.user_avatar = name.strip()[:2].upper()
        self.user_id = self.encryption.generate_user_id(name)
        self.is_logged_in = True

        self.storage.save_app_state({"last_user_id": self.user_id})
        self._save_state()
        self.screen_manager.current = "home"
        return True

    def logout(self):
        self._save_state()
        self.is_logged_in = False
        self.screen_manager.current = "login"

    # ─── Messaging ─────────────────────────────────────────────

    def get_chat_messages(self):
        return [m for m in self.messages if m.get("chat_id") == self.current_chat]

    def send_message(self, text, msg_type="text"):
        if not text or not text.strip():
            return False

        text = text.strip()

        contact = self.get_contact(self.current_chat)
        if contact and contact.get("is_blocked"):
            self.import_status = "Cannot send message to blocked contact"
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            return False

        if contact:
            restriction = self.chat_restrictions.get(contact.get("category", ""), {})
            if restriction.get("restrict_message_length", False):
                max_len = restriction.get("max_length", 500)
                if len(text) > max_len:
                    self.import_status = f"Message too long! Max {max_len} characters"
                    Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
                    return False

        is_encrypted = self.privacy_settings.get("encrypted_messages", True)

        msg_valid, _ = Validator.validate_message(text)
        if not msg_valid:
            return False

        now = datetime.now()
        time_str = now.strftime("%I:%M %p")

        self.messages.append({
            "chat_id": self.current_chat,
            "sender": "You",
            "text": text,
            "time": time_str,
            "is_me": True,
            "type": msg_type,
            "is_encrypted": is_encrypted
        })
        self._schedule_save()
        return True

    def send_voice_note(self, file_path, duration="00:00"):
        if not file_path:
            return False

        now = datetime.now()
        time_str = now.strftime("%I:%M %p")

        self.voice_notes.append({
            "sender": "You",
            "file_path": file_path,
            "duration": duration,
            "time": time_str,
            "is_me": True,
            "type": "voice"
        })

        self.messages.append({
            "chat_id": self.current_chat,
            "sender": "You",
            "text": f"Voice note ({duration})",
            "time": time_str,
            "is_me": True,
            "type": "voice",
            "is_encrypted": True
        })
        self._schedule_save()
        return True

    def send_media(self, file_path, media_type="image"):
        if not file_path:
            return False

        now = datetime.now()
        time_str = now.strftime("%I:%M %p")

        self.media_files.append({
            "sender": "You",
            "file_path": file_path,
            "media_type": media_type,
            "time": time_str,
            "is_me": True,
            "type": "media"
        })

        type_label = "Photo" if media_type == "image" else "Video" if media_type == "video" else "File"
        self.messages.append({
            "chat_id": self.current_chat,
            "sender": "You",
            "text": f"[{type_label}]",
            "time": time_str,
            "is_me": True,
            "type": "media",
            "is_encrypted": True
        })
        self._schedule_save()
        return True

    def delete_message(self, index):
        if 0 <= index < len(self.messages):
            self.messages.pop(index)
            self._schedule_save()
            return True
        return False

    def delete_message_by_chat_index(self, chat_index):
        chat_msgs = self.get_chat_messages()
        if 0 <= chat_index < len(chat_msgs):
            target = chat_msgs[chat_index]
            for i, msg in enumerate(self.messages):
                if msg is target:
                    self.messages.pop(i)
                    self._schedule_save()
                    return True
        return False

    def start_recording(self):
        self.is_recording = True
        self._recording_seconds = 0
        self._recording_timer = Clock.schedule_interval(self._update_recording_time, 1)

    def stop_recording(self):
        if self._recording_timer:
            self._recording_timer.cancel()
            self._recording_timer = None
        self.is_recording = False
        duration = self.recording_duration
        self.recording_duration = "00:00"
        return duration

    def _update_recording_time(self, dt):
        self._recording_seconds += 1
        minutes = self._recording_seconds // 60
        seconds = self._recording_seconds % 60
        self.recording_duration = f"{minutes:02d}:{seconds:02d}"

    # ─── Navigation ────────────────────────────────────────────

    def open_chat(self, contact_name):
        contact = self.get_contact(contact_name)
        if contact and contact.get("is_blocked"):
            self.import_status = "This contact is blocked"
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            return

        self.current_chat = contact_name
        if contact:
            self.is_group_chat = contact.get("is_group", False)
        self.screen_manager.current = "chat"

    def get_contact(self, name):
        for contact in self.contacts:
            if contact["name"] == name:
                return contact
        return None

    def go_home(self):
        self.screen_manager.current = "home"

    def open_profile(self):
        self.screen_manager.current = "profile"

    def open_group_interaction(self):
        self.screen_manager.current = "group_interaction"

    def open_contact_requests(self):
        self.screen_manager.current = "contact_request"

    def open_privacy(self):
        self.screen_manager.current = "privacy"

    # ─── Video Calls ───────────────────────────────────────────

    def start_video_call(self, contact_name):
        contact = self.get_contact(contact_name)
        if contact and contact.get("is_blocked"):
            self.import_status = "Cannot call blocked contact"
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            return

        self.current_chat = contact_name
        self.video_call_active = True
        self._call_seconds = 0
        self.update_call_duration()
        self._call_timer = Clock.schedule_interval(self._update_call_time, 1)
        self.screen_manager.current = "video_call"

    def _update_call_time(self, dt):
        self._call_seconds += 1
        self.update_call_duration()

    def update_call_duration(self):
        minutes = self._call_seconds // 60
        seconds = self._call_seconds % 60
        self.video_call_duration = f"{minutes:02d}:{seconds:02d}"

    def end_video_call(self):
        if self._call_timer:
            self._call_timer.cancel()
            self._call_timer = None
        self.video_call_active = False
        self._call_seconds = 0
        self.go_home()

    # ─── Profile Management ────────────────────────────────────

    def update_profile(self, name="", email="", phone="", status=""):
        if name:
            self.user_name = name
            self.user_avatar = name[:2].upper()
        if email:
            self.user_email = email
        if phone:
            self.user_phone = phone
        if status:
            self.user_status = status
        self._schedule_save()

    # ─── Contact Requests ──────────────────────────────────────

    def send_contact_request(self, to_phone, message=""):
        if not to_phone:
            return False

        self.contact_requests.append({
            "from": self.user_name,
            "from_phone": self.user_phone,
            "to_phone": to_phone,
            "message": message,
            "status": "pending",
            "time": "Just now",
            "direction": "outgoing"
        })
        self.import_status = "Contact request sent!"
        Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
        self._schedule_save()
        return True

    def accept_contact_request(self, request_index):
        if 0 <= request_index < len(self.contact_requests):
            request = self.contact_requests[request_index]
            if request["status"] == "pending":
                request["status"] = "accepted"

                self.contacts.append({
                    "name": request["from"],
                    "last_message": "",
                    "time": "",
                    "unread": 0,
                    "category": "friends",
                    "is_group": False,
                    "phone": request.get("from_phone", ""),
                    "status": "Available",
                    "can_message": True,
                    "is_blocked": False,
                    "is_verified": True
                })

                self.update_notification_count()
                self.import_status = f"You are now connected with {request['from']}!"
                Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
                self._schedule_save()
                return True
        return False

    def reject_contact_request(self, request_index):
        if 0 <= request_index < len(self.contact_requests):
            request = self.contact_requests[request_index]
            if request["status"] == "pending":
                request["status"] = "rejected"
                self.update_notification_count()
                self.import_status = "Request rejected"
                Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
                self._schedule_save()
                return True
        return False

    def block_user(self, user_name):
        if user_name not in self.blocked_users:
            self.blocked_users.append(user_name)
            contact = self.get_contact(user_name)
            if contact:
                contact["is_blocked"] = True
            self.import_status = f"{user_name} has been blocked"
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            self._schedule_save()
            return True
        return False

    def unblock_user(self, user_name):
        if user_name in self.blocked_users:
            self.blocked_users.remove(user_name)
            contact = self.get_contact(user_name)
            if contact:
                contact["is_blocked"] = False
            self.import_status = f"{user_name} has been unblocked"
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            self._schedule_save()
            return True
        return False

    # ─── Privacy Settings ──────────────────────────────────────

    def update_privacy(self, key, value):
        if key in self.privacy_settings:
            self.privacy_settings[key] = value
            self._schedule_save()
            return True
        return False

    def toggle_two_factor(self, enabled):
        self.two_factor_enabled = enabled
        if enabled:
            self.import_status = "Two-factor authentication enabled"
        else:
            self.import_status = "Two-factor authentication disabled"
        Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
        self._schedule_save()

    # ─── Group-to-Group Interaction ────────────────────────────

    def create_group_interaction(self, group1_name, group2_name):
        if not group1_name or not group2_name:
            return False

        existing = any(
            (i["group1"] == group1_name and i["group2"] == group2_name) or
            (i["group1"] == group2_name and i["group2"] == group1_name)
            for i in self.group_interactions
        )
        if not existing:
            self.group_interactions.append({
                "group1": group1_name,
                "group2": group2_name,
                "shared_chat": True,
                "messages": []
            })
            self._schedule_save()
            return True
        return False

    def send_group_interaction_message(self, from_group, text):
        if not text or not text.strip():
            return False

        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        for interaction in self.group_interactions:
            if interaction["group1"] == from_group or interaction["group2"] == from_group:
                interaction["messages"].append({
                    "sender": from_group,
                    "text": text.strip(),
                    "time": time_str
                })
                self._schedule_save()
                return True
        return False

    def get_group_interactions(self, group_name):
        return [i for i in self.group_interactions if i["group1"] == group_name or i["group2"] == group_name]

    # ─── WhatsApp Import ───────────────────────────────────────

    def import_whatsapp_chats(self, file_path=""):
        self.import_status = "Importing..."
        Clock.schedule_once(lambda dt: self._process_whatsapp_import(file_path), 0.1)

    def _process_whatsapp_import(self, file_path):
        if not file_path:
            self.import_status = "No file selected"
            return

        try:
            if not os.path.exists(file_path):
                self.import_status = "File not found"
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            groups = self._parse_whatsapp_export(content)

            for group_name, messages in groups.items():
                existing = any(c["name"] == group_name for c in self.contacts)
                if not existing:
                    self.contacts.append({
                        "name": group_name,
                        "last_message": messages[-1]["text"] if messages else "",
                        "time": messages[-1]["time"] if messages else "",
                        "unread": 0,
                        "category": "whatsapp",
                        "is_group": True,
                        "members": [],
                        "can_message": True,
                        "is_blocked": False
                    })

            self.import_status = f"Imported {len(groups)} groups!"
            Clock.schedule_once(lambda dt: setattr(self, 'import_status', ''), 3)
            self._schedule_save()

        except Exception as e:
            self.import_status = f"Import failed: {str(e)}"

    def _parse_whatsapp_export(self, content):
        groups = {}
        current_group = "Imported Chat"
        pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?:\s?[APap][Mm])?)\s+-?\s+([^:]+):\s+(.+)'

        for line in content.split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                date, time_str, sender, text = match.groups()
                if current_group not in groups:
                    groups[current_group] = []
                groups[current_group].append({
                    "sender": sender.strip(),
                    "text": text.strip(),
                    "time": time_str.strip(),
                    "is_me": sender.strip().lower() in ["you", "me"]
                })

        return groups

    # ─── Contact Management ────────────────────────────────────

    def add_contact(self, name, phone="", category="friends"):
        if not name:
            return

        name = Validator.sanitize_input(name)
        phone = Validator.sanitize_input(phone)

        self.contacts.append({
            "name": name,
            "last_message": "",
            "time": "",
            "unread": 0,
            "category": category,
            "is_group": False,
            "phone": phone,
            "status": "Available",
            "can_message": True,
            "is_blocked": False,
            "is_verified": False
        })
        self._schedule_save()

    def create_group(self, name, members):
        if not name or not members:
            return

        self.contacts.append({
            "name": Validator.sanitize_input(name),
            "last_message": "",
            "time": "",
            "unread": 0,
            "category": "friends",
            "is_group": True,
            "members": members,
            "can_message": True,
            "is_blocked": False
        })
        self._schedule_save()

    def get_all_groups(self):
        return [c for c in self.contacts if c.get("is_group")]

    def get_family_contacts(self):
        return [c for c in self.contacts if c.get("category") == "family"]

    def get_friend_contacts(self):
        return [c for c in self.contacts if c.get("category") == "friends"]

    def get_whatsapp_contacts(self):
        return [c for c in self.contacts if c.get("category") == "whatsapp"]

    def update_notification_count(self):
        pending_requests = sum(1 for r in self.contact_requests if r["status"] == "pending")
        self.notification_count = pending_requests
