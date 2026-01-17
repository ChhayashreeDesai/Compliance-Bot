"""Home page"""
import streamlit as st

def show():
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("## Welcome to Compliance Auditor")
        st.markdown("""
        Your trusted partner for ensuring website compliance with international data protection regulations.
        
        Our automated compliance checker helps you:
        - **Audit Multiple Laws** (DPDP, GDPR, CCPA...)
        - **Identify Violations** quickly and accurately
        - **Understand Requirements** for each regulation
        - **Generate Reports** for documentation and remediation
        - **Stay Compliant** with evolving data protection laws
        
        Whether you're a security analyst, compliance officer, or developer, 
        our platform makes compliance checking straightforward and efficient.
        """)
        
        st.markdown("### Quick Start")
        if st.button("Start Audit →", use_container_width=True, key="home_start_audit"):
            st.session_state.current_page = "audit"
            st.rerun()
    
    with col2:
        st.markdown("### Features")
        features = [
            ("- Multi-Law Support", "DPDP Act 2025 (India) & GDPR (EU)"),
            ("- Detailed Reports", "Comprehensive PDF and text audit reports"),
            ("- Fast Analysis", "Real-time compliance checking"),
            ("- Privacy First", "No data storage or logging"),
            ("- Compliance Scoring", "Get overall compliance ratings"),
            ("- Rule-Based Logic", "Transparent, auditable results")
        ]
        
        for title, desc in features:
            st.markdown(f"**{title}**  \n{desc}")
    
    st.markdown("---")
    
    # Supported Laws
    st.markdown("###  Supported Regulations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🇮🇳 DPDP Act 2025 (India)**
        
        - 7 Compliance Modules
        - Consent & Privacy Protection
        - Security & Data Retention
        
        [Learn More →](#)
        """)
    
    with col2:
        st.markdown("""
        **🇪🇺 GDPR (EU 2016/679)**
        
        - 5 Compliance Pillars  
        - Strict Consent Requirements
        - Data Subject Rights
        
        [Learn More →](#)
        """)
    
    st.markdown("---")
    
    # Metrics section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>12</h3>
            <p>Compliance Modules</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>∞</h3>
            <p>Websites Auditable</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>100%</h3>
            <p>Transparent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>24/7</h3>
            <p>Available</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Why choose us
    st.markdown("###  Why Choose Compliance Auditor?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Accuracy**
        
        Built on rule-based logic that reflects actual regulatory requirements. 
        No guessing, no approximations—just clear compliance checks.
        """)
        
        st.markdown("""
        **Security**
        
        Your audit data is processed locally. No external tracking or data storage. 
        Your website information remains completely private.
        """)
    
    with col2:
        st.markdown("""
        **Efficiency**
        
        Get comprehensive compliance reports in minutes. Identify issues and 
        remediation steps instantly.
        """)
        
        st.markdown("""
        **Extensibility**
        
        Built to support multiple regulations. New laws and requirements are 
        continuously being added (CCPA, LGPD, etc.).
        """)
