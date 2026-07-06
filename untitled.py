# ============================================================
#  HOLWIN REFERRAL BOT – WITH LOCAL TRACKING & FORCED INVITE
#  Flow: Mobile → Invite Code (required) → OTP → Password → Register
# ============================================================

import re
import logging
import aiohttp
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# ---------- CONFIG ----------
BOT_TOKEN = "8576883242:AAE2xf_iGoWZksEpJBHKxRzW3yp17HoaKy0"          # Replace
INVITE_CODE = "WLRPSY"                # <-- PUT YOUR VALID HOLWIN INVITE CODE HERE

# Holwin API
BASE_URL = "https://www.holwin123.top"
DI_TOKEN = "88dd52c70e7b377527be01c39f5a0a4f"
VTOKEN = "18667bd921478af5fe5f6506865e4f8a"

DATABASE_URL = "sqlite:///registrations.db"

# ---------- LOGGING ----------
logging.basicConfig(format="[%(asctime)s] %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- DATABASE ----------
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True)
    mobile = Column(String(20), nullable=False)
    invite_used = Column(String(20), nullable=False)
    telegram_id = Column(Integer, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# ---------- HOLWIN API ----------
class HolwinClient:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "di": DI_TOKEN,
            "vtoken": VTOKEN,
        }
        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def post(self, path, json):
        url = f"{BASE_URL}{path}"
        async with self.session.post(url, json=json) as resp:
            return await resp.json()

# ---------- CONVERSATION STATES ----------
MOBILE, INVITE, OTP, PASSWORD, CONFIRM = range(5)

# ---------- BOT ----------
app = Application.builder().token(BOT_TOKEN).build()

# Temporary storage
user_data = {}

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📱 Register Now", callback_data="register")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 *Holwin Referral Bot*\n\n"
        f"Your default invite code: `{INVITE_CODE}`\n"
        "Click the button below to start registration.\n"
        "Use /stats to see total registrations.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ---------- STATS ----------
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    total = db.query(Registration).count()
    recent = db.query(Registration).order_by(Registration.registered_at.desc()).limit(10).all()
    db.close()

    msg = f"📊 *Total Registrations:* {total}\n\n"
    if recent:
        msg += "🕒 *Last 10 Registrations:*\n"
        for r in recent:
            msg += f"• {r.mobile} – used `{r.invite_used}` at {r.registered_at.strftime('%Y-%m-%d %H:%M')}\n"
    else:
        msg += "No registrations yet."
    await update.message.reply_text(msg, parse_mode="Markdown")

# ---------- REGISTER BUTTON ----------
async def register_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📱 Please enter your mobile number (10-15 digits):")
    return MOBILE

# ---------- MOBILE ----------
async def mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mobile = update.message.text.strip()
    if not re.match(r"^\d{10,15}$", mobile):
        await update.message.reply_text("❌ Invalid. Enter 10-15 digits:")
        return MOBILE
    user_data[update.effective_user.id] = {"mobile": mobile}
    await update.message.reply_text(
        f"🎫 Enter the invite code (default is `{INVITE_CODE}`, type it or press any text):"
    )
    return INVITE

# ---------- INVITE (REQUIRED) ----------
async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    invite = update.message.text.strip()
    if not invite:
        invite = INVITE_CODE  # fallback
    # You can optionally validate the code with Holwin API? Not needed.
    user_data[update.effective_user.id]["invite"] = invite

    mobile = user_data[update.effective_user.id]["mobile"]
    await update.message.reply_text(f"📲 Sending OTP to {mobile}...")
    async with HolwinClient() as client:
        resp = await client.post("/api/system/sms/send", {"mobile": mobile, "type": "reg_code"})
    if resp.get("code") != 0:
        await update.message.reply_text(f"❌ OTP request failed: {resp.get('msg', 'Unknown')}")
        return ConversationHandler.END
    await update.message.reply_text("✅ OTP sent! Please enter the OTP you received:")
    return OTP

# ---------- OTP ----------
async def otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp_code = update.message.text.strip()
    if not otp_code.isdigit():
        await update.message.reply_text("❌ OTP must be numeric. Try again:")
        return OTP
    user_data[update.effective_user.id]["otp"] = otp_code
    await update.message.reply_text("🔑 Set a password (min 6 characters):")
    return PASSWORD

# ---------- PASSWORD ----------
async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pwd = update.message.text.strip()
    if len(pwd) < 6:
        await update.message.reply_text("❌ Min 6 characters. Try again:")
        return PASSWORD
    user_data[update.effective_user.id]["password"] = pwd
    data = user_data[update.effective_user.id]
    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data="confirm")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")],
    ]
    await update.message.reply_text(
        f"📋 *Registration Summary*\n"
        f"📱 Mobile: `{data['mobile']}`\n"
        f"🎫 Invite: `{data['invite']}`\n"
        f"🔑 Password: `{'*'*len(pwd)}`\n\n"
        f"Confirm?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return CONFIRM

# ---------- CONFIRM ----------
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "cancel":
        await query.edit_message_text("❌ Registration cancelled.")
        user_data.pop(update.effective_user.id, None)
        return ConversationHandler.END

    data = user_data[update.effective_user.id]
    mobile = data["mobile"]
    otp_code = data["otp"]
    pwd = data["password"]
    invite = data["invite"]

    async with HolwinClient() as client:
        payload = {
            "mobile": mobile,
            "authCode": otp_code,
            "password": pwd,
            "inviteCode": invite,
            "sourceAppType": "lobby",
            "registerHost": "www.holwin123.top",
            "sourceUrl": "https://www.hlowin.link/",
        }
        resp = await client.post("/api/user/register", payload)

    if resp.get("code") == 0:
        # Save registration locally
        db = SessionLocal()
        reg = Registration(
            mobile=mobile,
            invite_used=invite,
            telegram_id=update.effective_user.id
        )
        db.add(reg)
        db.commit()
        db.close()

        await query.edit_message_text(
            f"✅ *Registration successful!*\n\n"
            f"Mobile: {mobile}\n"
            f"Invite code used: {invite}\n\n"
            f"Your referral count on Holwin should increase now! 🚀",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text(f"❌ Registration failed: {resp.get('msg', 'Unknown')}")

    user_data.pop(update.effective_user.id, None)
    return ConversationHandler.END

# ---------- CANCEL ----------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data.pop(update.effective_user.id, None)
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

# ---------- SETUP ----------
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(register_button, pattern="^register$")],
    states={
        MOBILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, mobile)],
        INVITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, invite)],
        OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, otp)],
        PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password)],
        CONFIRM: [CallbackQueryHandler(confirm, pattern="^(confirm|cancel)$")],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(conv_handler)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run_polling()