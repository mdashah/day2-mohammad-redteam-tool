# Web Header Security Auditor

- 👤 **Candidate Name:** Mohammad Shah
- 🎯 **Track:** Red Team
- 🛠 **Tool Name:** Web Header Security Auditor CLI
- ⏱ **Time Spent:** ~2 hours

## Tool Description

My tool checks whether a website is actually telling browsers how to protect itself. You give it a URL (like a local DVWA lab on localhost), it sends a simple GET request, and then compares the response headers against a checklist of security headers — things like CSP, X-Frame-Options, and HSTS.

For every missing header, it tells you how bad the gap is and, more importantly, why it matters in plain English:

- No CSP means XSS just works
- No X-Frame-Options means clickjacking is on the table
- No HSTS means someone could strip your HTTPS

At the end, it hands you a JSON risk report with a score and grade, so you know exactly what to fix first.

## Installation

### Option 1 — pipx install (recommended, verified on Kali)

Newer Kali/Debian systems block system-wide pip installs (PEP 668), so use `pipx`:

```bash
sudo apt install pipx
pipx ensurepath
pipx install git+https://github.com/mdashah/day2-mohammad-redteam-tool.git
```

Then run the command from **anywhere** — no cloning or venv needed:

```bash
web-header-auditor --url http://localhost:3000
```

> **Note:** Installing via pipx provides the `web-header-auditor` command only.
> To use batch mode (`--input`) with the bundled `sample_input/urls.txt`, use
> Option 2 (clone), or create your own URL file anywhere and pass its path.

### Option 2 — Clone and run manually (no install needed)

```bash
git clone https://github.com/mdashah/day2-mohammad-redteam-tool.git
cd day2-mohammad-redteam-tool
python3 web_header_auditor.py --url http://localhost:3000
```

**Requirements:** Python 3.8+. No external dependencies needed (standard library only).

### Option 3 — pip (Windows / systems without PEP 668 restrictions)

```bash
pip install git+https://github.com/mdashah/day2-mohammad-redteam-tool.git
web-header-auditor --url http://localhost:3000
```

## How to Run

### Step 1 — Start a local target (Terminal 1)

Open a **first terminal**, then start a test web server to audit:

```bash
python3 -m http.server 3000
```

Keep this terminal running. It serves a basic server on `http://localhost:3000` (this server sends NO security headers, which is perfect for demonstrating the tool). You can also point the tool at your own DVWA or any other local lab instead.

### Step 2 — Run the auditor (Terminal 2)

**Scan a single URL:**

```bash
web-header-auditor --url http://localhost:3000
```

**Batch mode — scan all URLs in a file (one URL per line):**

```bash
# Using the bundled sample file (requires the cloned repo, Option 2):
cd day2-mohammad-redteam-tool
web-header-auditor --input sample_input/urls.txt

# Or with your own file from anywhere:
web-header-auditor --input ~/my_targets.txt
```

**If running manually from the cloned repo:**

```bash
python3 web_header_auditor.py --url http://localhost:3000
python3 web_header_auditor.py --input sample_input/urls.txt
```

### Step 3 — View the results

- The terminal prints a graded risk report (e.g., `Grade: CRITICAL`)
- A full JSON report is saved automatically to `sample_output/`
- Sample input lives in `sample_input/urls.txt`

## Expected Output

```
[*] Auditing http://localhost:3000 ...

===== SECURITY HEADER REPORT: http://localhost:3000 =====
Risk Score: 31/31 Grade: CRITICAL

[-] Content-Security-Policy: MISSING (Severity: HIGH)
[-] X-Frame-Options: MISSING (Severity: MEDIUM)
[-] Strict-Transport-Security: MISSING (Severity: HIGH)
...

[*] JSON report saved to: sample_output/report_http__localhost_3000.json
```

> ⚠️ **Non-destructive:** The tool only sends GET requests and refuses to scan
> any target that isn't localhost / 127.0.0.1.

## Output Evidence

**Terminal screenshot:**

![Terminal Output](sample_output/terminal_screenshot.png)

**pipx install verified:**

![pipx Install](sample_output/pipx_install.png)

**Generated JSON report:** [`sample_output/report_http__localhost_3000.json`](sample_output/report_http__localhost_3000.json)

## Self-Attestation

"I self-sourced all materials, used only public/synthetic/self-owned resources, built a working tool, and performed non-destructive work."
