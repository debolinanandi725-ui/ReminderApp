# ================= SMART REMINDER PRO (SCROLLABLE UI + MESSAGING DROPDOWN FIXED) =================
# Features:
# - Stable threaded scheduler
# - 5 Reminder slots
# - Scrollable UI
# - Snooze + Beep + Music
# - Messaging dropdown per reminder (Telegram / WhatsApp / Message App)

import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button, Entry, filedialog
from tkcalendar import DateEntry
import datetime
import threading
import time
import json
import os
import webbrowser
import winsound
import pygame

# ================= CONFIG =================
FILE = "reminders.json"
music_file = None
pygame.mixer.init()
lock = threading.Lock()
beep_event = threading.Event()
reminders = []

# ================= LOAD / SAVE =================

def load_data():
    global reminders
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
                reminders = data if isinstance(data, list) else []
        except:
            reminders = []


def save_data():
    with lock:
        with open(FILE, "w") as f:
            json.dump(reminders, f, indent=4)

# ================= SOUND =================

# ================= SOUND =================

def choose_music():
    global music_file
    music_file = filedialog.askopenfilename(
        title="Choose Alarm Music",
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )
    if music_file:
        messagebox.showinfo("Music Selected", "Alarm music added successfully!")

def play_music(path):
    try:
        if path and os.path.exists(path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
        else:
            print("Music file not found:", path)
    except Exception as e:
        print("Music error:", e)

def stop_alarm():
    try:
        pygame.mixer.music.stop()
    except:
        pass

def stop_beep():
    beep_event.set()
    stop_alarm()

def play_beep():
    beep_event.clear()
    for _ in range(10):
        if beep_event.is_set():
            break
        winsound.Beep(1500, 500)
        time.sleep(0.5)

def start_alarm(rem=None):
    music = ""

    if rem:
        music = rem.get("music", "")

    if not music:
        music = music_file

    if music and os.path.exists(music):
        play_music(music)
    else:
        threading.Thread(target=play_beep, daemon=True).start()

# ================= SNOOZE =================

def snooze(rem, mins, pop):
    rem["triggered"] = False
    rem["time"] = (datetime.datetime.now() + datetime.timedelta(minutes=mins)).strftime("%Y-%m-%d %H:%M")
    save_data()
    stop_beep()
    pop.destroy()



# ================= TELEGRAM =================

def send_telegram(to, msg):
    token = telegram_token.get()
    if not token or not to or not msg:
        return

    try:
        import requests
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": to, "text": msg})
    except:
        pass

# ================= OTHER MESSAGE APPS =================

def send_other(app, to, msg):
    print(f"[{app}] -> {to}: {msg}")

# ================= POPUP =================

def show_popup(rem):
    pop = Toplevel(root)
    pop.title("Smart Reminder")
    pop.geometry("430x460")
    pop.configure(bg="#0b0b12")
    pop.resizable(False, False)

    pop.attributes("-alpha", 0)

    def fade_in(alpha=0):
        if not pop.winfo_exists():
            return
        alpha += 0.06
        if alpha <= 1:
            pop.attributes("-alpha", alpha)
            pop.after(25, lambda: fade_in(alpha))
        else:
            pop.attributes("-alpha", 1)

    fade_in()

    # only animation, no new popup
    try:
        start_alarm_animation()
    except:
        pass

    header = tk.Label(
        pop,
        text="🔔 ⏰ REMINDER ALERT ⏰ 🔔",
        font=("Segoe UI", 16, "bold"),
        fg="#ff4fd8",
        bg="#0b0b12"
    )
    header.pack(pady=10)

    def header_glow(i=0):
        if not pop.winfo_exists():
            return
        colors = ["#ff4fd8", "#a855f7", "#38bdf8", "#facc15"]
        header.config(fg=colors[i % len(colors)])
        pop.after(450, lambda: header_glow(i + 1))

    header_glow()

    card = tk.Frame(
        pop,
        bg="#17172a",
        bd=2,
        relief="ridge",
        highlightbackground="#ff4fd8",
        highlightthickness=1
    )
    card.pack(padx=15, pady=8, fill="both", expand=True)

    alarm_icon = tk.Label(
        card,
        text="⏰",
        font=("Segoe UI Emoji", 42),
        bg="#17172a",
        fg="#ff4fd8"
    )
    alarm_icon.pack(pady=5)

    def bounce_icon(size=42, grow=True):
        if not pop.winfo_exists():
            return

        if grow:
            size += 2
            if size >= 50:
                grow = False
        else:
            size -= 2
            if size <= 42:
                grow = True

        alarm_icon.config(font=("Segoe UI Emoji", size))
        pop.after(120, lambda: bounce_icon(size, grow))

    bounce_icon()

    tk.Label(
        card,
        text=f"📌 {rem.get('title','')}",
        font=("Segoe UI", 13, "bold"),
        fg="#38bdf8",
        bg="#17172a"
    ).pack(pady=5)

    tk.Label(
        card,
        text=f"⏰ Time: {rem.get('time','')}",
        fg="#f8fafc",
        bg="#17172a",
        font=("Segoe UI", 10)
    ).pack()

    tk.Label(
        card,
        text=f"💬 {rem.get('msg','')}",
        fg="#d1d5db",
        bg="#17172a",
        wraplength=350,
        font=("Segoe UI", 10)
    ).pack(pady=8)

    def cute_button(parent, text, bg, fg, command, width=None):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground="#facc15",
            activeforeground="black",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            width=width
        )

        btn.bind("<Enter>", lambda e: btn.config(bg="#facc15", fg="black"))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg))

        return btn

    link = rem.get("link")
    if link:
        def open_link():
            ok = messagebox.askyesno("Open Link", "Open this link?\n\n" + link)
            if ok:
                webbrowser.open(link)

        cute_button(card, "🌐 Open Link", "#38bdf8", "black", open_link).pack(pady=5)

    tk.Label(
        card,
        text="💤 Snooze",
        fg="#facc15",
        bg="#17172a",
        font=("Segoe UI", 10, "bold")
    ).pack(pady=5)

    snooze_frame = tk.Frame(card, bg="#17172a")
    snooze_frame.pack()

    def add_snooze(mins):
        stop_beep()
        try:
            stop_alarm_animation()
        except:
            pass
        snooze(rem, mins, pop)

    for m in [1, 5, 10, 15, 30]:
        cute_button(
            snooze_frame,
            f"{m}m",
            "#a855f7",
            "white",
            lambda x=m: add_snooze(x),
            width=4
        ).pack(side="left", padx=3)

    btn_frame = tk.Frame(pop, bg="#0b0b12")
    btn_frame.pack(pady=10)

    def stop_all():
        stop_beep()
        try:
            stop_alarm_animation()
        except:
            pass

    def close_all():
        stop_beep()
        try:
            stop_alarm_animation()
        except:
            pass
        pop.destroy()

    cute_button(btn_frame, "🔇 Stop Beep", "#ef4444", "white", stop_all, width=12).pack(side="left", padx=5)
    cute_button(btn_frame, "❌ Close", "#334155", "white", close_all, width=12).pack(side="left", padx=5)

    pop.protocol("WM_DELETE_WINDOW", close_all)

    start_alarm(rem)
