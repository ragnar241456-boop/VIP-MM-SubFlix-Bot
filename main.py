import os
import asyncio
from pyrogram import Client, filters

# Environment Variables မှ ယူမည်
API_ID = int(os.environ.get("API_ID", "2040"))
API_HASH = os.environ.get("API_HASH", "b18441a1ed607e10e46b64752f7a284d")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8744124078:AAF_ZzrHZnRnf-zKVWYNO_rgIZINOByXSyE")
STORAGE_CHANNEL = int(os.environ.get("STORAGE_CHANNEL", "0"))

app = Client("vip_subflix_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    if len(message.command) > 1:
        msg_id = int(message.command[1])
        try:
            # ၁။ ပထမဆုံး ကြိုဆိုသည့် စာသားကို ပို့ပေးခြင်း
            welcome_msg = await message.reply_text(
                "<b>VIP MM SubFlix မှကြိုဆိုပါတယ် လူကြီးမင်း။ အလိုရှိသော ဇာတ်ကားကို ပို့ပေးနေပါပြီရှင့်။</b>",
                parse_mode="html"
            )
            
            # စာပို့သည့် အရှိန်သဘာဝကျစေရန် ၁ စက္ကန့် စောင့်ခြင်း
            await asyncio.sleep(1)

            # ၂။ Storage Channel ထံမှ ဇာတ်ကားဖိုင်ကို ပို့ပေးခြင်း
            sent_video = await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=STORAGE_CHANNEL,
                message_id=msg_id,
                caption="🎬 <b>VIP MM SubFlix Movie</b>",
                parse_mode="html"
            )

            # ၃။ မူပိုင်ခွင့် သတိပေးချက်နှင့် ဆုမွန်ကောင်းတောင်းသည့် စာသား ပို့ပေးခြင်း
            warning_msg = await message.reply_text(
                "⚠️ <b>မူပိုင်ခွင့်ဥပဒေကြောင့် ဤဇာတ်ကားဖိုင်သည် (၂) မိနစ်အတွင်း အလိုအလျောက် ပျက်ပါမည်။ မိမိ၏ Saved Messages ထဲသို့ ကြိုတင် Save ထားပေးပါရှင့်။</b>\n\n"
                "🌸 <i>သာယာတဲ့နေ့လေးတစ်နေ့ဖြစ်ပါစေလို့ ဆုမွန်ကောင်းတောင်းပေးလိုက်ပါတယ်ရှင့်။</i>",
                parse_mode="html"
            )

            # စက္ကန့် ၁၂၀ (၂ မိနစ်) စောင့်ခြင်း
            await asyncio.sleep(120)

            # ၄။ စက္ကန့် ၁၂၀ ပြည့်ပါက ဇာတ်ကားဖိုင်နှင့် စာသားများကို Auto-Delete ဖျက်ခြင်း
            await sent_video.delete()
            await warning_msg.delete()
            await welcome_msg.delete()

        except Exception as e:
            await message.reply_text("❌ ဇာတ်ကားဖိုင် ရှာမတွေ့ပါ သို့မဟုတ် ဖိုင်ပျက်နေပါသည်ရှင့်။")
    else:
        # ရိုးရိုး /start နှိပ်ပါက ပြသမည့် စာသား
        await message.reply_text(
            "<b>VIP MM SubFlix မှကြိုဆိုပါတယ် လူကြီးမင်း။</b>\n\nPublic Channel မူဗီလင့်ခ်များမှတစ်ဆင့် ဇာတ်ကားများကို ဝင်ရောက်ရယူနိုင်ပါတယ်ရှင့်။",
            parse_mode="html"
        )

print("VIP MM SubFlix Bot is active...")
app.run()
