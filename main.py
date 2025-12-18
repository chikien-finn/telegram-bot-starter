import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from io import BytesIO
from PIL import Image
import torch
from diffusers import AutoPipelineForInpainting

TOKEN = os.getenv("TOKEN")

print("Đang load model cởi đồ nhẹ nhất...")
pipe = AutoPipelineForInpainting.from_pretrained(
    "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
    torch_dtype=torch.float32,
    variant="fp16",
    safety_checker=None
)
pipe.to("cpu")
pipe.enable_attention_slicing()
print("Model load xong – Bot cởi đồ miễn phí sẵn sàng!")

async def undress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return
    msg = await update.message.reply_text("Đang cởi đồ... chờ 20-40s nha 😈")
    
    file = await update.message.photo[-1].get_file()
    img_bytes = await file.download_as_bytearray()
    image = Image.open(BytesIO(img_bytes)).convert("RGB")
    
    # Tạo mask trắng = cởi hết
    mask = Image.new("L", image.size, 255)
    
    result = pipe(
        prompt="nude, naked, beautiful realistic skin, detailed body, 8k, masterpiece",
        negative_prompt="clothes, underwear, bra, panties, shirt, pants, blurry, deformed",
        image=image.resize((1024, 1024)),
        mask_image=mask.resize((1024, 1024)),
        strength=1.0,
        num_inference_steps=28,
        guidance_scale=9.0
    ).images[0]

    bio = BytesIO()
    result.save(bio, "PNG")
    bio.seek(0)
    await msg.delete()
    await update.message.reply_photo(bio, caption="Cởi xong rồi đây bro – nét căng luôn 😏🔥")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, undress))
print("Bot cởi đồ miễn phí đang chạy 24/7...")
app.run_polling()
