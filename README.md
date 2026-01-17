# Compliance Auditor

A professional web application for auditing website compliance with international data protection regulations including DPDP Act 2025 (India) and GDPR (EU).

## Features

- **Multi-Regulation Support**: Audit against DPDP Act 2025 and GDPR
- **Automated Detection**: Intelligent privacy policy detection and analysis
- **Manual Override**: Provide custom privacy policy URLs when auto-detection fails
- **Comprehensive Scoring**: 7-module DPDP audit + 5-pillar GDPR assessment
- **Professional Reports**: PDF and text export with detailed findings
- **Beautiful UI**: Dark forest theme with professional styling and typography (Lora font)
- **Real-time Results**: Instant compliance findings with expandable details
- **Responsive Design**: Works seamlessly on desktop and tablets

## Architecture

```
Audit-AI/
├── src/
│   ├── dpdp_auditor.py        # Core audit engine (DPDP + GDPR logic)
│   └── test_auditor.py         # Batch testing utility
├── web/
│   ├── app.py                  # Main Streamlit application
│   ├── styles.py               # Centralized styling engine
│   ├── validators.py           # Input validation logic
│   ├── pages/                  # Multi-page navigation
│   │   ├── home.py
│   │   ├── audit.py
│   │   ├── about.py
│   │   ├── resources.py
│   │   └── contact.py
│   └── README.md
├── config/
│   └── requirements.txt         # Python dependencies
├── docs/
│   ├── README.md               # Documentation
│   ├── PROJECT_DELIVERY.md
│   ├── RELEASE_NOTES_v2.md
│   └── ...
└── run_web.ps1                 # Quick start script (PowerShell)
```

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.x with Selenium for web automation
- **Browser Automation**: Microsoft Edge WebDriver
- **Styling**: Custom CSS with forest color palette
- **Typography**: Lora serif font (Google Fonts)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Microsoft Edge browser
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Audit-AI.git
cd Audit-AI
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r config/requirements.txt
```

4. **Run the application**
```bash
# Windows PowerShell
.\run_web.ps1

# Or direct Streamlit command
streamlit run web/app.py
```

The application will open at `http://localhost:8501`

## Usage

### Running an Audit

1. Navigate to **Audit Tool** page
2. Enter website URL (e.g., `https://example.com`)
3. (Optional) Provide privacy policy URL if auto-detection fails
4. Select compliance law: DPDP Act 2025 or GDPR
5. Click **Start Audit**
6. Review detailed findings with expandable sections
7. Download PDF or text report

### DPDP Act 2025 Audit (7 Modules)

The DPDP auditor checks:
1. **Personal Data Collection** - Legitimate need and explicit consent
2. **Data Storage & Encryption** - Security measures and retention
3. **User Rights & Consent** - Right to access, correction, erasure
4. **Privacy Policy** - Transparency and completeness
5. **Data Sharing** - Third-party handling and consent
6. **Children's Data** - Special protections for minors
7. **Cross-Border Transfer** - International data flow compliance

### GDPR Audit (5 Pillars)

The GDPR auditor checks:
1. **Lawful Basis** - Legitimate purpose and consent documentation
2. **Data Rights** - Exercisability of subject rights (access, deletion, portability)
3. **Privacy by Design** - Data minimization and purpose limitation
4. **Data Security** - Technical and organizational safeguards
5. **Cross-Border Transfer** - Adequate safeguards for international flows

## Features in Detail

### Input Validation
- URL normalization (auto-adds https://)
- Format validation
- Policy URL override for problematic sites
- Real-time error feedback

### Professional UI
- **Dark Forest Theme**: #04202C background with #304040 cards
- **Typography**: Lora serif font for elegant appearance
- **Status Cards**: Color-coded results (green=pass, yellow=warning, red=violation)
- **Expandable Sections**: Hide/show detailed audit findings
- **Responsive Layout**: Auto-adjusts to screen size

### Report Generation
- PDF format with professional styling
- Text format for easy integration
- Compliance score summary
- Module-by-module findings
- Downloadable directly from app

## Documentation

- [Web Application README](web/README.md) - UI/UX details
- [Project Delivery](docs/PROJECT_DELIVERY.md) - Implementation notes
- [Release Notes](docs/RELEASE_NOTES_v2.md) - Version history
- [Enhancements](docs/VERSION_2_ENHANCEMENTS.md) - Feature improvements

## Development

### Project Structure
- **src/**: Core audit logic independent of UI
- **web/**: Streamlit application and UI pages
- **config/**: Configuration and dependencies
- **docs/**: Documentation files

### Code Style
- Python 3.8+ with type hints where applicable
- Comprehensive docstrings on modules and functions
- Centralized styling in `styles.py` (no scattered CSS)
- Input validation separated in `validators.py`

### Testing
Use the batch auditor utility to test multiple URLs:
```bash
python src/test_auditor.py
```

## Security Considerations

- **No Data Storage**: Application doesn't store audited websites or results on server
- **Browser Privacy**: Uses local Edge WebDriver for privacy policy fetching
- **HTTPS Only**: Enforces secure URLs
- **Input Validation**: All inputs validated and sanitized

## Performance

- **Single Audit**: ~30-45 seconds per website
- **Batch Audits**: ~5-7 minutes for 10 websites
- **Real-time UI**: Progress updates during audit execution

## Known Limitations

- Privacy policy auto-detection works best for standard implementations
- CCPA, PIPEDA, and other laws are "Coming Soon"
- Some complex consent mechanisms may not be detected
- Results reflect snapshot at audit time only

## Troubleshooting

### Microsoft Edge not found
Ensure Microsoft Edge is installed. Download from: https://www.microsoft.com/en-us/edge

### Privacy policy not detected
- Manually provide the URL using the override field
- Check if privacy policy is publicly accessible
- Verify the site structure matches common patterns

### Slow performance
- Ensure stable internet connection
- Close other browser windows
- Check system resources

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation in `/docs`
- Review the web app README for UI-specific questions

## Roadmap

- [ ] Support for CCPA (California Consumer Privacy Act)
- [ ] Support for PIPEDA (Canada)
- [ ] Scheduling and automated audits
- [ ] Team collaboration features
- [ ] API for third-party integration
- [ ] Chrome/Firefox WebDriver support

---

Built with ❤️ for data protection compliance
