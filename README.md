# ServerMonitorV2
versi upgrade dari server monitor sebelumnya, menampilakan info yang lebih lengkap

versi 1 = menampilka info yang lebih simple https://github.com/BlackRyuma/ServerMonitor.git

1. Pastikan Python sudah terinstal:
sudo apt update

sudo apt install python3 python3-pip -y

Instal library yang diperlukan:
pip3 install python-telegram-bot psutil

atau gunakan command pip3 install -r requirements.txt

###############

Ganti Placeholder:

Gunakan command 

nano config monitor.py

kemudian cari tulisan di bawah

YOUR_BOT_API_TOKEN: Ganti dengan token API bot.

@Yourchannel: ganti dengan id channel jika private atau jika publik bisa gunakan username atau id (channel harus menambahkan bot sebagai admin).


Jalankan Bot: Jalankan bot dengan perintah:

python3 server_monitor_bot.py
