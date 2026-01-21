import fetch from "node-fetch";
import { relayInit, getEventHash, signEvent, getPublicKey } from "nostr-tools";

const NSEC = process.env.NOSTR_PRIVATE_KEY;
const RELAY_URL = "wss://relay.damus.io";

function hexFromNsec(nsec) {
  const { data } = require("nostr-tools/nip19").decode(nsec);
  return data;
}

async function getBTCPrice() {
  const r = await fetch(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
  );
  const j = await r.json();
  return j.bitcoin.usd;
}

async function main() {
  if (!NSEC) throw new Error("Missing NOSTR_PRIVATE_KEY");

  const sk = hexFromNsec(NSEC);
  const pk = getPublicKey(sk);

  const relay = relayInit(RELAY_URL);
  await relay.connect();

  const price = await getBTCPrice();

  const event = {
    kind: 1,
    pubkey: pk,
    created_at: Math.floor(Date.now() / 1000),
    tags: [],
    content: `₿ Bitcoin price: $${price} USD\n⏰ Automatic hourly update`,
  };

  event.id = getEventHash(event);
  event.sig = signEvent(event, sk);

  relay.publish(event);
  relay.close();
}

main();
