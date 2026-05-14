from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler
)

BOT_TOKEN = "8977764016:AAEf9lhXD4qDFzguoHvxCS7gPu57WiH1dtY"

ADMIN_ID = 7693040685

REGISTER_LINK = "https://13lgame14.com/register?inviteCode=HVS2YBN&from=web"

CHANNEL_LINK = "https://t.me/+Rze4ddKfR944OWZl"

UID_RULE = "6"

UID, DEPOSIT_SS, ORDER_ID, UTR, WITHDRAW_SS = range(5)

verified_users = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🆔 Verify UID",
                callback_data="verify_uid"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🎧 Welcome To 13L Customer Service\n\n"
        "Please Verify Your UID First"
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "verify_uid":

        await query.message.reply_text(
            "📥 Send Your UID"
        )

        return UID

    elif query.data == "deposit_problem":

        if user_id not in verified_users:
            return

        await query.message.reply_text(
            "📸 Send Deposit Screenshot"
        )

        return DEPOSIT_SS

    elif query.data == "withdraw_problem":

        if user_id not in verified_users:
            return

        await query.message.reply_text(
            "📸 Send Withdraw Screenshot"
        )

        return WITHDRAW_SS

    elif query.data == "prediction_channel":

        keyboard = [
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url=CHANNEL_LINK
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "✅ Join Official Prediction Channel",
            reply_markup=reply_markup
        )


async def check_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.message.text

    if not uid.startswith(UID_RULE):

        keyboard = [
            [
                InlineKeyboardButton(
                    "📝 Register Now",
                    url=REGISTER_LINK
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "❌ Invalid UID\n\nRegister First",
            reply_markup=reply_markup
        )

        return ConversationHandler.END

    verified_users.add(update.effective_user.id)

    keyboard = [
        [
            InlineKeyboardButton(
                "🏦 Deposit Problem",
                callback_data="deposit_problem"
            )
        ],
        [
            InlineKeyboardButton(
                "💸 Withdraw Problem",
                callback_data="withdraw_problem"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Official Prediction Channel",
                callback_data="prediction_channel"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "✅ UID Verified\n\nSelect Your Problem",
        reply_markup=reply_markup
    )

    return ConversationHandler.END


async def deposit_ss(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["deposit_ss"] = update.message.photo[-1].file_id

    await update.message.reply_text(
        "📦 Send Deposit Order Number"
    )

    return ORDER_ID


async def order_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["order_id"] = update.message.text

    await update.message.reply_text(
        "💳 Send UTR Number"
    )

    return UTR


async def utr(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["utr"] = update.message.text

    user = update.effective_user

    caption = (
        f"🏦 Deposit Complaint\n\n"
        f"👤 User: @{user.username}\n"
        f"🆔 Telegram ID: {user.id}\n"
        f"📦 Order ID: {context.user_data['order_id']}\n"
        f"💳 UTR: {context.user_data['utr']}"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=context.user_data["deposit_ss"],
        caption=caption
    )

    await update.message.reply_text(
        "✅ Deposit Complaint Submitted Successfully"
    )

    return ConversationHandler.END


async def withdraw_ss(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo = update.message.photo[-1].file_id

    user = update.effective_user

    caption = (
        f"💸 Withdraw Complaint\n\n"
        f"👤 User: @{user.username}\n"
        f"🆔 Telegram ID: {user.id}"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption
    )

    await update.message.reply_text(
        "✅ Withdraw Complaint Submitted Successfully"
    )

    return ConversationHandler.END


app = ApplicationBuilder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            button_click
        )
    ],

    states={

        UID: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                check_uid
            )
        ],

        DEPOSIT_SS: [
            MessageHandler(
                filters.PHOTO,
                deposit_ss
            )
        ],

        ORDER_ID: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                order_id
            )
        ],

        UTR: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                utr
            )
        ],

        WITHDRAW_SS: [
            MessageHandler(
                filters.PHOTO,
                withdraw_ss
            )
        ]
    },

    fallbacks=[]
)

app.add_handler(CommandHandler("start", start))

app.add_handler(conv_handler)

app.run_polling()
