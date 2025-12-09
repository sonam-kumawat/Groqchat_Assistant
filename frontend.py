import tkinter as tk
import threading
from backend import generate_reply, handle_special_commands

# ---------------------- SEND HANDLER ----------------------
def send_message(event=None):
    text = entry_field.get()
    if not text.strip():
        return

    entry_field.delete(0, tk.END)
    add_chat_bubble(text, sender="user")

    special = handle_special_commands(text)
    if special:
        add_chat_bubble(special, sender="bot")
        return

    threading.Thread(target=get_bot_reply, args=(text,), daemon=True).start()

def get_bot_reply(user_text):
    try:
        reply = generate_reply(user_text)
    except Exception as e:
        reply = f"⚠️ Error: {e}"
    add_chat_bubble(reply, sender="bot")


# ---------------------- ADD CHAT BUBBLE ----------------------
def add_chat_bubble(text, sender="bot"):
    bubble_frame = tk.Frame(scrollable_frame, bg="white")
    bubble_frame.pack(fill="x", pady=5, padx=10)

    if sender == "user":
        bubble = tk.Label(
            bubble_frame,
            text=text,
            bg="#0078FF",
            fg="white",
            wraplength=root.winfo_width() - 120,
            justify="left",
            font=("Arial", 11),
            padx=10,
            pady=5
        )
        bubble.pack(anchor="e")   # RIGHT ALIGN

    else:
        bubble = tk.Label(
            bubble_frame,
            text=text,
            bg="#E5E5EA",
            fg="black",
            wraplength=root.winfo_width() - 120,
            justify="left",
            font=("Arial", 11),
            padx=10,
            pady=5
        )
        bubble.pack(anchor="w")   # LEFT ALIGN

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)


# ---------------------- GUI LAYOUT ----------------------
root = tk.Tk()
root.title("MindChat – LLM Chatbot")
root.geometry("500x600")
root.configure(bg="white")

# --- Scrollable chat canvas ---
chat_frame = tk.Frame(root, bg="white")
chat_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(chat_frame, bg="white", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)


# --- Bottom input area ---
entry_frame = tk.Frame(root, bg="white")
entry_frame.pack(side="bottom", fill="x", padx=10, pady=10)

entry_field = tk.Entry(entry_frame, font=("Arial", 12))
entry_field.pack(side="left", fill="x", expand=True, padx=(0, 10))

send_button = tk.Button(
    entry_frame,
    text="Send",
    command=send_message,
    bg="#0078FF",
    fg="white",
    padx=20,
    pady=5
)
send_button.pack(side="right")

root.bind("<Return>", send_message)

root.mainloop()
