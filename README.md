# Jamaa 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Kivy-orange.svg)](https://kivy.org/)
[![Platform](https://img.shields.io/badge/Platform-Android%20|%20iOS-green.svg)]()
[![Security](https://img.shields.io/badge/Security-E2EE%20|%20SHA--256-red.svg)]()

> **Jamaa** (*meaning "family" or "togetherness" in Swahili*) is a secure, privacy-focused cross-platform messaging application built to keep families, friends, and teams connected without compromising data control.

---

## ✨ Key Features

* **🔒 Privacy-First Communication:** End-to-End Encryption (E2EE) for messages and media, granular visibility controls (online status, last seen, read receipts), and optional Two-Factor Authentication (2FA).
* **🤝 User-Controlled Contacts:** No unwanted spam. Incoming conversations require mutual contact requests that you can accept, decline, or block.
* **🎙️ Rich Messaging:** Seamlessly exchange text, voice notes with live recording previews, files, images, videos, and emojis.
* **👥 Advanced Group & Cross-Group Collaboration:** Organize contacts into categories (Family, Friends, Work) with tailored restrictions, or connect two distinct groups using the **Group-to-Group Interaction** bridge.
* **📥 WhatsApp Import:** Import `.txt` WhatsApp export files directly to recreate and archive chats as native Jamaa groups.
* **📹 Integrated Calling:** Built-in direct video and audio calls with mute, speaker, and camera controls.

---

## 🧭 Category-Based Restriction Matrix

| Category | Add Members | Invite Groups | Message Character Limit |
| :--- | :---: | :---: | :--- |
| **Family** | ✅ | ✅ | Unlimited |
| **Friends** | ✅ | ✅ | Unlimited |
| **Work** | ❌ | ❌ | 500 characters |

---

## 🛠️ Tech Stack

* **Framework:** [Kivy](https://kivy.org/) / Python
* **Target Platforms:** Android, iOS, Desktop
* **Security & Auth:** End-to-End Encryption (E2EE), SHA-256 password hashing, 2FA
* **Data Storage:** Encrypted Local Storage

---

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* `pip` and `virtualenv`
* System dependencies for Kivy (see [Kivy Installation Guide](https://kivy.org/doc/stable/gettingstarted/installation.html))

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/jamaa-app.git](https://github.com/your-username/jamaa-app.git)
   cd jamaa-app
