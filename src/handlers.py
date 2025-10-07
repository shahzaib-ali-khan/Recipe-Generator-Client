import structlog
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from src.services.available_llm_service import get_available_llms
from src.services.recipe_service import get_recipe_response

logger = structlog.get_logger(__name__)

# Define conversation states
SELECT_MODEL, ENTER_INGREDIENTS = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    models = get_available_llms()
    if not models:
        logger.error("⚠️ Failed to fetch available models. Using default models.")
        models = ["ChatGPT", "Gemini"]

    context.user_data["models"] = models

    # Create a ReplyKeyboardMarkup
    keyboard = [[model] for model in models]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text(
        "👋 Welcome! I'm your Recipe Bot.\nPlease select a model to generate recipes:",
        reply_markup=reply_markup,
    )
    return SELECT_MODEL


async def select_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    models = context.user_data.get("models", [])
    selected_model = update.message.text

    if selected_model not in models:
        logger.warning(
            "Invalid model selected by %s: %s", user.username, selected_model
        )
        await update.message.reply_text(
            "⚠️ Please select a valid model from the options."
        )
        return SELECT_MODEL

    context.user_data["selected_model"] = selected_model
    logger.info("Model selected by %s: %s", user.username, selected_model)
    await update.message.reply_text(
        f"You selected {selected_model}. Please enter the ingredients (e.g., 'flour, sugar, eggs'):",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ENTER_INGREDIENTS


async def handle_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ingredients = update.message.text
    selected_model = context.user_data.get("selected_model")
    user = update.message.from_user

    if not selected_model:
        logger.error("No model selected for %s", user.username)
        await update.message.reply_text(
            "⚠️ No model selected. Please start again with /start."
        )
        return ConversationHandler.END

    logger.info(
        "Processing recipe request for %s with model %s and ingredients %s",
        user.username,
        selected_model,
        ingredients,
    )
    response = get_recipe_response(selected_model, ingredients)

    await update.message.reply_text(response or "No recipe generated.")

    context.user_data.clear()
    return ConversationHandler.END
