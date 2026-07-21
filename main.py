import os
import time
import threading
import telebot
from flask import Flask, request

BOT_TOKEN = "8744124078:AAF_ZzrHZnRnf-zKVWYNO_rgIZINOByXSyE"
STORAGE_CHANNEL_ID = -1004415434873  
VIP_CHANNEL_ID = -1004401727688  

PUBLIC_CHANNEL_LINK = "https://t.me/your_public_channel" 
VIP_ADMIN_LINK = "https://t.me/Lynn_subflix528"           

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

def is_vip_member(user_id):
    try:
        member = bot.get_chat_member(VIP_CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def auto_delete_message(chat_id, message_id):
    time.sleep(120)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

@bot.message_handler(commands=['start'])
def send_vip_movie(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    command_args = message.text.split()
    
    if len(command_args) == 1:
        welcome_text = (
            "<b>VIP MM SubFlix မှ ကြိုဆိုပါတယ်ရှင့်။ ✨</b>\n\n"
            "🎬 ဇာတ်ကားများကိုကြည့်ရှုရန် ကျွန်မတို့၏ <b>Public Channel</b> တွင် လင့်ခ်များ ဝင်ရောက်ရယူနိုင်ပါသည်။\n"
            "👑 VIP Member ဝင်ရောက်ပါက VIP ဇာတ်ကားပေါင်းများစွာကို ကြော်ငြာမပါဘဲ စိတ်တိုင်းကျ ကြည့်ရှုနိုင်ပါပြီ။\n\n"
            f"📢 <b>Public Channel:</b> <a href='{PUBLIC_CHANNEL_LINK}'>ဒီမှာနှိပ်၍ ဝင်ပါ</a>\n"
            f"💬 <b>VIP Member ဝင်ရန်:</b> <a href='{VIP_ADMIN_LINK}'>@Lynn_subflix528 သို့ ဆက်သွယ်ပါ</a>"
        )
        bot.send_message(chat_id, welcome_text, parse_mode="HTML", disable_web_page_preview=True)
        
    else:
        if not is_vip_member(user_id):
            not_vip_text = (
                "❌ <b>လူကြီးမင်းသည် VIP Member မဟုတ်သေးပါရှင့်။</b>\n\n"
                "ဤဇာတ်ကားကို ရယူနိုင်ရန်အတွက် VIP Member ဝင်ရောက်ပေးပါရန် လိုအပ်ပါသည်။\n"
                f"VIP Member ဝင်ရောက်လိုပါက <a href='{VIP_ADMIN_LINK}'>Admin (@Lynn_subflix528) ထံ ဆက်သွယ်ပေးပါရှင့်</a>။"
            )
            bot.send_message(chat_id, not_vip_text, parse_mode="HTML", disable_web_page_preview=True)
            return

        try:
            movie_message_id = int(command_args[1])
            
            welcome_msg = bot.send_message(
                chat_id, 
                "<b>VIP MM SubFlix မှ ကြိုဆိုပါတယ်ရှင့်။ အလိုရှိသော ဇာတ်ကားကို ပို့ပေးနေပါပြီ... ⏳</b>", 
                parse_mode="HTML"
            )
            
            time.sleep(1)
            
            sent_movie = bot.forward_message(
                chat_id, 
                from_chat_id=STORAGE_CHANNEL_ID, 
                message_id=movie_message_id
            )
            
            warning_text = (
                "⚠️ <b>မူပိုင်ခွင့်ဥပဒေကြောင့် ဤဇာတ်ကားဖိုင်သည် (၂) မိနစ်အတွင်း အလိုအလျောက် ပျက်ပါမည်။ "
                "မိမိ၏ Saved Messages ထဲသို့ ကြိုတင် Save ထားပေးပါရှင့်။</b>\n\n"
                "🌸 <i>သာယာသောနေ့လေးဖြစ်ပါစေကြောင်း VIP MM SubFlix မှ ဆုမွန်ကောင်းတောင်းပေးလိုက်ပါတယ်ရှင့်။</i>"
            )
            warning_msg = bot.send_message(chat_id, warning_text, parse_mode="HTML")
            
            threading.Thread(target=auto_delete_message, args=(chat_id, welcome_msg.message_id)).start()
            threading.Thread(target=auto_delete_message, args=(chat_id, sent_movie.message_id)).start()
            threading.Thread(target=auto_delete_message, args=(chat_id, warning_msg.message_id)).start()
            
        except Exception as e:
            bot.send_message(chat_id, "❌ ဇာတ်ကားဖိုင် ရှာမတွေ့ပါ သို့မဟုတ် ဖိုင်ပျက်နေပါသည်ရှင့်။")
            print(f"Error forwarding movie: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    reply_text = (
        "<b>VIP MM SubFlix</b>\n\n"
        f"📢 Public Channel မှတစ်ဆင့် ဇာတ်ကားများကို ရယူနိုင်ပါသည်:\n{PUBLIC_CHANNEL_LINK}\n\n"
        f"💬 VIP Member ဝင်ရောက်ရန်: <a href='{VIP_ADMIN_LINK}'>@Lynn_subflix528</a>"
    )
    bot.reply_to(message, reply_text, parse_mode="HTML", disable_web_page_preview=True)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return '', 403

@app.route('/')
def index():
    bot.remove_webhook()
    time.sleep(1)
    app_url = os.environ.get("RENDER_EXTERNAL_URL", "https://vip-mm-subflix-bot-1.onrender.com")
    bot.set_webhook(url=f"{app_url}/{BOT_TOKEN}")
    return "VIP MM SubFlix Bot is Running Smoothly!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
