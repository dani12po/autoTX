#!/usr/bin/env python3
import os
import sys
import time
import random
from dotenv import load_dotenv
from web3 import Web3
from colorama import init, Fore

init(autoreset=True)

def displayHeader():
    print(Fore.BLUE + "====================")
    print(Fore.BLUE + "   MONORAIL Bot     ")
    print(Fore.BLUE + "====================")

load_dotenv()
displayHeader()

RPC_URL = "https://testnet-rpc.monad.xyz"
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Minimal ABI that includes only the function we call (swapExactETHForTokens)
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactETHForTokens",
        "outputs": [
            {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
        ],
        "stateMutability": "payable",
        "type": "function"
    }
]

# Alamat sudah diformat checksum
CONTRACT_ADDRESS = w3.to_checksum_address("0xC995498c22a012353FAE7eCC701810D673E25794")
WETH_ADDRESS = w3.to_checksum_address("0x760aFe86E5DE5fA0Ee542Fc7b7b713E1C5425701")
TOKEN_OUT_ADDRESS = w3.to_checksum_address("0xCba6b9a951749B8735C603e7fFc5151849248772")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    print(Fore.RED + "xxx Private key tidak ditemukan! Set dalam .env file.")
    sys.exit(1)

account = w3.eth.account.from_key(PRIVATE_KEY)

print(Fore.BLUE + ">>> Starting Monorail >>>>\n")
print(Fore.GREEN + f"+++ Wallet initialized: {account.address}")

def checkBalance():
    balance = w3.eth.get_balance(account.address)
    print(Fore.CYAN + f">>> Balance: {w3.from_wei(balance, 'ether')} ETH")
    if balance < w3.to_wei(0.1, 'ether'):
        print(Fore.RED + "xxx Saldo tidak cukup untuk transaksi.")
        return False
    return True

def sendTransaction(max_retries=3, min_delay=10, max_delay=30):
    if not checkBalance():
        return

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    fn_call = contract.functions.swapExactETHForTokens(
        0,
        [WETH_ADDRESS, TOKEN_OUT_ADDRESS],
        account.address,
        int(time.time()) + 600
    )
    data = fn_call._encode_transaction_data()
    value = w3.to_wei(0.1, 'ether')

    for attempt in range(1, max_retries + 1):
        try:
            print(Fore.YELLOW + f">>> Simulasi transaksi (eth_call)... [Percobaan {attempt}]")
            w3.eth.call({
                'from': account.address,
                'to': CONTRACT_ADDRESS,
                'value': value,
                'data': data
            })
            print(Fore.GREEN + "+++ Transaksi valid. Melanjutkan...")

            try:
                gasLimit = w3.eth.estimate_gas({
                    'from': account.address,
                    'to': CONTRACT_ADDRESS,
                    'value': value,
                    'data': data
                })
            except Exception:
                print(Fore.YELLOW + "!!! Estimasi gas gagal. Menggunakan gas limit default.")
                gasLimit = 500000

            tx = {
                'from': account.address,
                'to': CONTRACT_ADDRESS,
                'data': data,
                'value': value,
                'gas': gasLimit,
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(account.address),
                'chainId': w3.eth.chain_id,
            }

            print(Fore.BLUE + ">>> Mengirim transaksi...")
            signed_tx = account.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            print(Fore.GREEN + "+++ Transaksi dikirim! Menunggu konfirmasi...")
            w3.eth.wait_for_transaction_receipt(tx_hash)
            print(Fore.GREEN + "+++ Transaksi sukses!")
            print(Fore.CYAN + f">>> Explorer: {EXPLORER_URL}{tx_hash.hex()}")

            # Tambahkan delay random sebelum lanjut transaksi berikutnya
            delay = random.randint(min_delay, max_delay)
            print(Fore.LIGHTBLACK_EX + f"... Menunggu {delay} detik sebelum transaksi berikutnya")
            time.sleep(delay)
            return  # sukses → keluar loop

        except Exception as error:
            error_msg = str(error)
            if "insufficient liquidity" in error_msg.lower():
                print(Fore.RED + "xxx Gagal: Likuiditas tidak cukup. Coba ulang nanti.")
                break
            elif "slippage" in error_msg.lower():
                print(Fore.RED + "xxx Gagal: Slippage terlalu kecil. Sesuaikan parameter.")
                break
            else:
                print(Fore.RED + f"xxx Error transaksi: {error_msg}")
                if attempt < max_retries:
                    wait_time = 5
                    print(Fore.YELLOW + f"!!! Retry dalam {wait_time} detik...")
                    time.sleep(wait_time)
                else:
                    print(Fore.RED + "xxx Gagal setelah semua percobaan.")
                    break

if __name__ == '__main__':
    sendTransaction()