# ================= ENGINE =================

# ================= SCHEDULER ENGINE =================
def engine():
    while True:
        with lock:
            for rem in reminders:
                if rem["triggered"]:
                    continue
                
                try:
                    rem_time = datetime.datetime.strptime(rem["time"], "%Y-%m-%d %H:%M")
                    now = datetime.datetime.now()
                    
                    if now >= rem_time:
                        rem["triggered"] = True
                        root.after(0, lambda r=rem: show_popup(r))
                        
                        # Send message if app is selected
                        app = rem.get("app", "None")
                        if app == "Telegram":
                            send_telegram(rem.get("to"), rem.get("msg"))
                        elif app != "None":
                            send_other(app, rem.get("to"), rem.get("msg"))
                        
                        
                except:
                    pass
        
        time.sleep(30) 

# ================= ADD =================

def add_reminder():
    for i in range(5):
        title = title_entries[i].get()
        time_val = time_entries[i].get()

        if not title or not time_val:
            continue

        try:
            datetime.datetime.strptime(time_val, "%H:%M")
        except:
            messagebox.showerror("Error","Time must be HH:MM")
            return

        rem = {
            "title": title,
            "time": f"{cal_entries[i].get_date()} {time_val}",
            "link": link_entries[i].get(),
            "music": music_entries[i].get() or music_file,
            "app": app_vars[i].get(),
            "to": to_entries[i].get(),
            "msg": msg_entries[i].get(),
            "triggered": False
        }

        with lock:
            reminders.append(rem)

    save_data()
    messagebox.showinfo("Success","Reminders added")


