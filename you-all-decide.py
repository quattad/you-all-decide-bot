import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import logging
import random

# Create instance of telegram.Bot class
bot = telegram.Bot(token='696904406:AAE7yA3ErhjAwJBNCJYu21ExOS4h8XnMyCU')

# Set up logging module to check for errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [["Add Places"],
                  ["Current Places"],
                  ["Generate Place"],
                  ["Done"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


# Define function to process update
def start(bot, update):
    update.message.reply_text("Hello, I am the YouAllDecide bot! \n"
                              "I aim to quickly eradicate indecisiveness! \n \n"
                              "What do you want to do? \n",
                              reply_markup=markup)

    return CHOOSING


def input2str(user_data):
    """ Takes all user inputs and prints it out"""
    input = list()

    for key, value in user_data.items():
        input.append('{}'.format(value))
        return "\n".join(input).join(['\n', '\n'])


def add_places(bot, update, user_data):
    text = update.message.text
    update.message.reply_text(
        "Sure, we can add a new place! \n" 
        "Send over the name of your place!"
    )

    return TYPING_REPLY


def current_places(bot, update, user_data):

    update.message.reply_text("This is what you added to the list so far.\n"
                              "{} \n"
                              "You can add more choices or randomly generate a place to go".format(input2str(user_data)),
                              reply_markup=markup)
    return CHOOSING


def received_information(bot, update, user_data):
    text = update.message.text
    output = []

    if 'places' in user_data:
        user_data['places'].append(text)
    else:
        user_data['places'] = [text]

    update.message.reply_text("Ok, added a new place! \n"
                              "This is what you added to the list so far."
                              "{}"
                              "You can add more choices or randomly generate a place to go. \n".format(input2str(user_data)),
                              reply_markup=markup)

    return CHOOSING


def generate_place(bot, update, user_data):

    if user_data is None:
        update.message.reply.text("You haven't entered any places!\n"
                                  "Please add some places using the Add Place button\n")
        return CHOOSING
    else:
        output = []

        for key in user_data:
            if key == 'places':
                output = user_data[key]

        random_choice = output[random.randint(0, len(output)-1)]
        print(random_choice)

        update.message.reply_text("The randomly generated place is: \n \n"
                                  "*** {} *** \n \n"
                                  "You can add more choices or randomly generate a place to go.".format(random_choice), reply_markup=markup)

        return CHOOSING


def done(bot, update, user_data):
    update.message.reply_text("Hope you found a place to go!")

    user_data.clear()

    return ConversationHandler.END


# Send message when command /help is issued by user.
def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Help!")


# Log errors caused by updates
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """ Start bot. """
    # Create updater object
    updater = Updater(token='696904406:AAE7yA3ErhjAwJBNCJYu21ExOS4h8XnMyCU')

    # Introduce dispatcher locally
    dp = updater.dispatcher

    # Add conversation handler with states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conversation_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                       states={
                                           CHOOSING: [RegexHandler('^Add Places$', add_places, pass_user_data=True),
                                                      RegexHandler('^Current Places$', current_places, pass_user_data=True),
                                                      RegexHandler('^Generate Place$', generate_place, pass_user_data=True)],
                                           TYPING_REPLY: [MessageHandler(Filters.text, received_information, pass_user_data=True)]
                                       },
                                       fallbacks=[RegexHandler("^Done$", done, pass_user_data=True)]
                                       )

    dp.add_handler(conversation_handler)

    # Log all errors
    dp.add_error_handler(error)

    # start the bot
    updater.start_polling()

    # stop bot by pressing Ctrl+C or sending signal to bot process
    updater.idle()


if __name__ == '__main__':
    main()