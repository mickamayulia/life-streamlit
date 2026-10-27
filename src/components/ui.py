"""
UI Theme, Styling & Common Layout Helpers for Streamlit Dashboard
Provides custom CSS tokens, modern glassmorphism metric cards, and badge components.
"""

import streamlit as st


def apply_custom_css():
    """
    Applies custom modern CSS styles for typography, KPI cards, sidebar, and plot containers.
    """
    st.markdown(
        """
        <style>
        /* Import Modern Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Hide default Streamlit multipage navigation tabs at the very top of sidebar */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Style sidebar page links */
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            border-radius: 8px;
            padding: 8px 12px;
            margin-bottom: 4px;
            transition: all 0.2s ease;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
            background-color: rgba(2, 132, 199, 0.15) !important;
            transform: translateX(3px);
        }

        /* Metric Card Styling */
        .metric-card {
            background: linear-gradient(135deg, rgba(17, 24, 39, 0.8) 0%, rgba(31, 41, 55, 0.6) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 20px 24px;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            border-color: rgba(2, 132, 199, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 8px 28px -4px rgba(2, 132, 199, 0.25);
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: #0284c7;
            border-radius: 4px 0 0 4px;
        }

        .metric-card.accent-emerald::before { background: #10b981; }
        .metric-card.accent-amber::before { background: #f59e0b; }
        .metric-card.accent-rose::before { background: #f43f5e; }
        .metric-card.accent-indigo::before { background: #6366f1; }

        .metric-label {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #9ca3af;
            font-weight: 600;
            margin-bottom: 6px;
        }

        .metric-value {
            font-size: 2.1rem;
            font-weight: 800;
            color: #f9fafb;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }

        .metric-sub {
            font-size: 0.82rem;
            color: #6b7280;
            margin-top: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Hero Header Banner */
        .hero-banner {
            background: radial-gradient(circle at 10% 20%, rgba(2, 132, 199, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
                        linear-gradient(180deg, rgba(17, 24, 39, 0.9) 0%, rgba(11, 15, 25, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 28px 32px;
            margin-bottom: 24px;
        }

        .hero-title {
            font-size: 1.85rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
            letter-spacing: -0.02em;
        }

        .hero-subtitle {
            font-size: 0.98rem;
            color: #94a3b8;
            line-height: 1.5;
            max-width: 800px;
        }

        /* Status Badges */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.03em;
        }
        .badge-developing {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .badge-developed {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .badge-anomaly {
            background: rgba(244, 63, 94, 0.15);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.3);
        }

        /* Plotly Chart Container */
        .chart-container {
            background: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_hero(title: str, subtitle: str, badge: str = "GLOBAL HEALTH ANALYTICS"):
    """
    Renders a top hero banner with clean aesthetics.
    """
    st.markdown(
        f"""
        <div class="hero-banner">
            <span class="badge" style="background: rgba(2, 132, 199, 0.2); color: #38bdf8; border: 1px solid rgba(2, 132, 199, 0.4); margin-bottom: 10px;">{badge}</span>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metric_card(
    label: str,
    value: str,
    sub: str = "",
    accent: str = "blue"
):
    """
    Renders a styled metric card.
    accent: 'blue', 'emerald', 'amber', 'rose', 'indigo'
    """
    accent_class = f"accent-{accent}" if accent != "blue" else ""
    st.markdown(
        f"""
        <div class="metric-card {accent_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
