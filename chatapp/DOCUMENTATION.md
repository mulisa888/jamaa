# Jamaa App Documentation

## Overview

**Jamaa** is a secure messaging application designed for families and friends to stay connected. It provides comprehensive privacy controls, multiple communication methods, and user-managed contact system.

---

## App Name

**Jamaa** - Meaning "family" or "togetherness" in Swahili.

---

## Core Features

### 1. Authentication & Account

**What it does:** Secure login and signup system.

**How to use:**
- Open the app to see the login screen
- Enter email and password to login
- Tap "Sign Up" to create a new account
- Enter name, email, phone, and password
- After signup, you're automatically logged in

**Security:**
- Passwords are hashed using SHA-256
- Two-factor authentication available
- Unique user ID generated for each account

---

### 2. Messaging

**What it does:** Send text messages, voice notes, media, and emojis.

**How to use:**
- Open a chat with any contact
- Type your message in the input field
- Tap "Send" or press Enter

**Message Types:**

| Type | Icon | Description |
|------|------|-------------|
| Text | None | Standard text message |
| Voice Note | 🎤 | Record and send audio |
| Media | 📎 | Share photos, videos, files |
| Emoji | 😊 | Express with emojis |

---

### 3. Voice Notes

**What it does:** Record and send audio messages.

**How to use:**
- Tap the microphone icon (🎤) in the input area
- Recording starts - you'll see the timer
- Tap "Stop" when done
- Preview the recording
- Tap "Send Voice Note" to send

---

### 4. Media Sharing

**What it does:** Share photos, videos, and files.

**How to use:**
- Tap the attachment icon (📎) in the input area
- Select media type:
  - Photo - Share images
  - Video - Share videos
  - File - Share documents
- Media is sent to the chat

---

### 5. Emoji Support

**What it does:** Add emojis to messages.

**How to use:**
- Tap the emoji icon (😊) in the input area
- The emoji picker appears above the input
- Tap any emoji to insert it
- Tap again to hide the picker

**Available Emojis:**
😀 😂 ❤️ 👍 🎉 😢 🔥 💯

---

### 6. Contact Management (User-Controlled)

**What it does:** You control who can contact you.

**How it works:**
- Others must send you a contact request
- You receive the request with their message
- You can Accept, Reject, or Block them
- Only accepted contacts appear in your list

**How to manage:**
- Tap "Requests" on the home screen
- View received requests
- See who's requesting to connect
- Accept to add them to contacts
- Reject to decline
- Block to prevent future requests

---

### 7. Contact Requests

**What it does:** Send and receive contact requests.

**To send a request:**
- Tap "Requests" on home screen
- Tap "+ New Request"
- Enter phone number
- Add an optional message
- Tap "Send Request"

**To manage requests:**
- Go to "Requests" screen
- View "Received" tab for incoming requests
- View "Sent" tab for outgoing requests
- Accept, Reject, or Block each request

---

### 8. Privacy Settings

**What it does:** Control your privacy and visibility.

**How to use:**
- Tap your avatar on home screen
- Go to "Privacy & Security"
- Toggle settings on/off

**Available Settings:**

| Setting | Description |
|---------|-------------|
| Show Online Status | Let others see when you're online |
| Show Last Seen | Let others see your last active time |
| Show Read Receipts | Let others know when you've read messages |
| Show Profile Photo | Let others see your profile photo |
| Allow Contact Requests | Let others send you requests |
| Block Unknown Numbers | Block messages from unknown numbers |
| End-to-End Encryption | Encrypt all messages |

---

### 9. Security Features

**What it does:** Protect your account and messages.

**Features:**
- Password hashing (SHA-256)
- Two-factor authentication
- End-to-end encryption for messages
- Block/unblock users
- User-controlled contacts

**Two-Factor Authentication:**
- Go to Privacy & Security
- Toggle "Two-Factor Authentication"
- Adds extra security layer

---

### 10. Profile Management

**What it does:** Manage your profile information.

**How to use:**
- Tap your avatar on home screen
- Edit your information:
  - Name
  - Email
  - Phone
  - Status
- Tap "Save Changes"

**Features:**
- Avatar shows your initials
- Status visible to contacts
- Profile photo toggle

---

### 11. Group Chats

**What it does:** Create groups for multiple people.

**How to use:**
- Tap "+" on home screen
- Select "Create Group"
- Enter group name
- Add members

---

### 12. Group-to-Group Interaction

**What it does:** Connect two groups for shared communication.

**How to use:**
- Tap "Groups" on home screen
- Select Group 1
- Select Group 2
- Tap "Create Interaction"
- Messages are shared between groups

**Use cases:**
- Family + Friends events
- Work teams collaborating
- Cross-group announcements

---

### 13. Video Calls

**What it does:** Make video calls to contacts.

**How to use:**
- Open a chat
- Tap "Video" or "Call" button
- Call screen opens
- Use controls:
  - Mute - Toggle microphone
  - Video - Toggle camera
  - Speaker - Toggle speaker
  - End Call - Hang up

---

### 14. WhatsApp Import

**What it does:** Import WhatsApp chat exports.

**How to use:**
- Export chat from WhatsApp (Chat > Export Chat)
- Save the .txt file
- Tap "Import WhatsApp" on home screen
- Select the file
- Chats are imported as groups

---

### 15. Chat Restrictions

**What it does:** Controls per category.

**Restrictions:**

| Category | Add Members | Invite Groups | Message Length |
|----------|-------------|---------------|----------------|
| Family | Yes | Yes | Unlimited |
| Friends | Yes | Yes | Unlimited |
| Work | No | No | 500 characters |

---

## Navigation

### Home Screen
- View contacts/groups
- Filter by category
- Access profile
- Access requests
- Access groups
- Add new contacts/groups

### Chat Screen
- Send messages
- Send voice notes
- Share media
- Add emojis
- Make calls

### Profile Screen
- Edit information
- View avatar

### Contact Requests Screen
- View received requests
- View sent requests
- Send new requests
- Accept/Reject/Block

### Privacy Screen
- Toggle privacy settings
- Enable 2FA
- View blocked users
- Logout

### Group Interaction Screen
- Create group connections
- Send shared messages

---

## Privacy & Security

### Your Data
- You control who can contact you
- You decide what information to share
- You can block anyone at any time

### Message Security
- End-to-end encryption enabled by default
- Messages are secure in transit
- Only you and recipient can read

### Contact Control
- Others must request to connect
- You accept or reject requests
- You can block unwanted contacts

---

## Tips

1. **Review requests regularly** - Check the Requests screen often
2. **Use categories** - Organize contacts by Family, Friends, Work
3. **Enable encryption** - Keep it on for security
4. **Use voice notes** - Quick way to send longer messages
5. **Block unwanted** - Don't hesitate to block spam

---

## Troubleshooting

**Can't receive messages:**
- Check privacy settings
- Ensure you're not blocking the sender
- Verify contact is accepted

**Voice note not working:**
- Grant microphone permission
- Check device storage

**Media not sending:**
- Grant storage permission
- Check file size

**Can't add contacts:**
- Ensure they've sent you a request
- Check if they're already in your list

---

## Technical Details

- **Framework:** Kivy
- **Platforms:** Android, iOS
- **Encryption:** End-to-end
- **Password Hash:** SHA-256
- **Storage:** Local

---

## Version

**Current Version:** 2.0.0

**App Name:** Jamaa

---

## Support

For issues or questions, contact support.
