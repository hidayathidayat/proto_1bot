from os import environ
import logging
from telegram import (
    Update, InlineKeyboardButton,
    InlineKeyboardMarkup, Bot
)
from telegram.ext import (
    CallbackContext, ConversationHandler,
    CommandHandler, CallbackQueryHandler,
    MessageHandler, Filters, Dispatcher
)
from flask import Flask, request, Response
from webhook import setwebhook, deletewebhook


logging.basicConfig(filename='logfile.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


TOKEN = environ.get('TOKEN')
global bot
global dp
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, None)
app = Flask(__name__)


# <Method>========================================================= #
def start(update: Update, _: CallbackContext):
    update.message.reply_text("Silahkan liat /menu yang tersedia")
    return ConversationHandler.END


def menu(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logging.info(f"User {user.first_name} started the conversation.")
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


def responInfoSN(update: Update, _: CallbackContext):
    sn = update.message.text
    if len(sn) >= 12:
        # find info berdasarkan sn
        update.message.reply_text(
            f'Data Teknis {sn.upper()} yaitu (some info)'
        )
        return ConversationHandler.END
    elif len(sn) < 12:
        update.message.reply_text('Cek kembali Nomor SN, minimal 12 karakter')


def ukurKualitasJaringan(update: Update, _: CallbackContext) -> str:
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


def responukurKualitasJaringan(update: Update, _: CallbackContext):
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


def deteksiNewSerialNumber(update: Update, _: CallbackContext) -> str:
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


def respondeteksiNewSerialNumber(update: Update, _: CallbackContext):
    sn = update.message.text
    if len(sn) >= 5:
        # find info berdasarkan sn
        update.message.reply_text(
            f'Hasil temuan {sn} adalah (data)'
        )
        return ConversationHandler.END
    elif len(sn) < 5:
        update.message.reply_text(' Cek kembali Nomor SN minimal 5 karakter terakhir')


def infoVlanByIpaddress(update: Update, _: CallbackContext) -> str:
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


def responinfoVlanByIpaddress(update: Update, _: CallbackContext):
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
# </Method>========================================================== #


# <Flask Route>====================================================== #
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return 'Server is running'


@app.route(f'/{TOKEN}', methods=['POST', 'GET'])
def Telegram_POST():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        dp.process_update(update)
        return Response('POST success', status=200)
    elif request.method == 'GET':
        return 'Server is running'
# # </Flask Route>===================================================== #


# <Main>============================================================= #
def main():
    # Restart Webhook================ #
    deletewebhook(TOKEN)
    logging.info('Webhook was deleted')
    MY_WEB = environ.get('MY_WEB')
    WEB_URL = f'{MY_WEB}/{TOKEN}'
    setwebhook(TOKEN, WEB_URL)
    logging.info('Webhook was set')
    # =============================== #

    # <Add Handler>================== #
    main_handler = ConversationHandler(
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

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(main_handler)
    # </Add Handler>================= #

    # <Run Flask>==================== #
    app.run(host='127.0.0.1', port=8443)
    # </Run Flask>=================== #
# </Main>============================================================ #


if __name__ == '__main__':
    main()
