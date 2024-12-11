from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import json

# Load tools from JSON
def load_tools():
    with open("tools.json", "r") as file:
        return json.load(file)

TOOLS = load_tools()

# /start Command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to MyToolSellerBot! Use /catalog to view available tools."
    )

# /catalog Command
def catalog(update: Update, context: CallbackContext):
    keyboard = []
    for tool in TOOLS:
        keyboard.append([InlineKeyboardButton(tool["name"], callback_data=tool["id"])])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Here are our tools:", reply_markup=reply_markup)

# Handle Tool Selection
def handle_tool_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    tool_id = query.data
    tool = next((t for t in TOOLS if t["id"] == tool_id), None)

    if tool:
        query.edit_message_text(
            text=f"**{tool['name']}**\n\n{tool['description']}\nPrice: {tool['price']} USD\n\nClick /buy_{tool['id']} to purchase.",
            parse_mode="Markdown"
        )

# Main Function
def main():
    # Replace 'YOUR_BOT_TOKEN' with your Bot Token from BotFather
    updater = Updater("7384832877:AAGBU1nqwCNGAJ-8x6cA04kfLIYGaAS-QVY")

    # Handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("catalog", catalog))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_tool_selection))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
