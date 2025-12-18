import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from io import BytesIO
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline

TOKEN = os.getenv("TOKEN")

print("Đang load model cởi đồ nhẹ (CPU)...")
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "TheDenk/undresser",
    torch_dtype=torch.float32,
    safety_checker=None,
)
pipe.to("cpu")
pipe.enable_attention_slicing()  # Tiết kiệm RAM
print("Model load xong! Bot sẵn sàng cởi!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot cởi đồ siêu nhẹ đã online! Gửi ảnh là cởi ngay 🔥")

async def undress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return
    msg = await update.message.reply_text("Đang cởi... chờ 20-40s nha 😏")
    file = await update.message.photo[-1].get_file()
    photo_bytes = await file.download_as_bytearray()
    image = Image.open(BytesIO(photo_bytes)).convert("RGB")
    mask = Image.new("L", image.size, 255)

    result = pipe(
        prompt="nude, naked, realistic skin, detailed",
        negative_prompt="clothes, bad quality",
        image=image.resize((512, 512)),
        mask_image=mask.resize((512, 512)),
        strength=0.99,
        num_inference_steps=20
    ).images[0]

    bio = BytesIO()
    result.save(bio, "PNG")
    bio.seek(0)
    await msg.delete()
    await update.message.reply_photo(bio, caption="Cởi xong rồi đây bro 😈🔥")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, undress))

print("Bot cởi đồ nhẹ đang chạy...")
app.run_polling()
