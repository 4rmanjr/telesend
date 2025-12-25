#!/usr/bin/env python3
import os
import time
import requests
import json
import datetime

# Lokasi config (relative terhadap lokasi script asli)
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config")

def get_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ File konfigurasi tidak ditemukan di: {CONFIG_FILE}")
        exit(1)
    
    config = {}
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                # Hapus tanda kutip " dari value
                config[key] = value.replace('"', '').replace("'", "")
    
    if "GANTI_DENGAN" in config.get('TOKEN', ''):
        print("❌ Konfigurasi belum diisi.")
        print(f"👉 Silakan edit file: {CONFIG_FILE}")
        exit(1)
        
    return config

def main():
    config = get_config()
    TOKEN = config.get('TOKEN')
    ALLOWED_CHAT_ID = config.get('CHAT_ID')
    
    if not TOKEN:
        print("❌ Token tidak ditemukan di konfigurasi.")
        exit(1)

    # Waktu mulai script
    START_TIME = time.time()
    start_str = datetime.datetime.fromtimestamp(START_TIME).strftime('%H:%M:%S')

    # Samarkan Chat ID untuk privasi
    masked_id = "*" * (len(ALLOWED_CHAT_ID) - 4) + ALLOWED_CHAT_ID[-4:] if len(ALLOWED_CHAT_ID) > 4 else "****"

    print(f"✅ Siap! Mode Live aktif mulai jam {start_str}")
    print(f"🔒 Mode Privat: Hanya menerima dari chat yang diotorisasi ({masked_id})")
    print("📥 Menunggu file baru... (Ctrl+C untuk stop)")
    
    offset = 0
    url = f"https://api.telegram.org/bot{TOKEN}"
    
    while True:
        try:
            # Cek pesan baru
            response = requests.get(f"{url}/getUpdates", params={'offset': offset, 'timeout': 30})
            data = response.json()
            
            if not data.get('ok'):
                time.sleep(5)
                continue

            for result in data['result']:
                # Update offset agar pesan ditandai "terbaca" di server
                offset = result['update_id'] + 1
                
                message = result.get('message', {})
                if not message:
                    continue

                # 1. Cek Pengirim (Keamanan)
                # Pastikan file berasal dari Chat ID yang benar (Anda/Grup Anda)
                incoming_chat_id = str(message['chat']['id'])
                if incoming_chat_id != ALLOWED_CHAT_ID:
                    # Silent skip untuk orang asing
                    continue

                # 2. Cek Waktu (Live Mode)
                # Abaikan pesan yang dikirim SEBELUM script ini jalan
                msg_date = message.get('date', 0)
                if msg_date < START_TIME:
                    # Lewati pesan lama (backlog)
                    continue

                file_id = None
                file_name = None
                
                # Deteksi tipe file
                if 'document' in message:
                    file_id = message['document']['file_id']
                    file_name = message['document'].get('file_name', 'dokumen_tanpa_nama')
                    print(f"📄 Mendeteksi Dokumen: {file_name}")
                
                elif 'photo' in message:
                    file_id = message['photo'][-1]['file_id'] # Ambil resolusi tertinggi
                    file_name = f"photo_{int(time.time())}.jpg"
                    print(f"🖼️  Mendeteksi Foto")
                
                elif 'video' in message:
                    file_id = message['video']['file_id']
                    file_name = message['video'].get('file_name', f"video_{int(time.time())}.mp4")
                    print(f"🎥 Mendeteksi Video")

                # Proses Download
                if file_id:
                    file_info = requests.get(f"{url}/getFile", params={'file_id': file_id}).json()
                    
                    if file_info.get('ok'):
                        remote_path = file_info['result']['file_path']
                        download_url = f"https://api.telegram.org/file/bot{TOKEN}/{remote_path}"
                        
                        print(f"   ⬇️  Mengunduh...", end='', flush=True)
                        file_content = requests.get(download_url).content
                        
                        # Simpan
                        with open(file_name, 'wb') as f:
                            f.write(file_content)
                        print(f" ✅ Selesai! ({file_name})")
                    else:
                        print("   ❌ Gagal mengambil path file.")
        
        except KeyboardInterrupt:
            print("\n🛑 Berhenti.")
            print("\n💡 Tips: Mau membalas/mengirim file? Gunakan perintah:")
            print("   \033[1;33mkirimtele <nama_file>\033[0m")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()