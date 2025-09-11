#!/data/data/com.termux/files/usr/bin/python3
import os
import sys
import time
import random
import json
import subprocess
import shutil
import tempfile
from dotenv import load_dotenv

# Ensure paths work in Termux
HOME = os.getenv('HOME', '/data/data/com.termux/files/home')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
from web3 import Web3
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = "https://testnet-rpc.monad.xyz"

if not PRIVATE_KEY or not RPC_URL:
    print(Fore.RED + "xxx Missing environment variables!")
    sys.exit(1)

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# ======================================
# Nama kontrak random generator
# ======================================
chemical_terms = ["Atom","Molecule","Electron","Proton","Neutron","Ion","Isotope","Reaction","Catalyst","Solution"]
planets = ["Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune"]

def generate_random_name():
    combined_terms = chemical_terms + planets
    random.shuffle(combined_terms)
    return "".join(combined_terms[:3])

# ======================================
# Smart contract source
# ======================================
contract_source = '''
pragma solidity ^0.8.19;

contract Counter {
    uint256 private count;
    
    event CountIncremented(uint256 newCount);
    
    function increment() public {
        count += 1;
        emit CountIncremented(count);
    }
    
    function getCount() public view returns (uint256) {
        return count;
    }
}
'''

# ======================================
# Compile contract
# ======================================
def compile_contract():
    print("Compiling contract...")
    try:
        import solcx
        solcx.install_solc('0.8.19')
        solcx.set_solc_version('0.8.19')

        compiled = solcx.compile_source(
            contract_source,
            output_values=['abi','bin'],
            optimize=True
        )
        contract_id, contract_interface = next(iter(compiled.items()))
        abi = contract_interface['abi']
        bytecode = contract_interface['bin']
        print(Fore.GREEN + "Contract compiled successfully!")
        return abi, bytecode

    except ImportError:
        solc_path = shutil.which("solc")
        if not solc_path:
            print(Fore.RED + "Solc not found. Install with: pip install py-solc-x")
            sys.exit(1)
        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, "Counter.sol")
            with open(src_path, "w") as f:
                f.write(contract_source)
            cmd = [solc_path, "--optimize", "--combined-json", "abi,bin", src_path]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
            combined = json.loads(proc.stdout)
            contract_key = next(iter(combined['contracts']))
            contract_data = combined['contracts'][contract_key]
            abi = json.loads(contract_data['abi'])
            bytecode = contract_data['bin']
            return abi, bytecode

# ======================================
# Deploy contract
# ======================================
def deploy_contract(contract_name):
    abi, bytecode = compile_contract()
    print(Fore.BLUE + f"Deploying contract {contract_name}...")
    try:
        nonce = w3.eth.get_transaction_count(account.address)
        Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = Contract.constructor().build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 3_000_000,
            'gasPrice': w3.eth.gas_price,
            'chainId': w3.eth.chain_id
        })
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status != 1:
            print(Fore.RED + "Deployment failed!")
        else:
            print(Fore.GREEN + f"Contract {contract_name} deployed successfully!")
            print(Fore.CYAN + f"Address: {receipt.contractAddress}")
            print(Fore.CYAN + f"Tx Hash: {tx_hash.hex()}")
    except Exception as e:
        print(Fore.RED + f"Deployment error: {str(e)}")

# ======================================
# Main
# ======================================
def main():
    print(Fore.BLUE + ">>> Starting Deploy Contract >>>")
    number_of_contracts = 5
    for i in range(number_of_contracts):
        name = generate_random_name()
        print(Fore.YELLOW + f"\n>>> Deploying contract {i+1}/{number_of_contracts}: {name}")
        deploy_contract(name)
        delay = random.uniform(4, 6)
        print(Fore.LIGHTBLACK_EX + f"... Waiting {delay:.2f} seconds")
        time.sleep(delay)
    print(Fore.GREEN + Style.BRIGHT + "\n+++ All contracts processed +++")

if __name__ == "__main__":
    main()
