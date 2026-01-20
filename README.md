# Telesend 🚀

**Telesend** adalah kumpulan alat CLI (Command Line Interface) cerdas dan efisien untuk manajemen file antara Laptop/PC (Linux) dan Telegram.

Project ini terdiri dari tiga alat utama:
1. **`kirimtele`**: Script Bash hybrid (Bash + Python) untuk mengirim file atau pesan teks. Mendukung **Drag & Drop** dan pengiriman massal (bulk).
2. **`terimatele`**: Script Python pintar untuk menerima file dari Telegram secara otomatis (Live Mode).
3. **`hapustele`**: Script Python interaktif untuk mengelola dan menghapus pesan/file yang telah dikirim.

## ✨ Fitur Unggulan

### 📤 Kirimtele
*   **Drag & Drop Support**: Cukup drag file (satu atau banyak) ke terminal untuk mengirim.
*   **Bulk Sender**: Kirim banyak file sekaligus dalam satu perintah.
*   **Smart Parsing**: Mendukung input campuran (File + Caption) saat drag & drop.
*   **Text & Files**: Bisa mengirim file dokumen, foto, video, atau hanya sekadar pesan teks.
*   **Progress Bar**: Visualisasi proses upload.

### 📥 Terimatele
*   **Live Receiver**: Hanya mendownload file yang masuk *setelah* script dijalankan (bebas spam file lama).
*   **Auto Filter**: Hanya menerima file dari Chat ID terdaftar (aman dari orang asing).
*   **Support Berbagai Tipe**: Dokumen, Foto, dan Video.

### 🗑️ Hapustele
*   **Interactive Menu**: Tampilan riwayat pesan yang user-friendly.
*   **Bulk Delete**: Hapus banyak pesan sekaligus (pisahkan ID dengan spasi).
*   **Smart History**: Mencatat riwayat pengiriman lokal untuk memudahkan penghapusan tanpa mencari Message ID manual.

## 🛠️ Prasyarat

*   OS: Linux / macOS (dengan Bash)
*   `curl` (untuk kirimtele)
*   `python3` (untuk parsing, terimatele & hapustele)
*   Library Python `requests`:
    ```bash
    pip install requests
    ```

## 📦 Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/4rmanjr/telesend.git
   cd telesend
   ```

2. **Jadikan Global Command (Disarankan)**
   Agar bisa dipanggil dari mana saja:

   ```bash
   mkdir -p ~/.local/bin
   ln -sf "$(pwd)/kirimtele" ~/.local/bin/kirimtele
   ln -sf "$(pwd)/terimatele.py" ~/.local/bin/terimatele
   ln -sf "$(pwd)/hapustele.py" ~/.local/bin/hapustele
   chmod +x kirimtele terimatele.py hapustele.py
   ```
   *(Pastikan `~/.local/bin` ada di PATH Anda)*

## ⚙️ Konfigurasi

Saat pertama kali menjalankan `kirimtele`, script akan memandu Anda mengisi:
1.  **Bot Token**: Dari [@BotFather](https://t.me/BotFather).
2.  **Chat ID**: Dari [@userinfobot](https://t.me/userinfobot).

Konfigurasi disimpan di file `config` di dalam direktori instalasi script.

## 🚀 Cara Penggunaan

### 1. Mengirim File / Pesan (`kirimtele`)

**Mode Interaktif (Paling Mudah):**
Ketik `kirimtele` tanpa argumen, lalu **Drag & Drop** file ke terminal.
```bash
kirimtele
# Output:
# 💡 Tips: Anda bisa Drag & Drop file ke terminal sekarang.
# 📂 Masukkan path file (atau ketik pesan): /home/user/file1.pdf /home/user/file2.pdf Ini captionnya
```
*Script otomatis mendeteksi mana yang file dan mana yang teks/caption.*

**Mode Manual (CLI Arguments):**
```bash
# Kirim satu file
kirimtele dokumen.pdf

# Kirim file dengan caption
kirimtele foto.jpg "Liburan kemarin"

# Kirim pesan teks saja
kirimtele "Halo, ini pesan dari terminal"
```

### 2. Menerima File (`terimatele`)
```bash
terimatele
```
*   Script akan *standby*.
*   Kirim file ke bot Telegram Anda.
*   File otomatis terdownload ke folder terminal yang sedang aktif.

### 3. Menghapus Pesan (`hapustele`)
Tarik pesan salah kirim atau bersihkan chat.

**Mode Interaktif:**
```bash
hapustele
```
Akan muncul daftar riwayat. Anda bisa:
*   Ketik satu ID: `1234`
*   Ketik banyak ID: `1234 1235 1236`
*   Ketik `all` untuk hapus semua.

**Mode Cepat (CLI):**
```bash
hapustele --id 12345        # Hapus satu pesan
hapustele --all             # Hapus SEMUA riwayat lokal & remote
```

## 🔄 Reset / Uninstall
Untuk mereset konfigurasi (ganti bot):
```bash
kirimtele --reset
```

## 🛡️ Keamanan
*   Token disimpan lokal di folder script.
*   `terimatele` memvalidasi `Chat ID` pengirim, sehingga orang lain tidak bisa mengirim file ke komputer Anda melalui bot ini.

---
*Dibuat dengan ❤️ dan Python/Bash.*
