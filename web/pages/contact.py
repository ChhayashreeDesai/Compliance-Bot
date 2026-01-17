"""Contact page"""
import streamlit as st
from styles import display_content_card, display_section_header

def show():
    display_section_header("Contact & Support", "We're here to help with any questions or feedback")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        display_section_header("Get in Touch", "Multiple ways to reach us")
        
        display_content_card(
            "Email Support",
            "General: info@complianceauditor.io | Business: business@complianceauditor.io | Bugs: bugs@complianceauditor.io | Support: support@complianceauditor.io"
        )
        
        display_content_card(
            "Response Times",
            "General Inquiries: 24-48 hours | Bug Reports: 12-24 hours | Business: 24-48 hours | Technical Support: Next business day"
        )
    
    with col2:
        st.markdown("### Send us a Message")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name", placeholder="John Doe")
            email = st.text_input("Your Email", placeholder="you@example.com")
            
            subject = st.selectbox(
                "Subject",
                [
                    "General Inquiry",
                    "Bug Report",
                    "Feature Request",
                    "Business Partnership",
                    "Feedback",
                    "Technical Support"
                ]
            )
            
            message = st.text_area(
                "Message",
                placeholder="Tell us how we can help...",
                height=150
            )
            
            submitted = st.form_submit_button("Send Message", use_container_width=True)
            
            if submitted:
                if name and email and message:
                    st.success("✅ Message received! We'll get back to you soon.")
                    st.info(f"""
                    **Sent from:** {name}
                    **Email:** {email}
                    **Subject:** {subject}
                    
                    We appreciate your message and will respond shortly.
                    """)
                else:
                    st.error("❌ Please fill in all fields")
    
    st.markdown("---")
    
    # FAQ section
    display_section_header("Quick Answers", "Common questions about Compliance Auditor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        display_content_card(
            "Version History",
            "Yes! Check our release notes in the Guides section for all updates and new features."
        )
        
        display_content_card(
            "Suggest Features",
            "Absolutely! Email us or use the contact form. We value your feedback and suggestions."
        )
    
    with col2:
        display_content_card(
            "Report Security Issues",
            "Please email bugs@complianceauditor.io with details. We take security seriously."
        )
        
        display_content_card(
            "Enterprise Support",
            "Yes! Contact business@complianceauditor.io for enterprise support options and pricing."
        )
    
    st.markdown("---")
    
    # Social and resources
    display_section_header("Connect With Us", "Resources and community")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        display_content_card(
            "Documentation",
            "Comprehensive guides and tutorials"
        )
    
    with col2:
        display_content_card(
            "Status Page",
            "System status and updates"
        )
    
    with col3:
        display_content_card(
            "GitHub",
            "Source code and issue tracker"
        )
    
    with col4:
        display_content_card(
            "Community",
            "Forum and discussions"
        )
    
    st.markdown("---")
    
    # Support tiers
    display_section_header("Support Options", "Choose the plan that fits your needs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_content_card(
            "Free Plan",
            "Community support | Documentation | Public resources | Email support | Response: 48 hours",
            badge="INCLUDED"
        )
    
    with col2:
        display_content_card(
            "Professional Plan",
            "Priority support | Dedicated support | Custom training | Email + Phone | Custom regulations | Response: 24 hours"
        )
    
    with col3:
        display_content_card(
            "Enterprise Plan",
            "24/7 support | Dedicated account manager | Custom development | On-site training | SLA guarantee | Response: 2 hours"
        )
    
    st.markdown("---")
    
    # Newsletter
    display_section_header("Stay Updated", "Subscribe for news and updates")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.text_input(
            "Subscribe to our newsletter",
            placeholder="your@email.com",
            label_visibility="collapsed"
        )
    
    with col2:
        st.button("Subscribe", use_container_width=True)
    
    st.markdown("""
    Get updates about:
    - New regulations added
    - Platform improvements
    - Compliance tips
    - Security advisories
    """)
