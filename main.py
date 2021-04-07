from os import environ
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def end(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def start(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the conversation.")
    keyboard = [
        [InlineKeyboardButton("Info Pelanggan", callback_data='infoPelanggan')],
        [InlineKeyboardButton("Laporan Performansi", callback_data='laporanPerformansi')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to Whepi Tools. Please select Whepi Menu", reply_markup=reply_markup)
    return 0


def infoPelanggan(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Info SN (All)', callback_data='infoSN')],
        [InlineKeyboardButton('Ukur Kualitas Jaringan (All)', callback_data='ukurKualitasJaringan')],
        [InlineKeyboardButton('Deteksi New Serial Number (All)', callback_data='deteksiNewSerialNumber')],
        [InlineKeyboardButton('Info vlan by ipaddress', callback_data='infoVlanByIpaddress')],
        [InlineKeyboardButton('Back', callback_data='mainMenu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Please select 1 of Whepi Menu", reply_markup=reply_markup
    )
    return 1


def laporanPerformansi(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back', callback_data='mainMenu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="(Belum ada pilihan)", reply_markup=reply_markup
    )
    return 1


def infoSN(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back', callback_data='infoPelanggan')],
        [InlineKeyboardButton('Back Main Menu', callback_data='mainMenu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Inputkan SN dengan awalan ZTEG / ALCL / HWTC / FHTT", reply_markup=reply_markup
    )
    return 2


def ukurKualitasJaringan(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back', callback_data='infoPelanggan')],
        [InlineKeyboardButton('Back Main Menu', callback_data='mainMenu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Inputkan No. Telp atau Inet", reply_markup=reply_markup
    )
    return 2


def deteksiNewSerialNumber(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back', callback_data='infoPelanggan')],
        [InlineKeyboardButton('Back Main Menu', callback_data='mainMenu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Inputkan SN dengan awalan ZTEG / ALCL / HWTC / FHTT", reply_markup=reply_markup
    )
    return 2


def infoVlanByIpaddress(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back', callback_data='infoPelanggan')],
        [InlineKeyboardButton('Back Main Menu', callback_data='mainMenu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Inputkan IPAddress", reply_markup=reply_markup
    )
    return 2


def mainMenu(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Info Pelanggan", callback_data='infoPelanggan')],
        [InlineKeyboardButton("Laporan Performansi", callback_data='laporanPerformansi')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Welcome to Whepi Tools. Please select Whepi Menu", reply_markup=reply_markup
    )
    return 0


def main() -> None:
    updater = Updater(environ['TOKEN'])
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [
                CallbackQueryHandler(infoPelanggan, pattern='^infoPelanggan$'),
                CallbackQueryHandler(laporanPerformansi, pattern='^laporanPerformansi$')
            ],
            1: [
                CallbackQueryHandler(infoSN, pattern='^infoSN$'),
                CallbackQueryHandler(ukurKualitasJaringan, pattern='^ukurKualitasJaringan$'),
                CallbackQueryHandler(deteksiNewSerialNumber, pattern='^deteksiNewSerialNumber$'),
                CallbackQueryHandler(infoVlanByIpaddress, pattern='^infoVlanByIpaddress$'),
                CallbackQueryHandler(mainMenu, pattern='^mainMenu$'),
            ],
            2: [
                CallbackQueryHandler(infoPelanggan, pattern='^infoPelanggan$'),
                CallbackQueryHandler(mainMenu, pattern='^mainMenu$'),
            ],

        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
