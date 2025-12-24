#!/usr/bin/env python3
import os
import sys
import requests
import argparse
import datetime

# Lokasi config
CONFIG_FILE = os.path.expanduser("~/.telechat_rc")
HISTORY_FILE = os.path.expanduser("~/.telechat_history")

def get_config():
    if not os.path.exists(CONFIG_FILE):
        print("❌ Konfigurasi belum ditemukan.")
        sys.exit(1)
    
    config = {}
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value.replace('"', '')
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
            
            # Support format lama (spasi) dan baru (pipe |)
            if '|' in line:
                parts = line.split('|')
                msg_id = parts[0]
                timestamp = float(parts[1])
                filename = parts[2] if len(parts) > 2 else "Tidak diketahui"
            else:
                parts = line.split()
                msg_id = parts[0]
                timestamp = float(parts[1]) if len(parts) > 1 else 0
                filename = "File Lama (Tanpa Nama)"
                
            entries.append({
                'id': msg_id,
                'ts': timestamp,
                'file': os.path.basename(filename), # Ambil nama file saja
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
            print(f"✅ Pesan {message_id} berhasil dihapus.")
            return True
        else:
            print(f"⚠️  Gagal menghapus pesan {message_id}: {data.get('description')}")
            # Jika pesan tidak ditemukan (sudah dihapus), anggap sukses agar history bersih
            if "message to delete not found" in str(data.get('description')).lower():
                return True
            return False
    except Exception as e:
        print(f"❌ Error koneksi: {e}")
        return False

def show_list(entries):
    print("\n📜 Riwayat Pesan Terkirim:")
    print("-" * 60)
    print(f"{ 'ID Pesan':<15} | {'Waktu':<20} | {'Nama File'}")
    print("-" * 60)
    
    # Tampilkan dari yang terbaru (reverse)
    for entry in reversed(entries):
        dt = datetime.datetime.fromtimestamp(entry['ts']).strftime('%Y-%m-%d %H:%M')
        print(f"{entry['id']:<15} | {dt:<20} | {entry['file']}")
    print("-" * 60)

def main():
    parser = argparse.ArgumentParser(description="Hapus pesan Telegram.")
    parser.add_argument('--id', type=str, help='Hapus ID pesan tertentu')
    parser.add_argument('--all', action='store_true', help='Hapus SEMUA riwayat')
    args = parser.parse_args()

    config = get_config()
    TOKEN = config.get('TOKEN')
    CHAT_ID = config.get('CHAT_ID')

    entries = get_history()

    # 1. Mode Hapus ID Spesifik (via argumen)
    if args.id:
        if delete_message(TOKEN, CHAT_ID, args.id):
            # Hapus dari history lokal
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
            # Coba hapus
            if not delete_message(TOKEN, CHAT_ID, entry['id']):
                # Jika gagal, simpan kembali (kecuali error not found)
                active_entries.append(entry)
        
        save_history(active_entries)
        if not active_entries:
            print("✅ Semua riwayat bersih.")
        return

    # 3. Mode Interaktif (Default / Seamless)
    if not entries:
        print("ℹ️  Belum ada riwayat pengiriman pesan.")
        return

    show_list(entries)
    
    print("\n💡 Ketik ID pesan untuk menghapus, atau 'all' untuk hapus semua.")
    choice = input("👉 Pilihan (Enter untuk batal): ").strip()

    if not choice:
        print("Selesai.")
        return

    if choice.lower() == 'all':
        # Re-run logic delete all
        os.system(f"{sys.argv[0]} --all")
    else:
        # Asumsikan input adalah ID
        # Cek apakah ID ada di list (opsional, tapi bagus untuk validasi)
        target = next((e for e in entries if str(e['id']) == choice), None)
        
        if delete_message(TOKEN, CHAT_ID, choice):
            # Hapus dari history lokal
            new_entries = [e for e in entries if str(e['id']) != choice]
            save_history(new_entries)
        elif not target:
            # Jika user memasukkan ID yang tidak ada di list lokal tapi ingin coba hapus
             delete_message(TOKEN, CHAT_ID, choice)

if __name__ == "__main__":
    main()