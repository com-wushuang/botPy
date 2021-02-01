from typing import Dict
import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)

# Stages
FIRST, SECOND = range(2)
# Callback data
LIST, ADD, MODIFY, DELETE, DONE = range(5)

keyboard = [
    [
        InlineKeyboardButton("广告列表", callback_data=(LIST)),
        InlineKeyboardButton("新增广告", callback_data=(ADD)),
    ],
    [
        InlineKeyboardButton("修改广告", callback_data=(MODIFY)),
        InlineKeyboardButton("删除广告", callback_data=(DELETE)),
    ],
    [InlineKeyboardButton("完成", callback_data=(DONE))],
]

reply_markup = InlineKeyboardMarkup(keyboard)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "你好，管理员！请选择菜单:", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def all(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = []
    advertisements = db.list_all()
    for ad in advertisements:
        id = ad["id"]
        profile = ad["profile"]
        btn = InlineKeyboardButton(profile, callback_data=str(id))
        keyboard.append([btn])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="广告列表如下：", reply_markup=reply_markup
    )
    return FIRST


# def add(update: Update, context: CallbackContext):
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("1", callback_data=str(ONE)),
#             InlineKeyboardButton("3", callback_data=str(THREE)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
#     )
#     return FIRST


# def modify(update: Update, context: CallbackContext):
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
#             InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
#     )
#     # Transfer to conversation state `SECOND`
#     return SECOND


# def delete(update: Update, context: CallbackContext):
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("2", callback_data=str(TWO)),
#             InlineKeyboardButton("4", callback_data=str(FOUR)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
#     )
#     return FIRST


def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)} Until next time!"
    )

    user_data.clear()
    return ConversationHandler.END


advertisements_handler = ConversationHandler(
    entry_points=[CommandHandler('advertisements', start)],
    states={
        FIRST: [
            CallbackQueryHandler(all, pattern='^' + str(LIST) + '$')
        ]
    },
    fallbacks=[CommandHandler('advertisements', start)],
)
