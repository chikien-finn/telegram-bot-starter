from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8380482564:AAGh0btVTdONkjtn3ozw8dgKWDYOS4mKMpY"  # ← THAY TOKEN THẬT CỦA @prank_bot VÀO ĐÂY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Prank bot đã online 100% 🔥\nGửi gì t rep lại hết!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("Bot đang chạy ngon lành...")
app.run_polling()
