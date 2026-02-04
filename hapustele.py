#!/usr/bin/env python3
import os
import sys

# Pengecekan Dependency
try:
    import requests
except ImportError:
    print("❌ Error: Library 'requests' tidak ditemukan.")
    
    # Deteksi distro
    install_cmd = "pip install requests"
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            os_info = f.read().lower()
            if "arch" in os_info or "cachy" in os_info:
                install_cmd = "sudo pacman -S --noconfirm python-requests"
            elif "debian" in os_info or "ubuntu" in os_info:
                install_cmd = "sudo apt update && sudo apt install -y python3-requests"
            elif "fedora" in os_info:
                install_cmd = "sudo dnf install -y python3-requests"
    
    confirm = input(f"❓ Ingin menginstallnya secara otomatis? (y/n): ").lower()
    if confirm == 'y':
        print(f"🚀 Menjalankan: {install_cmd}")
        os.system(install_cmd)
        # Cek ulang setelah install
        try:
            import requests
            print("✅ Berhasil menginstall library 'requests'.")
        except ImportError:
            print("❌ Gagal menginstall. Silakan install manual.")
            sys.exit(1)
    else:
        print(f"💡 Silakan install secara manual dengan:\n   {install_cmd}")
        sys.exit(1)

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
            # Format: ID|TS|FILENAME|CHAT_ID
            if '|' in line:
                parts = line.split('|')
                msg_id = parts[0]
                timestamp = float(parts[1])
                
                # Logic parsing filename & chat_id yang lebih robust
                if len(parts) > 3:
                    # Asumsi format baru: elemen terakhir adalah chat_id
                    chat_id = parts[-1]
                    # Sisanya di tengah adalah filename (jika filename mengandung pipe yang lolos sanitasi)
                    filename = "|".join(parts[2:-1])
                else:
                    # Format legacy tanpa chat_id: ID|TS|FILENAME
                    filename = "|".join(parts[2:])
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
                'chat_id': chat_id, 
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
            # Jika pesan tidak ditemukan (sudah terhapus), anggap sukses agar dihapus dari history
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
    
    # Tampilkan 20 entri terakhir saja agar tidak terlalu panjang
    limit = 20
    display_entries = entries[-limit:]
    
    for entry in reversed(display_entries):
        dt = datetime.datetime.fromtimestamp(entry['ts']).strftime('%Y-%m-%d %H:%M')
        display_chat_id = entry['chat_id'] if entry['chat_id'] else f"{default_chat_id} (Def)"
        
        print(f"{entry['id']:<10} | {display_chat_id:<15} | {dt:<18} | {entry['file']}")
    print("-" * 85)
    if len(entries) > limit:
        print(f"... (dan {len(entries) - limit} pesan lama lainnya)")

def main():
    parser = argparse.ArgumentParser(description="Hapus pesan Telegram.")
    parser.add_argument('--id', type=str, help='Hapus ID pesan tertentu')
    parser.add_argument('--all', action='store_true', help='Hapus SEMUA riwayat')
    args = parser.parse_args()

    config = get_config()
    TOKEN = config.get('TOKEN')
    DEFAULT_CHAT_ID = config.get('CHAT_ID')

    entries = get_history()

    def resolve_chat_id(entry):
        return entry['chat_id'] if entry['chat_id'] else DEFAULT_CHAT_ID

    # 1. Mode Hapus ID Spesifik (via argumen)
    if args.id:
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
    
    print("\n💡 Ketik ID pesan untuk menghapus.")
    print("   Bisa input banyak ID dipisah spasi (contoh: 123 124 125).")
    print("   Atau ketik 'all' untuk hapus semua.")
    choice = input("👉 Pilihan (Enter untuk batal): ").strip()

    if not choice:
        print("Selesai.")
        return

    if choice.lower() == 'all':
        os.system(f"{sys.argv[0]} --all")
    else:
        # Support multiple IDs separated by space or comma
        ids_to_delete = choice.replace(',', ' ').split()
        
        updated_entries = list(entries) # Copy list
        changes_made = False
        
        for msg_id in ids_to_delete:
            target = next((e for e in updated_entries if str(e['id']) == msg_id), None)
            
            if target:
                target_chat_id = resolve_chat_id(target)
                if delete_message(TOKEN, target_chat_id, msg_id):
                    updated_entries = [e for e in updated_entries if str(e['id']) != msg_id]
                    changes_made = True
            else:
                # Coba hapus meski tidak ada di history (mungkin input manual ID)
                print(f"⚠️  ID {msg_id} tidak ada di history lokal, mencoba hapus remote...")
                if delete_message(TOKEN, DEFAULT_CHAT_ID, msg_id):
                    changes_made = True

        if changes_made:
            save_history(updated_entries)
            print("\n✅ Penghapusan selesai.")
            print("💡 Tips: Mau kirim revisi? Ketik \033[1;33mkirimtele <file>\033[0m")