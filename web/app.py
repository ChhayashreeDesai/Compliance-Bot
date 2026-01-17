"""
DPDP Compliance Auditor - Streamlit Web Application
A professional compliance checking tool for websites
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

# Import styling engine
from styles import load_custom_css

# Page configuration
st.set_page_config(
    page_title="Compliance Auditor",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load professional CSS styling
load_custom_css()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Sidebar Navigation
with st.sidebar:
    st.markdown("### Navigation")
    
    pages = {
        "Home": "home",
        "Audit Tool": "audit",
        "About": "about",
        "Resources": "resources",
        "Contact": "contact"
    }
    
    for label, page_name in pages.items():
        if st.button(label, key=f"btn_{page_name}", use_container_width=True):
            st.session_state.current_page = page_name
    
    st.markdown("---")
    st.markdown("""
    ### About This Tool
    A comprehensive compliance checking platform designed to audit websites against data protection regulations.
    
    **Currently Supported:**
    - DPDP Act 2025 (India)
    - GDPR (EU 2016/679)
    
    **Coming Soon:**
    - CCPA (USA)
    - And more...
    """)

# Header
st.markdown("# Compliance Auditor")
st.markdown("*Professional Website Compliance Checking Platform*")
st.markdown("---")

# Route to appropriate page
if st.session_state.current_page == 'home':
    from pages import home
    home.show()

elif st.session_state.current_page == 'audit':
    from pages import audit
    audit.show()

elif st.session_state.current_page == 'about':
    from pages import about
    about.show()

elif st.session_state.current_page == 'resources':
    from pages import resources
    resources.show()

elif st.session_state.current_page == 'contact':
    from pages import contact
    contact.show()

# Footer
st.markdown("---")
st.markdown("""
**© 2026 Compliance Auditor. All rights reserved.**

A professional compliance checking tool for websites | Built with security and accuracy in mind

Disclaimer: This tool provides automated compliance checking based on public information visible on websites. 
For legal compliance advice, consult with qualified legal professionals.
""")
