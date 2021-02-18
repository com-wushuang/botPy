import logging
import json
import db

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

# Stages
FIRST, SECOND, THIRD = range(3)

# Callback data
LIST_ALL, ADD, MODIFY, DELETE, DONE = range(5)

# Button text
LIST_TEXT, ADD_TEXT, MODIFY_TEXT, DELETE_TEXT, DONE_TEXT = "广告列表", "新增广告", "修改广告", "删除广告", "完成"

# tips
advertisement_content_tip = json.dumps({
    "key": "关键字",
    "introduction": "广告简介",
    "content": "广告内容"
}, ensure_ascii=False, indent=4)


def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton(LIST_TEXT, callback_data=str(LIST_ALL)),
            InlineKeyboardButton(ADD_TEXT, callback_data=str(ADD)),
            InlineKeyboardButton(DELETE_TEXT, callback_data=str(DELETE)),
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
    advertisement_list = db.list_ads()
    if not advertisement_list:
        keyboard = [
            [
                InlineKeyboardButton(ADD_TEXT, callback_data=str(ADD)),
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
                InlineKeyboardButton(LIST_TEXT, callback_data=str(LIST_ALL)),
                InlineKeyboardButton(ADD_TEXT, callback_data=str(ADD)),
                InlineKeyboardButton(DELETE_TEXT, callback_data=str(DELETE)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            '广告列表如下:\n' + json.dumps(advertisement_list, ensure_ascii=False, indent=4),
            reply_markup=reply_markup,
        )
        return FIRST


def add(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        '新增广告格式如下:\n' + advertisement_content_tip
    )

    return SECOND


def save(update: Update, context: CallbackContext):
    text = update.message.text
    obj = json.loads(text)
    db.create_ad(obj)
    update.message.reply_text(
        "广告添加成功，请在广告列表查看!"
    )
    return FIRST


def delete(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    advertisement_list = db.list_ads()
    query.edit_message_text(
        '广告列表如下:\n' + json.dumps(advertisement_list, ensure_ascii=False, indent=4) + '\n' + '请输入要删除的广告id',
    )

    return THIRD


def deleted(update: Update, context: CallbackContext):
    identify = int(update.message.text)
    try:
        obj = db.Advertisement.get_by_id(identify)
    except Exception:
        update.message.reply_text(
            "您输入的广告不存在!"
        )
        return FIRST

    obj.delete_instance()
    update.message.reply_text(
        "广告删除成功!"
    )
    return FIRST


def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you:  Until next time!"
    )

    user_data.clear()
    return ConversationHandler.END


# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST: [
            CommandHandler('start', start),
            CallbackQueryHandler(list_all, pattern='^' + str(LIST_ALL) + '$'),
            CallbackQueryHandler(add, pattern='^' + str(ADD) + '$'),
            CallbackQueryHandler(delete, pattern='^' + str(DELETE) + '$'),
        ],
        SECOND: [
            CommandHandler('start', start),
            MessageHandler(Filters.text, save)
        ],
        THIRD: [
            MessageHandler(
                Filters.text, deleted,
            )
        ],
    },
    fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
)
