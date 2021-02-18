import logging
import start
import job

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
    request_kwargs = {
        # "USERNAME:PASSWORD@" is optional, if you need authentication:
        'proxy_url': 'http://127.0.0.1:1087',
    }

    with open('token', 'r', encoding='utf-8') as f:
        token = f.read()

    updater = Updater(token=token, use_context=True, request_kwargs=request_kwargs)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handler
    dispatcher.add_handler(start.start_handler)

    job.init()
    # Start the Bot
    updater.start_polling()

    updater.idle()


app = None

if __name__ == '__main__':
    main()
