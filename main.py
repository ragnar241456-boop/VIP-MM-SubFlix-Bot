import os
import asyncio
from pyrogram import Client, filters
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Web Service မသေစေရန် Keep-Alive Server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"VIP MM SubFlix Bot is Online!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# Environment Variables မှ ယူမည်
API_ID = int(os.environ.get("API_ID", "6113807"))
API_HASH = os.environ.get("API_HASH", "2918231982fb7fb5e3158b681938063d")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8744124078:AAF_ZzrHZnRnf-zKVWYNO_rgIZINOByXSyE")
STORAGE_CHANNEL = os.environ.get("STORAGE_CHANNEL", "0")

try:
    STORAGE_CHANNEL = int(STORAGE_CHANNEL)
except ValueError:
    STORAGE_CHANNEL = 0

app = Client("vip_subflix_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    if len(message.command) > 1:
        try:
            msg_id = int(message.command[1])
            welcome_msg = await message.reply_text(
                "<b>VIP MM SubFlix မှကြိုဆိုပါတယ် လူကြီးမင်း။ အလိုရှိသော ဇာတ်ကားကို ပို့ပေးနေပါပြီရှင့်။</b>",
                parse_mode="html"
            )
            await asyncio.sleep(1)

            sent_video = await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=STORAGE_CHANNEL,
                message_id=msg_id,
                caption="🎬 <b>VIP MM SubFlix Movie</b>",
                parse_mode="html"
            )

            warning_msg = await message.reply_text(
                "⚠️ <b>မူပိုင်ခွင့်ဥပဒေကြောင့် ဤဇာတ်ကားဖိုင်သည် (၂) မိနစ်အတွင်း အလိုအလျောက် ပျက်ပါမည်။ မိမိ၏ Saved Messages ထဲသို့ ကြိုတင် Save ထားပေးပါရှင့်။</b>\n\n"
                "🌸 <i>သာယာတဲ့နေ့လေးတစ်နေ့ဖြစ်ပါစေလို့ ဆုမွန်ကောင်းတောင်းပေးလိုက်ပါတယ်ရှင့်။</i>",
                parse_mode="html"
            )

            await asyncio.sleep(120)

            await sent_video.delete()
            await warning_msg.delete()
            await welcome_msg.delete()

        except Exception as e:
            await message.reply_text("❌ ဇာတ်ကားဖိုင် ရှာမတွေ့ပါ သို့မဟုတ် ဖိုင်ပျက်နေပါသည်ရှင့်။")
    else:
        await message.reply_text(
            "<b>VIP MM SubFlix မှကြိုဆိုပါတယ် လူကြီးမင်း။</b>\n\nPublic Channel မူဗီလင့်ခ်များမှတစ်ဆင့် ဇာတ်ကားများကို ဝင်ရောက်ရယူနိုင်ပါတယ်ရှင့်။",
            parse_mode="html"
        )

print("VIP MM SubFlix Bot is active...")
app.run()
