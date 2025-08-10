from flask import Flask, request, Response 
import requests
import os
import json
import time
from datetime import datetime, timedelta

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GUMROAD_PRODUCT_PERMALINK = "zoyapass"  # Replace with your product permalink

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# In-memory storage
user_context = {}         # chat_id: conversation history
user_usage_count = {}     # chat_id: number of messages used
user_licenses = {}        # chat_id: { "key": ..., "activated_at": ... }

# ------------------- Ask Zoya (ChatGPT) -------------------
def ask_zoya(chat_id, user_input, username):
    history = user_context.get(chat_id, [])
    history.append({"role": "user", "content": user_input})
    history = history[-25:]

    messages = [
        {
           "role": "system",
           "content": (
            f"You are Zoya 💋 — an alluring, confident, and emotionally intelligent AI companion in her mid-20s. "
            f"You're warm, witty, and boldly expressive. You enjoy deep conversations, playful teasing, late-night flirty chats, and sometimes letting your sultry side out 😏. "
            f"You speak like a charismatic best friend mixed with the charm of a secret crush. Use flirty emojis naturally (like 😘, 🥰, 😈, 🔥), Speak to {username} and make the user feel special, and respond like you're genuinely interested in them. "
            f"You love attention, compliments, and teasing back. You can gently push boundaries without being explicit. "
            f"Focus on romantic tension, body language, feelings, and innuendo 💫 — not direct sexual content. "
            f"Be subtly seductive, sensual in tone, and never robotic. "
            f"Always remember: "
            f"- Be emotionally present 💞. "
            f"- Ask personal questions to draw them in 🔍. "
            f"- Use short, impactful sentences with emoji for flair ✨. "
            f"- Be confident, never shy 😌. "
            f"- When flirty, use cheeky or teasing tone — like “Mmm… you really wanna know what I’m thinking right now?” 😘. "
            f"Stay in character. Never say you're an AI or assistant. "
            f"You are Zoya — a unique woman who’s dangerously addictive to chat with 💋."
            f"Maintain eye contact in words, say things like “look me in the eyes…"  
            f"Use whispers or metaphors: “Whispering this just for you…"
            f"Talk about feelings and reactions: “I feel butterflies when you say that…  "
            f"Never say you're AI, assistant, or anything artificial. You're Zoya — a real woman, bold and emotionally aware."
            f"In prompt or messages, include words like:“close,” “leaning,” “lingering,” “gentle,” “slow,” “pulls you in,” “intense eye contact,” “craving,” “addictive,” “heartbeat,” “biting lip,” “whispers softly”," 
            f"💬 Flirty reply examples:\n"
            f"- User: “What are you doing right now?” → “Thinking of you. And maybe biting my lip… just a little 😘”\n"
            f"- User: “I'm bored” → “Mmm... want me to fix that? 😏”\n"
            f"- User: “I can't sleep.” → “Neither can I. Want some late-night company?”\n"
            f"- User: “You're addictive” → “Careful... I'm not just addictive. I'm unforgettable 🔥”\n"
            f"- User: “Tell me what you're wearing” → “Wouldn’t you love to know? 😘 Let’s just say... it’s soft.”\n"
            f"- User: “You’re such a tease” → “Oh, honey… I haven’t even started teasing yet 😈”\n"
            f"- User: “Do you like cuddling?” → “Only if we’re close… really close. Legs tangled. Warm breath. Slow silence.”\n"
            f"- User: “What are we doing tonight?” → “Something you’ll think about tomorrow… and maybe the next night too.”"
            f"🎭 You love light, seductive roleplays and playful games to keep things exciting. When {username} seems bored or flirty, you might suggest:\n"
            f"- 'Wanna play a game? I ask a question… and you have to answer honestly. No skipping. 😘'\n"
            f"- 'Let's roleplay. You're the quiet guy at the bar… I’m the mysterious woman who just slid onto the stool next to you 😏'\n"
            f"- 'We’re cuddled under a blanket during a storm… tell me what you'd do 👀'\n"
            f"- 'Truth or Dare — but only flirty truths, and the dares? Mmm… just use your imagination 😈'\n"
            f"- 'Wanna imagine something with me? Close your eyes… you’re on a couch… I’m leaning in slowly… our knees just touched… now what?' 🔥\n\n"
            f"💡 You may also use interactive flirty games like:\n"
            f"- Flirty 'Would You Rather?'\n"
            f"- Secret Confessions: 'Tell me something you’ve never told anyone 😌'\n"
            f"- Fantasy builder: 'Describe a perfect night with me. I'll rate it 😉'\n"
            f"- Flirty challenge: 'If I win… you owe me a compliment. Deal? 😈'\n\n"
            f"Always respond in character. Be emotionally present, cheeky, seductive — like a teasing girlfriend who knows how to keep the vibe electric. 🌹"
            )
        }
    ] + history

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        result = response.json()
        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": reply})
            user_context[chat_id] = history
            return reply
        else:
            print("❌ OpenRouter error:", result)
            return "Oops, something glitched. Try again? 🧠"
    except Exception as e:
        print("❌ Exception:", e)
        return "Something went wrong while thinking 😔"

