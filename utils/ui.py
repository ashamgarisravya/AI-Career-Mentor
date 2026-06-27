"""Reusable Streamlit UI components for the AI Career Mentor app."""

from __future__ import annotations

from collections.abc import Iterable
from html import escape

import streamlit as st


def inject_styles() -> None:
    """Apply shared SaaS-style spacing, typography, and component styling."""
    st.markdown(
        """
        <style>
        :root {
            --mentor-bg: #f7f9fc;
            --mentor-card: #ffffff;
            --mentor-border: #dbe3ef;
            --mentor-muted: #667085;
            --mentor-text: #101828;
            --mentor-blue: #2563eb;
            --mentor-teal: #0f766e;
            --mentor-green: #15803d;
            --mentor-amber: #b45309;
            --mentor-red: #b91c1c;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1220px;
        }
        h1, h2, h3 {
            letter-spacing: 0;
            color: var(--mentor-text);
        }
        div[data-testid="stMetric"] {
            background: var(--mentor-card);
            border: 1px solid var(--mentor-border);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
        }
        div[data-testid="stMetricLabel"] p {
            color: var(--mentor-muted);
            font-weight: 600;
        }
        .mentor-hero {
            border: 1px solid var(--mentor-border);
            border-radius: 8px;
            background: linear-gradient(135deg, #ffffff 0%, #f4f8ff 54%, #effaf8 100%);
            padding: 1.1rem 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(16, 24, 40, 0.06);
        }
        .mentor-kicker {
            color: var(--mentor-blue);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.3rem;
        }
        .mentor-title {
            font-size: 2rem;
            line-height: 1.15;
            font-weight: 750;
            margin: 0;
        }
        .mentor-subtitle {
            color: var(--mentor-muted);
            margin-top: 0.45rem;
            max-width: 760px;
        }
        .mentor-badges {
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
            margin-top: 0.8rem;
        }
        .mentor-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            border: 1px solid var(--mentor-border);
            border-radius: 999px;
            padding: 0.2rem 0.55rem;
            background: #ffffff;
            color: #344054;
            font-size: 0.78rem;
            font-weight: 650;
        }
        .mentor-badge.success { color: var(--mentor-green); background: #ecfdf3; border-color: #bbf7d0; }
        .mentor-badge.warning { color: var(--mentor-amber); background: #fffbeb; border-color: #fde68a; }
        .mentor-badge.danger { color: var(--mentor-red); background: #fef2f2; border-color: #fecaca; }
        .mentor-badge.info { color: var(--mentor-blue); background: #eff6ff; border-color: #bfdbfe; }
        .mentor-panel {
            border: 1px solid var(--mentor-border);
            border-radius: 8px;
            background: var(--mentor-card);
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
        }
        .mentor-panel-title {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            color: var(--mentor-text);
        }
        .mentor-panel-copy {
            color: var(--mentor-muted);
            font-size: 0.9rem;
            margin-bottom: 0.6rem;
        }
        .mentor-list {
            margin: 0.2rem 0 0 0;
            padding-left: 1rem;
            color: #344054;
        }
        .mentor-list li {
            margin-bottom: 0.25rem;
        }
        .mentor-quick-link {
            display: block;
            border: 1px solid var(--mentor-border);
            border-radius: 8px;
            padding: 0.65rem 0.8rem;
            margin-bottom: 0.5rem;
            background: #ffffff;
            text-decoration: none;
            color: #1d4ed8 !important;
            font-weight: 650;
        }
        .mentor-divider {
            height: 1px;
            background: var(--mentor-border);
            margin: 0.8rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str, badge_items: Iterable[tuple[str, str]] = ()) -> None:
    """Render a consistent page header."""
    badges = "".join(
        f'<span class="mentor-badge {escape(kind)}">{escape(label)}</span>'
        for label, kind in badge_items
    )
    badge_block = f'<div class="mentor-badges">{badges}</div>' if badges else ""
    st.markdown(
        f"""
        <div class="mentor-hero">
            <div class="mentor-kicker">AI Career Mentor</div>
            <h1 class="mentor-title">{escape(title)}</h1>
            <div class="mentor-subtitle">{escape(subtitle)}</div>
            {badge_block}
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(label: str, kind: str = "info") -> str:
    """Return a styled badge snippet for markdown blocks."""
    return f'<span class="mentor-badge {escape(kind)}">{escape(label)}</span>'


def panel(title: str, copy: str = "") -> None:
    """Render a compact panel heading inside Streamlit containers."""
    st.markdown(
        f"""
        <div class="mentor-panel-title">{escape(title)}</div>
        {f'<div class="mentor-panel-copy">{escape(copy)}</div>' if copy else ''}
        """,
        unsafe_allow_html=True,
    )


def bullet_list(items: Iterable[str]) -> None:
    """Render a styled list of text items."""
    html = "".join(f"<li>{escape(str(item))}</li>" for item in items)
    st.markdown(f'<ul class="mentor-list">{html}</ul>', unsafe_allow_html=True)


def empty_state(title: str, message: str) -> None:
    """Render a consistent empty state."""
    st.markdown(
        f"""
        <div class="mentor-panel">
            <div class="mentor-panel-title">{escape(title)}</div>
            <div class="mentor-panel-copy">{escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_kind(score: int) -> str:
    """Map a score to a badge style."""
    if score >= 75:
        return "success"
    if score >= 50:
        return "warning"
    return "danger"
