# DPDP Act 2025 Compliance Auditor

A robust, object-oriented Python tool to audit websites against the Digital Personal Data Protection (DPDP) Act 2025 requirements.

## Overview

This auditor performs automated compliance checks across 4 critical DPDP legal requirements:

### Module 1: Consent Audit (DPDP Sec 6)
- **Requirement**: No pre-consent tracking/data processing
- **Logic**: Visits URL, waits 5 seconds, extracts cookies WITHOUT accepting
- **Detection**: Filters out essential cookies and flags 3rd-party trackers
- **Output**: `[VIOLATION]` if unauthorized tracking cookies found

### Module 2: Notice Audit (DPDP Sec 5)
- **Requirement**: Privacy Notice must be accessible
- **Logic**: Scans homepage for privacy-related links ("Privacy", "Policy", "Notice", "Data")
- **Detection**: Locates and stores Privacy Policy URL
- **Output**: `[PASS]` if link found, `[VIOLATION]` if missing

### Module 3: Security Safeguards (DPDP Sec 8)
- **Requirement**: Implement technical security measures
- **Logic**: Checks HTTP headers for security implementations
- **Detection**: Validates presence of:
  - Strict-Transport-Security (HSTS)
  - X-Frame-Options (clickjacking protection)
  - X-Content-Type-Options (MIME sniffing protection)
- **Output**: `[RISK]` if headers are missing

### Module 4: Grievance Redressal (DPDP Sec 8)
- **Requirement**: Grievance Officer contact details must be available
- **Logic**: Scrapes Privacy Policy page for contact information
- **Detection**: Uses regex to find emails and checks context for grievance-related keywords
- **Output**: `[PASS]` if grievance contact found, `[VIOLATION]` if missing

## Installation

### Prerequisites
- Python 3.8+
- Microsoft Edge browser installed

### Setup Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python -c "import selenium; import requests; print('✓ All dependencies installed')"
   ```

## Usage

### Basic Execution
```bash
python dpdp_auditor.py
```

Then enter the target URL when prompted:
```
Enter the target URL to audit (e.g., example.com): example.com
```

### Advanced Usage (Python Script)

```python
from dpdp_auditor import DPDP_Auditor

# Create auditor instance
auditor = DPDP_Auditor("https://example.com")

# Run complete audit
audit_report = auditor.run_audit()

# Access results
for module, findings in audit_report.items():
    print(f"{module}: {findings}")
```

## Features

### Anti-Detection Measures
✓ Real Windows 10 Chrome User-Agent
✓ Disabled automation flags
✓ Headed mode (visible browser) for CAPTCHA verification
✓ Explicit 5-second waits for script loading
✓ Webdriver Manager for automatic driver updates

### Error Handling
✓ Module-level exception handling (one failure doesn't crash the script)
✓ Comprehensive logging at INFO and DEBUG levels
✓ Graceful fallbacks for missing Privacy Policy
✓ Proper WebDriver cleanup

### Output Format
Clean, structured terminal report with:
- `[PASS]` - Compliance requirement met
- `[VIOLATION]` - Legal requirement not met
- `[RISK]` - Potential security/compliance issue
- `[SKIP]` - Module skipped (dependent data unavailable)
- `[ERROR]` - Technical error during audit

## Technical Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Selenium | 4.15.2 | Browser automation with Selenium 4 syntax |
| WebDriver Manager | 4.0.1 | Automatic Microsoft Edge driver management |
| Requests | 2.31.0 | HTTP header inspection |
| Python | 3.8+ | Core scripting |

## DPDP Legal References

### Sections Audited
- **Sec 5**: Privacy Notice Requirements
- **Sec 6**: Pre-Consent Data Processing
- **Sec 8(5)**: Technical and Organizational Measures
- **Sec 8(9)**: Grievance Redressal Mechanism

### Source Documents
- DPDP Act 2023 (Initial framework)
- DPDP Act 2025 (Updated provisions)

## Output Example

```
======================================================================
DPDP ACT 2025 COMPLIANCE AUDITOR
Target URL: https://example.com
======================================================================

=== MODULE 1: CONSENT AUDIT (DPDP Sec 6) ===
[PASS] Sec 6(1): No unauthorized pre-consent tracking detected

=== MODULE 2: NOTICE AUDIT (DPDP Sec 5) ===
[PASS] Sec 5(1): Privacy Notice link found
  └─ URL: https://example.com/privacy

=== MODULE 3: SECURITY SAFEGUARDS (DPDP Sec 8) ===
[RISK] Sec 8(5): Missing Security Headers
  ✗ X-Frame-Options (Clickjacking Protection)

=== MODULE 4: GRIEVANCE REDRESSAL (DPDP Sec 8) ===
[PASS] Sec 8(9): Grievance Officer contact details found
  ✓ Contact: privacy@example.com

======================================================================
AUDIT SUMMARY
======================================================================
Compliance Level: MEDIUM ⚠
Violations: 0
Risks: 1
Passed: 3
======================================================================
```

## Important Notes

⚠️ **Headed Mode**: The browser runs in visible mode so you can handle CAPTCHAs manually if needed.

⚠️ **Waits**: Each module includes explicit 5-second waits to ensure JavaScript has loaded before scraping.

⚠️ **Cookie Filtering**: The auditor intelligently filters essential cookies (session, CSRF tokens) to avoid false positives.

⚠️ **3rd Party Detection**: Flags any cookies from domains different than the target URL.

## Troubleshooting

### Issue: "Chrome driver not found"
**Solution**: 
```bash
pip install --upgrade webdriver-manager
```

### Issue: "CAPTCHA appears"
**Solution**: The browser is running in headed mode - complete the CAPTCHA manually. The script will continue.

### Issue: "Privacy Policy page times out"
**Solution**: Check if the Privacy Policy URL is accessible and not blocked. Increase the timeout by modifying `time.sleep()` values.

### Issue: "No cookies detected"
**Solution**: Some modern sites use in-memory storage. The script handles this gracefully.

## Compliance Recommendations

Based on audit results:

- **[VIOLATION]**: Immediate action required to meet legal compliance
- **[RISK]**: Address security gaps to meet technical standards
- **[PASS]**: Requirement met, continue monitoring

## License

For Security Analyst Use - DPDP Act 2025 Compliance

## Support

For issues or questions:
1. Check the log output for detailed error messages
2. Verify the target website is accessible
3. Ensure Chrome browser is installed and updated
