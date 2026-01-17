# Compliance Auditor - Streamlit Web Application

A professional, interactive web interface for auditing websites against data protection compliance regulations.

## Features

✅ **Professional UI** - Clean, intuitive interface
✅ **Multi-page Navigation** - Home, Audit, About, Resources, Contact
✅ **Regulation Selector** - Choose which law to audit against (DPDP, GDPR coming soon)
✅ **Real-time Results** - Instant compliance findings
✅ **Multiple Export Formats** - PDF and text report downloads
✅ **Detailed Explanations** - Expandable sections for each module
✅ **Compliance Scoring** - Overall compliance percentage
✅ **Responsive Design** - Works on desktop and tablet

## Quick Start

### Prerequisites
- Python 3.8+
- Microsoft Edge browser installed
- All dependencies from `config/requirements.txt`

### Installation

1. Install dependencies:
```bash
pip install -r config/requirements.txt
```

2. Navigate to web directory:
```bash
cd web
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

4. Open in browser (automatically opens at http://localhost:8501)

## Project Structure

```
web/
├── app.py                    # Main Streamlit application
├── pages/
│   ├── __init__.py
│   ├── home.py              # Home page with overview
│   ├── audit.py             # Main audit tool interface
│   ├── about.py             # About Us page
│   ├── resources.py         # Resources and documentation
│   └── contact.py           # Contact and support page
└── README.md                # This file
```

## Pages Overview

### 🏠 Home
- Project overview and introduction
- Quick start button
- Key features highlight
- Compliance metrics

### 🔍 Audit Tool (Main Feature)
- URL input field
- Regulation selector dropdown
  - DPDP Act 2025 (Currently available)
  - GDPR (Coming Soon)
  - CCPA (Coming Soon)
  - Other (Coming Soon)
- Expandable module descriptions
- Report format options
- Real-time progress tracking
- Detailed result display with color-coded status
- Module-by-module findings
- PDF and text report downloads

### ℹ️ About Us
- Mission statement
- Feature explanations
- Technology stack overview
- DPDP Act 2025 modules breakdown
- Methodology explanation
- Why choose us section

### 📚 Resources
- **Guides Tab**
  - Getting started tutorial
  - Understanding results
  - Module interpretation guide
- **Regulations Tab**
  - DPDP Act 2025 details
  - GDPR overview (coming soon)
  - CCPA overview (coming soon)
- **FAQ Tab**
  - Common questions answered
  - Accuracy information
  - Privacy assurance
  - Duration expectations
- **Links Tab**
  - External resources
  - Official documents
  - Related tools and standards

### 📞 Contact
- Contact form
- Email addresses by category
- FAQ section
- Support tiers
- Newsletter subscription

## Key Features

### Law Selector Dropdown
Located on the audit page, allows users to:
- Select DPDP Act 2025 (current)
- Preview GDPR availability (coming soon)
- See other regulations in development

Automatically displays relevant audit modules for selected regulation.

### Report Download Options
Users can choose:
- **PDF Format** - Professional report with full formatting
- **Text Format** - Simple text summary for documentation
- **Detailed vs Summary** - Include or exclude technical details

### Interactive Audit Results
- Progress tracking during audit
- Real-time status updates
- Compliance score calculation
- Module-by-module results with expandable details
- Recommended remediation steps
- One-click downloads

## Usage Guide

### Running an Audit

1. Click **🔍 Audit Tool** in sidebar
2. Enter website URL (e.g., https://example.com)
3. Select regulation from dropdown (DPDP Act 2025 available)
4. Configure report preferences
5. Click **🚀 Start Audit**
6. Wait for analysis (typically 2-3 minutes)
7. Review results
8. Download report in preferred format

### Understanding Results

**Status Indicators:**
- ✅ **PASS** - Requirement met
- ❌ **VIOLATION** - Requirement not met
- ⚠️ **WARNING** - Potential issue
- ℹ️ **INFO** - Additional information

**Compliance Score:**
- 90-100%: Excellent ✨
- 70-89%: Good 👍
- 50-69%: Fair ⚠️
- Below 50%: Poor ❌

## Architecture

The web app integrates with the backend auditor:

```
Streamlit UI (web/app.py)
    ↓
Page Routers (web/pages/*)
    ↓
DPDP Auditor Engine (src/dpdp_auditor.py)
    ↓
Browser Automation (Selenium + Edge)
    ↓
Website Analysis
    ↓
Report Generation & Download
```

## Customization

### Adding a New Regulation

To add support for a new regulation (e.g., GDPR):

1. Update `audit.py` dropdown with new option
2. Add regulation explanation in expander
3. Create new audit modules in backend (`src/dpdp_auditor.py`)
4. Update results display logic
5. Add documentation in `resources.py`

### Styling

Custom CSS is defined in `app.py` with variables for:
- Color scheme (purple gradient: #667eea to #764ba2)
- Card styling
- Status badge colors
- Button appearance
- Responsive layout

Modify the `st.markdown()` with CSS class to customize appearance.

## Future Enhancements

### Planned Features
- [ ] GDPR compliance auditing
- [ ] CCPA compliance auditing
- [ ] Batch audit functionality
- [ ] Audit history and trends
- [ ] Custom regulation support
- [ ] Team collaboration features
- [ ] Integration with monitoring tools
- [ ] Email report delivery

### Roadmap
- Q1 2026: GDPR support
- Q2 2026: CCPA support
- Q3 2026: Batch processing
- Q4 2026: Analytics and reporting

## Troubleshooting

### App Won't Start
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/

# Try again
streamlit run app.py
```

### Audit Fails
- Verify URL is correct and accessible
- Check internet connection
- Ensure Edge browser is installed
- Try again after a moment

### Report Download Issues
- Check browser download settings
- Ensure sufficient disk space
- Try different format (PDF vs Text)

## Performance

- Typical audit duration: 2-3 minutes
- Supports unlimited concurrent audits (if resources allow)
- PDF generation: < 30 seconds
- No data storage - all processing is ephemeral

## Privacy & Security

🔒 **Privacy-First Design:**
- No tracking of user activity
- No storage of audit data
- No logging of website URLs
- Completely local processing
- No external API calls for audit data

## Dependencies

- **streamlit==1.28.1** - Web framework
- **selenium==4.15.2** - Browser automation
- **requests==2.31.0** - HTTP operations
- **reportlab==4.0.7** - PDF generation
- **Microsoft Edge** - Required browser

## Deployment

### Local Development
```bash
streamlit run web/app.py
```

### Production Deployment
```bash
# Using Streamlit Cloud
streamlit deploy

# Or using Docker
docker build -t compliance-auditor .
docker run -p 8501:8501 compliance-auditor
```

### Environment Variables
None required - fully self-contained

## Support & Documentation

- 📖 See Resources page in app for guides
- 💬 Use Contact page for inquiries
- 🐛 Report bugs via contact form
- 💡 Check FAQ for common questions

## License

Proprietary - All rights reserved

## Version History

**v2.1** (Current)
- ✨ New Streamlit web interface
- 🎨 Professional UI/UX
- 📱 Multi-page navigation
- 🔄 Law selector dropdown

**v2.0**
- 7 DPDP audit modules
- PDF report generation
- Enhanced tracker detection

**v1.0**
- Initial 4-module auditor
- Chrome to Edge migration

---

**Last Updated:** January 14, 2026
