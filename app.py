        """
app.py
-------
ConsultIQ AI — main Streamlit entry point.

Handles login/session management and wires up role-based multipage
navigation. Run with:  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from auth.auth_manager import authenticate, has_permission, seed_demo_users
from config import settings
from database.db_manager import init_db
from ingestion.pipeline import get_or_create_store
from ui.components import inject_theme

st.set_page_config(
    page_title="ConsultIQ AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
seed_demo_users()
inject_theme()

if "user" not in st.session_state:
    st.session_state.user = None
if "store" not in st.session_state:
    st.session_state.store = get_or_create_store()
if "chat_session_id" not in st.session_state:
    import uuid

    st.session_state.chat_session_id = str(uuid.uuid4())


def login_view() -> None:
    left, right = st.columns([1, 1])
    with left:
        st.markdown(
            f"""
            <div style="padding-top:3rem;">
            <h1 style="color:#1E2761; font-size:2.6rem;">🧠 ConsultIQ AI</h1>
            <p style="font-size:1.05rem; color:#4B5563; max-width:32rem;">
            Enterprise Knowledge Intelligence Platform — semantic search,
            RAG-powered chat, proposal recommendations, and analytics across
            your firm's proposals, SOWs, case studies, and project reports.
            </p>
            <span class="ciq-badge">Educational / Portfolio Build — Synthetic Data Only</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("### Sign in")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            user = authenticate(username, password)
            if user is None:
                st.error("Invalid username or password.")
            else:
                st.session_state.user = user
                st.rerun()

        with st.expander("Demo credentials"):
            st.code(
                "admin        / Admin@123      (full access)\n"
                "consultant   / Consult@123    (upload, chat, search, recommend)\n"
                "viewer       / Viewer@123     (search, chat only)",
                language="text",
            )


def build_navigation() -> st.navigation:
    user = st.session_state.user
    pages = [st.Page("ui/pages/1_upload.py", title="Upload Documents", icon="📤")]
    pages.append(st.Page("ui/pages/2_chat.py", title="AI Chat Assistant", icon="💬"))
    pages.append(st.Page("ui/pages/3_search.py", title="Semantic Search", icon="🔍"))
    pages.append(st.Page("ui/pages/4_dashboard.py", title="Analytics Dashboard", icon="📊"))
    if has_permission(user.role, "recommend"):
        pages.append(st.Page("ui/pages/5_recommendations.py", title="Proposal Recommender", icon="📋"))
    if has_permission(user.role, "admin_console"):
        pages.append(st.Page("ui/pages/6_admin.py", title="Admin Console", icon="⚙️"))
    return st.navigation(pages)


if st.session_state.user is None:
    login_view()
else:
    with st.sidebar:
        st.markdown(f"**{st.session_state.user.full_name}**")
        st.caption(f"Role: {st.session_state.user.role.capitalize()}")
        st.caption(f"LLM provider: `{settings.llm_provider}`")
        if st.button("Log out", use_container_width=True):
            st.session_state.user = None
            st.rerun()
        st.divider()

    nav = build_navigation()
    nav.run()
