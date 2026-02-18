#!/bin/bash

# Dapatkan path absolute dari direktori script ini
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BIN_DIR="/usr/local/bin"

echo "Memasang script telesend ke $BIN_DIR..."

# Daftar script yang akan di-link
scripts=("hapustele.py" "kirimtele" "terimatele.py")

for script in "${scripts[@]}"; do
    if [ -f "$SOURCE_DIR/$script" ]; then
        # Tentukan nama command (hapus ekstensi .py jika ada)
        cmd_name=$(basename "$script" .py)
        
        echo "Menghubungkan $script sebagai $cmd_name..."
        
        # Pastikan file bisa dieksekusi
        chmod +x "$SOURCE_DIR/$script"
        
        # Buat symlink menggunakan sudo
        sudo ln -sf "$SOURCE_DIR/$script" "$BIN_DIR/$cmd_name"
        
        if [ $? -eq 0 ]; then
            echo "✅ Berhasil: $cmd_name sekarang bisa dipanggil dari mana saja."
        else
            echo "❌ Gagal: Gagal membuat symlink untuk $cmd_name."
        fi
    else
        echo "⚠️ Peringatan: $script tidak ditemukan di $SOURCE_DIR"
    fi
done

echo "--------------------------------------------------"
echo "Instalasi selesai. Anda sekarang bisa menggunakan perintah:"
echo " - kirimtele"
echo " - hapustele"
echo " - terimatele"
