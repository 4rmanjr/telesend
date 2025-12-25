#!/usr/bin/env python3
import os
import sys
import requests
import argparse
import datetime

# Lokasi config (relative terhadap lokasi script asli)
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config")
HISTORY_FILE = os.path.expanduser("~/.telechat_history")

def get_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ File konfigurasi tidak ditemukan di: {CONFIG_FILE}")
        sys.exit(1)
    
    config = {}
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key] = value.replace('"', '').replace("'", "")
    
    if "GANTI_DENGAN" in config.get('TOKEN', ''):
        print("❌ Konfigurasi belum diisi.")
        print(f"👉 Silakan edit file: {CONFIG_FILE}")
        sys.exit(1)

    return config

def get_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    
    entries = []
    try:
        with open(HISTORY_FILE, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line: continue
            
            chat_id = None
            
            # Parsing format history
            if '|' in line:
                parts = line.split('|')
                msg_id = parts[0]
                timestamp = float(parts[1])
                filename = parts[2] if len(parts) > 2 else "Tidak diketahui"
                # Ambil Chat ID jika ada (format baru)
                if len(parts) > 3:
                    chat_id = parts[3]
            else:
                # Format legacy (spasi)
                parts = line.split()
                msg_id = parts[0]
                timestamp = float(parts[1]) if len(parts) > 1 else 0
                filename = "File Lama"
                
            entries.append({
                'id': msg_id,
                'ts': timestamp,
                'file': os.path.basename(filename),
                'chat_id': chat_id, # Bisa None jika format lama
                'raw_line': line
            })
    except Exception:
        pass
        
    return entries

def save_history(entries):
    with open(HISTORY_FILE, 'w') as f:
        for entry in entries:
            f.write(entry['raw_line'] + '\n')

def delete_message(token, chat_id, message_id):
    url = f"https://api.telegram.org/bot{token}/deleteMessage"
    try:
        resp = requests.post(url, json={'chat_id': chat_id, 'message_id': message_id})
        data = resp.json()
        if data.get('ok'):
            print(f"✅ Pesan {message_id} (Chat: {chat_id}) berhasil dihapus.")
            return True
        else:
            desc = data.get('description')
            print(f"⚠️  Gagal menghapus pesan {message_id}: {desc}")
            if "message to delete not found" in str(desc).lower():
                return True
            return False
    except Exception as e:
        print(f"❌ Error koneksi: {e}")
        return False

def show_list(entries, default_chat_id):
    print("\n📜 Riwayat Pesan Terkirim:")
    print("-" * 85)
    print(f"{ 'ID Pesan':<10} | {'Chat ID':<15} | {'Waktu':<18} | {'Nama File'}")
    print("-" * 85)
    
    for entry in reversed(entries):
        dt = datetime.datetime.fromtimestamp(entry['ts']).strftime('%Y-%m-%d %H:%M')
        # Gunakan Chat ID dari history jika ada, kalau tidak pakai default config
        display_chat_id = entry['chat_id'] if entry['chat_id'] else f"{default_chat_id} (Def)"
        
        print(f"{entry['id']:<10} | {display_chat_id:<15} | {dt:<18} | {entry['file']}")
    print("-" * 85)

def main():
    parser = argparse.ArgumentParser(description="Hapus pesan Telegram.")
    parser.add_argument('--id', type=str, help='Hapus ID pesan tertentu')
    parser.add_argument('--all', action='store_true', help='Hapus SEMUA riwayat')
    args = parser.parse_args()

    config = get_config()
    TOKEN = config.get('TOKEN')
    DEFAULT_CHAT_ID = config.get('CHAT_ID')

    entries = get_history()

    # Fungsi helper untuk menentukan Chat ID yang dipakai
    def resolve_chat_id(entry):
        return entry['chat_id'] if entry['chat_id'] else DEFAULT_CHAT_ID

    # 1. Mode Hapus ID Spesifik (via argumen)
    if args.id:
        # Cari entry untuk ID ini agar tahu Chat ID-nya
        target = next((e for e in entries if str(e['id']) == str(args.id)), None)
        target_chat_id = resolve_chat_id(target) if target else DEFAULT_CHAT_ID
        
        if delete_message(TOKEN, target_chat_id, args.id):
            entries = [e for e in entries if str(e['id']) != str(args.id)]
            save_history(entries)
        return

    # 2. Mode Hapus Semua
    if args.all:
        confirm = input("⚠️  Yakin ingin menghapus SEMUA pesan di riwayat? (y/n): ")
        if confirm.lower() != 'y':
            print("Dibatalkan.")
            return

        active_entries = []
        for entry in entries:
            chat_id = resolve_chat_id(entry)
            if not delete_message(TOKEN, chat_id, entry['id']):
                active_entries.append(entry)
        
        save_history(active_entries)
        if not active_entries:
            print("✅ Semua riwayat bersih.")
        return

    # 3. Mode Interaktif
    if not entries:
        print("ℹ️  Belum ada riwayat pengiriman pesan.")
        return

    show_list(entries, DEFAULT_CHAT_ID)
    
    print("\n💡 Ketik ID pesan untuk menghapus, atau 'all' untuk hapus semua.")
    choice = input("👉 Pilihan (Enter untuk batal): ").strip()

    if not choice:
        print("Selesai.")
        return

    if choice.lower() == 'all':
        os.system(f"{sys.argv[0]} --all")
    else:
        target = next((e for e in entries if str(e['id']) == choice), None)
        target_chat_id = resolve_chat_id(target) if target else DEFAULT_CHAT_ID
        
        if delete_message(TOKEN, target_chat_id, choice):
            new_entries = [e for e in entries if str(e['id']) != choice]
            save_history(new_entries)
            print("\n💡 Tips: File terhapus. Mau kirim revisi? Ketik \033[1;33mkirimtele <file>\033[0m")
        elif not target:
             delete_message(TOKEN, DEFAULT_CHAT_ID, choice)

if __name__ == "__main__":
    main()
