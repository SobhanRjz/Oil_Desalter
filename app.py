
"""
Desalter Optimization Suite
==========================
Professional multi-objective optimization tool for petroleum desalting operations.

This application provides advanced parameter optimization for desalter systems,
maximizing throughput while ensuring quality compliance and minimizing operational costs.

Author: Engineering Team
Version: 2.0
License: Proprietary
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import time
from src.core.optimizer import DesalterOptimizer
from src.ui.theme import ThemeManager
from src.ui.components import render_header, show_optimization_progress
from src.ui.charts import render_advanced_charts
from src.ui.login import show_login_page


# ============================================================================
# CORE OPTIMIZATION ENGINE
# ============================================================================

# Removed in favor of src.core.optimizer.DesalterOptimizer


# ============================================================================
# USER INTERFACE THEME ENGINE
# ============================================================================


# ============================================================================
# APPLICATION CONFIGURATION & INITIALIZATION
# ============================================================================

def initialize_app():
    st.set_page_config(page_title="Desalter Optimization Suite", page_icon="⚗️", layout="wide", initial_sidebar_state="expanded")
    ThemeManager().apply()


# ============================================================================
# MAIN APPLICATION
# ============================================================================
import sys

def get_login_preference():
    """Get login preference from environment variable or default to Streamlit."""
    import os
    # Check environment variable first
    use_html_login = os.environ.get('USE_HTML_LOGIN', 'false').lower() == 'true'
    
    # Store in session state for login page to access
    
    st.session_state.login_preference = use_html_login
    
    return use_html_login

# Get login preference
USE_HTML_LOGIN = get_login_preference()


# Initialize application only if logged in (to apply theme)
if st.session_state.get('logged_in', False):
    initialize_app()

# ============================================================================
# PAGE NAVIGATION
# ============================================================================

# Initialize session state for page navigation and authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'input'
if 'optimization_results' not in st.session_state:
    st.session_state.optimization_results = None

# Check for login URL parameters
query_params = st.query_params
if query_params.get('login') == '1' and not st.session_state.logged_in:
    st.session_state.logged_in = True
    # Clear the URL parameters after successful login
    st.query_params.clear()
    st.rerun()

def show_input_page():
    """Display the input configuration page."""
    render_header()
    

    
    # Compact Dashboard Style with Hover Focus Effects
    st.markdown("""
    <style>
    .wide-card {
        background: linear-gradient(135deg, rgba(212,175,55,0.1), rgba(244,208,63,0.05));
        border: 1px solid rgba(212,175,55,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .parameter-card {
        background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(244,208,63,0.05));
        border: 1px solid rgba(212,175,55,0.2);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .parameter-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(212,175,55,0.15);
        border-color: rgba(212,175,55,0.4);
    }
    .card-header {
        color: #d4af37;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    .wide-header {
        color: #d4af37;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    with st.container():
        # Top Section: Quality & Strategy (wrapped for hover effects)
        st.markdown('<div class="page-section quality-strategy focus-hover dim-on-hover">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
        <span class="section-icon">🎯</span>
        <span class="section-title">Quality & Strategy</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Quality & Strategy inputs in 3 columns
        # Centered row with inputs
        center = st.columns([1, 2, 1])[1]  # middle column
        with center:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                spec_bsw = st.number_input(
                    "🎯 Target BS&W (%)",
                    min_value=0.05, max_value=2.0,
                    value=0.5, step=0.05,
                    key="spec_bsw",
                    help="Maximum allowable BS&W content"
                )
            c1, c2, c3 = st.columns([1, 1, 1])
            with c2:
                n_samples = st.slider(
                    "🔬 Samples",
                    min_value=500, max_value=10000,
                    value=3000, step=500,
                    key="n_samples",
                    help="More samples = higher accuracy"
                )
            with c3:
                use_minimize_wash = st.toggle(
                    "🌊 Minimize Wash",
                    value=False,
                    key="use_minimize_wash",
                    help="Add wash water minimization as 5th priority"
                )
        # Priority ranking display (centered pills)
        st.markdown("""
        <div class="priority-info" aria-label="Optimization priority order" role="list">
        <span class="prio-pill" role="listitem" title="Primary objective">
            <span class="num">1</span> 📈 Maximize Flow
        </span>
        <span class="prio-pill" role="listitem" title="Reduce chemical cost">
            <span class="num">2</span> 💰 Minimize Chemical
        </span>
        <span class="prio-pill" role="listitem" title="Lower heating duty">
            <span class="num">3</span> 🌡️ Minimize Temperature
        </span>
        <span class="prio-pill" role="listitem" title="Lower electrical load">
            <span class="num">4</span> ⚡ Minimize Voltage
        </span>
        <span class="prio-pill" role="listitem" title="Save fresh water">
            <span class="num">5</span> 💧 Minimize Wash
        </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close quality-strategy-section
        
        # Add space before Operating Parameters section
        st.markdown("<br>", unsafe_allow_html=True)
        
    with st.container():
        # Middle Section: Parameter Grid (wrapped for hover effects)
        st.markdown('<div class="page-section parameters focus-hover dim-on-hover">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
        <span class="section-icon">📊</span>
        <span class="section-title">Operating Parameters</span>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            with st.expander("🏭 Process Flow", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    flow_min = st.number_input("Min Flow (BPD)", 20000.0, step=1000.0, key="flow_min")
                with c2:
                    flow_max = st.number_input("Max Flow (BPD)", 60000.0, step=1000.0, key="flow_max")

        with col2:
            with st.expander("🌡️ Temperature Control", expanded=True):
                t1, t2 = st.columns(2)
                with t1:
                    T_min = st.number_input("Min Temp (°C)", value=105.0, step=1.0, key="T_min")
                with t2:
                    T_max = st.number_input("Max Temp (°C)", value=130.0, step=1.0, key="T_max")

        col3, col4 = st.columns(2)
        with col3:
            with st.expander("⚡ Electrical Settings", expanded=True):
                v1, v2 = st.columns(2)
                with v1:
                    V_min = st.number_input("Min Voltage (kV)", value=22.0, step=1.0, key="V_min")
                with v2:
                    V_max = st.number_input("Max Voltage (kV)", value=32.0, step=1.0, key="V_max")

        with col4:
            with st.expander("💧 Chemical Treatment", expanded=True):
                p1, p2 = st.columns(2)
                with p1:
                    ppm_min = st.number_input("Min Demulsifier (ppm)", value=10.0, step=1.0, key="ppm_min")
                with p2:
                    ppm_max = st.number_input("Max Demulsifier (ppm)", value=90.0, step=1.0, key="ppm_max")

        # ---- Row: Wash Water | (leave second column for next card or empty) ----
        col5, col6 = st.columns(2)

        with col5:
            with st.expander("🚿 Wash Water System", expanded=True):
                w1, w2 = st.columns(2)
                with w1:
                    wash_min = st.number_input("Min Wash (% crude)", value=0.5, step=0.1, format="%.1f", key="wash_min")
                with w2:
                    wash_max = st.number_input("Max Wash (% crude)", value=4.0, step=0.1, format="%.1f", key="wash_max")
        with col6:
            with st.expander("⚙️ Advanced Options", expanded=True):
                st.info("💡 **Tip:** Use default ranges for most applications. Adjust only if you have specific facility constraints.")
                st.markdown("**Design Flow Rate:** 30,000 BPD")
                st.markdown("**Optimization Method:** Lexicographic")
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close parameters-section

    

    # Store parameters in session state
    st.session_state.parameters = {
        'spec_bsw': spec_bsw,
        'n_samples': n_samples,
        'flow_min': flow_min,
        'flow_max': flow_max,
        'T_min': T_min,
        'T_max': T_max,
        'V_min': V_min,
        'V_max': V_max,
        'ppm_min': ppm_min,
        'ppm_max': ppm_max,
        'wash_min': wash_min,
        'wash_max': wash_max,
        'use_minimize_wash': use_minimize_wash
    }
    
    # Optimization button in the middle
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        if st.button("🚀 Start Optimization", type="primary", use_container_width=True):
            st.session_state.current_page = 'progress'
            st.empty()
            st.rerun()

def show_progress_page():
    """Display the optimization progress page only."""
    # Render fresh header
    #render_header()
    st.empty()
    st.empty()
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: #d4af37; font-size: 2rem; margin-bottom: 1rem;">🔬 Optimization in Progress</h2>
        <p style="color: #9ca3af; font-size: 1.1rem;">Analyzing parameter space and finding optimal solutions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show progress animation
    show_optimization_progress()
    
    # Execute optimization
    params = st.session_state.parameters
    ranges = {
        "flow_bpd": (params['flow_min'], params['flow_max']),
        "T": (params['T_min'], params['T_max']),
        "V": (params['V_min'], params['V_max']),
        "ppm": (params['ppm_min'], params['ppm_max']),
        "wash_pct": (params['wash_min'], params['wash_max']),
    }
    priorities = ["flow_bpd", "ppm", "T", "V"] + (["wash_pct"] if params['use_minimize_wash'] else [])
    
    optimizer = DesalterOptimizer()
    df_dict, cols = optimizer.optimize_multiobjective(
        n_samples=params['n_samples'], 
        ranges=ranges, 
        spec_bsw=params['spec_bsw'], 
        priorities=priorities
    )
    best_idx, feasible_mask = optimizer.select_optimal_lexicographic(df_dict, priorities)
    
    # Store results
    st.session_state.optimization_results = {
        'data': pd.DataFrame(df_dict),
        'best_idx': best_idx,
        'feasible_mask': feasible_mask,
        'params': params
    }
    
    # Show success message
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(21, 128, 61, 0.1)); 
                    border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 16px; padding: 2rem;">
            <h3 style="color: #22c55e; margin-bottom: 1rem;">✅ Successfully Done!</h3>
            <p style="color: #9ca3af; margin-bottom: 1.5rem;">Optimization completed successfully. Ready to view results.</p>
            <div style="display: inline-block; animation: pulse 1s ease-in-out infinite;">
                <span style="font-size: 2rem;">✨</span>
            </div>
        </div>
    </div>
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    time.sleep(1)  # Show success message for 1 second
    st.session_state.current_page = 'results'
    st.rerun()

def show_results_page():
    """Display the optimization results page."""
    st.empty()
    time.sleep(1)
    st.empty()
    st.empty()
    
    # Auto-scroll to top of page
    st.markdown("""
    <script>
    window.scrollTo(0, 0);
    </script>
    """, unsafe_allow_html=True)
    

    results = st.session_state.optimization_results
    data = results['data']
    best_idx = results['best_idx']
    params = results['params']
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 2rem 0; position: relative;">
        <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(255, 215, 0, 0.05)); 
                    border-radius: 24px; padding: 2.5rem; margin: 0 auto; max-width: 800px;
                    border: 1px solid rgba(212, 175, 55, 0.2); 
                    box-shadow: 0 8px 32px rgba(212, 175, 55, 0.1), 0 2px 8px rgba(0, 0, 0, 0.1);">
            <div style="display: inline-block; background: linear-gradient(135deg, #d4af37, #f4d03f); 
                        background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                        font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; letter-spacing: -0.02em;">
                📊 Optimization Results
            </div>
            <div style="height: 2px; width: 60px; background: linear-gradient(90deg, #d4af37, #f4d03f); 
                        margin: 1rem auto; border-radius: 2px;"></div>
            <p style="color: #e5e7eb; font-size: 1.2rem; font-weight: 400; margin: 0; opacity: 0.9;">
                Your optimal desalter operating parameters
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if best_idx is None:
        st.error("❌ **No feasible solution found.** Consider widening parameter ranges or relaxing BS&W specification.")
    else:
        best = data.iloc[best_idx]

        # Create metric cards in a responsive grid (centered)
    # Centered 6-column row
    center_col = st.columns([1, 10, 1])[1]  # makes the whole block centered
    with center_col:
        cols = st.columns(6)

        with cols[0]:
            st.markdown(f"<div style='font-size: 1.2rem;'><b>🏭 Flow Rate</b><br><br><strong>{best['flow_bpd']:,.0f} BPD</strong></div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"<div style='font-size: 1.2rem;'><b>💧 Demulsifier</b><br><br><strong>{best['ppm']:.0f} ppm</strong></div>", unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"<div style='font-size: 1.2rem;'><b>🌡️ Temperature</b><br><br><strong>{best['T']:.0f} °C</strong></div>", unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f"<div style='font-size: 1.2rem;'><b>⚡ Voltage</b><br><br><strong>{best['V']:.0f} kV</strong></div>", unsafe_allow_html=True)
        with cols[4]:
            st.markdown(f"<div style='font-size: 1.2rem;'><b>🚿 Wash Water</b><br><br><strong>{best['wash_pct']:.1f} % crude</strong></div>", unsafe_allow_html=True)
        with cols[5]:
            st.markdown(f"<div style='font-size: 1.2rem;'><b>🎯 BS&W Result</b><br><br><strong>{best['BSW']:.2f} % (✓ Compliant)</strong></div>", unsafe_allow_html=True)
        # Success message
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(21, 128, 61, 0.1)); 
                    border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; padding: 1rem; margin: 2rem 0;">
            <h4 style="color: #22c55e; margin: 0 0 0.5rem 0;">✅ Optimization Successful</h4>
            <p style="color: #9ca3af; margin: 0; font-size: 0.9rem;">
                Solution found using lexicographic optimization: maximized flow while meeting quality constraints and minimizing operational costs.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced Charts and Analysis
        render_advanced_charts(data, best_idx, params)

        # Summary card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(244, 208, 63, 0.1)); 
                    border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 16px; padding: 1.5rem; margin-top: 2rem;">
            <h4 style="color: #d4af37; margin: 0 0 1rem 0;">✨ Recommended Operating Point</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; color: #e5e7eb;">
                <div><strong>Flow:</strong> {best['flow_bpd']:,.0f} BPD</div>
                <div><strong>Demulsifier:</strong> {best['ppm']:.0f} ppm</div>
                <div><strong>Temperature:</strong> {best['T']:.0f}°C</div>
                <div><strong>Voltage:</strong> {best['V']:.0f} kV</div>
                <div><strong>Wash Water:</strong> {best['wash_pct']:.1f}%</div>
                <div><strong>BS&W:</strong> {best['BSW']:.2f}% ✓</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Back to input page button at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        if st.button("🔄 Back to Input Page", type="secondary", use_container_width=True):
            st.session_state.current_page = 'input'
            st.rerun()

# ============================================================================
# MAIN APPLICATION ROUTING
# ============================================================================

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    # Show login page
    show_login_page()
else:
    # Create main content area that can be cleared
    if 'main_container' not in st.session_state:
        st.session_state.main_container = st.empty()

    # Route to appropriate page with proper content clearing
    page = st.session_state.current_page

    if page == "input":
        with st.session_state.main_container.container():
            show_input_page()
    elif page == "progress":
        # Clear previous content completely
        st.session_state.main_container.empty()
        with st.session_state.main_container.container():
            show_progress_page()
    elif page == "results":
        with st.session_state.main_container.container():
            time.sleep(1)
            show_results_page()