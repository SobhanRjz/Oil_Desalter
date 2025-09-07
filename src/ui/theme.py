"""UI theme application utilities."""

from __future__ import annotations

import pathlib
import streamlit as st


class ThemeManager:
    """Injects external CSS into Streamlit app."""

    def __init__(self, css_path: str = "assets/luxury.css") -> None:
        self._css_path = css_path

    def apply(self) -> None:
        css_file = pathlib.Path(self._css_path)
        if css_file.exists():
            st.markdown(f"<style>{css_file.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
        else:
            st.warning("Custom theme CSS not found. Falling back to default styling.")


