from telegram.ext import (ApplicationBuilder, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from src.config import TELEGRAM_TOKEN
from src.handlers import (ENTER_INGREDIENTS, SELECT_MODEL, handle_ingredients,
                          select_model, start)


def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_MODEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_model)
            ],
            ENTER_INGREDIENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ingredients)
            ],
        },
        allow_reentry=True,
        fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ingredients)],
    )

    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
