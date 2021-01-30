import logging
import advertisements
import info
import jobs
import accounts

from telegram.ext import Updater

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    REQUEST_KWARGS = {
        # "USERNAME:PASSWORD@" is optional, if you need authentication:
        'proxy_url': 'http://192.168.31.80:10809',
    }
    updater = Updater(token='1526755862:AAGdvU35rbPN1FEvPd5JgOcSTa2XBqOG6uk',
                      use_context=True, request_kwargs=REQUEST_KWARGS)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handler
    dispatcher.add_handler(info.info_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
