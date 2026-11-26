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

### Option 1 — One-command install (recommended)

Install directly from GitHub as a CLI command:

```bash
pip install git+https://github.com/mdashah/day2-mohammad-redteam-tool.git
```

Then run from anywhere — no cloning or venv needed:

```bash
web-header-auditor --url http://localhost:3000
```

### Option 2 — Clone and run manually

```bash
git clone https://github.com/mdashah/day2-mohammad-redteam-tool.git
cd day2-mohammad-redteam-tool
```

**Requirements:** Python 3.8+. No external dependencies needed (standard library only).

## How to Run

### Step 1 — Start a local target (Terminal 1)

Open a **first terminal**, then start a test web server to audit:

```bash
python3 -m http.server 3000
```

Keep this terminal running. It serves a basic server on `http://localhost:3000` (this server sends NO security headers, which is perfect for demonstrating the tool).

You can also point the tool at your own DVWA or any other local lab instead.

### Step 2 — Run the auditor (Terminal 2)

**If installed via pip (Option 1):**

```bash
# Scan a single URL directly:
web-header-auditor --url http://localhost:3000

# Or scan all URLs listed in sample_input/urls.txt (one URL per line):
web-header-auditor --input sample_input/urls.txt
```

**If running manually from the cloned repo (Option 2):**

```bash
# Scan all URLs listed in sample_input/urls.txt (one URL per line):
python3 web_header_auditor.py --input sample_input/urls.txt

# Or scan a single URL directly:
python3 web_header_auditor.py --url http://localhost:3000
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

**Generated JSON report:** [`sample_output/report_http__localhost_3000.json`](sample_output/report_http__localhost_3000.json)

## Self-Attestation

"I self-sourced all materials, used only public/synthetic/self-owned resources, built a working tool, and performed non-destructive work."
