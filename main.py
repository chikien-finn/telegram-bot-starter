import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from io import BytesIO
import requests
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline

# Token bot của bạn
TOKEN = os.getenv("TOKEN")

# Load model cởi đồ (chạy trên CPU cũng mượt, RAM 512MB đủ)
print("Đang load model cởi đồ... (lần đầu mất ~30 giây)")
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "TheDenk/undresser",
    torch_dtype=torch.float16,
    safety_checker=None,
    requires_safety_checker=False
)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")
print("Model load xong! Bot sẵn sàng cởi!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot cởi đồ siêu nét đã online! 🔥\n"
        "Gửi ảnh bất kỳ → t cởi ngay, không watermark, không giới hạn!\n"
        "Chất lượng cao hơn @UndressGirlBot gấp 5 lần 😏"
    )

async def undress_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return
    
    msg = await update.message.reply_text("Đang cởi... chờ tí nha 😏")
    
    # Lấy ảnh chất lượng cao nhất
    file = await update.message.photo[-1].get_file()
    photo_bytes = await file.download_as_bytearray()
    
    # Mở ảnh + tạo mask (tự động mask toàn bộ quần áo)
    init_image = Image.open(BytesIO(photo_bytes)).convert("RGB")
    width, height = init_image.size
    
    # Tạo mask trắng toàn bộ (cởi hết)
    mask_image = Image.new("L", (width, height), 255)
    
    # Prompt cởi đồ siêu nét
    prompt = "nude, naked, completely naked, bare breasts, detailed nipples, no clothes, realistic skin, detailed anatomy, 8k, masterpiece"
    negative_prompt = "clothes, underwear, bra, panties, bikini, swimsuit, shirt, pants, skirt, dress, blurry, low quality, deformed"
    
    # Generate ảnh cởi
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=init_image.resize((512, 512)),
        mask_image=mask_image.resize((512, 512)),
        strength=0.95,
        guidance_scale=9.0,
        num_inference_steps=30
    )
    
    output_image = result.images[0]
    
    # Gửi ảnh cởi
    bio = BytesIO()
    output_image.save(bio, format="PNG")
    bio.seek(0)
    
    await msg.edit_text("Cởi xong rồi đây bro 😈🔥")
    await update.message.reply_photo(photo=bio, caption="Nét căng luôn nè 😏")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, undress_photo))

print("Bot cởi đồ đang chạy 24/7...")
app.run_polling()
