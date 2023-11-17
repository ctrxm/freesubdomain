## Documentation
Code ini adalah Code/Script Pembuat Subdomain Otomatis Menggunakan Bot di Telegram. Code ini bisa MultiDomain, dan CDN nya ialah Cloudflare!

**One-Line Installing on Fresh VPS Ubuntu**
```shell script
sudo apt-get update && sudo apt-get install -y screen python3 python3-pip && git clone https://github.com/powergunn/freesubdomain.git && cd freesubdomain && pip3 install -r requirements.txt
```
1. Buat Bot Telegram Menggunakan [BotFather](https://t.me/BotFather)
```shell script
nano bot.py
```
2. Edit `TELEGRAM_TOKEN` `CLOUDFLARE_API_KEY` `CLOUDFLARE_EMAIL` dan yang terakhir `ZONE_ID_CLOUDFLARE` sesuaikan dengan domain anda. Lalu SAVE `CTRL+X`+`CTRL+Y` dan `ENTER`
3. Selanjutnya Jalankan `Screen` Supaya BOT online terus.
```shell script
screen -S botsession
```
```shell script
python3 bot.py
```
4. Sekarang BOT anda sudah dapat di gunakan! Untuk masuk kembali ke `Screen` yang telah di buat sebelumnya.
```shell script
screen -r botsession
```
**💰 Tengkyu For :**

<b>Cloudflare</b> <code>https://dash.cloudflare.com</code></br>
<b>BotFather</b> <code>https://t.me/BotFather</code></br>
<b>SCRIPT BY</b> <code>https://t.me/gungrate</code></br>
