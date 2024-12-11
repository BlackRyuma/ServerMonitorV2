import asyncio
import psutil
import subprocess
from telegram import Bot
import os

# Ganti dengan token bot Anda
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "YOUR_CHANNEL_ID"

# Fungsi untuk mendapatkan informasi CPU
def get_cpu_info():
    cpu_info = ""
    cpu_info += f"CPU Usage: {psutil.cpu_percent(interval=1)}%\n"
    cpu_info += "CPU per Core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_info += f"  Core {i}: {percentage}%\n"
    cpu_freq = psutil.cpu_freq()
    cpu_info += f"CPU Frequency: {cpu_freq.current:.2f} MHz\n"
    cpu_info += f"Total CPU Cores: {psutil.cpu_count(logical=False)}\n"
    return cpu_info

# Fungsi untuk mendapatkan informasi RAM
def get_ram_info():
    ram = psutil.virtual_memory()
    ram_info = ""
    ram_info += f"Total RAM: {ram.total / (1024**3):.2f} GB\n"
    ram_info += f"Used RAM: {ram.used / (1024**3):.2f} GB\n"
    ram_info += f"Available RAM: {ram.available / (1024**3):.2f} GB\n"
    ram_info += f"RAM Usage: {ram.percent}%\n"
    return ram_info

# Fungsi untuk mendapatkan informasi Disk
def get_disk_info():
    disk_usage = psutil.disk_usage('/')
    disk_info = ""
    disk_info += f"Disk Total: {disk_usage.total / (1024**3):.2f} GB\n"
    disk_info += f"Disk Used: {disk_usage.used / (1024**3):.2f} GB\n"
    disk_info += f"Disk Free: {disk_usage.free / (1024**3):.2f} GB\n"
    disk_info += f"Disk Usage: {disk_usage.percent}%\n"
    return disk_info

# Fungsi untuk mendapatkan daftar sesi screen
def get_screen_sessions():
    try:
        result = subprocess.run(["screen", "-ls"], stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error fetching screen sessions: {e}"

# Fungsi untuk melakukan ping ke server tertentu
def get_ping():
    try:
        # Melakukan ping ke Google
        response = subprocess.run(
            ["ping", "-c", "1", "google.com"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Ekstrak waktu respons dari hasil ping
        if response.returncode == 0:
            for line in response.stdout.split("\n"):
                if "time=" in line:
                    return f"Ping to google.com: {line.split('time=')[1].split(' ')[0]}\n"
        return "Ping failed: No response\n"
    except Exception as e:
        return f"Ping Error: {e}\n"

# Fungsi utama untuk mengirim data ke Telegram
async def send_to_telegram():
    bot = Bot(token=BOT_TOKEN)
    while True:
        try:
            # Ambil informasi CPU, RAM, Disk, Screen Sessions, dan Ping
            cpu_info = get_cpu_info()
            ram_info = get_ram_info()
            disk_info = get_disk_info()
            screen_info = get_screen_sessions()
            ping_info = get_ping()

            # Gabungkan semua info menjadi satu pesan
            message = (
                "📊 **Server Monitoring** 📊\n\n"
                f"**CPU Info:**\n{cpu_info}\n"
                f"**RAM Info:**\n{ram_info}\n"
                f"**Disk Info:**\n{disk_info}\n"
                f"**Active Screen Sessions:**\n{screen_info}\n"
                f"**Ping Info:**\n{ping_info}\n"
            )

            # Kirim pesan ke Telegram
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
        except Exception as e:
            print(f"Error: {e}")

        # Tunggu 600 detik sebelum mengirim pesan berikutnya
        await asyncio.sleep(600)

# Menjalankan bot
if __name__ == "__main__":
    asyncio.run(send_to_telegram())
