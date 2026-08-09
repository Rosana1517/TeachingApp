// One-off local keygen for Web Push VAPID keys, matching the raw-bytes
// base64url format @block65/webcrypto-web-push expects (publicKey = raw
// uncompressed EC point, privateKey = JWK `d`). Run once with `node
// scripts/generate_vapid_keys.mjs`, then store the output as Cloudflare
// Worker secrets — never commit the private key.
import { webcrypto } from "node:crypto";

function base64url(buf) {
  return Buffer.from(buf).toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

const keyPair = await webcrypto.subtle.generateKey(
  { name: "ECDSA", namedCurve: "P-256" },
  true,
  ["sign", "verify"]
);

const rawPublic = await webcrypto.subtle.exportKey("raw", keyPair.publicKey);
const jwkPrivate = await webcrypto.subtle.exportKey("jwk", keyPair.privateKey);

console.log("VAPID_PUBLIC_KEY=" + base64url(rawPublic));
console.log("VAPID_PRIVATE_KEY=" + jwkPrivate.d);
