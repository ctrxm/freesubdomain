import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from CloudFlare import CloudFlare
import random
import string

# Ganti dengan token bot Telegram Anda
TELEGRAM_TOKEN = '7045651779:AAFUJTYLVVwgGXNVrlkd5OtwYWsJq2sJCQQ'

# Ganti dengan API Key Cloudflare Anda
CLOUDFLARE_API_KEY = '4c6c88b6cffbe2f738489f5cb1612700f17f3'
CLOUDFLARE_EMAIL = 'hendra1rangga@gmail.com'

# Dictionary untuk menyimpan alamat IP server pengguna
user_ips = {}

def start(update, context):
    user_id = update.message.from_user.id
    context.bot.send_message(chat_id=update.message.chat_id, text="Buat Subdomain Gratis! Untuk Kamu Yang Mau Belajar! BY : @ctrxzip")

    # Pilihan domain
    reply_keyboard = [['cilacap.city', 'gafoqe.com', 'Cancel']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(chat_id=user_id, text="Pilih domain:", reply_markup=markup)

    # Mengatur state agar bot tahu kita sedang menunggu pemilihan domain
    return 'wait_domain'

def cancel(update, context):
    user_id = update.message.from_user.id
    context.bot.send_message(chat_id=user_id, text="Terimakasih.", reply_markup=ReplyKeyboardRemove())
    # Hapus data pengguna dari kamus jika ada
    if user_id in user_ips:
        del user_ips[user_id]
    return ConversationHandler.END

def wait_domain(update, context):
    user_id = update.message.from_user.id
    selected_domain = update.message.text.lower()

    if selected_domain not in ['cilacap.city', 'gafoqe.com', 'cancel']:
        context.bot.send_message(chat_id=user_id, text="Pilihan domain tidak valid. Silakan pilih domain yang benar.")
        return 'wait_domain'
    elif selected_domain == 'cancel':
        return cancel(update, context)

    user_ips[user_id] = {'domain': selected_domain}

    # Menggunakan keyboard khusus untuk memudahkan input IP
    reply_keyboard = [['Cancel']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(chat_id=user_id, text="Masukkan IP server Hosting/Bug/VPS Kamu:", reply_markup=markup)

    # Mengatur state agar bot tahu kita sedang menunggu IP
    return 'wait_ip'

def wait_ip(update, context):
    user_id = update.message.from_user.id
    user_data = user_ips[user_id]
    user_data['ip'] = update.message.text

    if 'domain' not in user_data:
        context.bot.send_message(chat_id=user_id, text="Terjadi kesalahan. Silakan coba lagi.")
        return cancel(update, context)

    # Membuat string acak untuk subdomain
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    subdomain = f"gun{random_string}"

    # Mengelola subdomain di Cloudflare
    cf = CloudFlare(email=CLOUDFLARE_EMAIL, token=CLOUDFLARE_API_KEY)

    # Menentukan zone id berdasarkan pilihan domain
    if user_data['domain'] == 'cilacap.city':
        zone_id = 'ZONE_ID_CLOUDFLARE'
    elif user_data['domain'] == 'gafoqe.com':
        zone_id = 'ZONE_ID_CLOUDFLARE'
    else:
        context.bot.send_message(chat_id=user_id, text="Terjadi kesalahan. Silakan coba lagi.")
        return cancel(update, context)

    record = {
        'type': 'A',
        'name': f"{subdomain}.{user_data['domain']}",
        'content': user_data['ip'],
    }

    try:
        cf.zones.dns_records.post(zone_id, data=record)
        # Mengirimkan pesan ke pengguna dengan subdomain yang dibuat
        message = f"Subdomain Berhasil dibuat.\nCreated by @ctrxzip\n\nDOMAIN : {user_data['domain']}\nIP : {user_data['ip']}\n\nSubdomain Kamu :\n{subdomain}.{user_data['domain']}\n\nThx.\nID Kamu : {user_id}\n"
        context.bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        print(f"Error creating DNS record: {e}")
        context.bot.send_message(chat_id=user_id, text="Terjadi kesalahan saat membuat rekaman DNS. Silakan coba lagi.")

    # Menghapus data pengguna dari kamus setelah digunakan
    del user_ips[user_id]

    return cancel(update, context)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'wait_domain': [MessageHandler(Filters.text & ~Filters.command, wait_domain)],
            'wait_ip': [MessageHandler(Filters.text & ~Filters.command, wait_ip)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    
    # Mulai bot
    updater.start_polling()

    # Jalankan bot sampai pengguna menekan Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
    
