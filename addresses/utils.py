import base58
import secrets
import sr25519
from web3 import Web3

from bitcoin import *
from random import randbytes
from eth_account import Account


def generate_btc_address():
    try:
        # create private key
        btc_private_key = random_key()

        # create public key
        btc_public_key = privtopub(btc_private_key)

        # create BTC address
        btc_address = pubtoaddr(btc_public_key)

        # validate address
        base58Decoder = base58.b58decode(btc_address).hex()
        prefixAndHash = base58Decoder[:len(base58Decoder) - 8]
        checksum = base58Decoder[len(base58Decoder) - 8:]
        hash = prefixAndHash
        for x in range(1, 3):
            hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
        if checksum != hash[:8]:
            return f"{btc_address} is not valid!"

        return btc_address

    except Exception as e:
        return e


def generate_eth_address():
    try:
        # create private key
        priv = secrets.token_hex(32)
        eth_private_key = f'0x{priv}'

        # create account
        eth_account = Account.from_key(eth_private_key)

        # create ETH address
        eth_address = eth_account.address

        # validate address
        if not Web3.is_address(eth_address):
            return f"{eth_address} is not valid!"

        return eth_address

    except Exception as e:
        return e


def generate_dot_address():
    try:
        message = b"test"
        raw_seed = randbytes(32)
        public_key, private_key = sr25519.pair_from_seed(raw_seed)

        # Generate signature
        signature = sr25519.sign((public_key, private_key), message)
        dot_address = signature.hex()

        # Verify message with signature
        if not sr25519.verify(signature, message, public_key):
            f"{dot_address} is not valid!"

        return dot_address

    except Exception as e:
        return e

