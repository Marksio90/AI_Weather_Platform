from __future__ import annotations
import streamlit as st
from core.auth import User


# co który plan ma – to samo co w core/auth, ale tu tylko do pokazania w UI
PLAN_FEATURES_UI = {
    "free": ["✅ Podstawowa prognoza", "❌ Radar", "❌ TTS", "❌ Walidacja"],
    "pro": ["✅ Podstawowa prognoza", "✅ Radar", "✅ TTS", "❌ Walidacja"],
    "enterprise": ["✅ Wszystkie moduły", "✅ Radar", "✅ TTS", "✅ Walidacja", "✅ SLA"],
}

PLAN_COLORS = {
    "free": "rgba(148, 163, 184, 0.35)",
    "pro": "rgba(56, 189, 248, 0.20)",
    "enterprise": "rgba(190, 242, 100, 0.15)",
}


def render_business_panel(user: User) -> None:
    plan_key = user.plan.lower()
    features = PLAN_FEATURES_UI.get(plan_key, PLAN_FEATURES_UI["free"])
    bg_color = PLAN_COLORS.get(plan_key, "rgba(15, 23, 42, 0.35)")

    # badge koloru planu
    plan_badge = f"""
    <span style="
        background: rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(148, 163, 184, 0.35);
        border-radius: 9999px;
        padding: .15rem .75rem;
        font-size: .65rem;
        letter-spacing: .06em;
        text-transform: uppercase;
    ">{user.plan}</span>
    """

    features_html = "<ul style='margin: .5rem 0 0 1rem; padding:0; font-size:.70rem; color:#94a3b8;'>"
    for ftr in features:
        features_html += f"<li style='margin-bottom:.25rem;'>{ftr}</li>"
    features_html += "</ul>"

    st.markdown(
        f"""
        <div style="
            background: {bg_color};
            border: 1px solid rgba(148, 163, 184, .25);
            border-radius: 1rem;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        ">
            <div style="display:flex; justify-content: space-between; align-items: center;">
                <h3 style="margin:0 0 .5rem 0;">💼 Dane abonenta</h3>
                {plan_badge}
            </div>
            <p style="margin:0; font-size:.8rem;">Użytkownik: <strong>{user.username}</strong></p>
            <p style="margin:.25rem 0 .5rem 0; font-size:.8rem;">Plan: <strong>{user.plan.upper()}</strong></p>
            <p style="margin:0; font-size:.7rem; color:#94a3b8;">
                Dostępność funkcji zależy od planu:
            </p>
            {features_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
