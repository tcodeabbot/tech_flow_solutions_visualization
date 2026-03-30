import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TechFlow Solutions — Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

is_dark = st.session_state.theme == "Dark"

# ─── Branding Colours ──────────────────────────────────────────────────────────
GOLD = "#BF994A"

if is_dark:
    NAVY = "#e9eaec"
    DARK_NAVY = "#1a2233"
    WHITE = "#FFFFFF"
    LIGHT_BG = "#0f1523"
    CARD_BG = "#1a2233"
    GRID_COLOR = "#2a3449"
    TEXT_COLOR = "#e9eaec"
    POS_COLOR = "#4CAF50"
    NEG_COLOR = "#EF5350"
    APP_GRADIENT = f"linear-gradient(135deg, {LIGHT_BG} 0%, #131926 100%)"
else:
    NAVY = "#334366"
    DARK_NAVY = "#232d44"
    WHITE = "#FFFFFF"
    LIGHT_BG = "#F7F9FC"
    CARD_BG = "#FFFFFF"
    GRID_COLOR = "#eaedf3"
    TEXT_COLOR = NAVY
    POS_COLOR = "#2E7D32"
    NEG_COLOR = "#C62828"
    APP_GRADIENT = f"linear-gradient(135deg, {LIGHT_BG} 0%, #eef1f8 100%)"

# Categorical colors: blue / amber / violet / cyan — distinguishable for common CVD; no red–green pairs
if is_dark:
    PRODUCT_COLORS = {
        "Software": "#7EB8FF",
        "Cloud Services": "#E8C547",
        "Security": "#C9A0FF",
        "Services": "#5ED4E0",
    }
    REGION_COLORS = {
        "Northeast": "#7EB8FF",
        "Southeast": "#E8C547",
        "Midwest": "#C9A0FF",
        "West": "#5ED4E0",
    }
