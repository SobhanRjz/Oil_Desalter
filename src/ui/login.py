"""
Login Page Module
================
Professional login interface for the Desalter Optimization Suite.

Features a split-screen design with branding on the left and login form on the right.

Author: Engineering Team
Version: 2.0
License: Proprietary
"""

import streamlit as st
from streamlit.components.v1 import html

class LoginPage:
    """Professional login page with split-screen design."""
    
    def __init__(self):
        self.setup_page_config()
        self.apply_login_styles()
    
    def setup_page_config(self):
        """Configure the login page."""
        st.set_page_config(
            page_title="Login - Desalter Optimization Suite",
            page_icon="⚗️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    def apply_login_styles(self):
        """Apply custom CSS for the login page."""
        st.markdown("""
        <style>
        /* Force dark theme for login page */
        .stApp {
            background: radial-gradient(1200px 800px at 10% 10%, #0f1420 0%, #0b0f14 35%, #111827 100%) !important;
            color: #e5e7eb !important;
            color-scheme: dark !important;
        }
        
        /* Hide Streamlit chrome */
        #MainMenu, footer, header {visibility: hidden;}


        /* Full container */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
            background: transparent !important;
        }

        /* Left branding (unchanged) */
        .branding-section {
            flex: 0 0 60%;
            background: linear-gradient(135deg, #0b0f19 0%, #1a1f2e 50%, #0f1424 100%);
            background-image:
                radial-gradient(600px 400px at 20% 30%, rgba(212,175,55,.08), transparent 50%),
                radial-gradient(800px 600px at 80% 70%, rgba(244,208,63,.05), transparent 50%);
            color: #e5e7eb;
            position: relative;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            padding: 3rem;
        }

        .main-title {
            font-size: clamp(2.4rem, 6vw, 4rem);
            font-weight: 800; line-height: 1.1; margin-bottom: 1.5rem; text-align: center;
            background: linear-gradient(135deg, #f6e27a 0%, #ffd24a 35%, #fff 100%);
            -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 8px 28px rgba(212,175,55,.22));
        }
        .subtitle { font-size: 1.2rem; font-weight: 300; color:#9ca3af; text-align:center; margin-bottom: 2rem; }
        .feature-list{ list-style:none; margin:0; padding:0; }
        .feature-list li{ color:#d1d5db; margin:.6rem 0; display:flex; align-items:center; opacity:0; animation: slideIn .55s ease-out forwards; }
        .feature-list li:nth-child(1){ animation-delay:.15s } .feature-list li:nth-child(2){ animation-delay:.3s }
        .feature-list li:nth-child(3){ animation-delay:.45s } .feature-list li:nth-child(4){ animation-delay:.6s }
        .feature-list li::before{ content:'✓'; color:#eab308; font-weight:700; margin-right:.75rem; }
        @keyframes slideIn { from{ transform:translateX(-18px); opacity:0 } to{ transform:translateX(0); opacity:1 } }


        /* Top bar title */
        .card-head {
        background: rgba(255,255,255,0.22);
        color:#fff;
        font-weight:800;
        letter-spacing:.4px;
        text-transform: uppercase;
        text-align:center;
        padding: 8px 10px;
        border-radius: 12px;
        margin: 4px auto 14px auto;
        width: 88%;
        box-shadow: inset 0 1px 0 rgba(255,255,255,.28);
        font-size: 0.95rem;
        }

        /* Underline inputs */
        .stTextInput label{ display:none !important; }
        .stTextInput > div > div > input {
        background: transparent !important;
        color: #f3f4f6 !important;
        border: none !important;
        border-bottom: 1.4px solid rgba(255,255,255,0.32) !important;
        border-radius: 0 !important;
        padding: 9px 2px !important;
        font-size: 0.96rem !important;
        outline: none !important;
        box-shadow: none !important;
        }
        .stTextInput > div > div > input::placeholder{ color: rgba(243,244,246,.75); }
        .stTextInput > div > div > input:focus{
        border-bottom-color: rgba(255,255,255,.85) !important;
        }
        .stTextInput > div { margin-bottom: 8px; }

        /* Forgot link */
        .forgot { margin: 6px 2px 10px 2px; font-size:.88rem; text-align:right; }
        .forgot-link { color:#ffffff; font-weight:700; text-decoration:none; }
        .forgot-link:hover { text-decoration:underline; }

        /* Button */
        .stButton > button {
        background: linear-gradient(180deg, #bebebe, #9f9f9f) !important;
        color:#1f2937 !important;
        border: 0 !important;
        border-radius: 12px !important;
        padding: .7rem .9rem !important;
        font-weight: 800 !important;
        letter-spacing: .25px;
        text-transform: uppercase;
        box-shadow: 0 10px 18px rgba(0,0,0,.24) !important;
        width: 100% !important;
        }
        .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,.30) !important;
        }
        .stButton > button:active {
        transform: translateY(0) scale(.99) !important;
        }
        
        /* Force dark theme for all form elements */
        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.04) !important;
            color: #e5e7eb !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 8px !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #d4af37 !important;
            box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.25) !important;
        }
        
        .stFormSubmitButton > button {
            background: linear-gradient(135deg, #d4af37, #b8941f) !important;
            color: #0b0f14 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        .stFormSubmitButton > button:hover {
            background: linear-gradient(135deg, #f4d03f, #d4af37) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Ensure all text is light colored */
        .stMarkdown, .stText, p, span, div, label {
            color: #e5e7eb !important;
        }
        
        /* Form container styling */
        div[data-testid="stForm"] {
            background: rgba(255,255,255,0.02) !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 16px !important;
            padding: 2rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <style>
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Full screen container */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }
        
        /* Split screen layout */
        .login-container {
            display: flex;
            height: 100vh;
            font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial;
        }
        
        /* Left side - 60% dark branding */
        .branding-section {
            flex: 0 0 60%;
            background: linear-gradient(135deg, #0b0f19 0%, #1a1f2e 50%, #0f1424 100%);
            background-image: 
                radial-gradient(600px 400px at 20% 30%, rgba(212, 175, 55, 0.08), transparent 50%),
                radial-gradient(800px 600px at 80% 70%, rgba(244, 208, 63, 0.05), transparent 50%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            padding: 3rem;
            color: #e5e7eb;
        }
        
        /* Animated background elements */
        .branding-section::before {
            content: '';
            position: absolute;
            top: 20%;
            left: 10%;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(212, 175, 55, 0.1), transparent 70%);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        .branding-section::after {
            content: '';
            position: absolute;
            bottom: 30%;
            right: 15%;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, rgba(244, 208, 63, 0.08), transparent 70%);
            border-radius: 50%;
            animation: float 8s ease-in-out infinite reverse;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-20px) scale(1.05); }
        }
        
        /* Main title styling */
        .main-title {
            font-size: 4rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 2rem;
            text-align: center;
            background: linear-gradient(135deg, #d4af37 0%, #f4d03f 50%, #fff 100%);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 4px 20px rgba(212, 175, 55, 0.3));
            position: relative;
            z-index: 2;
        }
        
        .subtitle {
            font-size: 1.5rem;
            font-weight: 300;
            color: #9ca3af;
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
            z-index: 2;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
            margin: 0;
            position: relative;
            z-index: 2;
        }
        
        .feature-list li {
            font-size: 1.1rem;
            color: #d1d5db;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            opacity: 0;
            animation: slideIn 0.6s ease-out forwards;
        }
        
        .feature-list li:nth-child(1) { animation-delay: 0.2s; }
        .feature-list li:nth-child(2) { animation-delay: 0.4s; }
        .feature-list li:nth-child(3) { animation-delay: 0.6s; }
        .feature-list li:nth-child(4) { animation-delay: 0.8s; }
        
        .feature-list li::before {
            content: '✓';
            color: #d4af37;
            font-weight: bold;
            margin-right: 1rem;
            font-size: 1.2rem;
        }
        
        @keyframes slideIn {
            from { transform: translateX(-30px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        /* Right side - 40% yellow login */
        .login-section {
            flex: 0 0 40%;
            background: linear-gradient(135deg, #d4af37 0%, #f4d03f 50%, #ffd700 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 3rem 2rem;
            position: relative;
        }
        
        .login-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.1);
            background-image: 
                radial-gradient(400px 300px at 30% 20%, rgba(255, 255, 255, 0.1), transparent 50%),
                radial-gradient(300px 200px at 70% 80%, rgba(0, 0, 0, 0.1), transparent 50%);
        }
        
        .login-form {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            position: relative;
            z-index: 2;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .login-title {
            font-size: 2rem;
            font-weight: 700;
            color: #1f2937;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .login-subtitle {
            font-size: 1rem;
            color: #6b7280;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Form styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.8) !important;
            border: 2px solid rgba(212, 175, 55, 0.3) !important;
            border-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #d4af37 !important;
            box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #d4af37, #b8941f) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            margin-top: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(212, 175, 55, 0.4) !important;
            background: linear-gradient(135deg, #b8941f, #d4af37) !important;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .login-container {
                flex-direction: column;
            }
            
            .branding-section {
                flex: 0 0 40%;
                padding: 2rem 1rem;
            }
            
            .main-title {
                font-size: 2.5rem;
            }
            
            .login-section {
                flex: 0 0 60%;
                padding: 2rem 1rem;
            }
            
            .login-form {
                padding: 2rem 1.5rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_branding_section(self):
        """Render the left branding section."""
        return """
        <div class="branding-section">
            <div class="main-title">
                Desalter<br>Optimization<br>Suite
            </div>
            <div class="subtitle">
                Advanced Multi-Objective Parameter Optimization
            </div>
            <ul class="feature-list">
                <li>Maximize throughput while ensuring quality compliance</li>
                <li>Minimize operational costs and chemical usage</li>
                <li>Real-time performance analytics and insights</li>
                <li>Professional-grade optimization algorithms</li>
            </ul>
        </div>
        """
    
    def render_login_section(self):
        """Render the right login section."""
        return """
        <div class="login-section">
            <div class="login-form">
                <div class="login-title">Welcome Back</div>
                <div class="login-subtitle">Sign in to access the optimization suite</div>
                <div id="login-form-inputs">
                    <!-- Streamlit inputs will be inserted here -->
                </div>
            </div>
        </div>
        """
    
    def show(self):
        """Display the complete login page."""
        # Check if HTML login is enabled via session state
        use_html_login = st.session_state.get('login_preference', False)
        
        if use_html_login:
            self._render_html_login()
        else:
            self._render_streamlit_login()
    
    def _render_html_login(self):
        """Render the HTML-based login interface."""
        # Use Streamlit columns for the split layout
        left, right = st.columns([6, 4])  # 60% / 40% split
        
        # Left side - Dark branding section
        with left:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #0b0f19 0%, #1a1f2e 50%, #0f1424 100%);
                background-image: 
                    radial-gradient(600px 400px at 20% 30%, rgba(212, 175, 55, 0.08), transparent 50%),
                    radial-gradient(800px 600px at 80% 70%, rgba(244, 208, 63, 0.05), transparent 50%);
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 3rem 2rem;
                color: #e5e7eb;
                position: relative;
            ">
                <div style="
                    font-size: 3.5rem;
                    font-weight: 800;
                    line-height: 1.1;
                    margin-bottom: 2rem;
                    text-align: center;
                    background: linear-gradient(135deg, #d4af37 0%, #f4d03f 50%, #fff 100%);
                    background-clip: text;
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    filter: drop-shadow(0 4px 20px rgba(212, 175, 55, 0.3));
                ">
                    Desalter<br>Optimization<br>Suite
                </div>
                <div style="
                    font-size: 1.3rem;
                    font-weight: 300;
                    color: #9ca3af;
                    text-align: center;
                    margin-bottom: 3rem;
                ">
                    Advanced Multi-Objective Parameter Optimization
                </div>
                <div style="list-style: none; padding: 0; margin: 0;">
                    <div style="font-size: 1rem; color: #d1d5db; margin-bottom: 1rem; display: flex; align-items: center;">
                        <span style="color: #d4af37; font-weight: bold; margin-right: 1rem;">✓</span>
                        Maximize throughput while ensuring quality compliance
                    </div>
                    <div style="font-size: 1rem; color: #d1d5db; margin-bottom: 1rem; display: flex; align-items: center;">
                        <span style="color: #d4af37; font-weight: bold; margin-right: 1rem;">✓</span>
                        Minimize operational costs and chemical usage
                    </div>
                    <div style="font-size: 1rem; color: #d1d5db; margin-bottom: 1rem; display: flex; align-items: center;">
                        <span style="color: #d4af37; font-weight: bold; margin-right: 1rem;">✓</span>
                        Real-time performance analytics and insights
                    </div>
                    <div style="font-size: 1rem; color: #d1d5db; margin-bottom: 1rem; display: flex; align-items: center;">
                        <span style="color: #d4af37; font-weight: bold; margin-right: 1rem;">✓</span>
                        Professional-grade optimization algorithms
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with right:
            # Render the whole yellow side + card as a component
            html("""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8" />
        <style>
        /* Yellow side background + centering */
        body {
            margin:0;
            font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial;
        }
                   html, body { height: 100%; margin: 0; background: transparent; }

        /* NEW wrapper to create space around the panel so corners can show */
        .panel-wrap{
            height: 100%;
            width: 100%; 
            padding: 32px;                      /* space from iframe edges */
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        /* Yellow panel now fills the wrapper height and shows rounded corners */
        .yellow-panel{
        height: 90%;
        width: 90%;
        border-radius: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 48px;
        background: linear-gradient(135deg, #b8860b 0%, #d4a017 50%, #ffbf00 100%);
        box-shadow: 0 12px 28px rgba(0,0,0,0.25);
        }

        /* Slim glass card */
        .glass-card{
        width: min(480px, 92%);   /* was 340px → now bigger */
        background: rgba(0,0,0,0.45);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,.35);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        padding: 32px 28px 28px;  /* more breathing room */
        color:#f3f4f6;
        }

        /* Title strip */
        .card-head{
            background:rgba(255,255,255,.22);
            color:#fff; font-weight:800; letter-spacing:.4px;
            text-transform:uppercase; text-align:center;
            padding:8px 10px; border-radius:12px;
            margin:4px auto 14px; width:88%;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.28);
            font-size:.95rem;
        }
        .login-form{ display:flex; flex-direction:column; gap:10px; }
        .field{ margin:4px 2px; }
        .field label{ display:block; font-size:.86rem; color:#e5e7eb; opacity:.9; margin-bottom:6px; }
        .field input{
            width:100%;
            background:transparent;
            color:#f3f4f6;
            border:none; border-bottom:1.4px solid rgba(255,255,255,.32);
            padding:9px 2px; font-size:.96rem; outline:none;
        }
        .field input::placeholder{ color:rgba(243,244,246,.75); }
        .field input:focus{ border-bottom-color:rgba(255,255,255,.85); }
        .forgot{ margin:6px 2px 10px; text-align:right; font-size:.88rem; }
        .forgot a{ color:#fff; font-weight:700; text-decoration:none; }
        .forgot a:hover{ text-decoration:underline; }
        .btn{
            width:100%; cursor:pointer;
            background: linear-gradient(180deg, #bebebe, #9f9f9f);
            color:#1f2937; border:0; border-radius:12px;
            padding:.7rem .9rem; font-weight:800; letter-spacing:.25px; text-transform:uppercase;
            box-shadow:0 10px 18px rgba(0,0,0,.24);
            transition: transform .12s ease, box-shadow .12s ease;
        }
        .btn:hover{ transform:translateY(-1px); box-shadow:0 12px 24px rgba(0,0,0,.30); }
        .btn:active{ transform:translateY(0) scale(.99); }
        </style>
        </head>
        <body>
        <div class="panel-wrap">
            <div class="yellow-panel">
                <div class="glass-card">
                <div class="card-head">LOGIN</div>
                <form class="login-form" onsubmit="return false">
                    <div class="field">
                    <label for="login-username">Username</label>
                    <input id="login-username" type="text" placeholder="Username" autocomplete="username">
                    </div>
                    <div class="field">
                    <label for="login-password">Password</label>
                    <input id="login-password" type="password" placeholder="Password" autocomplete="current-password">
                    </div>
                    <div class="forgot">Forgot Password? <a href="#">Click Here</a></div>
                    <button id="signin" type="button" class="btn">SIGN IN</button>
                </form>
                </div>
            </div>
        </div>
        <script>
        // On click, write values into the parent URL as query params, then reload.
        document.getElementById('signin').addEventListener('click', function(){
            const u = document.getElementById('login-username').value || "";
            const p = document.getElementById('login-password').value || "";
            const url = new URL(window.parent.location);
            url.searchParams.set('login','1');
            url.searchParams.set('u', u);
            url.searchParams.set('p', p);  // remove if you don't want to expose it
            window.parent.location = url.toString();
        });
        </script>
        </body>
        </html>
            """, height=1000, scrolling=False)

    def _render_streamlit_login(self):
        """Render the Streamlit-based login interface."""
        left, right = st.columns([6, 4])
        
        with left:
            st.markdown(self.render_branding_section(), unsafe_allow_html=True)
        
        with right:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-head">LOGIN</div>', unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.form_submit_button("SIGN IN", use_container_width=True):
                        st.session_state.login_attempt = {'username': username, 'password': password}
                        st.session_state.logged_in = True
                        st.session_state.current_page = 'input'
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)


def show_login_page():
    """Main function to display the login page."""
    login_page = LoginPage()
    login_page.show()
