import requests
import os
from nostr_sdk import Keys, Client, EventBuilder
from nostr_sdk.bech32 import decode_bech32

# 🔐 Read nsec key from GitHub Secrets
NSEC = os.environ["NOSTR_PRIVATE_KEY"]

RELAY = "wss://relay.damus.io"

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    return requests.get(url).json()["bitcoin"]["usd"]

def main():
    price = get_btc_price()
    content = f"₿ Bitcoin price: ${price} USD\n⏰ Automatic hourly update"

    # 🔑 Convert nsec → hex
    prefix, hex_key = decode_bech32(NSEC)
    keys = Keys.from_sk_hex(hex_key)

    client = Client(keys)
    client.add_relay(RELAY)
    client.connect()

    event = EventBuilder.text_note(content).to_event(keys)
    client.send_event(event)

    client.disconnect()

main()
