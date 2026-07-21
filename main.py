import os
import time
import threading
import telebot
from flask import Flask, request

# Telegram Bot Token
BOT_TOKEN = "8744124078:AAF_ZzrHZnRnf-zKVWYNO_rgIZINOByXSyE"

# VIP MM SubFlix Private Channel ID (အတိုအကျ အမှန်ထည့်ပေးထားသည်)
STORAGE_CHANNEL_ID = -1004401727688  

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# မက်ဆေ့ခ်ျကို ၂ မိနစ် (စက္ကန့် ၁၂၀) ပြည့်ရင် Auto ဖျက်မည့် Function
def auto_delete_message(chat_id, message_id):
    time.sleep(120)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

# Start Command (/start) စနစ်
@bot.message_handler(commands=['start'])
def send_vip_movie(message):
    chat_id = message.chat.id
    command_args = message.text.split()
    
    # အခြေအနေ ၁ - ဒီအတိုင်း /start နှိပ်ပြီး ဝင်လာသူ
    if len(command_args) == 1:
        welcome_text = (
            "<b>VIP MM SubFlix မှကြိုဆိုပါတယ် လူကြီးမင်း။</b>\n\n"
            "Public Channel မူဗီလင့်ခ်များမှတစ်ဆင့် ဇာတ်ကားများကို ဝင်ရောက်ရယူနိုင်ပါတယ်ရှင့်။"
        )
        bot.send_message(chat_id, welcome_text, parse_mode="HTML")
        
    # အခြေအနေ ၂ - VIP Movie Link (https://t.me/BotName?start=123) နှိပ်ပြီး ရောက်လာသူ
    else:
        try:
            movie_message_id = int(command_args[1]) # လင့်ခ်ထဲက 123 ဆိုတဲ့ Message ID
            
            # ၁။ ကြိုဆိုသည့် စာသား ပို့ခြင်း
            welcome_msg = bot.send_message(
                chat_id, 
                "<b>VIP MM SubFlix မှကြိုဆိုပါတယ် လူကြီးမင်း။ အလိုရှိသော ဇာတ်ကားကို ပို့ပေးနေပါပြီရှင့်။</b>", 
                parse_mode="HTML"
            )
            
            time.sleep(1)
            
            # ၂။ Private Channel ထဲက ဇာတ်ကားဖိုင်ကို Forward ယူပြီး ပို့ပေးခြင်း
            sent_movie = bot.forward_message(
                chat_id, 
                from_chat_id=STORAGE_CHANNEL_ID, 
                message_id=movie_message_id
            )
            
            # ၃။ မူပိုင်ခွင့် သတိပေးချက်နှင့် ဆုမွန်ကောင်းတောင်းသည့် စာသား
            warning_text = (
                "⚠️ <b>မူပိုင်ခွင့်ဥပဒေကြောင့် ဤဇာတ်ကားဖိုင်သည် (၂) မိနစ်အတွင်း အလိုအလျောက် ပျက်ပါမည်။ "
                "မိမိ၏ Saved Messages ထဲသို့ ကြိုတင် Save ထားပေးပါရှင့်။</b>\n\n"
                "🌸 <i>သာယာတဲ့နေ့လေးတစ်နေ့ဖြစ်ပါစေလို့ ဆုမွန်ကောင်းတောင်းပေးလိုက်ပါတယ်ရှင့်။</i>"
            )
            warning_msg = bot.send_message(chat_id, warning_text, parse_mode="HTML")
            
            # ၄။ ၂ မိနစ်ပြည့်ရင် စာများရော ဇာတ်ကားဖိုင်ပါ Auto-Delete ဖျက်ပေးခြင်း
            threading.Thread(target=auto_delete_message, args=(chat_id, welcome_msg.message_id)).start()
            threading.Thread(target=auto_delete_message, args=(chat_id, sent_movie.message_id)).start()
            threading.Thread(target=auto_delete_message, args=(chat_id, warning_msg.message_id)).start()
            
        except Exception as e:
            bot.send_message(chat_id, "❌ ဇာတ်ကားဖိုင် ရှာမတွေ့ပါ သို့မဟုတ် ဖိုင်ပျက်နေပါသည်ရှင့်။")
            print(f"Error forwarding movie: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "<b>VIP MM SubFlix</b>\n\nဇာတ်ကားများကို Public Channel ထဲရှိ လင့်ခ်များမှတစ်ဆင့် ရယူနိုင်ပါတယ်ရှင့်။", parse_mode="HTML")

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    app_url = os.environ.get("RENDER_EXTERNAL_URL", "https://vip-mm-subflix-bot.onrender.com")
    bot.set_webhook(url=f"{app_url}/{BOT_TOKEN}")
    return "VIP MM SubFlix Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
