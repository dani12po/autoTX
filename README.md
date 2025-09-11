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

## 💡 CATATAN TENTANG `sudo`

* `sudo` hanya diperlukan di Linux jika Anda menginstall paket secara global.
* Jika menggunakan **virtual environment**, Anda **tidak perlu sudo** karena semua paket akan terinstall di folder `venv` lokal proyek.
* Windows dan Termux **tidak menggunakan sudo** sama sekali.

---

## 🚀 TUTORIAL INSTALASI PER PLATFORM

### 1️⃣ Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git -y
pkg install python-pip -y
pkg install nano -y
```

* Clone repository:

```bash
git clone https://github.com/dani12po/autoTX.git
cd autoTX
```

* Buat file `.env` dan tambahkan Private Key:

```
PRIVATE_KEY=0xYourPrivateKeyHere
```

* Buat virtual environment dan install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install web3 python-dotenv colorama
```

* Jalankan bot:

```bash
python bot.py
```

### 2️⃣ Linux

```bash
# Install Git dan Python3 (opsional jika pakai global)
sudo apt update
sudo apt install git python3 python3-pip python3-venv -y
```

* Clone repository:

```bash
git clone https://github.com/dani12po/autoTX.git
cd autoTX
```

* Buat file `.env` dan tambahkan Private Key:

```
PRIVATE_KEY=0xYourPrivateKeyHere
```

* Buat virtual environment dan install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install web3 python-dotenv colorama
```

* Jalankan bot:

```bash
python3 bot.py
```

### 3️⃣ Windows

* Install Git dari [git-scm.com](https://git-scm.com/)
* Install Python dari [python.org](https://www.python.org/downloads/) (centang **Add Python to PATH**)
* Clone repository:

```cmd
git clone https://github.com/dani12po/autoTX.git
cd autoTX
```

* Buat file `.env` dan tambahkan Private Key:

```
PRIVATE_KEY=0xYourPrivateKeyHere
```

* Buat virtual environment dan install dependencies:

```cmd
python -m venv venv
venv\Scripts\activate
pip install web3 python-dotenv colorama
```

* Jalankan bot:

```cmd
python bot.py
```

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
