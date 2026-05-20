# ReminderApp
It is a  smart user friendly reminder
====================================================================================
````markdown
# 📓 Smart Reminder PRO

A Python-based desktop reminder application with popup alerts, snooze system, sound alerts, and messaging support.

---

# 🚀 Features

✅ Multiple Reminder Support  
✅ Scrollable Modern UI  
✅ Popup Reminder Alerts  
✅ Beep Sound / Custom Music Alarm  
✅ Snooze Option  
✅ JSON-based Data Storage  
✅ Dynamic Reminder Scheduler  
✅ WhatsApp / Telegram Placeholder Routing  
✅ Link Attachment Support  
✅ Background Reminder Engine  
✅ Automatic Reminder Checking  

---

# 🛠 Technologies Used

- Python
- Tkinter
- tkcalendar
- JSON
- Threading
- winsound
- pygame

---

# 📂 Project Structure

```text
Smart_Reminder/
│
├── main.py
├── reminders.json
├── assets/
│   └── alarm.wav
├── README.md
└── requirements.txt
````

---

# ▶️ How to Run

## Step 1: Install Python

Download Python from:

[Python Official Website](https://www.python.org/downloads/?utm_source=chatgpt.com)

During installation:
✅ Check **"Add Python to PATH"**

---

## Step 2: Install Required Libraries

Open terminal inside project folder and run:

```bash
pip install tkcalendar pygame
```

---

## Step 3: Run the Application

```bash
python main.py
```

---

# 📦 Create EXE File

To convert the project into a desktop application:

Install PyInstaller:

```bash
pip install pyinstaller
```

Build EXE:

```bash
pyinstaller --onefile --windowed main.py
```

Generated file:

```text
dist/main.exe
```

Double click `main.exe` to open the app.

---

# 🔄 Dynamic Reminder System

The application stores reminders in a JSON file and continuously checks current date and time using a background scheduler thread.

Even if the UI is minimized, reminders continue working.

For automatic startup after restarting the computer:

1. Press `Win + R`
2. Type:

```text
shell:startup
```

3. Paste the shortcut of `main.exe`

Now the app starts automatically with Windows.

---

# 🔔 Reminder Workflow

```text
User Input
   ↓
Reminder Saved in JSON
   ↓
Background Scheduler
   ↓
Time Match Detection
   ↓
Popup Alert + Alarm
   ↓
Snooze / Stop
```

---

# 📸 Screenshots

## Main Interface

<img width="1280" height="720" alt="WhatsApp Image 2026-05-20 at 19 22 14" src="https://github.com/user-attachments/assets/b4326cef-5f5c-4f5f-80ee-0c2898da8dc1" />


## Reminder Popup


## Scrollable Reminder List



---

# 📘 Future Improvements

* Real WhatsApp API Integration
* Telegram Bot Messaging
* Email Notifications
* Cloud Database Support
* Voice Assistant Support
* System Tray Integration
* Mobile App Version

---

# 👨‍💻 Author

Developed by Debolina Nandi

---

# 📄 License

This project is for educational and academic purposes.

```
```
