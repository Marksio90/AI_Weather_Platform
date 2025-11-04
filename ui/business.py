from __future__ import annotations
import streamlit as st
from core.auth import User

def render_business_panel(user: User) -> None:
    st.markdown(
        f"""
        <div style="background: rgba(15, 23, 42, 0.35); border: 1px solid rgba(148, 163, 184, .2);
                    border-radius: 1rem; padding: 1rem 1.2rem; margin-bottom: 1rem;">
            <h3 style="margin:0 0 .5rem 0;">💼 Dane abonenta</h3>
            <p style="margin:0;">Użytkownik: <strong>{user.username}</strong></p>
            <p style="margin:0;">Plan: <strong>{user.plan.upper()}</strong></p>
            <p style="margin-top:.4rem; font-size:.75rem; color:#94a3b8;">
                Dostępność funkcji zależy od planu: Free → podstawy, Pro → radar i TTS, Enterprise → wszystko + SLA + walidacja.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
