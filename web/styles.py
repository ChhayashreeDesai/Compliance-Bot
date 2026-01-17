"""
Professional CSS Styling Engine for Compliance Auditor
Uses forest color palette and Lora font for SaaS-grade appearance
"""

import streamlit as st

# --- 🎨 FOREST COLOR PALETTE ---
COLORS = {
    "forest": "#1C0D31",           # Dark Forest (Background)
    "evergreen": "#1F0C0A",        # Evergreen (Card Background)
    "pine": "#0F1513",             # Pine (Accents/Hover)
    "fog": "#D7A3A0",              # Fog (Text/Light)
    "text_main": "#ABA39B",        # Main Text (Light Fog)
    "text_sub": "#838989",         # Subtitle/Muted Text
    "success": "#4CAF50",          # Success Green (darker)
    "warning": "#FFC107",          # Warning Yellow
    "danger": "#F44336",           # Danger Red
    "border": "#0D1521"            # Subtle Border
}

def load_custom_css():
    """Injects professional CSS to create SaaS appearance"""
    st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* --- GLOBAL STYLING --- */
        * {{
            font-family: 'Lora', serif;
        }}
        
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: {COLORS['forest']};
            color: {COLORS['text_main']};
        }}
        
        /* --- MAIN APP --- */
        .stApp {{
            background-color: {COLORS['forest']};
        }}
        
        .main {{
            padding: 2rem;
            background-color: {COLORS['forest']};
        }}
        
        /* --- SIDEBAR --- */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['evergreen']};
            border-right: 2px solid {COLORS['pine']};
        }}
        
        [data-testid="stSidebarNav"] {{
            display: none;
        }}
        
        /* --- TEXT STYLING --- */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Lora', serif;
            color: {COLORS['fog']};
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        h2 {{
            font-size: 2rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        h3 {{
            font-size: 1.5rem;
            margin-top: 1rem;
            margin-bottom: 0.75rem;
        }}
        
        p, span, div {{
            font-family: 'Lora', serif;
            line-height: 1.6;
        }}
        
        /* --- BUTTONS --- */
        .stButton > button {{
            background-color: {COLORS['pine']};
            color: {COLORS['fog']};
            border: none;
            border-radius: 6px;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            cursor: pointer;
        }}
        
        .stButton > button:hover {{
            background-color: {COLORS['forest']};
            box-shadow: 0 4px 12px rgba(94, 112, 101, 0.4);
            transform: translateY(-2px);
        }}
        
        /* --- INPUT FIELDS --- */
        .stTextInput > div > div > input {{
            background-color: {COLORS['evergreen']};
            color: {COLORS['fog']};
            border: 2px solid {COLORS['pine']};
            border-radius: 6px;
            padding: 12px 16px;
            font-family: 'Lora', serif;
            font-size: 1rem;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {COLORS['fog']};
            box-shadow: 0 0 8px rgba(201, 209, 200, 0.3);
        }}
        
        /* --- SELECTBOX --- */
        .stSelectbox > div > div > select {{
            background-color: {COLORS['evergreen']};
            color: {COLORS['fog']};
            border: 2px solid {COLORS['pine']};
            border-radius: 6px;
            padding: 12px 16px;
            font-family: 'Lora', serif;
            font-size: 1rem;
        }}
        
        /* --- EXPANDER --- */
        .streamlit-expanderHeader {{
            background-color: {COLORS['evergreen']};
            border: 2px solid {COLORS['pine']};
            border-radius: 6px;
            padding: 12px 16px;
        }}
        
        .streamlit-expanderHeader:hover {{
            background-color: {COLORS['pine']};
        }}
        
        /* --- METRIC CARDS --- */
        div.css-1r6slb0, div.stMetric {{
            background-color: {COLORS['evergreen']};
            border: 2px solid {COLORS['pine']};
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }}
        
        /* --- AUDIT STATUS CARDS --- */
        .audit-card {{
            background-color: {COLORS['evergreen']};
            border-left: 6px solid {COLORS['pine']};
            border-right: 1px solid {COLORS['pine']};
            border-top: 1px solid {COLORS['pine']};
            border-bottom: 1px solid {COLORS['pine']};
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            color: {COLORS['text_main']};
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .audit-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }}
        
        .audit-card.pass {{
            border-left-color: {COLORS['success']};
        }}
        
        .audit-card.warning {{
            border-left-color: {COLORS['warning']};
        }}
        
        .audit-card.danger {{
            border-left-color: {COLORS['danger']};
        }}
        
        .audit-card.skip {{
            border-left-color: {COLORS['text_sub']};
            opacity: 0.7;
        }}
        
        .audit-card.error {{
            border-left-color: {COLORS['danger']};
        }}
        
        .audit-header {{
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: {COLORS['fog']};
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .audit-status {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        
        .audit-status.pass {{
            background-color: rgba(76, 175, 80, 0.2);
            color: {COLORS['success']};
        }}
        
        .audit-status.warning {{
            background-color: rgba(255, 193, 7, 0.2);
            color: {COLORS['warning']};
        }}
        
        .audit-status.danger {{
            background-color: rgba(244, 67, 54, 0.2);
            color: {COLORS['danger']};
        }}
        
        .audit-status.skip {{
            background-color: rgba(154, 159, 154, 0.2);
            color: {COLORS['text_sub']};
        }}
        
        .audit-sub {{
            font-size: 0.95rem;
            color: {COLORS['text_main']};
            line-height: 1.6;
        }}
        
        .audit-details {{
            font-size: 0.85rem;
            color: {COLORS['text_sub']};
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid {COLORS['pine']};
        }}
        
        /* --- MESSAGES --- */
        .stError {{
            background-color: rgba(244, 67, 54, 0.1) !important;
            border: 2px solid {COLORS['danger']} !important;
            color: {COLORS['fog']} !important;
            border-radius: 6px;
            padding: 15px;
        }}
        
        .stWarning {{
            background-color: rgba(255, 193, 7, 0.1) !important;
            border: 2px solid {COLORS['warning']} !important;
            color: {COLORS['fog']} !important;
            border-radius: 6px;
            padding: 15px;
        }}
        
        .stSuccess {{
            background-color: rgba(76, 175, 80, 0.1) !important;
            border: 2px solid {COLORS['success']} !important;
            color: {COLORS['fog']} !important;
            border-radius: 6px;
            padding: 15px;
        }}
        
        .stInfo {{
            background-color: rgba(94, 112, 101, 0.1) !important;
            border: 2px solid {COLORS['pine']} !important;
            color: {COLORS['fog']} !important;
            border-radius: 6px;
            padding: 15px;
        }}
        
        /* --- DIVIDERS --- */
        hr {{
            border: none;
            border-top: 2px solid {COLORS['pine']};
            margin: 2rem 0;
        }}
        
        /* --- HIDE DEFAULT UI --- */
        #MainMenu {{
            visibility: hidden;
        }}
        
        footer {{
            visibility: hidden;
        }}
        
        .stDeployButton {{
            visibility: hidden;
        }}
        
        /* --- SCROLLBAR --- */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {COLORS['evergreen']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['pine']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['fog']};
        }}
        
    </style>
    """, unsafe_allow_html=True)


def display_status_card(title, detail, status="neutral", icon=""):
    """
    Render a beautiful professional status card
    
    Args:
        title: Card header/title
        detail: Main message/detail
        status: One of 'PASS', 'VIOLATION', 'RISK', 'SKIP', 'ERROR'
        icon: Optional emoji/icon to display
    """
    # Map status to CSS class
    status_class = "pass" if status == "PASS" else \
                  "danger" if status == "VIOLATION" else \
                  "warning" if status == "RISK" else \
                  "skip" if status == "SKIP" else \
                  "error" if status == "ERROR" else "neutral"
    
    # Status badge
    status_badge = f'<span class="audit-status {status_class}">{status}</span>'
    
    st.markdown(f"""
    <div class="audit-card {status_class}">
        <div class="audit-header">{icon} {title} {status_badge}</div>
        <div class="audit-sub">{detail}</div>
    </div>
    """, unsafe_allow_html=True)


def display_result_summary(total, passed, failed, risks):
    """Display a beautiful result summary section"""
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0;">
        <div class="audit-card pass" style="border-left-color: {COLORS['success']};">
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['success']};">{passed}</div>
            <div style="color: {COLORS['text_sub']}; font-size: 0.9rem;">Passed</div>
        </div>
        <div class="audit-card danger" style="border-left-color: {COLORS['danger']};">
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['danger']};">{failed}</div>
            <div style="color: {COLORS['text_sub']}; font-size: 0.9rem;">Violations</div>
        </div>
        <div class="audit-card warning" style="border-left-color: {COLORS['warning']};">
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['warning']};">{risks}</div>
            <div style="color: {COLORS['text_sub']}; font-size: 0.9rem;">Risks</div>
        </div>
        <div class="audit-card" style="border-left-color: {COLORS['pine']};">
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['fog']};">{total}</div>
            <div style="color: {COLORS['text_sub']}; font-size: 0.9rem;">Total Checks</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_section_header(title, subtitle=""):
    """Display a professional section header"""
    subtitle_html = f"<p style='color: {COLORS['text_sub']}; font-size: 0.95rem; margin: 5px 0 0 0;'>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div style="margin-top: 2rem; margin-bottom: 1.5rem;">
        <h2 style="margin: 0; color: {COLORS['fog']};">{title}</h2>
        {subtitle_html}
        <div style="width: 60px; height: 3px; background: {COLORS['pine']}; margin-top: 10px; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)


def display_content_card(title, content):
    """Display a content card with title and description"""
    st.markdown(f"""
    <div style="
        background-color: {COLORS['evergreen']};
        border-left: 4px solid {COLORS['pine']};
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    ">
        <div style="color: {COLORS['fog']}; font-weight: 600; margin-bottom: 8px; font-family: 'Lora', serif;">
            {title}
        </div>
        <div style="color: {COLORS['muted']}; font-size: 14px; line-height: 1.6;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_info_box(title, content, box_type="info"):
    """Display an informational box with styling"""
    colors = {
        "info": (COLORS['pine'], COLORS['fog']),
        "success": (COLORS['success'], COLORS['fog']),
        "warning": (COLORS['warning'], COLORS['forest']),
        "error": (COLORS['danger'], COLORS['fog'])
    }
    
    color, text_color = colors.get(box_type, (COLORS['pine'], COLORS['fog']))
    
    st.markdown(f"""
    <div style="background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1); 
                border-left: 5px solid {color}; 
                padding: 15px; 
                border-radius: 6px;
                margin: 15px 0;">
        <p style="color: {color}; font-weight: 700; margin: 0 0 8px 0;">{title}</p>
        <p style="color: {COLORS['text_main']}; margin: 0;">{content}</p>
    </div>
    """, unsafe_allow_html=True)
