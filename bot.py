import requests
import json
import websocket
from nostr.event import Event
from nostr.key import PrivateKey
from nostr.message_type import ClientMessage

PRIVATE_KEY = "${NOSTR_PRIVATE_KEY}"
RELAY = "wss://relay.damus.io"

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    return requests.get(url).json()["bitcoin"]["usd"]

def publish():
    price = get_btc_price()
    content = f"₿ Bitcoin price: ${price} USD\n⏰ Automatic hourly update"

    priv = PrivateKey.from_nsec(PRIVATE_KEY)
    event = Event(priv.public_key.hex(), content)
    event.sign(priv)

    ws = websocket.WebSocket()
    ws.connect(RELAY)
    ws.send(json.dumps(ClientMessage.event(event.to_dict()).to_json_object()))
    ws.close()

publish()
