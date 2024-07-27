import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import timedelta

# Token của bạn từ BotFather
TOKEN = '6349202722:AAGfvut3DDLnPNKleejCutPUWYe-QSMf-ZY'
CHANNEL_ID = '@iOSFreeHackVN'  # Thay đổi bằng ID hoặc username của kênh

# Cấu hình logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Hàm start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Xin chào! Tôi là bot gửi tin nhắn hẹn giờ. Gõ /schedule <thời gian tính bằng phút> <nội dung> để đặt lịch gửi tin nhắn.')

# Hàm để gửi tin nhắn sau một khoảng thời gian nhất định
async def send_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(job.data['chat_id'], text=job.data['text'])

# Hàm đặt lịch gửi tin nhắn
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = context.args
        delay = int(args[0])
        text = ' '.join(args[1:])
        
        due = timedelta(minutes=delay)

        context.job_queue.run_once(send_message, due, data={'chat_id': CHANNEL_ID, 'text': text})

        await update.message.reply_text(f'Tin nhắn của bạn sẽ được gửi vào kênh sau {delay} phút.')
    except (IndexError, ValueError):
        await update.message.reply_text('Cú pháp không hợp lệ. Vui lòng sử dụng: /schedule <thời gian tính bằng phút> <nội dung>')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", schedule))

    application.run_polling()

if __name__ == '__main__':
    main()
