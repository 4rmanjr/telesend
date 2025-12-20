# Telesend 🚀

**Telesend** adalah kumpulan alat CLI (Command Line Interface) sederhana namun powerful untuk mengirim dan menerima file antara Laptop/PC (Linux) dan Telegram.

Project ini terdiri dari dua alat utama:
1. **`kirimtele`**: Script Bash ringan untuk mengirim file ke Telegram dengan progress bar.
2. **`terimatele`**: Script Python cerdas untuk menerima file dari Telegram secara otomatis (Live Mode).

## ✨ Fitur

*   **Tanpa Login Rumit**: Hanya butuh Bot Token & Chat ID.
*   **Progress Bar**: Tampilan visual saat mengupload file besar.
*   **Live Receiver**: `terimatele` hanya mendownload file yang masuk *setelah* script dijalankan (tidak mendownload history lama).
*   **Aman**: Memiliki filter keamanan (hanya menerima file dari Chat ID pemilik/grup yang terdaftar).
*   **Global Access**: Bisa dipanggil dari folder mana saja di terminal.

## 🛠️ Prasyarat

*   OS: Linux / macOS (dengan Bash)
*   `curl` (untuk kirimtele)
*   `python3` (untuk terimatele)
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

2. **Jadikan Global Command (Opsional tapi Disarankan)**
   Agar bisa dipanggil dari mana saja tanpa mengetik path lengkap.

   ```bash
   # Beri izin eksekusi
   chmod +x kirimtele terimatele.py

   # Buat symbolic link (butuh akses sudo)
   sudo ln -sf "$(pwd)/kirimtele" /usr/local/bin/kirimtele
   sudo ln -sf "$(pwd)/terimatele.py" /usr/local/bin/terimatele
   ```

## ⚙️ Konfigurasi Awal

Saat pertama kali Anda menjalankan `kirimtele`, script akan meminta:
1.  **Bot Token**: Buat bot baru di [@BotFather](https://t.me/BotFather) (`/newbot`).
2.  **Chat ID**:
    *   Untuk **Pribadi**: Cek di [@userinfobot](https://t.me/userinfobot).
    *   Untuk **Grup**: Undang bot ke grup, cek ID grup (biasanya diawali `-100...`).

Data ini akan disimpan secara aman di `~/.telechat_rc`.

## 🚀 Penggunaan

### 1. Mengirim File (`kirimtele`)
Kirim file apa saja dari terminal ke Telegram Anda.

```bash
# Format: kirimtele <nama_file> [caption]
kirimtele dokumen.pdf
kirimtele foto_liburan.jpg "Ini foto liburan kemarin"
```

### 2. Menerima File (`terimatele`)
Jadikan laptop Anda server penerima file.

```bash
# Jalankan perintah ini, lalu kirim file ke Bot Telegram Anda
terimatele
```
*   Script akan masuk ke mode **Live Listening**.
*   File yang Anda kirim ke bot akan otomatis terdownload ke folder terminal yang sedang aktif.
*   Tekan `Ctrl + C` untuk berhenti.

## 🔄 Reset Konfigurasi
Jika Anda ingin mengganti akun bot atau tujuan pengiriman:

```bash
kirimtele --reset
```

## 🛡️ Privasi
*   Token dan Chat ID disimpan lokal di komputer Anda (`~/.telechat_rc`).
*   Script `terimatele` memfilter pesan berdasarkan Chat ID, sehingga orang asing tidak bisa sembarangan mengirim file ke laptop Anda melalui bot tersebut.

---
*Dibuat dengan ❤️ dan Bash.*
