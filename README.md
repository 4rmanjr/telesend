# Telesend 🚀

**Telesend** adalah kumpulan alat CLI (Command Line Interface) sederhana namun powerful untuk mengirim dan menerima file antara Laptop/PC (Linux) dan Telegram.

Project ini terdiri dari tiga alat utama:
1. **`kirimtele`**: Script Bash ringan untuk mengirim file ke Telegram dengan progress bar.
2. **`terimatele`**: Script Python cerdas untuk menerima file dari Telegram secara otomatis (Live Mode).
3. **`hapustele`**: Script Python interaktif untuk menghapus pesan/file yang telah dikirim oleh bot.

## ✨ Fitur

*   **Tanpa Login Rumit**: Hanya butuh Bot Token & Chat ID.
*   **Progress Bar**: Tampilan visual saat mengupload file besar.
*   **Live Receiver**: `terimatele` hanya mendownload file yang masuk *setelah* script dijalankan.
*   **Message Deletion**: Hapus pesan tertentu atau semua pesan yang dikirim bot dengan sistem riwayat terintegrasi.
*   **Smart History**: `hapustele` mencatat nama file, waktu, dan Chat ID untuk memudahkan pengelolaan pesan.
*   **Global Access**: Bisa dipanggil dari folder mana saja di terminal.

## 🛠️ Prasyarat

*   OS: Linux / macOS (dengan Bash)
*   `curl` (untuk kirimtele)
*   `python3` (untuk terimatele & hapustele)
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
   Pilih salah satu metode di bawah ini agar bisa dipanggil langsung dari terminal:

   **Metode A (User Local - Tanpa Sudo):**
   ```bash
   mkdir -p ~/.local/bin
   ln -sf "$(pwd)/kirimtele" ~/.local/bin/kirimtele
   ln -sf "$(pwd)/terimatele.py" ~/.local/bin/terimatele
   ln -sf "$(pwd)/hapustele.py" ~/.local/bin/hapustele
   chmod +x kirimtele terimatele.py hapustele.py
   ```

   **Metode B (Sistem - Butuh Sudo):**
   ```bash
   sudo ln -sf "$(pwd)/kirimtele" /usr/local/bin/kirimtele
   sudo ln -sf "$(pwd)/terimatele.py" /usr/local/bin/terimatele
   sudo ln -sf "$(pwd)/hapustele.py" /usr/local/bin/hapustele
   ```

## ⚙️ Konfigurasi Awal

Saat pertama kali Anda menjalankan `kirimtele`, script akan meminta:
1.  **Bot Token**: Buat bot baru di [@BotFather](https://t.me/BotFather) (`/newbot`).
2.  **Chat ID**: Cek di [@userinfobot](https://t.me/userinfobot) atau undang bot ke grup Anda.

Data ini disimpan di `~/.telechat_rc`.

## 🚀 Penggunaan

### 1. Mengirim File (`kirimtele`)
```bash
kirimtele dokumen.pdf
kirimtele foto.jpg "Caption foto"
```

### 2. Menerima File (`terimatele`)
```bash
terimatele
```
File yang dikirim ke bot akan otomatis terdownload ke folder aktif Anda.

### 3. Menghapus Pesan (`hapustele`)
Fitur ini sangat berguna untuk menarik kembali file yang salah kirim atau membersihkan history chat.

*   **Mode Interaktif (Seamless):**
    Cukup ketik `hapustele`, maka daftar pesan terakhir akan muncul. Ketik ID-nya untuk menghapus.
    ```bash
    hapustele
    ```

*   **Hapus Semua:**
    Menghapus semua pesan yang tercatat di riwayat lokal.
    ```bash
    hapustele --all
    ```

*   **Hapus ID Spesifik:**
    ```bash
    hapustele --id 12345
    ```

## 🔄 Reset Konfigurasi
Jika ingin mengganti bot atau Chat ID:
```bash
kirimtele --reset
```

## 🛡️ Privasi & Keamanan
*   Token & Chat ID disimpan lokal di komputer Anda.
*   `terimatele` memfilter pengirim, hanya Chat ID yang terdaftar yang bisa mengirim file ke laptop Anda.

---
*Dibuat dengan ❤️ dan Python/Bash.*