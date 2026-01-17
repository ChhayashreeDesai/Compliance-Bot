"""Audit tool page - main functionality"""
import streamlit as st
import sys
from pathlib import Path
import time
import tempfile
import os

# Add source to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from dpdp_auditor import DPDP_Auditor
from validators import FormValidator, validate_and_show_errors
from styles import display_status_card, display_section_header, display_result_summary


def show():
    st.markdown("## Website Compliance Audit")
    st.markdown("Enter a website URL and select which compliance law to check against.")
    
    # Create two columns for input and settings
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("### Website Details")
        url_input = st.text_input(
            "Website URL",
            placeholder="https://example.com",
            help="Enter the complete URL including https://",
            key="url_input"
        )
        
        # Manual Privacy Policy URL Override
        policy_url_input = st.text_input(
            "Privacy Policy URL (Optional Override)",
            placeholder="https://example.com/privacy-policy",
            help="If the bot fails to find the privacy policy automatically, paste the link here.",
            key="policy_url_input"
        )
    
    with col2:
        st.markdown("### Regulation")
        regulation = st.selectbox(
            "Select Law to Check",
            ["DPDP Act 2025 (India)", "GDPR (EU 2016/679)", "CCPA (Coming Soon)", "Other (Coming Soon)"],
            help="Choose which data protection law to audit against"
        )
    
    st.markdown("---")
    
    # Explain modules for selected regulation
    if "DPDP" in regulation:
        with st.expander("DPDP Act 2025 - 7 Audit Modules", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **1. Consent Audit** (Section 6)
                - Detects pre-consent tracking cookies
                - Identifies known tracker signatures
                - Flags stealth trackers on first-party domain
                
                **2. Notice Audit** (Section 5)
                - Validates privacy policy presence
                - Confirms notice requirement compliance
                
                **3. Security Safeguards** (Section 8)
                - Checks security headers (HSTS, X-Frame-Options, CSP)
                - Validates encryption requirements
                """)
            
            with col2:
                st.markdown("""
                **4. Grievance Redressal** (Section 8)
                - Finds grievance officer contact information
                - Validates grievance handling procedures
                
                **5. Breach Notification** (Rule 7)
                - Scans for breach notification policies
                - Checks for incident response procedures
                
                **6. Children's Data** (Section 9 & Rule 10)
                - Identifies child data protection measures
                - Validates parental consent mechanisms
                
                **7. Data Retention** (Rule 8)
                - Verifies data deletion policies
                - Checks retention timelines
                """)

    elif "GDPR" in regulation:
        with st.expander("GDPR (EU 2016/679) - 5 Compliance Pillars", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **1. Strict Consent** (Article 6)
                - Detects trackers loading before consent
                - Validates consent mechanisms
                - Checks cookie banners
                
                **2. Governance** (Article 37)
                - Verifies Data Protection Officer (DPO) presence
                - Checks organizational responsibilities
                
                **3. Rights Bundle** (Articles 15-21)
                - Right of Access (Art 15)
                - Right to Rectification (Art 16)
                - Right to Erasure (Art 17)
                """)
            
            with col2:
                st.markdown("""
                **3. Rights Bundle (Continued)**
                - Right to Restriction (Art 18)
                - Right to Portability (Art 20)
                - Right to Object (Art 21)
                
                **4. Transparency & Complaints** (Article 77)
                - Supervisory Authority information
                - Complaint procedures
                
                **5. International Transfers** (Articles 44-46)
                - Transfer mechanism safeguards
                - Standard Contractual Clauses
                - Adequacy Decisions
                """)
    
    elif "CCPA" in regulation:
        st.info("This regulation is coming soon. We are actively developing support for it.")
    
    st.markdown("---")
    
    # Download preferences
    st.markdown("### Report Download Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_format = st.radio(
            "Report Format",
            ["PDF (Recommended)", "Summary (Text)"],
            horizontal=True
        )
    
    with col2:
        include_details = st.checkbox("Include Detailed Findings", value=True)
    
    st.markdown("---")
    
    # Audit button and execution
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        run_audit = st.button(
            "Start Audit",
            use_container_width=True,
            type="primary",
            key="run_audit_btn"
        )
    
    if run_audit:
        # Validate inputs before running audit
        validation_result = FormValidator.validate_and_prepare_audit(
            url_input, 
            policy_url_input, 
            regulation
        )
        
        if not validate_and_show_errors(validation_result):
            st.stop()
        
        # Check if coming soon regulation was selected
        if "Coming Soon" in regulation:
            st.error(f"❌ {regulation} is not yet available. Please select DPDP or GDPR.")
            st.stop()
        else:
            # Use validated inputs
            validated_url = validation_result['url']
            validated_policy_url = validation_result['policy_url']
            law = validation_result['law']
            
            # Run the audit
            audit_container = st.container()
            
            with audit_container:
                st.markdown("---")
                st.markdown(f"### ⏳ Running {law} Audit...")
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_placeholder = st.empty()
                
                try:
                    # Initialize auditor with validated URL
                    status_text.text("Initializing auditor...")
                    progress_bar.progress(10)
                    
                    auditor = DPDP_Auditor(validated_url, law=law)
                    
                    # Inject manual privacy policy URL if provided and validated
                    if validated_policy_url:
                        auditor.privacy_policy_url = validated_policy_url
                        st.info(f"Using manual Privacy Policy URL: {validated_policy_url}")
                    
                    status_text.text("Scanning website...")
                    progress_bar.progress(30)
                    
                    # Run audit
                    auditor.run_audit()
                    
                    progress_bar.progress(80)
                    status_text.text("Generating report...")
                    
                    # Get audit results
                    report = auditor.audit_report
                    
                    # Display results
                    progress_bar.progress(100)
                    status_text.text("Audit complete!")
                    
                    time.sleep(1)
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Display audit results
                    st.markdown("---")
                    st.markdown("##  Audit Results")
                    
                    # Calculate statistics
                    violations = 0
                    passes = 0
                    risks = 0
                    errors = 0
                    
                    for module_results in report.values():
                        for result in module_results:
                            if result.get('status') == 'VIOLATION':
                                violations += 1
                            elif result.get('status') == 'PASS':
                                passes += 1
                            elif result.get('status') == 'RISK':
                                risks += 1
                            elif result.get('status') == 'ERROR':
                                errors += 1
                    
                    # Display metrics
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric(" Passed", passes, delta=None)
                    with col2:
                        st.metric(" Risks", risks, delta=None)
                    with col3:
                        st.metric(" Violations", violations, delta=None)
                    with col4:
                        st.metric(" Errors", errors, delta=None)
                    with col5:
                        total_checks = passes + violations + risks + errors
                        compliance_score = int((passes / total_checks * 100)) if total_checks > 0 else 0
                        st.metric(" Compliance %", f"{compliance_score}%", delta=None)
                    
                    st.markdown("---")
                    
                    # Display detailed results by module
                    st.markdown("### Detailed Module Results")
                    
                    if law == "DPDP":
                        module_titles = {
                            'module_1': '1️⃣ Consent Audit (Sec 6)',
                            'module_2': '2️⃣ Notice Audit (Sec 5)',
                            'module_3': '3️⃣ Security Safeguards (Sec 8)',
                            'module_4': '4️⃣ Grievance Redressal (Sec 8)',
                            'module_5': '5️⃣ Breach Notification (Rule 7)',
                            'module_6': '6️⃣ Children\'s Data (Sec 9 & Rule 10)',
                            'module_7': '7️⃣ Data Retention (Rule 8)'
                        }
                    else:  # GDPR
                        module_titles = {
                            'gdpr_1': '1️⃣ Strict Consent (Article 6)',
                            'gdpr_2': '2️⃣ Governance - DPO (Article 37)',
                            'gdpr_3': '3️⃣ Rights Bundle (Articles 15-21)',
                            'gdpr_4': '4️⃣ Transparency & Complaints (Article 77)',
                            'gdpr_5': '5️⃣ International Transfers (Articles 44-46)'
                        }
                    
                    for module_key, module_title in module_titles.items():
                        if module_key in report:
                            with st.expander(module_title, expanded=True):
                                for result in report[module_key]:
                                    status = result.get('status', 'UNKNOWN')
                                    message = result.get('message', 'No information')
                                    details = result.get('details', [])
                                    
                                    # Color-coded status
                                    if status == 'PASS':
                                        st.success(f"✅ {message}")
                                    elif status == 'VIOLATION':
                                        st.error(f"❌ {message}")
                                    elif status == 'RISK':
                                        st.warning(f"⚠️ {message}")
                                    elif status == 'SKIP':
                                        st.info(f"⏭️ {message}")
                                    else:
                                        st.info(f"ℹ️ {message}")
                                    
                                    # Show recommendations if present
                                    if 'recommendation' in result:
                                        st.info(f"💡 Recommendation: {result['recommendation']}")
                                    
                                    # Show score deduction if present
                                    if 'score_deduction' in result:
                                        st.warning(f"Score Impact: {result['score_deduction']} points")
                                    
                                    # Show details if present
                                    if details and include_details:
                                        with st.expander("View Details", expanded=False):
                                            if isinstance(details, list):
                                                for detail in details:
                                                    if isinstance(detail, dict):
                                                        st.write(detail)
                                                    else:
                                                        st.write(detail)
                                            else:
                                                st.write(details)
                    
                    st.markdown("---")
                    
                    # Download report
                    st.markdown("###  Download Audit Report")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Generate text summary
                        summary_text = generate_text_report(url_input, report, compliance_score, law)
                        
                        st.download_button(
                            label=" Download as Text",
                            data=summary_text,
                            file_name=f"compliance_audit_{law}_{url_input.replace('https://', '').replace('http://', '').replace('/', '_')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with col2:
                        # Check if PDF was already generated by auditor
                        if hasattr(auditor, 'pdf_path') and auditor.pdf_path:
                            with open(auditor.pdf_path, 'rb') as pdf_file:
                                st.download_button(
                                    label=" Download as PDF",
                                    data=pdf_file,
                                    file_name=auditor.pdf_path.split('/')[-1],
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                        else:
                            st.info("PDF report generated by auditor (check your audit folder)")
                    
                    st.markdown("---")
                    
                    # Recommendations
                    if violations > 0 or risks > 0:
                        st.markdown("### 💡 Recommendations")
                        st.info(f"""
                        **Action Items for Remediation ({law}):**
                        
                        1. **Review each violation** listed above
                        2. **Address risks** that could lead to violations
                        3. **Prioritize high-impact items** (e.g., pre-consent tracking for GDPR/DPDP)
                        4. **Implement fixes** following the regulation requirements
                        5. **Re-run audit** to verify improvements
                        6. **Document compliance** efforts for regulatory purposes
                        
                        For detailed guidance, consult the Resources section or official regulations.
                        """)
                
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Audit failed: {str(e)}")
                    st.info(" Troubleshooting tips:\n- Verify the URL is correct\n- Ensure internet connection\n- Try again in a moment")


def generate_text_report(url, report, compliance_score, law="DPDP"):
    """Generate a text summary of the audit report"""
    text = f"""
COMPLIANCE AUDIT REPORT ({law})
================================

URL Audited: {url}
Compliance Score: {compliance_score}%
Audit Type: {law} Compliance

SUMMARY
-------
"""
    
    violations = 0
    passes = 0
    risks = 0
    
    for module_results in report.values():
        for result in module_results:
            if result.get('status') == 'VIOLATION':
                violations += 1
            elif result.get('status') == 'PASS':
                passes += 1
            elif result.get('status') == 'RISK':
                risks += 1
    
    text += f"Passed: {passes}\nRisks: {risks}\nViolations: {violations}\n\n"
    
    text += "DETAILED RESULTS\n"
    text += "================\n\n"
    
    if law == "DPDP":
        module_titles = {
            'module_1': '1. Consent Audit (Sec 6)',
            'module_2': '2. Notice Audit (Sec 5)',
            'module_3': '3. Security Safeguards (Sec 8)',
            'module_4': '4. Grievance Redressal (Sec 8)',
            'module_5': '5. Breach Notification (Rule 7)',
            'module_6': '6. Children\'s Data (Sec 9 & Rule 10)',
            'module_7': '7. Data Retention (Rule 8)'
        }
    else:  # GDPR
        module_titles = {
            'gdpr_1': '1. Strict Consent (Article 6)',
            'gdpr_2': '2. Governance - DPO (Article 37)',
            'gdpr_3': '3. Rights Bundle (Articles 15-21)',
            'gdpr_4': '4. Transparency & Complaints (Article 77)',
            'gdpr_5': '5. International Transfers (Articles 44-46)'
        }
    
    for module_key, module_title in module_titles.items():
        if module_key in report:
            text += f"\n{module_title}\n"
            text += "-" * 50 + "\n"
            
            for result in report[module_key]:
                status = result.get('status', 'UNKNOWN')
                message = result.get('message', 'No information')
                text += f"[{status}] {message}\n"
                
                # Include recommendations
                if 'recommendation' in result:
                    text += f"  Recommendation: {result['recommendation']}\n"
                
                # Include score deduction
                if 'score_deduction' in result:
                    text += f"  Score Impact: {result['score_deduction']} points\n"
    
    text += "\n\nDISCLAIMER\n"
    text += "==========\n"
    text += f"This is an automated {law} compliance check. For legal compliance advice, consult qualified professionals.\n"
    text += "Report generated by Compliance Auditor - https://audit-ai.com\n"
    
    return text