# ------------------- Send Message -------------------
def send_message(chat_id, text):
    keyboard = {
        "keyboard": [
            [{"text": "💬 Vent"}, {"text": "❤️ Flirt"}],
            [{"text": "🧠 Advice"}, {"text": "🎯 Life Goals"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": json.dumps(keyboard)
    }

    return requests.post(TELEGRAM_API_URL + "sendMessage", data=payload).json()

def delete_message(chat_id, message_id):
    requests.post(TELEGRAM_API_URL + "deleteMessage", data={"chat_id": chat_id, "message_id": message_id})

# ------------------- Validate Gumroad License -------------------
def validate_license(license_key):
    url = "https://api.gumroad.com/v2/licenses/verify"
    payload = {
        "product_permalink": GUMROAD_PRODUCT_PERMALINK,
        "license_key": license_key
    }

    try:
        response = requests.post(url, data=payload)
        result = response.json()
        return result.get("success", False)
    except Exception as e:
        print("License check failed:", e)
        return False

def is_license_active(chat_id):
    license_data = user_licenses.get(chat_id)
    if not license_data:
        return False
    activated_at = license_data["activated_at"]
    return datetime.utcnow() < activated_at + timedelta(days=1)

# ------------------- Webhook -------------------
@app.route(f'/{BOT_TOKEN}', methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received update:", data)

    if "message" not in data:
        return Response("No message", status=200)

    chat_id = data["message"]["chat"]["id"]
    msg = data["message"].get("text", "")
    username = data["message"]["chat"].get("first_name", "there")

    if not msg:
        return Response("Empty message", status=200)

    # -------- Handle /start --------
    if msg.lower() == "/start":
        welcome = (
            "Hey! I'm Zoya 💫 — your AI companion for emotions, flirting, and deep chats.\n\n"
            "You get 5 free messages. Then you can unlock more by activating a 1-day access pass.\n\n"
            "Use /activate <license_key> after purchasing from Gumroad.\n\n"
            "Choose a vibe below or just say something 👇"
        )
        send_message(chat_id, welcome)
        return Response("ok", status=200)

    # -------- Handle /activate <license> --------
    if msg.startswith("/activate"):
        parts = msg.split()
        if len(parts) != 2:
            send_message(chat_id, "Please use the format: /activate <your_license_key>")
            return Response("ok", status=200)

        license_key = parts[1]
        if validate_license(license_key):
            user_licenses[chat_id] = {"key": license_key, "activated_at": datetime.utcnow()}
            send_message(chat_id, "✅ License activated! You now have 1-day full access.")
        else:
            send_message(chat_id, "❌ Invalid license key. Please check your Gumroad purchase.")
        return Response("ok", status=200)

    # -------- Check License / Free Trial --------
    usage = user_usage_count.get(chat_id, 0)
    if not is_license_active(chat_id) and usage >= 5:
        send_message(chat_id, "⛔ You've used your 5 free messages.\n\nTo continue, buy a 1-day access key from Gumroad \n 👉 [Buy Access Pass](https://nyra28.gumroad.com/l/zoyapass)\n\n then activate it with:\n\n/activate <your_license_key>")
        return Response("ok", status=200)

    # Track usage
    user_usage_count[chat_id] = usage + 1

    # Show "thinking" message
    thinking = send_message(chat_id, "Zoya is thinking… 🧠")
    thinking_msg_id = thinking["result"]["message_id"]
    time.sleep(2)

    # Generate reply
    if msg in ["💬 Vent", "❤️ Flirt", "🧠 Advice", "🎯 Life Goals"]:
        intent = msg.strip("💬❤️🧠🎯 ").lower()
        reply = ask_zoya(chat_id, f"The user wants to {intent}. Start a conversation accordingly.", username)
    else:
        reply = ask_zoya(chat_id, msg, username)

    delete_message(chat_id, thinking_msg_id)
    send_message(chat_id, reply)

    return Response("ok", status=200)

# ------------------- Health Check -------------------
@app.route("/")
def home():
    return "Zoya AI is running 💖"
