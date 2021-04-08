from os import environ
import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Silahkan liat /menu yang tersedia")
    return ConversationHandler.END


def menu(update: Update, _: CallbackContext) -> int:
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


def infoSN(update: Update, _: CallbackContext) -> str:
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
    return 'responInfoSN'


def responInfoSN(update: Update, _: CallbackContext) -> None:
    sn = update.message.text
    if len(sn) >= 12:
        # find info berdasarkan sn
        update.message.reply_text(
            f'Data Teknis {sn.upper()} yaitu (some info)'
        )
        return ConversationHandler.END
    elif len(sn) < 12:
        update.message.reply_text('Cek kembali Nomor SN, minimal 12 karakter')


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
    return 'responukurKualitasJaringan'


def responukurKualitasJaringan(update: Update, _: CallbackContext) -> None:
    telponInet = update.message.text
    if len(telponInet) >= 5:
        # find info berdasarkan sn
        update.message.reply_text(
            'Output dari API : \n'
            'Nama : \n'
            'Hostname : \n'
            'IP Address : \n'
            'Shelf : \n'
            'Slot : \n'
            'Port : \n'
            'Onu : \n'
            'Serial Number : \n'
            'Status Operasi : \n'
            'Onu RX Power : \n'
            'OLT RX Power: \n'
        )
        return ConversationHandler.END
    elif len(telponInet) < 5:
        update.message.reply_text('Cek kembali Nomor POTS, minimal 5 angka')


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
    return 'respondeteksiNewSerialNumber'


def respondeteksiNewSerialNumber(update: Update, _: CallbackContext) -> None:
    sn = update.message.text
    if len(sn) >= 5:
        # find info berdasarkan sn
        update.message.reply_text(
            f'Hasil temuan {sn} adalah (data)'
        )
        return ConversationHandler.END
    elif len(sn) < 5:
        update.message.reply_text(' Cek kembali Nomor SN minimal 5 karakter terakhir')


def infoVlanByIpaddress(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back', callback_data='infoPelanggan')],
        [InlineKeyboardButton('Back Main Menu', callback_data='mainMenu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Inputkan IP Address", reply_markup=reply_markup
    )
    return 'responinfoVlanByIpaddress'


def responinfoVlanByIpaddress(update: Update, _: CallbackContext) -> None:
    ip = update.message.text
    # find info berdasarkan sn
    update.message.reply_text(
        f'Your IP Address : {ip} \n'
        'Info : (some info)'
    )
    return ConversationHandler.END


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
    PORT = environ.get('PORT', '8443')
    updater = Updater(environ['TOKEN'])
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', menu)],
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
            'responInfoSN': [
                MessageHandler(Filters.text & ~Filters.command, responInfoSN),
                CallbackQueryHandler(infoPelanggan, pattern='^infoPelanggan$'),
                CallbackQueryHandler(mainMenu, pattern='^mainMenu$'),
            ],
            'responukurKualitasJaringan': [
                MessageHandler(Filters.text & ~Filters.command, responukurKualitasJaringan),
                CallbackQueryHandler(infoPelanggan, pattern='^infoPelanggan$'),
                CallbackQueryHandler(mainMenu, pattern='^mainMenu$'),
            ],
            'respondeteksiNewSerialNumber': [
                MessageHandler(Filters.text & ~Filters.command, respondeteksiNewSerialNumber),
                CallbackQueryHandler(infoPelanggan, pattern='^infoPelanggan$'),
                CallbackQueryHandler(mainMenu, pattern='^mainMenu$'),
            ],
            'responinfoVlanByIpaddress': [
                MessageHandler(Filters.text & ~Filters.command, responinfoVlanByIpaddress),
                CallbackQueryHandler(infoPelanggan, pattern='^infoPelanggan$'),
                CallbackQueryHandler(mainMenu, pattern='^mainMenu$'),
            ],
        },
        fallbacks=[CommandHandler('menu', menu), CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("start", start))

    # updater.start_polling()
    updater.start_webhook(listen='0.0.0.0',
                          port=PORT,
                          url_path=environ['TOKEN'],
                          webhook_url='https://proto-1bot.herokuapp.com/' + environ['TOKEN'])
    updater.idle()


if __name__ == '__main__':
    main()
