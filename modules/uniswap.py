#!/data/data/com.termux/files/usr/bin/python3
import os
import time
import random
from dotenv import load_dotenv

# Ensure paths work in Termux
HOME = os.getenv('HOME', '/data/data/com.termux/files/home')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
from web3 import Web3
from colorama import init, Fore, Style

# Inisialisasi colorama dan load .env
init(autoreset=True)
load_dotenv()

def display_header():
    print(Style.BRIGHT + Fore.CYAN + "======================================")
    print(Style.BRIGHT + Fore.CYAN + "            UNISWAP Bot               ")
    print(Style.BRIGHT + Fore.CYAN + "====================================\n")

display_header()

# Baca PRIVATE_KEY dari .env
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise Exception("No PRIVATE_KEY in .env")

RPC_URLS = ["https://testnet-rpc.monad.xyz"]
CHAIN_ID = 10143
UNISWAP_V2_ROUTER_ADDRESS = Web3.to_checksum_address("0xCa810D095e90Daae6e867c19DF6D9A8C56db2c89")
WETH_ADDRESS = Web3.to_checksum_address("0x760AfE86e5de5fa0Ee542fc7B7B713e1c5425701")

TOKEN_ADDRESSES = {
    "DAC": Web3.to_checksum_address("0x0f0bdebf0f83cd1ee3974779bcb7315f9808c714"),
    "USDT": Web3.to_checksum_address("0x88b8e2161dedc77ef4ab7585569d2415a1c1055d"),
    "WETH": Web3.to_checksum_address("0x836047a99e11f376522b447bffb6e3495dd0637c"),
    "MUK": Web3.to_checksum_address("0x989d38aeed8408452f0273c7d4a17fef20878e62"),
    "USDC": Web3.to_checksum_address("0xf817257fed379853cDe0fa4F97AB987181B1E5Ea"),
    "CHOG": Web3.to_checksum_address("0xE0590015A873bF326bd645c3E1266d4db41C4E6B")
}

erc20Abi = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}],
     "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": False, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}],
     "name": "approve", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
]

routerAbi = [
    {
        "name": "swapExactETHForTokens",
        "type": "function",
        "stateMutability": "payable",
        "inputs": [
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}]
    },
    {
        "name": "swapExactTokensForETH",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}]
    }
]

def connect_to_rpc():
    for url in RPC_URLS:
        provider = Web3(Web3.HTTPProvider(url))
        if provider.is_connected():
            print(Fore.BLUE + ">>> Connected to RPC <<<")
            return provider
        print(Fore.RED + f"Failed to connect to {url}")
    raise Exception("Unable to connect to any RPC")

w3 = connect_to_rpc()
wallet = w3.eth.account.from_key(PRIVATE_KEY)
print(Fore.GREEN + f">>> Account: {wallet.address}")

def get_balance():
    balance = w3.eth.get_balance(wallet.address)
    print(Fore.GREEN + f">>> ETH: {w3.from_wei(balance, 'ether'):.6f}")
    weth_contract = w3.eth.contract(address=WETH_ADDRESS, abi=erc20Abi)
    weth_balance = weth_contract.functions.balanceOf(wallet.address).call()
    print(Fore.GREEN + f">>> WETH: {w3.from_wei(weth_balance, 'ether'):.6f}\n")

def approve_token_once(tokenAddress):
    token_contract = w3.eth.contract(address=tokenAddress, abi=erc20Abi)
    allowance = token_contract.functions.balanceOf(wallet.address).call()
    if allowance > 0:
        approve_tx = token_contract.functions.approve(UNISWAP_V2_ROUTER_ADDRESS, 2**256-1).build_transaction({
            'from': wallet.address,
            'nonce': w3.eth.get_transaction_count(wallet.address),
            'gasPrice': w3.eth.gas_price
        })
        signed = wallet.sign_transaction(approve_tx)
        w3.eth.send_raw_transaction(signed.rawTransaction)
        print(Fore.YELLOW + f"+++ Approved {tokenAddress}")

def swap_eth_to_token(tokenSymbol, slippage=0.03):
    try:
        amountIn = w3.to_wei(random.uniform(0.01, 0.05), 'ether')
        router = w3.eth.contract(address=UNISWAP_V2_ROUTER_ADDRESS, abi=routerAbi)
        path = [WETH_ADDRESS, TOKEN_ADDRESSES[tokenSymbol]]

        # Slippage protection (amountOutMin = 97% dari estimate)
        amounts = router.functions.swapExactETHForTokens(0, path, wallet.address, int(time.time()+1200)).call({'from': wallet.address, 'value': amountIn})
        amountOutMin = int(amounts[1] * (1 - slippage))

        tx = router.functions.swapExactETHForTokens(
            amountOutMin,
            path,
            wallet.address,
            int(time.time()+1200)
        ).build_transaction({
            'from': wallet.address,
            'value': amountIn,
            'nonce': w3.eth.get_transaction_count(wallet.address),
            'gas': w3.eth.estimate_gas({'from': wallet.address, 'to': UNISWAP_V2_ROUTER_ADDRESS, 'value': amountIn}),
            'gasPrice': w3.eth.gas_price
        })

        signed = wallet.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        print(Fore.YELLOW + f">>> Swap ETH > {tokenSymbol} Hash: {tx_hash.hex()}")
    except Exception as e:
        print(Fore.RED + f"xxx Swap ETH > {tokenSymbol} Failed: {e}")

def swap_token_to_eth(tokenSymbol, slippage=0.03):
    tokenAddress = TOKEN_ADDRESSES[tokenSymbol]
    token_contract = w3.eth.contract(address=tokenAddress, abi=erc20Abi)
    balance = token_contract.functions.balanceOf(wallet.address).call()
    if balance == 0:
        print(Fore.BLACK + f"xxx No {tokenSymbol} balance, skip")
        return

    approve_token_once(tokenAddress)
    router = w3.eth.contract(address=UNISWAP_V2_ROUTER_ADDRESS, abi=routerAbi)
    try:
        # Slippage protection
        amounts = router.functions.swapExactTokensForETH(balance, 0, [tokenAddress, WETH_ADDRESS], wallet.address, int(time.time()+1200)).call({'from': wallet.address})
        amountOutMin = int(amounts[1] * (1 - slippage))

        tx = router.functions.swapExactTokensForETH(
            balance,
            amountOutMin,
            [tokenAddress, WETH_ADDRESS],
            wallet.address,
            int(time.time()+1200)
        ).build_transaction({
            'from': wallet.address,
            'nonce': w3.eth.get_transaction_count(wallet.address),
            'gas': w3.eth.estimate_gas({'from': wallet.address, 'to': UNISWAP_V2_ROUTER_ADDRESS, 'value': 0}),
            'gasPrice': w3.eth.gas_price
        })

        signed = wallet.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        print(Fore.YELLOW + f">>> Swap {tokenSymbol} > ETH Hash: {tx_hash.hex()}")
    except Exception as e:
        print(Fore.RED + f"xxx Swap {tokenSymbol} > ETH Failed: {e}")

def main():
    get_balance()
    for token in TOKEN_ADDRESSES.keys():
        swap_eth_to_token(token)
        time.sleep(random.uniform(1, 3))
    print(Fore.WHITE + "\n>>> Swapping all tokens back to ETH...\n")
    for token in TOKEN_ADDRESSES.keys():
        swap_token_to_eth(token)
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(Fore.RED + f"xxx Error: {e}")
