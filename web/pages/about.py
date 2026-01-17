"""About Us page"""
import streamlit as st

def show():
    st.markdown("## About Us")
    st.markdown("""
    ### Our Mission
    
    To empower organizations with transparent, accurate, and accessible compliance checking tools.
    We believe data protection should be straightforward—not shrouded in complexity.
    """)
    
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("""
        ### What We Do
        
        **Compliance Auditor** is a professional compliance checking platform that helps organizations
        understand if their websites meet data protection regulations. We focus on:
        
        ** * Accuracy**
        - Rule-based logic that reflects actual regulatory requirements
        - No assumptions, no approximations—just clear results
        
        ** * Security**
        - Local processing with no data storage
        - Your website information stays completely private
        
        ** * Efficiency**
        - Comprehensive audits in minutes
        - Instant identification of compliance gaps
        
        ** * Transparency**
        - Every check is auditable and explainable
        - Understand exactly why a violation was flagged
        
        ### Technology Stack
        
        - **Rule Engine**: Transparent, deterministic compliance checks
        - **Browser Automation**: Selenium (Edge)
        - **Web Interface**: Streamlit
        - **Report Generation**: PDF with detailed findings
        - **Code Base**: Python with 937 lines of auditing logic
        """)
    
    with col2:
        st.markdown("""
        ### Key Features
        
        - **7 Audit Modules** for DPDP Act 2025
        
        - **Real-Time Results** with actionable insights
        
        - **Detailed Reports** in multiple formats
        
        - **Zero Data Collection** - fully private
        
        - **Extensible Platform** for multiple laws
        
        - **Professional UI** for easy navigation
        
        ### Supported Regulations
        
        **Currently Available:**
        - DPDP Act 2025 (India)
        
        **In Development:**
        - GDPR (EU)
        - CCPA (USA)
        - PIPEDA (Canada)
        - And more...
        """)
    
    st.markdown("---")
    
    # Audit modules breakdown
    st.markdown("### 📋 DPDP Act 2025 - Our 7 Audit Modules")
    
    tabs = st.tabs([
        "Consent", "Notice", "Security", "Grievance", 
        "Breach", "Children", "Retention"
    ])
    
    with tabs[0]:
        st.markdown("""
        **Module 1: Consent Audit (Section 6)**
        
        Ensures data collection has proper consent:
        - Detects pre-consent tracking cookies
        - Identifies stealth trackers on first-party domain
        - Flags known tracker signatures (_ga, _fbp, etc.)
        - Validates no data processing before consent
        """)
    
    with tabs[1]:
        st.markdown("""
        **Module 2: Notice Audit (Section 5)**
        
        Verifies proper privacy notice availability:
        - Confirms privacy policy presence
        - Validates notice accessibility
        - Checks for required disclosures
        """)
    
    with tabs[2]:
        st.markdown("""
        **Module 3: Security Safeguards (Section 8)**
        
        Validates security measures:
        - HSTS (HTTP Strict Transport Security)
        - X-Frame-Options header
        - X-Content-Type-Options header
        - Encryption requirements
        """)
    
    with tabs[3]:
        st.markdown("""
        **Module 4: Grievance Redressal (Section 8)**
        
        Ensures grievance handling procedures:
        - Grievance officer contact information
        - Accessible complaint mechanisms
        - Response procedures validation
        """)
    
    with tabs[4]:
        st.markdown("""
        **Module 5: Breach Notification (Rule 7)**
        
        Checks breach notification requirements:
        - Breach notification policies
        - Incident response procedures
        - Notification timelines (72 hours)
        """)
    
    with tabs[5]:
        st.markdown("""
        **Module 6: Children's Data Protection (Section 9 & Rule 10)**
        
        Safeguards for minor data subjects:
        - Age verification mechanisms
        - Parental consent requirements
        - Special protections for children
        - Clear child-friendly policies
        """)
    
    with tabs[6]:
        st.markdown("""
        **Module 7: Data Retention (Rule 8)**
        
        Validates data lifecycle management:
        - Data deletion policies
        - Retention timelines
        - Purpose-limited storage
        - Secure data destruction
        """)
    
    st.markdown("---")
    
    # Methodology
    st.markdown("### Our Methodology")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Step 1: Analysis**
        
        We scan your website and extract:
        - Cookies and tracking data
        - Privacy policy information
        - Security headers
        - Contact information
        """)
    
    with col2:
        st.markdown("""
        **Step 2: Checking**
        
        We compare findings against:
        - Regulatory requirements
        - Best practices
        - Technical standards
        - Legal obligations
        """)
    
    with col3:
        st.markdown("""
        **Step 3: Reporting**
        
        We generate reports showing:
        - Violations found
        - Compliance status
        - Specific issues
        - Remediation guidance
        """)
    
    st.markdown("---")
    
    # Why choose us
    st.markdown("###  Why Organizations Choose Us")
    
    reasons = [
        ("No AI Guessing", "Rule-based deterministic logic. Every result is auditable and explainable."),
        ("Privacy-First", "No tracking, no storage, no logging. Audits run completely locally."),
        ("Comprehensive", "7 modules covering all major DPDP Act requirements."),
        ("User-Friendly", "Professional interface designed for non-technical users."),
        ("Scalable", "Designed to support multiple regulations and frameworks."),
        ("Free to Use", "Accessible compliance checking for organizations of all sizes.")
    ]
    
    for title, desc in reasons:
        st.markdown(f"** {title}**")
        st.markdown(f"{desc}\n")
