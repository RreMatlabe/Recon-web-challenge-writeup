# Recon & Web Challenge Walkthrough — Cybersecurity Assessment

*Note: company and domain names have been anonymized/genericized, as this was a private assessment challenge rather than a public CTF.*

## Overview

As part of a technical screening process for a junior SOC/GRC-adjacent role, I was given a self-paced, multi-level web-based challenge. Each level required a different technique — DNS reconnaissance, viewing page source, decoding/encoding schemes (Base64, ROT13, character codes), AES decryption, constraint-solving (Sudoku), and basic OSINT/attention-to-detail on an image. This write-up documents my approach and reasoning through each stage.

---

## Level 0 — DNS A-Record Lookup
**Task:** Find the IP address of a given subdomain.
**Approach:** A general web search returned nothing useful, so I used a DNS A-record lookup (Python's `socket.gethostbyname()`, equivalent to `nslookup`/`dig`).
**Result:** The lookup returned a loopback-range (`127.0.0.0/8`) address — a private address, not a real public IP, which was itself a small "gotcha" in the task.

## Level 0b — DNS TXT Record
**Task:** Find the TXT record of a related subdomain.
**Approach:** Same technique, different record type — a DNS TXT lookup.
**Result:** Returned a string ending in a Base64-encoded fragment that, when decoded, simply repeated the plaintext portion of the string — a self-referential check to confirm the solver actually decoded it rather than just copying the raw value.

## Level 1 — Hardcoded Credential in Source
**Approach:** Viewed the page's HTML/JS source directly. The correct password was hardcoded in plaintext inside a JavaScript `if` statement.
**Twist:** The next level's URL wasn't shown anywhere — it was constructed as `level2_<MD5 hash of password>.html`, so I had to compute that hash myself before I could proceed.

## Level 2 — Base64 Comparison
**Approach:** Source inspection revealed the check compared `btoa(password)` (i.e., the *encoded* version of my input) against a fixed Base64 string. Since `btoa` encodes, I decoded the target string instead to recover the plaintext password directly.

## Level 3 — Multi-Part Obfuscated String
**Approach:** The password was assembled from three separately obfuscated pieces in the source:
- one Base64-encoded fragment,
- one built from raw character codes (`String.fromCharCode`),
- one derived by decoding a longer Base64 sentence and extracting individual characters at specific string indices.

Reconstructing and concatenating all three gave the correct password.

## Level 4 — Blocking JavaScript Dialog
**Approach:** This page threw a JS `confirm()` dialog on load that couldn't be dismissed normally, blocking interaction. I disabled JavaScript execution in browser DevTools to load the page without the dialog firing, then read the hardcoded redirect URL straight from the page source instead of needing to click through the UI.

## Level 5 — DNS TXT Record (again)
**Approach:** Same technique as Level 0b, applied to a different subdomain.

## Level 6 — Sudoku-Derived AES Key
**Approach:** This level combined a logic puzzle with cryptography. A Sudoku grid was shown with only ~22 clues and five specific cells highlighted. Since that's too few clues to solve reliably by hand with certainty, I wrote a small backtracking solver to compute the unique completed grid. I then pulled the values from the five highlighted cells to form a numeric key, testing a few orderings until one correctly decrypted the accompanying AES-encrypted string (in a CryptoJS-compatible format).

## Level 7 — ROT13 and QR Code
**Approach:** A banner image contained ROT13-scrambled text (a simple 13-position letter substitution cipher), which decoded to a hint pointing toward a QR code elsewhere on the page. Scanning the QR code gave the next level's URL directly, bypassing a distractor table of quotes/ciphers that turned out to be decorative.

## Level 8 — Reading Credentials from an Image
**Approach:** This level had no interactive form at all — just a stock-style image of someone logged into a fake system. The actual task was visual attention: zooming into the image revealed a username and a ROT13-encoded password field, plus a hash value visible in the browser address bar shown within the image itself. Decoding the password and using the visible hash as the next filename completed the level.

## Level 9 — Final Redirect
**Approach:** The final URL redirected to the real public website of the security team running the assessment, revealing the organization behind the challenge as the intended "reveal" ending.

---

## Skills Demonstrated
- DNS reconnaissance (A/TXT records)
- Browser DevTools usage (source inspection, disabling JS, network/sources tabs)
- Encoding/decoding: Base64, ROT13, character-code obfuscation
- Symmetric cryptography: AES decryption (CryptoJS/OpenSSL key-derivation format)
- Scripting for automation (Python — DNS queries, hashing, a Sudoku backtracking solver, AES decryption)
- OSINT-style visual attention to detail
- Clear technical documentation of methodology and reasoning under time constraints

---

## Supporting Scripts

The `scripts/` folder contains cleaned-up, reusable versions of the tools I built while working through this challenge (generalized — no puzzle-specific data included):

| Script | Purpose |
|---|---|
| `scripts/dns_lookup.py` | Resolves A and TXT DNS records for any domain |
| `scripts/sudoku_solver.py` | Backtracking solver for 9x9 Sudoku grids |
| `scripts/aes_decrypt.py` | Decrypts CryptoJS-style AES-encrypted (Base64/OpenSSL-format) strings given a passphrase |

Each script is standalone and runnable from the command line — see the docstring at the top of each file for usage.
