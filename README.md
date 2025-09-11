# MONAD AUTO TX BOT

## JOIN COMMUNITY

[Telegram Channel: DANI XYZ](https://t.me/YaapGitHUB)

---

## ⚠️ PENTING: KEAMANAN PRIVATE KEY

Bot ini menggunakan **Private Key wallet** Anda.
**\[!] Jangan pernah membagikan key ini ke orang lain.**
Simpan di file `.env` yang aman.

---

## 🌐 Situs Referensi Wallet / Trading

Sebelum menjalankan bot, pastikan wallet Anda siap:

* [APR Stake](https://stake.apr.io/)
* [Bean Swap](https://swap.bean.exchange/)
* [Bebop Trade](https://bebop.xyz/trade)
* [Alpha Izumi Swap](https://alpha.izumi.finance/trade/swap)
* [Kintsu Staking](https://kintsu.xyz/staking)
* [Magma Staking](https://www.magmastaking.xyz/)
* [Monorail](https://monorail.xyz/)
* [Testnet Rubic Exchange](https://testnet.rubic.exchange/)

---

## ✅ PRASYARAT

* Python 3.10+
* Git
* Akses internet & RPC Node blockchain

---

## 📦 DAFTAR DEPENDENCIES

| Package         | Fungsi                                  |
| --------------- | --------------------------------------- |
| `web3`          | Koneksi blockchain & transaksi Ethereum |
| `python-dotenv` | Membaca file `.env` (PRIVATE\_KEY, RPC) |
| `colorama`      | Warna dan formatting di console         |

> Semua dependency dapat diinstall via `pip`.

---

## 🚀 TUTORIAL INSTALASI LENGKAP

### 1️⃣ Install Git

**Linux:**

```bash
sudo apt update
sudo apt install git -y
```

**Windows:**
Download dan install Git dari [git-scm.com](https://git-scm.com/).

---

### 2️⃣ Install Python 3 dan pip

**Linux:**

```bash
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install python3-venv -y
```

**Windows:**
Download Python 3 dari [python.org](https://www.python.org/downloads/) dan centang opsi **Add Python to PATH** saat install.

---

### 3️⃣ Clone Repository

```bash
git clone https://github.com/dani12po/autoTX.git
cd autoTX
```

---

### 4️⃣ Buat File `.env`

Buat file `.env` di folder `autoTX` dan tambahkan Private Key Anda:

```
PRIVATE_KEY=0xYourPrivateKeyHere
```

> \[!] Jangan commit `.env` ke GitHub atau bagikan ke orang lain.

---

### 5️⃣ Buat Virtual Environment & Install Dependencies

**Linux / Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install web3 python-dotenv colorama
```

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
pip install web3 python-dotenv colorama
```

> Virtual environment mencegah konflik paket Python dengan sistem global.

---

### 6️⃣ Jalankan Bot

**Linux / Mac:**

```bash
python3 bot.py
```

**Windows:**

```cmd
python bot.py
```

Bot akan mulai otomatis melakukan transaksi sesuai konfigurasi.

---

## 📝 CATATAN PENGGUNAAN

* Pastikan saldo wallet mencukupi.
* Gunakan RPC yang stabil agar transaksi tidak gagal.
* Delay acak dan jumlah transaksi dapat diatur di skrip untuk keamanan.
* Gunakan console yang mendukung UTF-8 agar warna muncul dengan benar.
* Pantau log bot untuk memastikan transaksi berjalan lancar.

---

## 🔧 SUPPORT

Jika mengalami error atau butuh bantuan:
Gabung ke [Telegram Channel DANI XYZ](https://t.me/YaapGitHUB)
