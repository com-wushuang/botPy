import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# reade admin_list file and store it to a variable admin_list
admin_list = []
with open('admin_list', 'r', encoding='utf-8') as f:
    admin_str = f.read()
    admin_list = admin_str.split("\n")

# Stages
FIRST, SECOND = range(2)

# Callback data
LIST_ALL, ADD, MODIFY, DELETE, DONE = range(5)


def start(update: Update, context: CallbackContext):
    # init advertisement list
    if not context.bot_data.get("advertisement_list", []):
        context.bot_data["advertisement_list"] = []
    # add admin config
    if not context.bot_data.get("admin_list", []):
        context.bot_data["admin_list"] = admin_list

    keyboard = [
        [
            InlineKeyboardButton("广告列表", callback_data=(LIST_ALL)),
            InlineKeyboardButton("新增广告", callback_data=(ADD)),
        ],
        [
            InlineKeyboardButton("修改广告", callback_data=(MODIFY)),
            InlineKeyboardButton("删除广告", callback_data=(DELETE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "管理界面!",
        reply_markup=reply_markup,
    )

    return FIRST


def list_all(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    # get advertisement_list
    advertisement_list = context.bot_data["advertisement_list"]
    if not advertisement_list:
        keyboard = [
            [
                InlineKeyboardButton("新增广告", callback_data=(ADD)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            '还没有广告，请添加！',
            reply_markup=reply_markup,
        )
        return FIRST
    else:
        # return advertisement_list
        keyboard = [
            [
                InlineKeyboardButton("广告列表", callback_data=(LIST)),
                InlineKeyboardButton("新增广告", callback_data=(ADD)),
            ],
            [
                InlineKeyboardButton("修改广告", callback_data=(MODIFY)),
                InlineKeyboardButton("删除广告", callback_data=(DELETE)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            '这是广告列表',
            reply_markup=reply_markup,
        )
        return FIRST


def add(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Alright, please send me the category first, ' 'for example "Most impressive skill"'
    )

    return FIRST


def received_information(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)} You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return FIRST


def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)} Until next time!"
    )

    user_data.clear()
    return ConversationHandler.END


# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST: [
            CallbackQueryHandler(list_all, pattern='^' + str(LIST_ALL) + '$'),
            CallbackQueryHandler(two, pattern='^' + str(ADD) + '$'),
            # CallbackQueryHandler(three, pattern='^' + str(UPDATE) + '$'),
            # CallbackQueryHandler(four, pattern='^' + str(DELETE) + '$'),
        ],
        # LIST_ALL: [
        #     MessageHandler(
        #         Filters.text & ~(Filters.command | Filters.regex(
        #             '^Done$')), regular_choice
        #     )
        # ],
        # UPDATE: [
        #     MessageHandler(
        #         Filters.text & ~(Filters.command | Filters.regex('^Done$')),
        #         received_information,
        #     )
        # ],
        # DELETE: [
        #     MessageHandler(
        #         Filters.text & ~(Filters.command | Filters.regex('^Done$')),
        #         received_information,
        #     )
        # ],
        # DONE: [
        #     MessageHandler(
        #         Filters.text & ~(Filters.command | Filters.regex('^Done$')),
        #         received_information,
        #     )
        # ],
    },
    fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
)