else:
    PRODUCT_COLORS = {
        "Software": "#2E5AAC",
        "Cloud Services": "#B8860B",
        "Security": "#5C3D8C",
        "Services": "#007C92",
    }
    REGION_COLORS = {
        "Northeast": "#2E5AAC",
        "Southeast": "#B8860B",
        "Midwest": "#5C3D8C",
        "West": "#007C92",
    }

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    /* Global background */
    .stApp {{
        background: {APP_GRADIENT};
    }}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background: {DARK_NAVY};
    }}
    section[data-testid="stSidebar"] * {{
        color: {WHITE} !important;
    }}
    section[data-testid="stSidebar"] .stButton button {{
        background-color: {GOLD} !important;
        border: none !important;
        border-radius: 8px !important;
    }}
    section[data-testid="stSidebar"] .stButton button * {{
        color: {DARK_NAVY} !important;
        fill: {DARK_NAVY} !important;
        font-weight: 700 !important;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background-color: #d4af58 !important;
    }}
    section[data-testid="stSidebar"] .stRadio label {{
        color: {WHITE} !important;
    }}

    /* KPI Cards */
    .kpi-card {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 22px 18px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 4px solid {GOLD};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.14);
    }}
    .kpi-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {TEXT_COLOR};
        margin: 4px 0;
    }}
    .kpi-label {{
        font-size: 0.85rem;
        color: #8e99b0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .kpi-delta {{
        font-size: 0.8rem;
        color: {POS_COLOR};
        margin-top: 2px;
    }}
    .kpi-delta.negative {{
        color: {NEG_COLOR};
    }}

    /* Section headers */
    .section-header {{
        font-size: 1.15rem;
        font-weight: 600;
        color: {TEXT_COLOR};
        margin: 14px 0 6px 0;
        padding-bottom: 4px;
        border-bottom: 2px solid {GOLD};
        display: inline-block;
    }}

    /* Dashboard title */
    .dashboard-title {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {TEXT_COLOR};
        margin-bottom: 4px;
    }}
    .dashboard-subtitle {{
        font-size: 1rem;
        color: #8e99b0;
        margin-bottom: 24px;
    }}

    /* Header styling and collapse icon visibility */
    header[data-testid="stHeader"] {{
        background: transparent;
    }}
    header[data-testid="stHeader"] button, 
    header[data-testid="stHeader"] button * {{
        fill: {TEXT_COLOR} !important;
        stroke: {TEXT_COLOR} !important;
        color: {TEXT_COLOR} !important;
    }}
    [data-testid="collapsedControl"] {{
        color: {TEXT_COLOR} !important;
    }}
    [data-testid="collapsedControl"] * {{
        fill: {TEXT_COLOR} !important;
        stroke: {TEXT_COLOR} !important;
        color: {TEXT_COLOR} !important;
    }}

    /* Constrain max width for large screens */
    .block-container {{
        max-width: 1550px;
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }}

    /* @st.dialog modal: Streamlit keeps a light panel; app TEXT_COLOR is light in dark mode → fix contrast */
    div[role="dialog"] {{
        background: #f7f9fc !important;
        color: #1a2233 !important;
    }}
    div[role="dialog"] h1,
    div[role="dialog"] h2,
    div[role="dialog"] h3,
    div[role="dialog"] p,
    div[role="dialog"] li,
    div[role="dialog"] ul,
    div[role="dialog"] strong,
    div[role="dialog"] b,
    div[role="dialog"] i,
    div[role="dialog"] .stMarkdown,
    div[role="dialog"] [data-testid="stMarkdownContainer"] {{
        color: #1a2233 !important;
    }}
    div[role="dialog"] hr {{
        border-color: {GOLD} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ─── Info Dialog ───────────────────────────────────────────────────────────────
@st.dialog("📖 Dashboard Instructions")
def show_instructions():
    # Fixed light-panel colors: dialog shell stays light even when app “dark” theme uses light TEXT_COLOR elsewhere.
    _dlg_bg = "#f0f3f8"
    _dlg_text = "#1a2233"
    _dlg_muted = "#4a5568"
    st.markdown(
        f"""
    <div style="background:{_dlg_bg};color:{_dlg_text};padding:14px 16px;border-radius:12px;line-height:1.55;border:1px solid #dde3ed;">
    <h3 style="color:{_dlg_text};margin-top:0;">Welcome to TechFlow Solutions</h3>
    <p style="color:{_dlg_text};"><b>How to Navigate:</b></p>
    <ul style="color:{_dlg_text};">
        <li><b>Dashboard Selection</b>: Use the radio buttons in the left sidebar to toggle between the <i>Executive Dashboard</i> and the <i>Operations Dashboard</i>.</li>
        <li><b>Filtering Data</b>: Use the multi-select dropdowns to filter metrics and charts by specific Regions or Product Categories dynamically.</li>
        <li><b>Theming</b>: Switch between Light and Dark mode using the sidebar toggle for your preferred viewing experience.</li>
        <li><b>Interactivity</b>: Hover over any chart to view exact data points, or double-click to reset zooming.</li>
    </ul>
    <br>
    <hr style="border-top:1px solid {GOLD};margin:12px 0;">
    <p style="font-size:0.9em;text-align:center;margin-bottom:0;color:{_dlg_muted};">
        <b style="color:{_dlg_text};">Authors:</b> Abbot Tubeine, Harrison Herschberger
    </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df["date_label"] = df["date"].dt.strftime("%Y-%m-%d")
    return df


df = load_data()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div style='text-align:center; padding: 18px 0 10px 0;'>
            <svg width="60" height="60" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 6px;">
                <path d="M4 18L12 4L20 18H4Z" fill="{GOLD}" fill-opacity="0.9"/>
                <path d="M16 26L26 8L30 14.5L19 32.5L16 26Z" fill="{TEXT_COLOR}" fill-opacity="0.85"/>
            </svg>
            <br>
            <span style='font-size:1.4rem; font-weight:800; color:{GOLD}; letter-spacing: 0.5px;'>TECHFLOW</span><br>
            <span style='font-size:0.75rem; color:#8e99b0; text-transform:uppercase; letter-spacing: 1.5px; font-weight: 600;'>Solutions</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    
    if st.button("Dashboard Guide", icon=":material/info:", use_container_width=True):
        show_instructions()
    
    def toggle_theme():
        st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"
        
    st.toggle("Dark Theme", value=is_dark, on_change=toggle_theme)
    st.markdown("---")
    
    dashboard = st.radio(
        "Select Dashboard",
        ["Executive Analytics", "Operations Engine"],
        index=0,
    )
    st.markdown("---")

    # Filters
    st.markdown(
        f"<p style='font-weight:600; color:{GOLD}; margin-bottom:4px;'>Filters</p>",
        unsafe_allow_html=True,
    )
    regions = st.multiselect(
        "Region", df["region"].unique().tolist(), default=df["region"].unique().tolist()
    )
    products = st.multiselect(
        "Product Category",
        df["product_category"].unique().tolist(),
        default=df["product_category"].unique().tolist(),
    )

# Apply filters
mask = df["region"].isin(regions) & df["product_category"].isin(products)
fdf = df[mask].copy()

# ─── Helper: Plotly Layout Defaults ───────────────────────────────────────────
LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=TEXT_COLOR),
    margin=dict(t=50, b=40, l=50, r=20),
    hovermode="x unified",
)


def styled_fig(fig, height=420):
    fig.update_layout(**LAYOUT_DEFAULTS, height=height)
    fig.update_xaxes(gridcolor=GRID_COLOR, zeroline=False, showline=True, linewidth=1, linecolor=TEXT_COLOR, automargin=True)
    fig.update_yaxes(gridcolor=GRID_COLOR, zeroline=False, showline=True, linewidth=1, linecolor=TEXT_COLOR, automargin=True)
    return fig


def compact_line_hover(fig, *, currency: bool = True, dollars_as_k: bool = False):
    """Hover: 'Cloud Services, March 01, 2024, $126K' (y in thousands when dollars_as_k)."""
    if currency and dollars_as_k:
        yfmt = "$%{y:,.0f}K"
    elif currency:
        yfmt = "$%{y:,.0f}"
    else:
        yfmt = "%{y}"
    for tr in fig.data:
        if getattr(tr, "type", None) != "scatter":
            continue
        mode = getattr(tr, "mode", "") or ""
        if "lines" not in mode:
            continue
        name = getattr(tr, "name", "") or "Series"
        tr.hovertemplate = f"{name}, %{{x|%B %d, %Y}}, {yfmt}<extra></extra>"


def compact_bar_hover(
    fig,
    *,
    currency: bool = False,
    currency_decimals: int = 0,
    dollars_as_k: bool = False,
    percent: bool = False,
    percent_decimals: int = 2,
    include_legend_name: bool = False,
):
    """Bar hover: 'Northeast, $125.5K' or 'Northeast, Software, 2.35%' — no axis= labels."""
    if currency and dollars_as_k:
        ypart = "$%{y:,.0f}K"
    elif currency:
        if currency_decimals == 0:
            ypart = "$%{y:,.0f}"
        else:
            ypart = f"$%{{y:,.{currency_decimals}f}}"
    elif percent:
        ypart = f"%{{y:.{percent_decimals}f}}%"
    else:
        ypart = "%{y}"
    for tr in fig.data:
        if getattr(tr, "type", None) != "bar":
            continue
        name = getattr(tr, "name", "") or ""
        if include_legend_name and name:
            tr.hovertemplate = f"%{{x}}, {name}, {ypart}<extra></extra>"
        else:
            tr.hovertemplate = f"%{{x}}, {ypart}<extra></extra>"


def compact_scatter_hover_spend_profit(fig):
    """Marketing vs profit (full dollars): 'Software, Spend $1,200, Profit $4,950'."""
    for tr in fig.data:
        if getattr(tr, "type", None) != "scatter":
            continue
        mode = getattr(tr, "mode", "") or ""
        if "markers" not in mode:
            continue
        name = getattr(tr, "name", "") or "Series"
        tr.hovertemplate = (
            f"{name}, Spend $%{{x:,.0f}}, Profit $%{{y:,.0f}}<extra></extra>"
        )


def kpi_card(label, value, delta=None, delta_negative=False):
    delta_html = ""
    if delta:
        cls = "negative" if delta_negative else ""
        delta_html = f'<div class="kpi-delta {cls}">{delta}</div>'
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


# ═══════════════════════════════════════════════════════════════════════════════
#  EXECUTIVE DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if "Executive" in dashboard:
    st.markdown(
        '<div class="dashboard-title">Executive Dashboard</div>'
        '<div class="dashboard-subtitle">TechFlow Solutions — Q1 2024 Performance Overview</div>',
        unsafe_allow_html=True,
    )

    # ── KPI Calculations ──────────────────────────────────────────────────────
    total_revenue = fdf["revenue"].sum()
    total_profit = fdf["profit"].sum()
    profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0
    avg_satisfaction = fdf["customer_satisfaction"].mean()

    first_date_rev = fdf[fdf["date"] == fdf["date"].min()]["revenue"].sum()
    last_date_rev = fdf[fdf["date"] == fdf["date"].max()]["revenue"].sum()
    rev_growth = (
        ((last_date_rev - first_date_rev) / first_date_rev * 100)
        if first_date_rev
        else 0
    )

    # ── KPI Cards (3 cards) ───────────────────────────────────────────────────
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            kpi_card(
                "Total Revenue",
                f"${total_revenue/1_000_000:,.2f}M",
                f"+{rev_growth:.1f}% growth",
            ),
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            kpi_card("Gross Profit", f"${total_profit/1_000:,.0f}K"),
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            kpi_card("Profit Margin", f"{profit_margin:.1f}%"),
            unsafe_allow_html=True,
        )

    # ── Row 1 of Charts: Pie Revenue by Product | Revenue Trend by Product ──
    col_1, col_2 = st.columns(2)
    
    with col_1:
        st.markdown(
            '<div class="section-header">Revenue by Product Line</div>',
            unsafe_allow_html=True,
        )
        prod_rev = fdf.groupby("product_category")["revenue"].sum().reset_index()
        prod_rev["revenue_k"] = prod_rev["revenue"] / 1000
        fig1 = px.bar(
            prod_rev,
            x="product_category",
            y="revenue_k",
            color="product_category",
            color_discrete_map=PRODUCT_COLORS,
            labels={"product_category": "Product", "revenue_k": "Revenue ($K)"},
        )
        fig1.update_yaxes(tickprefix="$", tickformat=",.0f", ticksuffix="K")
        fig1.update_layout(showlegend=False)
        compact_bar_hover(fig1, currency=True, dollars_as_k=True)
        st.plotly_chart(styled_fig(fig1, 340), use_container_width=True, theme=None)

    with col_2:
        st.markdown(
            '<div class="section-header">Revenue Trend by Product Line</div>',
            unsafe_allow_html=True,
        )
        trend = fdf.groupby(["month", "product_category"])["revenue"].sum().reset_index()
        trend["revenue_k"] = trend["revenue"] / 1000
        fig2 = px.line(
            trend,
            x="month",
            y="revenue_k",
            color="product_category",
            color_discrete_map=PRODUCT_COLORS,
            markers=True,
            labels={
                "month": "Month",
                "revenue_k": "Revenue ($K)",
                "product_category": "Product Line",
            },
        )
        fig2.update_traces(line=dict(width=2.5), marker=dict(size=7))
        compact_line_hover(fig2, currency=True, dollars_as_k=True)
        fig2.update_yaxes(tickprefix="$", tickformat=",.0f", ticksuffix="K")
        fig2.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(styled_fig(fig2, 340), use_container_width=True, theme=None)

    # ── Row 2 of Charts: Revenue by Region (bar) | Revenue Trend by Region (line) ──
    col_3, col_4 = st.columns(2)

    with col_3:
        st.markdown(
            '<div class="section-header">Revenue by Region</div>',
            unsafe_allow_html=True,
        )
        reg_rev = fdf.groupby("region")["revenue"].sum().reset_index()
        reg_rev["revenue_k"] = reg_rev["revenue"] / 1000
        fig3 = px.bar(
            reg_rev,
            x="region",
            y="revenue_k",
            color="region",
            color_discrete_map=REGION_COLORS,
            labels={"region": "Region", "revenue_k": "Revenue ($K)"},
        )
        fig3.update_yaxes(tickprefix="$", tickformat=",.0f", ticksuffix="K")
        fig3.update_layout(showlegend=False)
        compact_bar_hover(fig3, currency=True, dollars_as_k=True)
        st.plotly_chart(styled_fig(fig3, 340), use_container_width=True, theme=None)

    with col_4:
        st.markdown(
            '<div class="section-header">Revenue Trend by Region</div>',
            unsafe_allow_html=True,
        )
        reg_trend = fdf.groupby(["month", "region"])["revenue"].sum().reset_index()
        reg_trend["revenue_k"] = reg_trend["revenue"] / 1000
        fig4 = px.line(
            reg_trend,
            x="month",
            y="revenue_k",
            color="region",
            color_discrete_map=REGION_COLORS,
            markers=True,
            labels={
                "month": "Month",
                "revenue_k": "Revenue ($K)",
                "region": "Region",
            },
        )
        fig4.update_traces(line=dict(width=2.5), marker=dict(size=7))
        compact_line_hover(fig4, currency=True, dollars_as_k=True)
        fig4.update_yaxes(tickprefix="$", tickformat=",.0f", ticksuffix="K")
        fig4.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(styled_fig(fig4, 340), use_container_width=True, theme=None)


# ═══════════════════════════════════════════════════════════════════════════════
#  OPERATIONS DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown(
        '<div class="dashboard-title">Operations Dashboard</div>'
        '<div class="dashboard-subtitle">TechFlow Solutions — Q1 2024 Operational Insights</div>',
        unsafe_allow_html=True,
    )

    # ── Ops KPI Calculations ──────────────────────────────────────────────────
    avg_return_rate = fdf["return_rate"].mean() * 100
    fdf_units = fdf[fdf["units_sold"] > 0]
    avg_profit_per_unit = (
        (fdf_units["profit"].sum() / fdf_units["units_sold"].sum())
        if fdf_units["units_sold"].sum()
        else 0
    )
    avg_satisfaction = fdf["customer_satisfaction"].mean()
    total_customers = fdf["customer_count"].sum()

    # ── Ops KPI Cards ─────────────────────────────────────────────────────────
    o1, o2, o3, o4 = st.columns(4)
    with o1:
        st.markdown(
            kpi_card("Avg Return Rate", f"{avg_return_rate:.2f}%"),
            unsafe_allow_html=True,
        )
    with o2:
        st.markdown(
            kpi_card("Profit / Unit", f"${avg_profit_per_unit:,.0f}"),
            unsafe_allow_html=True,
        )
    with o3:
        st.markdown(
            kpi_card("Avg Satisfaction", f"{avg_satisfaction:.2f} / 5"),
            unsafe_allow_html=True,
        )
    with o4:
        st.markdown(
            kpi_card("Total Customers", f"{total_customers:,}"),
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ── Return Rate by Product & Region ───────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown(
            '<div class="section-header">Avg Return Rate by Product</div>',
            unsafe_allow_html=True,
        )
        rr_prod = (
            fdf.groupby("product_category")["return_rate"]
            .mean()
            .reset_index()
        )
        rr_prod["return_rate_pct"] = rr_prod["return_rate"] * 100
        fig = px.bar(
            rr_prod,
            x="product_category",
            y="return_rate_pct",
            color="product_category",
            color_discrete_map=PRODUCT_COLORS,
            labels={
                "product_category": "Product",
                "return_rate_pct": "Return Rate (%)",
            },
        )
        fig.update_yaxes(ticksuffix="%")
        fig.update_layout(showlegend=False)
        compact_bar_hover(fig, percent=True)
        st.plotly_chart(styled_fig(fig, 380), use_container_width=True, theme=None)

    with col_r:
        st.markdown(
            '<div class="section-header">Avg Return Rate by Region & Product</div>',
            unsafe_allow_html=True,
        )
        rr_rp = (
            fdf.groupby(["region", "product_category"])["return_rate"]
            .mean()
            .reset_index()
        )
        rr_rp["return_rate_pct"] = rr_rp["return_rate"] * 100
        fig = px.bar(
            rr_rp,
            x="region",
            y="return_rate_pct",
            color="product_category",
            color_discrete_map=PRODUCT_COLORS,
            barmode="stack",
            labels={
                "region": "Region",
                "return_rate_pct": "Return Rate (%)",
                "product_category": "Product",
            },
        )
        fig.update_yaxes(ticksuffix="%")
        fig.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            )
        )
        compact_bar_hover(fig, percent=True, include_legend_name=True)
        st.plotly_chart(styled_fig(fig, 380), use_container_width=True, theme=None)

    # ── Profit Per Unit ───────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Profit Per Unit by Product Category</div>',
        unsafe_allow_html=True,
    )
    fdf_pu = fdf[fdf["units_sold"] > 0]
    ppu = (
        fdf_pu.groupby("product_category")
        .apply(lambda x: x["profit"].sum() / x["units_sold"].sum())
        .reset_index(name="profit_per_unit")
    )
    fig = px.bar(
        ppu,
        x="product_category",
        y="profit_per_unit",
        color="product_category",
        color_discrete_map=PRODUCT_COLORS,
        labels={
            "product_category": "Product Category",
            "profit_per_unit": "Profit / Unit ($)",
        },
    )
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    fig.update_layout(showlegend=False)
    compact_bar_hover(fig, currency=True, currency_decimals=0)
    st.plotly_chart(styled_fig(fig, 400), use_container_width=True, theme=None)

    # ── Scatter Plots ─────────────────────────────────────────────────────────
    col_l2, col_r2 = st.columns(2)

    with col_l2:
        st.markdown(
            '<div class="section-header">Satisfaction vs Return Rate</div>',
            unsafe_allow_html=True,
        )
        fig = px.scatter(
            fdf,
            x="customer_satisfaction",
            y="return_rate",
            color="product_category",
            color_discrete_map=PRODUCT_COLORS,
            opacity=0.7,
            labels={
                "customer_satisfaction": "Customer Satisfaction (1‑5)",
                "return_rate": "Return Rate",
                "product_category": "Product",
            },
        )
        fig.update_yaxes(tickformat=".0%")
        fig.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            )
        )
        st.plotly_chart(styled_fig(fig, 420), use_container_width=True, theme=None)

    with col_r2:
        st.markdown(
            '<div class="section-header">Marketing Spend vs Profit</div>',
            unsafe_allow_html=True,
        )
        fig = px.scatter(
            fdf,
            x="marketing_spend",
            y="profit",
            color="product_category",
            color_discrete_map=PRODUCT_COLORS,
            opacity=0.65,
            labels={
                "marketing_spend": "Marketing spend ($)",
                "profit": "Profit ($)",
                "product_category": "Product",
            },
        )
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        compact_scatter_hover_spend_profit(fig)
        fig.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            )
        )
        st.plotly_chart(styled_fig(fig, 420), use_container_width=True, theme=None)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align:center; padding:15px 0 10px 0; color:#8e99b0; font-size:0.85rem; line-height: 1.6;'>
        <b>TechFlow Solutions</b> &nbsp;|&nbsp; Data Visualization Lab<br>
        Submitted to Dr. Benjamin Harris<br>
        <span style='color:{TEXT_COLOR}; font-weight: 600;'>Authors: Abbot Tubeine & Harrison Herschberger</span>
    </div>
    """,
    unsafe_allow_html=True,
)
