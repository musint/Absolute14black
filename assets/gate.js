/* Absolute 14 Black · team password gate
   Each protected page ships as a shell (masthead + password form) plus an
   AES-GCM encrypted payload. The key is derived from the team password with
   PBKDF2. After a successful unlock the derived key is kept in localStorage so
   the device stays unlocked across pages and visits. "Sign out" clears it. */
(() => {
  const KEY_STORE = "avc14.key";
  const enc = new TextEncoder();
  const dec = new TextDecoder();
  const b64d = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
  const b64e = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf)));

  const payloadEl = document.getElementById("payload");
  const form = document.getElementById("gate");
  const input = document.getElementById("pw");
  const msg = document.getElementById("msg");
  if (!payloadEl || !form || !input) return;

  const payload = JSON.parse(payloadEl.textContent);
  const salt = b64d(payload.salt);
  const iv = b64d(payload.iv);
  const data = b64d(payload.data);
  const iterations = payload.iter;

  // The password is short and case is easy to get wrong on a phone keyboard,
  // so it is matched without regard to case or surrounding spaces.
  const normalize = (s) => s.trim().toUpperCase();

  async function deriveKey(password) {
    const base = await crypto.subtle.importKey("raw", enc.encode(normalize(password)), "PBKDF2", false, ["deriveKey"]);
    return crypto.subtle.deriveKey(
      { name: "PBKDF2", salt, iterations, hash: "SHA-256" },
      base,
      { name: "AES-GCM", length: 256 },
      true,
      ["decrypt"]
    );
  }

  function importStoredKey(b64) {
    return crypto.subtle.importKey("raw", b64d(b64), { name: "AES-GCM" }, true, ["decrypt"]);
  }

  async function decryptPage(key) {
    const plain = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, key, data);
    return JSON.parse(dec.decode(plain));
  }

  function render(page) {
    document.title = page.title;
    document.body.innerHTML = page.body;
    window.scrollTo(0, 0);
  }

  async function unlockWith(key) {
    const page = await decryptPage(key); // throws on a wrong key
    try {
      const raw = await crypto.subtle.exportKey("raw", key);
      localStorage.setItem(KEY_STORE, b64e(raw));
    } catch (_) {
      /* storage unavailable: still show the page for this visit */
    }
    render(page);
  }

  function showForm() {
    form.hidden = false;
    input.focus();
  }

  // Sign out: works on links rendered from the decrypted body too.
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-lock]");
    if (!a) return;
    e.preventDefault();
    try { localStorage.removeItem(KEY_STORE); } catch (_) {}
    location.reload();
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    msg.hidden = true;
    form.classList.add("busy");
    try {
      const key = await deriveKey(input.value);
      await unlockWith(key);
    } catch (_) {
      form.classList.remove("busy");
      msg.hidden = false;
      input.select();
    }
  });

  // Auto-unlock when this device has already entered the password.
  (async () => {
    let stored = null;
    try { stored = localStorage.getItem(KEY_STORE); } catch (_) {}
    if (!stored) return showForm();
    try {
      await unlockWith(await importStoredKey(stored));
    } catch (_) {
      try { localStorage.removeItem(KEY_STORE); } catch (_) {}
      showForm();
    }
  })();
})();
