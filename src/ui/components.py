"""UI components for the Desalter app."""

from __future__ import annotations

import streamlit as st
import time


def render_header() -> None:
    # Header with logout button
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col1:
        st.markdown("")  # Empty space
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0 1.5rem 0;">
            <h1 style="color: #d4af37; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                Desalter Optimization Suite
            </h1>
            <div style="background: linear-gradient(90deg, #d4af37, #f4d03f); height: 3px; width: 200px; margin: 0 auto 1rem; border-radius: 2px;"></div>
            <p style="color: #9ca3af; font-size: 1.1rem; line-height: 1.6; max-width: 800px; margin: 0 auto;">
                Advanced multi-objective optimization for petroleum desalting operations.<br>
                <span style="color: #d4af37; font-weight: 500;">Maximize throughput • Minimize costs • Ensure quality compliance</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Logout button
        if st.button("🚪 Logout", key="logout_btn", help="Sign out"):
            st.session_state.logged_in = False
            st.session_state.current_page = 'input'
            st.rerun()


def show_optimization_progress() -> None:
    """Display a big modern circular progress ring centered on the page."""

    import time
    import streamlit as st

    st.markdown("""
    <style>
    .progress-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      margin: 3rem auto;
    }

    .progress-title {
      color: #d4af37;
      font-weight: 700;
      font-size: 1.5rem;
      margin-bottom: 2rem;
    }

    /* Large circular progress ring */
    .ring {
      --size: 300px;      /* diameter */
      --thickness: 20px;  /* ring thickness */
      --val: 0;           /* 0–100 (set inline) */

      width: var(--size);
      height: var(--size);
      border-radius: 50%;
      background:
        conic-gradient(#d4af37 calc(var(--val)*1%), rgba(255,255,255,0.08) 0);
      display: grid;
      place-items: center;
      position: relative;
      margin-bottom: 2rem;
      box-shadow: 0 0 0 2px rgba(212,175,55,.25) inset, 0 10px 28px rgba(212,175,55,.25);
      transition: background .45s ease;
    }

    .ring::before {
      content: "";
      position: absolute;
      inset: calc(var(--thickness));
      border-radius: 50%;
      background: rgba(17,24,39,.9);
      box-shadow: inset 0 0 0 1px rgba(212,175,55,.15);
    }

    .ring .val {
      position: relative;
      z-index: 1;
      color: #f7e7b2;
      font-weight: 800;
      font-size: 2rem;
      font-variant-numeric: tabular-nums;
      text-shadow: 0 1px 0 rgba(0,0,0,.4);
    }
    .ring .val small {
      font-size: 1rem;
      opacity: .85;
      margin-left: 4px;
      font-weight: 600;
    }

    .status-line1 {
      color: #e5e7eb;
      font-size: 1.2rem;
      margin-bottom: 0.3rem;
    }

    .status-line2 {
      color: #9ca3af;
      font-size: 1rem;
    }

    @keyframes pop {
      0% { transform: scale(1); }
      50% { transform: scale(1.06); }
      100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

    container = st.container()
    ring_ph = st.empty()
    status1 = st.empty()
    status2 = st.empty()

    steps = [
        ("Initializing optimization engine…", "Loading core algorithms", 0.5),
        ("Analyzing parameter space…", "Generating Monte Carlo samples", 0.7),
        ("Evaluating combinations…", "Calculating BS&W responses", 1.5),
        ("Applying quality constraints…", "Filtering feasible solutions", 0.6),
        ("Lexicographic optimization…", "Ranking optimal solutions", 1.0),
        ("Finalizing results…", "Preparing visualizations", 0.6),
    ]

    with container:
        st.markdown('<div class="progress-wrap"><div class="progress-title">🔬 Optimization in Progress</div>', unsafe_allow_html=True)

    for i, (headline, sub, duration) in enumerate(steps):
        pct = int(round((i + 1) / len(steps) * 100))
        ring_ph.markdown(f"""
        <div class="progress-wrap">
          <div class="ring" style="--val:{pct};">
            <div class="val">{pct}<small>%</small></div>
          </div>
          <div class="status">
            <div class="status-line1">{headline}</div>
            <div class="status-line2">{sub}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(duration)

    # Final completion
    ring_ph.markdown(f"""
    <div class="progress-wrap">
      <div class="ring" style="--val:100; animation: pop 0.9s ease;">
        <div class="val">100<small>%</small></div>
      </div>
      <div class="status">
        <div class="status-line1" style="color:#22c55e;">✅ Optimization Complete!</div>
        <div class="status-line2">Results ready for analysis</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(0.5)