#-------------------============================--------------------------

# ================= PREMIUM CUTE MOBILE UI =================
from PIL import Image, ImageTk

BG = "#080814"
CARD = "#17172a"
CARD2 = "#211f3d"
PINK = "#ff4fd8"
PURPLE = "#a855f7"
SKY = "#38bdf8"
YELLOW = "#facc15"
TEXT = "#f8fafc"
MUTED = "#a1a1aa"
BUTTON = "#ff4fd8"
SHADOW = "#2d2d44"

root = tk.Tk()
root.title("📓 Smart Reminder Notebook PRO")
root.geometry("900x900")
root.configure(bg=BG)

# ================= MAIN SCROLL =================
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True)

canvas = tk.Canvas(main, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(main, command=canvas.yview)

scroll_frame = tk.Frame(canvas, bg=BG)
window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

def resize_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(window, width=event.width)

scroll_frame.bind("<Configure>", resize_scroll)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def mouse_scroll(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", mouse_scroll)

# ================= FLOATING PENCIL RIGHT =================
pencil = tk.Label(root, text="✏️", font=("Arial", 42), bg=BG, fg=PINK)
pencil.place(x=830, y=160)

pencil_y = 160
pencil_dir = 1

def move_pencil():
    global pencil_y, pencil_dir
    pencil_y += 2 * pencil_dir
    pencil.place(x=830, y=pencil_y)

    if pencil_y > 650:
        pencil_dir = -1
    elif pencil_y < 120:
        pencil_dir = 1

    root.after(35, move_pencil)

move_pencil()

def pencil_glow(i=0):
    colors = [PINK, PURPLE, SKY, YELLOW]
    pencil.config(fg=colors[i % len(colors)])
    root.after(450, lambda: pencil_glow(i + 1))

pencil_glow()

# ================= HEADER =================
title = tk.Label(
    scroll_frame,
    text="📓 Smart Reminder Notebook ✏️",
    font=("Segoe UI", 24, "bold"),
    fg=PINK,
    bg=BG
)
title.pack(pady=(15, 5))

subtitle = tk.Label(
    scroll_frame,
    text="Your cute AI reminder assistant",
    font=("Segoe UI", 11),
    fg=MUTED,
    bg=BG
)
subtitle.pack(pady=(0, 10))

def title_glow(i=0):
    colors = [PINK, PURPLE, SKY, YELLOW]
    title.config(fg=colors[i % len(colors)])
    root.after(650, lambda: title_glow(i + 1))

title_glow()

# ================= ALARM CLOCK CARD =================
alarm_card = tk.Frame(scroll_frame, bg=CARD, padx=16, pady=16)
alarm_card.pack(fill="x", padx=35, pady=12)

# cute alarm image
try:
    img_raw = Image.open(r"/mnt/data/0846c9ae-64f6-44f1-a0b3-fb75c31e8945.png")
    img_raw = img_raw.resize((115, 115))
    clock_img = ImageTk.PhotoImage(img_raw)

    alarm_img_label = tk.Label(alarm_card, image=clock_img, bg=CARD)
    alarm_img_label.pack()
    root.clock_img = clock_img
except Exception:
    alarm_img_label = tk.Label(
        alarm_card,
        text="⏰",
        font=("Arial", 64),
        bg=CARD,
        fg=PINK
    )
    alarm_img_label.pack()

clock_text = tk.Label(
    alarm_card,
    text="🕒 00:00:00",
    font=("Segoe UI", 18, "bold"),
    fg=SKY,
    bg=CARD
)
clock_text.pack(pady=5)

alarm_status = tk.Label(
    alarm_card,
    text="💤 Waiting for your next reminder...",
    font=("Segoe UI", 10),
    fg=MUTED,
    bg=CARD
)
alarm_status.pack()

# ================= CLOCK UPDATE =================
def update_clock():
    clock_text.config(text="🕒 " + time.strftime("%I:%M:%S %p"))
    root.after(1000, update_clock)

update_clock()

# ================= RINGING SHAKE + FLASH ANIMATION =================
shake_active = False

def start_alarm_animation():
    global shake_active
    shake_active = True
    alarm_status.config(text="🔔 ALARM RINGING!", fg=YELLOW)
    shake_clock()
    flash_alarm()

def stop_alarm_animation():
    global shake_active
    shake_active = False
    alarm_status.config(text="💤 Waiting for your next reminder...", fg=MUTED)
    alarm_card.config(bg=CARD)
    clock_text.config(bg=CARD)
    alarm_img_label.config(bg=CARD)

def shake_clock(count=0):
    if not shake_active:
        return

    offset = -6 if count % 2 == 0 else 6
    alarm_img_label.pack_configure(padx=offset)

    root.after(80, lambda: shake_clock(count + 1))

def flash_alarm(i=0):
    if not shake_active:
        return

    colors = [CARD, "#3b1d4f", "#4a1232", "#2e365f"]
    alarm_card.config(bg=colors[i % len(colors)])
    clock_text.config(bg=colors[i % len(colors)])
    alarm_img_label.config(bg=colors[i % len(colors)])

    root.after(250, lambda: flash_alarm(i + 1))

# ================= SOUND WAVE ANIMATION =================
wave_frame = tk.Frame(alarm_card, bg=CARD)
wave_frame.pack(pady=10)

waves = []
for i in range(12):
    bar = tk.Label(
        wave_frame,
        text="▮",
        font=("Segoe UI", 12),
        fg=SKY,
        bg=CARD
    )
    bar.pack(side="left", padx=2)
    waves.append(bar)

def animate_wave(step=0):
    heights = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    colors = [SKY, PINK, PURPLE, YELLOW]

    for i, bar in enumerate(waves):
        bar.config(
            text=heights[(step + i) % len(heights)],
            fg=colors[(step + i) % len(colors)],
            bg=alarm_card["bg"]
        )

    root.after(160, lambda: animate_wave(step + 1))

animate_wave()

# ================= TELEGRAM CARD =================
def make_mobile_card(title_text, color=SKY):
    card = tk.Frame(
        scroll_frame,
        bg=CARD,
        padx=15,
        pady=15,
        highlightbackground=SHADOW,
        highlightthickness=1
    )
    card.pack(fill="x", padx=35, pady=10)

    tk.Label(
        card,
        text=title_text,
        bg=CARD,
        fg=color,
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w")

    return card

token_card = make_mobile_card("📡 Telegram Bot Token", SKY)

telegram_token = tk.Entry(
    token_card,
    bg="#0f172a",
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat"
)
telegram_token.pack(fill="x", pady=6)

# ================= ARRAYS =================
options = ["None", "Telegram", "WhatsApp", "Message App"]

title_entries = []
time_entries = []
cal_entries = []
link_entries = []
music_entries = []
app_vars = []
to_entries = []
msg_entries = []

def make_label(parent, text):
    return tk.Label(parent, text=text, bg=parent["bg"], fg=MUTED)

def make_entry(parent):
    return tk.Entry(
        parent,
        bg="#0f172a",
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    )

# ================= STICKY NOTE REMINDER CARDS =================
sticky_colors = [CARD, "#1f183d", "#201b2f", "#14233a", "#2b2135"]

for i in range(5):
    note_color = sticky_colors[i % len(sticky_colors)]

    card = tk.Frame(
        scroll_frame,
        bg=note_color,
        padx=15,
        pady=15,
        highlightbackground=YELLOW if i % 2 == 0 else PURPLE,
        highlightthickness=1
    )
    card.pack(fill="x", padx=35, pady=12)

    tk.Label(
        card,
        text=f"📌 Sticky Note {i+1}",
        bg=note_color,
        fg=YELLOW,
        font=("Segoe UI", 13, "bold")
    ).pack(anchor="w")

    def label(text, parent=card):
        return tk.Label(parent, text=text, bg=parent["bg"], fg=MUTED)

    def entry(parent=card):
        return tk.Entry(
            parent,
            bg="#0f172a",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )

    label("Title").pack(anchor="w")
    t = entry(); t.pack(fill="x", pady=2)

    label("Date").pack(anchor="w")
    c = DateEntry(card, width=18)
    c.pack(fill="x", pady=2)

    label("Time (HH:MM)").pack(anchor="w")
    tm = entry(); tm.pack(fill="x", pady=2)

    label("Link (YouTube / Meet)").pack(anchor="w")
    l = entry(); l.pack(fill="x", pady=2)

    label("Music").pack(anchor="w")
    m = entry(); m.pack(fill="x", pady=2)

    def browse_music(entry_box=m):
     path = filedialog.askopenfilename(
        title="Choose Alarm Music",
        filetypes=[("Audio Files", "*.mp3 *.wav")]
     )
     if path:
        entry_box.delete(0, tk.END)
        entry_box.insert(0, path)

    tk.Button(
        card,
        text="🎵 Browse Music",
        bg=SKY,
        fg="black",
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        command=browse_music
    ).pack(pady=5)

    tk.Button(
    card,
    text="🎵 Choose Alarm Music",
    command=choose_music,
    bg="#FFB6C1",
    font=("Arial", 12, "bold")
).pack(pady=5)

    label("App").pack(anchor="w")
    var = tk.StringVar(value="None")
    tk.OptionMenu(card, var, *options).pack(fill="x", pady=2)

    label("To").pack(anchor="w")
    to = entry(); to.pack(fill="x", pady=2)

    label("Message").pack(anchor="w")
    ms = entry(); ms.pack(fill="x", pady=2)

    title_entries.append(t)
    time_entries.append(tm)
    cal_entries.append(c)
    link_entries.append(l)
    music_entries.append(m)
    app_vars.append(var)
    to_entries.append(to)
    msg_entries.append(ms)

# ================= MOBILE BOTTOM ACTION BAR =================
bottom_bar = tk.Frame(root, bg="#0f172a", padx=10, pady=10)
bottom_bar.pack(side="bottom", fill="x")

add_btn = tk.Button(
    bottom_bar,
    text="✨ ADD REMINDER ✨",
    bg=BUTTON,
    fg="black",
    font=("Segoe UI", 13, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    command=add_reminder
)
add_btn.pack(side="left", expand=True, fill="x", padx=5)

demo_alarm_btn = tk.Button(
    bottom_bar,
    text="🔔 Preview Alarm",
    bg=YELLOW,
    fg="black",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    padx=10,
    pady=8,
    command=start_alarm_animation
)
demo_alarm_btn.pack(side="left", expand=True, fill="x", padx=5)

stop_anim_btn = tk.Button(
    bottom_bar,
    text="Stop",
    bg="#ef4444",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    padx=10,
    pady=8,
    command=stop_alarm_animation
)
stop_anim_btn.pack(side="left", expand=True, fill="x", padx=5)

# ================= BUTTON PULSE =================
def button_pulse(state=True):
    add_btn.config(bg=PINK if state else PURPLE)
    root.after(700, lambda: button_pulse(not state))

button_pulse()

# ================= SAFE ENGINE START =================
def start_engine():
    threading.Thread(target=engine, daemon=True).start()

root.after(500, start_engine)

load_data()
root.mainloop()