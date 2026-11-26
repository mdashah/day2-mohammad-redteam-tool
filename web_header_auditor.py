#!/usr/bin/env python3
"""
Web Header Security Auditor (Day 2 - Red Team)

Audits HTTP security headers for a given URL.
Non-destructive: GET only. By default scans localhost/127.0.0.1 targets
only; pass --allow-external for sites you own or are authorized to test.
"""

import argparse
import json
import os
import sys
import datetime
import urllib.request
import urllib.error
import ssl

# header: (severity, why dangerous when missing)
CHECKS = {
    "Content-Security-Policy": ("HIGH", "Without CSP, the browser has no policy restricting script sources. "
        "Injected XSS payloads execute freely, enabling session theft and defacement."),
    "X-Frame-Options": ("MEDIUM", "Without X-Frame-Options (or CSP frame-ancestors), the page can be "
        "iframed by attackers, enabling clickjacking to trick users into actions."),
    "Strict-Transport-Security": ("HIGH", "Without HSTS, users can be downgraded to HTTP via SSL-stripping "
        "MITM attacks, exposing cookies and credentials in plaintext."),
    "X-Content-Type-Options": ("LOW", "Without nosniff, browsers may MIME-sniff responses and execute "
        "user-uploaded content as scripts."),
    "Referrer-Policy": ("LOW", "Without a Referrer-Policy, full URLs (with tokens/params) leak to "
        "third-party sites via the Referer header."),
    "Permissions-Policy": ("LOW", "Without Permissions-Policy, embedded content may access sensitive "
        "browser features (camera, geolocation, mic) on your pages."),
    "X-XSS-Protection": ("INFO", "Legacy header, largely deprecated; modern browsers ignore it. "
        "CSP is the correct modern control."),
}

SEVERITY_SCORE = {"HIGH": 10, "MEDIUM": 5, "LOW": 3, "INFO": 0}

# Max possible risk = sum of all severity weights (computed, never hardcoded)
MAX_SCORE = sum(SEVERITY_SCORE[sev] for sev, _ in CHECKS.values())


def fetch_headers(url: str, timeout: int = 10):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # local labs use self-signed certs
    req = urllib.request.Request(url, headers={"User-Agent": "HeaderAuditor/1.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return dict(resp.headers)


def audit(headers: dict):
    findings, risk = [], 0
    lower = {k.lower(): v for k, v in headers.items()}
    for header, (severity, why) in CHECKS.items():
        if header.lower() in lower:
            findings.append({"header": header, "status": "PRESENT", "severity": "-",
                             "risk": "-", "value": lower[header.lower()]})
        else:
            findings.append({"header": header, "status": "MISSING", "severity": severity,
                             "risk": f"Why dangerous: {why}"})
            risk += SEVERITY_SCORE[severity]
    return findings, risk


def grade(risk: int) -> str:
    if risk >= 25:
        return "CRITICAL"
    if risk >= 15:
        return "HIGH"
    if risk >= 8:
        return "MEDIUM"
    if risk > 0:
        return "LOW"
    return "SECURE"


def main():
    p = argparse.ArgumentParser(description="Web Header Security Auditor")
    p.add_argument("--url", help="Target URL (localhost/own lab only by default)")
    p.add_argument("--input", help="File with one URL per line (e.g. sample_input/urls.txt)")
    p.add_argument("--output", default="sample_output", help="Output directory")
    p.add_argument("--allow-external", action="store_true",
                   help="Allow scanning non-localhost targets (GET only; "
                        "use only for sites you own or are authorized to test)")
    args = p.parse_args()

    # Load targets: from file or single --url
    if args.input:
        with open(args.input) as f:
            targets = [line.strip() for line in f if line.strip()]
    elif args.url:
        targets = [args.url]
    else:
        p.error("Provide either --url or --input")

    for target in targets:
        # Non-destructive guard: localhost / 127.0.0.1 by default,
        # unless --allow-external is explicitly passed
        if not ("localhost" in target or "127.0.0.1" in target) and not args.allow_external:
            print(f"[!] SKIPPED (non-destructive policy — not localhost): {target}")
            print("    Tip: use --allow-external for sites you own or are authorized to test.")
            continue

        print(f"\n[*] Auditing {target} ...")
        try:
            headers = fetch_headers(target)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            print(f"[x] Request failed: {e}")
            continue

        findings, risk = audit(headers)
        report = {
            "target": target,
            "timestamp": datetime.datetime.now().isoformat(),
            "overall_risk_score": risk,
            "max_possible_score": MAX_SCORE,
            "overall_grade": grade(risk),
            "findings": findings,
        }

        os.makedirs(args.output, exist_ok=True)
        fname = os.path.join(args.output, f"report_{target.replace('://','_').replace('/','').replace(':','_')}.json")
        with open(fname, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n===== SECURITY HEADER REPORT: {target} =====")
        print(f"Risk Score: {risk}/{MAX_SCORE}  Grade: {report['overall_grade']}\n")
        for f_ in findings:
            mark = "[+]" if f_["status"] == "PRESENT" else "[-]"
            print(f"{mark} {f_['header']}: {f_['status']}"
                  + (f" (Severity: {f_['severity']})" if f_["status"] == "MISSING" else ""))
        print(f"\n[*] JSON report saved to: {fname}")


if __name__ == "__main__":
    main()
