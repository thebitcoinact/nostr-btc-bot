import requests
import os
from nostr_sdk import Keys, Client, EventBuilder

RELAY = "wss://relay.damus.io"

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    return requests.get(url).json()["bitcoin"]["usd"]

def main():
    nsec = os.getenv("NOSTR_PRIVATE_KEY")

    if not nsec:
        raise Exception("NOSTR_PRIVATE_KEY secret is missing")

    content = f"₿ Bitcoin price: ${get_btc_price()} USD\n⏰ Automatic hourly update"

    # ✅ Correct way
    keys = Keys.parse(nsec)

    client = Client(keys)
    client.add_relay(RELAY)
    client.connect()

    event = EventBuilder.text_note(content).to_event(keys)
    client.send_event(event)

    client.disconnect()

main()
