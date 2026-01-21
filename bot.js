const fetch = require("node-fetch");
const { SimplePool, getEventHash, signEvent, getPublicKey, nip19 } = require("nostr-tools");

const RELAYS = ["wss://relay.damus.io"];
const NSEC = process.env.NOSTR_PRIVATE_KEY;

async function getBTCPrice() {
  const r = await fetch(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
  );
  const j = await r.json();
  return j.bitcoin.usd;
}

async function main() {
  if (!NSEC) {
    throw new Error("NOSTR_PRIVATE_KEY secret is missing");
  }

  // convert nsec → hex secret key
  const decoded = nip19.decode(NSEC);
  const sk = decoded.data;
  const pk = getPublicKey(sk);

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

  const pool = new SimplePool();
  await pool.publish(RELAYS, event);
  pool.close(RELAYS);
}

main();
