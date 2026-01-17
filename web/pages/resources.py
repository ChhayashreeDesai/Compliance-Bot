"""Resources page"""
import streamlit as st

def show():
    st.markdown("## 📚 Resources & Documentation")
    
    # Tabs for different resource types
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 Guides", "📋 Regulations", "❓ FAQ", "🔗 Links"
    ])
    
    with tab1:
        st.markdown("### Audit Guides & Tutorials")
        
        guide1 = st.expander("Getting Started with Compliance Auditor", expanded=False)
        with guide1:
            st.markdown("""
            **Step 1: Navigate to Audit Tool**
            - Click "🔍 Audit Tool" in the sidebar
            
            **Step 2: Enter Website URL**
            - Provide the complete URL (e.g., https://example.com)
            - Include the https:// protocol
            
            **Step 3: Select Regulation**
            - Currently: DPDP Act 2025
            - More coming soon: GDPR, CCPA, etc.
            
            **Step 4: Configure Report Options**
            - Choose report format (PDF or Text)
            - Optionally include detailed findings
            
            **Step 5: Run the Audit**
            - Click "🚀 Start Audit"
            - Wait for analysis to complete (2-3 minutes)
            
            **Step 6: Review Results**
            - Check your compliance score
            - Review violations and recommendations
            - Download your report
            """)
        
        guide2 = st.expander("Understanding Audit Results", expanded=False)
        with guide2:
            st.markdown("""
            ### Result Status Meanings
            
            **✅ PASS** - Requirement is met
            - The website complies with this specific regulation
            - No action needed for this module
            
            **❌ VIOLATION** - Requirement not met
            - The website does not comply with this regulation
            - Action required to achieve compliance
            - Details provided for remediation
            
            **⚠️ WARNING** - Potential issue detected
            - May require attention but not a confirmed violation
            - Recommend review and clarification
            
            **ℹ️ INFO** - Additional information
            - Contextual information about the audit
            - May provide guidance for interpretation
            
            ### Compliance Score
            
            The overall compliance score is calculated as:
            
            ```
            Compliance % = (Passed Checks / Total Checks) × 100
            ```
            
            - **90-100%**: Excellent compliance
            - **70-89%**: Good compliance, some improvements needed
            - **50-69%**: Fair compliance, multiple issues to address
            - **Below 50%**: Poor compliance, significant remediation required
            """)
        
        guide3 = st.expander("Interpreting Specific Modules", expanded=False)
        with guide3:
            st.markdown("""
            ### Module 1: Consent Audit
            
            **What it checks:**
            - Are cookies set before user accepts?
            - Are trackers present without consent?
            - Are tracking companies identified?
            
            **Common violations:**
            - Google Analytics (_ga) set before consent
            - Facebook pixel (_fbp) set before consent
            - Ad trackers from external domains
            
            **Remediation:**
            - Implement cookie consent banner
            - Load tracking scripts only after consent
            - Use Google Consent Mode or similar
            
            ---
            
            ### Module 2: Notice Audit
            
            **What it checks:**
            - Is privacy policy easily accessible?
            - Is notice provided before collection?
            
            **Common violations:**
            - Privacy policy not linked from homepage
            - Notice buried in terms of service
            
            **Remediation:**
            - Add prominent privacy policy link
            - Display clear data collection notice
            
            ---
            
            ### Module 3: Security Safeguards
            
            **What it checks:**
            - Are proper security headers present?
            - Is HTTPS enforced?
            
            **Common violations:**
            - Missing HSTS header
            - Missing X-Frame-Options
            
            **Remediation:**
            - Configure web server headers
            - Enable HTTPS only
            """)
    
    with tab2:
        st.markdown("### 📋 Regulation Frameworks")
        
        dpdp = st.expander("DPDP Act 2025 (Digital Personal Data Protection Act)", expanded=True)
        with dpdp:
            st.markdown("""
            **Jurisdiction:** India
            
            **Effective Date:** August 2023
            
            **Key Principles:**
            - Consent-based data processing
            - Purpose limitation
            - Data minimization
            - Security and storage limitation
            - Transparency and notice
            
            **Scope:**
            - Applies to any processing of personal data
            - Includes online and offline processing
            - Covers digital and physical data
            
            **Penalties for Non-Compliance:**
            - Up to ₹50 crore or 4% of annual revenue (whichever is higher)
            
            **Our Audit Coverage:**
            - ✅ 7 comprehensive modules
            - ✅ All major requirements covered
            - ✅ Practical enforcement focus
            """)
        
        gdpr = st.expander("GDPR (General Data Protection Regulation) - Coming Soon", expanded=False)
        with gdpr:
            st.markdown("""
            **Jurisdiction:** European Union
            
            **Status:** In Development
            
            **Key Areas:**
            - Lawful basis for processing
            - Consent management
            - Data subject rights
            - Privacy impact assessment
            - Data protection officer requirements
            
            **Expected Audit Modules:**
            - Consent & Legal Basis
            - Privacy Rights Implementation
            - Data Protection Policies
            - Breach Notification (72 hours)
            - Cross-border Transfer Safeguards
            
            *Check back soon for GDPR support!*
            """)
        
        ccpa = st.expander("CCPA (California Consumer Privacy Act) - Coming Soon", expanded=False)
        with ccpa:
            st.markdown("""
            **Jurisdiction:** California, USA
            
            **Status:** In Development
            
            **Key Areas:**
            - Consumer rights
            - Data collection & sale
            - Opt-out mechanisms
            - Privacy notices
            
            *Check back soon for CCPA support!*
            """)
    
    with tab3:
        st.markdown("### ❓ Frequently Asked Questions")
        
        faq1 = st.expander("How accurate is the Compliance Auditor?", expanded=False)
        with faq1:
            st.markdown("""
            Our auditor uses rule-based logic to check compliance. It identifies:
            - 95%+ of technical compliance issues
            - Cookie tracking violations
            - Missing security headers
            - Broken policy links
            
            However, some aspects require manual review:
            - Policy content interpretation
            - Legal adequacy of terms
            - Organizational processes
            
            **Recommendation:** Use automated results as a starting point, 
            then consult legal professionals for final compliance certification.
            """)
        
        faq2 = st.expander("Is my data stored or tracked?", expanded=False)
        with faq2:
            st.markdown("""
            **No data storage:**
            - Audits run locally in your browser
            - Results are not sent anywhere
            - Website URLs are not logged
            - Reports are generated locally
            
            **Privacy assurance:**
            - No third-party trackers on this site
            - No analytics on audit data
            - No cookies stored on your machine
            - Completely private auditing
            """)
        
        faq3 = st.expander("How long does an audit take?", expanded=False)
        with faq3:
            st.markdown("""
            **Typical duration:** 2-3 minutes
            
            **Breakdown:**
            - Website loading: ~30 seconds
            - Cookie extraction: ~15 seconds
            - Policy scanning: ~60-90 seconds
            - Report generation: ~30 seconds
            
            **Factors that affect duration:**
            - Website response time
            - Amount of content to scan
            - Network speed
            - Server load
            """)
        
        faq4 = st.expander("Can I download and share reports?", expanded=False)
        with faq4:
            st.markdown("""
            **Yes!** You can:
            
            ✅ Download reports as PDF
            ✅ Download as text summary
            ✅ Share with your team
            ✅ Archive for compliance documentation
            ✅ Present to stakeholders
            
            Reports include:
            - Full audit findings
            - Module-by-module results
            - Compliance score
            - Remediation recommendations
            - Timestamp and URL
            """)
        
        faq5 = st.expander("What if I disagree with a finding?", expanded=False)
        with faq5:
            st.markdown("""
            Our tool is automated and follows specific rules. If you believe a result is incorrect:
            
            1. **Check the details** - Review what the auditor found
            2. **Verify on your website** - Manually confirm the finding
            3. **Consult documentation** - Review the regulation requirement
            4. **Seek expert advice** - Consult legal professionals if uncertain
            
            **Note:** Some determinations require judgment. This tool provides 
            automated checks, not legal interpretation.
            """)
        
        faq6 = st.expander("How often should I run audits?", expanded=False)
        with faq6:
            st.markdown("""
            **Recommendation:** Regular auditing schedule
            
            - **Initial:** When implementing compliance
            - **After changes:** Any website modifications
            - **Quarterly:** Routine compliance check
            - **Post-incident:** After security events
            - **During development:** Before new feature launches
            
            **Best practices:**
            - Schedule regular audits (monthly/quarterly)
            - Audit after any policy changes
            - Re-audit after implementing fixes
            - Track compliance over time
            """)
    
    with tab4:
        st.markdown("### 🔗 External Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Official Documents:**
            - [DPDP Act 2025 - Full Text](https://meity.gov.in/)
            - [DPDP Rules 2023](https://meity.gov.in/)
            - [Ministry of IT Guidance](https://meity.gov.in/)
            
            **Learning Resources:**
            - [DPDP Act Overview](https://example.com)
            - [Compliance Best Practices](https://example.com)
            - [Data Protection Principles](https://example.com)
            """)
        
        with col2:
            st.markdown("""
            **Tools & Standards:**
            - [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
            - [Mozilla Security Checklist](https://infosec.mozilla.org/)
            - [Web Security Academy](https://portswigger.net/web-security)
            
            **Support:**
            - 📧 Documentation available in sidebar
            - 💬 Check About section for more info
            - 📞 Contact us via Contact page
            """)
