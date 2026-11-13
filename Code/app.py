"""
RR SupeRR Selector - Round 1 dashboard (executive RR design system)
====================================================================
Install : pip install streamlit plotly pandas pyarrow
Run     : streamlit run app.py
Best    : run with the dark base theme so native widgets (date pickers, tooltips, menus) match as well:

  streamlit run app.py --theme.base dark --theme.backgroundColor "#070D1E" --theme.secondaryBackgroundColor "#0F1C3F" --theme.textColor "#F1F5F9" --theme.primaryColor "#EA1A85"

Paths   : defaults to the D:\\ folders below. Override without editing:
              set RR_STEP2_DIR=D:\\RR SupeRR Hackathon\\step2_outputs
              set RR_DATA_DIR=D:\\RR SupeRR Hackathon\\6af458274c1e8_data_pack\\Data Pack
          or use the sidebar "Data locations" box.

Step-2 files (first match wins; Step-2 script names and the names in the brief both work):
    batters_metrics.parquet|csv | all_batters_metrics.csv      bowlers_metrics.parquet|csv | all_bowlers_metrics.csv
    top20_batters.csv | top_batters_under_pressure.(csv|parquet)   (fallbacks if the full table is missing)
    top20_bowlers.csv | top_bowlers_under_pressure.(csv|parquet)
    ball_pressure.parquet   pressure_config.json
"""
from __future__ import annotations

import html
import json
import os
import sys
from pathlib import Path

try:
    import streamlit as st
except ImportError:  # pragma: no cover
    sys.exit("streamlit is not installed.  Run:  pip install streamlit plotly pandas pyarrow")

st.set_page_config(page_title="RR SupeRR Selector", page_icon="🏏", layout="wide", initial_sidebar_state="collapsed")

# ======================================================================================
# Design tokens
# ======================================================================================
BG, CARD, BORDER = "#070D1E", "#0F1C3F", "#1E2F65"
PINK, BLUE, GOLD = "#EA1A85", "#2563EB", "#F59E0B"
BLUE_DEEP = "#004BA0"   # Royal Blue: hero gradient + badges (BLUE is its lighter tint for lines/marks on navy)
TEXT, TEXT2, MUTED = "#FFFFFF", "#F1F5F9", "#94A3B8"
FONT = "Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
GOOD, BAD = "#34D399", "#FB7185"

# ======================================================================================
# 1. Universal RR theme: injected before anything else is rendered
# ======================================================================================
CSS = f"""
<style>
/* ---------- base surfaces ---------- */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] {{
  background:{BG} !important; color:{TEXT2} !important; font-family:{FONT} !important; }}
[data-testid="stHeader"] {{ background:transparent !important; }}
[data-testid="stToolbar"], [data-testid="stDecoration"], footer, #MainMenu {{ display:none !important; visibility:hidden !important; }}
.block-container {{ max-width:1500px !important; padding:1.4rem 2rem 3rem !important; }}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {{ background:{CARD} !important; border-right:1px solid {BORDER} !important; }}
[data-testid="stVerticalBlock"] {{ gap:.9rem; }}

/* ---------- typography: kill every black text ---------- */
.stApp p, .stApp span, .stApp label, .stApp div, .stApp li, .stApp td, .stApp th, .stApp small, .stApp strong, .stApp em,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp .stMarkdown, .stApp .stSelectbox, .stApp .stRadio,
.stApp .stCheckbox, .stApp .stSlider, .stApp .stTextInput, .stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stMarkdownContainer"] {{
  color:{TEXT2} !important; }}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {{ color:{TEXT} !important; font-weight:800 !important; letter-spacing:.2px; }}
.stApp h2 {{ font-size:1.55rem !important; border-left:5px solid {PINK}; padding-left:.7rem; margin-top:.2rem; }}
.stApp h3 {{ font-size:1.15rem !important; }}
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] * {{ color:{MUTED} !important; }}
.stApp a {{ color:{GOLD} !important; }}
.stApp code {{ background:#16275A !important; color:{GOLD} !important; border-radius:6px; padding:1px 6px; }}
.stApp .katex, .stApp .katex * {{ color:{TEXT} !important; }}
.stApp .katex-display {{ background:{CARD}; border:1px solid {BORDER}; border-radius:12px; padding:14px 10px; overflow-x:auto; overflow-y:hidden; }}

/* ---------- tabs ---------- */
.stApp .stTabs [data-baseweb="tab-list"] {{ display:flex; flex-wrap:wrap; gap:10px 8px; padding:6px 0 10px; border-bottom:1px solid {BORDER}; overflow:visible !important; }}
.stApp .stTabs [data-baseweb="tab"] {{ flex:0 0 auto; height:auto !important; white-space:nowrap; padding:10px 22px !important; margin:0 !important;
  border-radius:999px; background:{CARD} !important; border:1px solid {BORDER}; }}
.stApp .stTabs [data-baseweb="tab"] p, .stApp .stTabs [data-baseweb="tab"] span, .stApp .stTabs [data-baseweb="tab"] div {{
  color:{MUTED} !important; font-weight:600; font-size:.95rem; }}
.stApp .stTabs [aria-selected="true"] {{ background:{PINK} !important; border-color:{PINK} !important; box-shadow:0 4px 18px rgba(234,26,133,.35); }}
.stApp .stTabs [aria-selected="true"] p, .stApp .stTabs [aria-selected="true"] span, .stApp .stTabs [aria-selected="true"] div {{
  color:{TEXT} !important; font-weight:800; }}
.stApp .stTabs [data-baseweb="tab-highlight"], .stApp .stTabs [data-baseweb="tab-border"] {{ display:none !important; }}

/* ---------- inputs / dropdowns ---------- */
div[data-baseweb="select"] > div, .stApp .stTextInput input, .stApp .stNumberInput input {{
  background:{CARD} !important; border:1px solid {BORDER} !important; border-radius:10px !important; min-height:44px;
  color:{TEXT2} !important; -webkit-text-fill-color:{TEXT2} !important; }}
div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within {{ border-color:{PINK} !important; }}
div[data-baseweb="select"] div[value], div[data-baseweb="select"] span {{ white-space:nowrap !important; overflow:hidden !important; text-overflow:ellipsis !important;
  max-width:100% !important; color:{TEXT2} !important; }}
div[data-baseweb="select"] input {{ color:{TEXT2} !important; -webkit-text-fill-color:{TEXT2} !important; }}
div[data-baseweb="select"] svg, .stApp [data-testid="stSelectbox"] svg {{ fill:{MUTED} !important; }}
/* the dropdown menu is rendered in a portal outside .stApp, so it needs unscoped selectors */
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="menu"], ul[role="listbox"] {{
  background:{CARD} !important; border:1px solid {BORDER} !important; border-radius:10px !important; }}
li[role="option"], div[data-baseweb="popover"] li {{ background:{CARD} !important; color:{TEXT2} !important; white-space:nowrap !important;
  overflow:hidden !important; text-overflow:ellipsis !important; max-width:100%; }}
li[role="option"] *, div[data-baseweb="popover"] li * {{ color:{TEXT2} !important; overflow:hidden; text-overflow:ellipsis; }}
li[role="option"]:hover, li[role="option"][aria-selected="true"] {{ background:{BORDER} !important; }}
div[data-baseweb="popover"] * {{ color:{TEXT2} !important; }}
.stApp [data-testid="stWidgetLabel"] p {{ font-size:.78rem !important; font-weight:700 !important; text-transform:uppercase; letter-spacing:.8px; }}
.stApp [data-testid="stRadio"] label p {{ font-size:.92rem !important; text-transform:none; letter-spacing:0; font-weight:600 !important; }}
.stApp [data-testid="stRadio"] [role="radiogroup"] {{ gap:.4rem 1.2rem; flex-wrap:wrap; }}
.stApp [data-baseweb="radio"] > div:first-child {{ border-color:{PINK} !important; background:{CARD} !important; }}
.stApp [data-baseweb="checkbox"] > div:first-child {{ border-color:{PINK} !important; }}
.stApp [data-baseweb="slider"] div[role="slider"] {{ background:{PINK} !important; border-color:{PINK} !important; }}
.stApp [data-testid="stSliderThumbValue"], .stApp [data-testid="stSliderThumbValue"] * {{ color:{GOLD} !important; }}
.stApp .stButton > button, .stApp .stDownloadButton > button {{ background:{PINK} !important; border:0 !important; border-radius:10px; padding:.5rem 1.2rem;
  box-shadow:0 4px 14px rgba(234,26,133,.3); }}
.stApp .stButton > button *, .stApp .stDownloadButton > button * {{ color:{TEXT} !important; font-weight:700; }}
.stApp .stButton > button:hover {{ background:{BLUE} !important; }}
.stApp [data-testid="stExpander"] {{ background:{CARD} !important; border:1px solid {BORDER} !important; border-radius:12px; }}
.stApp [data-testid="stExpander"] summary {{ background:{CARD} !important; }}
.stApp [data-testid="stAlert"] {{ background:{CARD} !important; border:1px solid {BORDER}; border-left:5px solid {GOLD}; border-radius:10px; }}

/* ---------- charts ---------- */
.stApp [data-testid="stPlotlyChart"] {{ background:{CARD}; border:1px solid {BORDER}; border-radius:12px; padding:6px 6px 2px; }}
.stApp .js-plotly-plot, .stApp .plotly, .stApp .plot-container {{ background:transparent !important; }}
.stApp .modebar {{ background:transparent !important; }} .stApp .modebar-btn path {{ fill:{MUTED} !important; }}

/* ---------- custom components (higher specificity so the universal text rule never wins) ---------- */
.stApp .rr-hero {{ background:linear-gradient(110deg,{BLUE_DEEP} 0%,{PINK} 100%); border-radius:16px; padding:22px 30px; margin-bottom:12px;
  box-shadow:0 10px 30px rgba(234,26,133,.28); border:1px solid rgba(255,255,255,.12); }}
.stApp .rr-hero h1 {{ margin:0; font-size:2.05rem !important; color:{TEXT} !important; border:0 !important; padding:0 !important; }}
.stApp .rr-hero p {{ margin:.3rem 0 0; color:#FFE4F1 !important; font-size:1rem; }}
.stApp .rr-kpis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:14px; margin:6px 0 16px; }}
.stApp .rr-kpi {{ background:{CARD}; border:1px solid {BORDER}; border-top:4px solid {PINK}; border-radius:12px; padding:14px 18px;
  box-shadow:0 6px 20px rgba(0,0,0,.35); min-width:0; }}
.stApp .rr-kpi.gold {{ border-top-color:{GOLD}; }} .stApp .rr-kpi.blue {{ border-top-color:{BLUE}; }}
.stApp .rr-kpi .lbl {{ color:{MUTED} !important; font-size:.72rem; text-transform:uppercase; letter-spacing:1px; font-weight:700; }}
.stApp .rr-kpi .val {{ color:{TEXT} !important; font-size:1.9rem; font-weight:800; line-height:1.2; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.stApp .rr-kpi .sub {{ color:{MUTED} !important; font-size:.82rem; margin-top:2px; }}
.stApp .rr-kpi .sub.good {{ color:{GOOD} !important; }} .stApp .rr-kpi .sub.bad {{ color:{BAD} !important; }}
.stApp .rr-badge {{ display:inline-block; padding:4px 13px; margin:3px 8px 3px 0; border-radius:999px; font-size:.78rem; font-weight:700;
  background:{CARD}; border:1px solid {BORDER}; color:{TEXT2} !important; }}
.stApp .rr-badge.pink {{ background:{PINK}; border-color:{PINK}; color:{TEXT} !important; }}
.stApp .rr-badge.gold {{ background:{GOLD}; border-color:{GOLD}; color:#0A1128 !important; }}
.stApp .rr-badge.blue {{ background:{BLUE_DEEP}; border-color:{BLUE}; color:{TEXT} !important; }}
.stApp .rr-wrap {{ overflow-x:auto; border-radius:12px; }}
.stApp .rr-table {{ width:100%; border-collapse:separate; border-spacing:0 6px; font-size:.86rem; }}
.stApp .rr-table th {{ color:{MUTED} !important; text-align:left; font-weight:700; padding:4px 12px; font-size:.7rem; text-transform:uppercase; letter-spacing:.8px; white-space:nowrap; }}
.stApp .rr-table td {{ background:{CARD}; border-top:1px solid {BORDER}; border-bottom:1px solid {BORDER}; padding:9px 12px; color:{TEXT2} !important; white-space:nowrap; }}
.stApp .rr-table td:first-child {{ border-left:1px solid {BORDER}; border-radius:10px 0 0 10px; font-weight:800; color:{GOLD} !important; }}
.stApp .rr-table td:last-child {{ border-right:1px solid {BORDER}; border-radius:0 10px 10px 0; }}
.stApp .rr-table td.hl {{ color:{PINK} !important; font-weight:800; }}
.stApp .rr-table td.name {{ color:{TEXT} !important; font-weight:700; }}
.stApp .rr-table tr:hover td {{ background:#16275A; }}
.stApp .rr-note {{ background:{CARD}; border:1px solid {BORDER}; border-left:5px solid {GOLD}; border-radius:10px; padding:12px 16px; font-size:.92rem; }}
.stApp .rr-bar {{ background:{CARD}; border:1px solid {BORDER}; border-radius:12px; padding:14px 18px 4px; margin-bottom:10px; }}
/* multiselect chips, winner tiles, head-to-head headers */
.stApp [data-baseweb="tag"] {{ background:{PINK} !important; border-radius:999px !important; max-width:100%; }}
.stApp [data-baseweb="tag"] span, .stApp [data-baseweb="tag"] svg {{ color:{TEXT} !important; fill:{TEXT} !important; }}
.stApp .rr-kpis.two {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
.stApp .rr-kpi.win {{ border-color:{GOLD}; border-top-color:{GOLD}; box-shadow:0 0 0 1px {GOLD}, 0 8px 24px rgba(245,158,11,.25); }}
.stApp .rr-kpi.win .val {{ color:{GOLD} !important; }}
.stApp .rr-phead {{ background:{CARD}; border:1px solid {BORDER}; border-left:6px solid {PINK}; border-radius:12px; padding:12px 18px; margin-bottom:10px; }}
.stApp .rr-phead.b {{ border-left-color:{BLUE}; }}
.stApp .rr-phead .nm {{ font-size:1.3rem; font-weight:800; color:{TEXT} !important; }}
.stApp .rr-phead .tm {{ color:{MUTED} !important; font-size:.85rem; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

try:
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.io as pio
    from plotly.subplots import make_subplots
except ImportError as exc:  # pragma: no cover
    st.error(f"Missing dependency: **{exc.name}**.  Run:  `pip install streamlit plotly pandas pyarrow`")
    st.stop()

HIGH_PI_DEFAULT = 0.65
DEFAULT_STEP2 = os.environ.get("RR_STEP2_DIR", r"D:\RR SupeRR Hackathon\step2_outputs")
DEFAULT_DATA = os.environ.get("RR_DATA_DIR", r"D:\RR SupeRR Hackathon\6af458274c1e8_data_pack\Data Pack")

FILES = {
    "bat": ["batters_metrics.parquet", "batters_metrics.csv", "all_batters_metrics.csv"],
    "bowl": ["bowlers_metrics.parquet", "bowlers_metrics.csv", "all_bowlers_metrics.csv"],
    "bat_top": ["top20_batters.csv", "top_batters_under_pressure.parquet", "top_batters_under_pressure.csv"],
    "bowl_top": ["top20_bowlers.csv", "top_bowlers_under_pressure.parquet", "top_bowlers_under_pressure.csv"],
    "balls": ["ball_pressure.parquet"],
    "config": ["pressure_config.json"],
}
DEFAULT_CFG = dict(
    high_pi=0.65, med_pi=0.45,
    weights_chase=dict(state=0.35, rate=0.15, late=0.20, close=0.30),
    weights_first=dict(par=0.40, coll=0.25, late=0.35),
    k_state=3.0, rate_scale=3.0, close_sigma=0.5, late_pow=1.5,
    final_weights=dict(hp=0.60, delta=0.25, cons=0.15),
    thresholds=dict(min_hp_balls=60, min_hp_matches=8, min_base_balls=100),
)

# ======================================================================================
# 3. Unified Plotly theme
# ======================================================================================
COLORWAY = [PINK, BLUE, GOLD, "#8B5CF6", "#14B8A6", "#F97316"]


def rr_layout(fig: "go.Figure", title: str | None = None, height: int | None = None, legend_bottom: bool = False,
              margin: dict | None = None) -> "go.Figure":
    """Apply the RR chart theme. An explicit `margin` (or one set by an earlier call) is never overwritten."""
    fig.update_layout(
        paper_bgcolor=CARD, plot_bgcolor=CARD,
        font=dict(color="#F8F9FA", family=FONT, size=13), colorway=COLORWAY,
        title_font=dict(color=TEXT, size=16, family=FONT), title_x=0.01, title_xanchor="left", title_y=0.97, title_yanchor="top",
        hoverlabel=dict(bgcolor=BG, bordercolor=PINK, font=dict(color=TEXT, family=FONT)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT2), title=dict(font=dict(color=TEXT2)),
                    **(dict(orientation="h", x=0, y=-0.22, yanchor="top") if legend_bottom else {})),
    )
    if margin is None and fig.layout.margin.l is None:
        margin = dict(l=60, r=45, t=70, b=95 if legend_bottom else 55)
    if margin is not None:
        fig.update_layout(margin=margin)
    if title is not None:
        fig.update_layout(title_text=title)
    if height:
        fig.update_layout(height=height)
    axis = dict(gridcolor=BORDER, zerolinecolor=BORDER, linecolor=BORDER, tickfont=dict(color=MUTED), title_font=dict(color=TEXT2), automargin=True)
    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)
    fig.update_polars(bgcolor=CARD, radialaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=MUTED)),
                      angularaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=TEXT2)))
    fig.update_annotations(font_color=TEXT2)
    return fig


def register_plotly_template() -> None:
    t = go.layout.Template()
    t.layout = go.Layout(paper_bgcolor=CARD, plot_bgcolor=CARD, font=dict(color="#F8F9FA", family=FONT), colorway=COLORWAY,
                         colorscale=dict(sequential=[[0, BLUE], [0.5, PINK], [1, GOLD]]))
    pio.templates["rr"] = t
    pio.templates.default = "rr"


def plot(fig: "go.Figure", key: str) -> None:
    rr_layout(fig)
    try:  # theme=None stops Streamlit from overriding the RR palette with its own chart theme
        st.plotly_chart(fig, theme=None, width="stretch", key=key)
    except TypeError:
        st.plotly_chart(fig, theme=None, use_container_width=True, key=key)


# ======================================================================================
# 2. UI helpers
# ======================================================================================
def fnum(x, d: int = 1, suffix: str = "") -> str:
    return "–" if x is None or pd.isna(x) else f"{x:,.{d}f}{suffix}"


def kpi(label: str, value: str, sub: str = "", tone: str = "", accent: str = "", win: bool = False) -> str:
    cls = f"rr-kpi {accent} {'win' if win else ''}"
    return (f'<div class="{cls}"><div class="lbl">{html.escape(label)}</div><div class="val">{html.escape(value)}</div>'
            f'<div class="sub {tone}">{html.escape(("★ better · " if win else "") + sub)}</div></div>')


def kpi_row(*cards: str, cls: str = "") -> None:
    st.markdown(f'<div class="rr-kpis {cls}">{"".join(cards)}</div>', unsafe_allow_html=True)


def badge(text: str, tone: str = "") -> str:
    return f'<span class="rr-badge {tone}">{html.escape(text)}</span>'


def df_to_html(df: "pd.DataFrame", highlight: tuple[str, ...] = (), name_cols: tuple[str, ...] = ("Player",)) -> str:
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in df.columns)
    rows = []
    for _, r in df.iterrows():
        cells = "".join(
            f'<td class="{"hl" if c in highlight else ("name" if c in name_cols else "")}">{html.escape(str(r[c]))}</td>' for c in df.columns)
        rows.append(f"<tr>{cells}</tr>")
    return f'<div class="rr-wrap"><table class="rr-table"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def pct_rank(pool: "pd.Series", v: float, higher_better: bool) -> float:
    pool = pd.to_numeric(pool, errors="coerce").dropna()
    if pool.empty or pd.isna(v):
        return float("nan")
    return float((pool <= v).mean() * 100 if higher_better else (pool >= v).mean() * 100)


def clip(text: str, n: int) -> str:
    text = str(text)
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


# ======================================================================================
# Data loading (unchanged logic)
# ======================================================================================
def find_file(folder: str, key: str) -> Path | None:
    for name in FILES[key]:
        p = Path(folder) / name
        if p.exists():
            return p
    return None


def read_table(path: Path) -> "pd.DataFrame":
    if path.suffix.lower() == ".parquet":
        try:
            return pd.read_parquet(path)
        except ImportError:
            try:
                import polars as pl

                return pd.DataFrame(pl.read_parquet(path).to_dict(as_series=False))
            except ImportError:
                raise RuntimeError("Reading parquet needs pyarrow:  pip install pyarrow  (or use the CSV outputs).")
    return pd.read_csv(path, low_memory=False)


def prep_players(df: "pd.DataFrame", role: str) -> "pd.DataFrame":
    df = df.copy()
    if "player" not in df.columns:
        df["player"] = range(len(df))
    df["player"] = df["player"].astype(str)
    if "player_name" not in df.columns:
        df["player_name"] = df["player"]
    df["player_name"] = df["player_name"].fillna(df["player"]).astype(str)
    if "eligible" not in df.columns:
        df["eligible"] = True
    df["eligible"] = df["eligible"].astype(str).str.lower().isin(["true", "1", "1.0"])
    if "final_z" not in df.columns:
        df["final_z"] = df["rating"].sub(50).div(10) if "rating" in df.columns else np.nan
    if "rating" not in df.columns:
        df["rating"] = 50 + 10 * df["final_z"]
    num = lambda c: pd.to_numeric(df[c], errors="coerce") if c in df.columns else pd.Series(np.nan, index=df.index)
    if role == "Batter":
        df["hp_wkt100"] = num("hp_sum_out") / num("hp_n") * 100
        df["base_wkt100"] = num("b_sum_out") / num("b_n") * 100
        df["delta_kpi"] = num("hp_strike_rate") - num("base_strike_rate")
    else:
        df["hp_wkt100"] = num("hp_sum_wkt") / num("hp_legal") * 100
        df["base_wkt100"] = num("b_sum_wkt") / num("b_legal") * 100
        df["delta_kpi"] = num("hp_economy") - num("base_economy")
    df["comp_group"] = np.where(num("hp_t20i_share") > 0.5, "T20I", "IPL")
    return df


@st.cache_data(show_spinner="Loading player metrics…")
def load_players(step2_dir: str) -> dict:
    out, notes = {}, []
    for role, key in (("Batter", "bat"), ("Bowler", "bowl")):
        p = find_file(step2_dir, key) or find_file(step2_dir, key + "_top")
        if p is None:
            notes.append(f"No {role.lower()} metrics file found in {step2_dir}.")
            continue
        if "top" in p.name:
            notes.append(f"Using {p.name} (top-N only); the full metrics file was not found, so the deep-dive pool is limited.")
        out[role] = prep_players(read_table(p), role)
    return dict(data=out, notes=notes)


@st.cache_data(show_spinner="Loading ball-level pressure data…")
def load_balls(step2_dir: str) -> "pd.DataFrame | None":
    p = find_file(step2_dir, "balls")
    return None if p is None else read_table(p)


@st.cache_data
def load_config(step2_dir: str) -> tuple:
    p = find_file(step2_dir, "config")
    cfg = json.loads(p.read_text()) if p else {}
    return {**DEFAULT_CFG, **cfg}, bool(p)


@st.cache_data(show_spinner="Loading match metadata…")
def load_match_meta(data_dir: str) -> dict:
    d, out = Path(data_dir), {}
    for k, f in (("matches", "matches.csv"), ("comps", "competitions.csv"), ("teams", "teams.csv"), ("map", "competition_team_player_mapping.csv")):
        p = d / f
        out[k] = pd.read_csv(p, low_memory=False) if p.exists() else None
    return out


@st.cache_data(show_spinner=False)
def build_team_map(data_dir: str) -> "pd.DataFrame":
    """player -> primary country (most-frequent T20I squad) and primary IPL franchise (most-frequent league squad)."""
    meta = load_match_meta(data_dir)
    mp, teams, comps = meta.get("map"), meta.get("teams"), meta.get("comps")
    if mp is None:
        return pd.DataFrame(columns=["player", "country", "franchise"])
    d = mp.copy()
    if teams is not None and {"comp_id", "team_id", "team_name"} <= set(teams.columns):
        t = teams[["comp_id", "team_id", "team_name"]].drop_duplicates(["comp_id", "team_id"]).rename(columns={"team_name": "team_name_t"})
        d = d.merge(t, on=["comp_id", "team_id"], how="left")
        d["team"] = d["team_name"].fillna(d["team_name_t"])
    else:
        d["team"] = d["team_name"]
    if comps is not None:
        d = d.merge(comps[["comp_id", "match_format"]].drop_duplicates("comp_id"), on="comp_id", how="left")
    else:
        d["match_format"] = ""
    d["player"] = d["player_id"].astype(str)
    d = d.dropna(subset=["team"])
    nat = d["match_format"].astype(str).eq("T20I")
    mode = lambda f: f.groupby("player")["team"].agg(lambda x: x.value_counts().idxmax())
    out = pd.DataFrame({"country": mode(d[nat]) if nat.any() else pd.Series(dtype=object),
                        "franchise": mode(d[~nat]) if (~nat).any() else pd.Series(dtype=object)})
    return out.rename_axis("player").reset_index()


def attach_teams(df: "pd.DataFrame", tm: "pd.DataFrame") -> "pd.DataFrame":
    df = df.drop(columns=[c for c in ("country", "franchise") if c in df.columns])
    if tm is None or tm.empty:
        return df.assign(country=np.nan, franchise=np.nan)
    return df.merge(tm, on="player", how="left")


def team_options(P: dict) -> dict:
    frames = [df[["player", "country", "franchise"]] for df in P.values()]
    if not frames:
        return {}
    u = pd.concat(frames).drop_duplicates("player")
    opts = {}
    for name in u["country"].dropna().value_counts().index:
        opts[f"{name} · Country"] = ("country", name)
    for name in u["franchise"].dropna().value_counts().index:
        opts[f"{name} · IPL"] = ("franchise", name)
    return opts


def apply_team_filter(df: "pd.DataFrame", sel: list) -> "pd.DataFrame":
    if not sel:
        return df
    m = pd.Series(False, index=df.index)
    for kind, name in sel:
        m |= df[kind].eq(name)
    return df[m]


def team_sig(sel: list) -> str:
    return "|".join(sorted(f"{k}:{n}" for k, n in sel)) or "all"


def team_label(row) -> str:
    for c in ("franchise", "country"):
        v = row.get(c)
        if v is not None and not pd.isna(v):
            return clip(v, 18)
    return "–"


# ======================================================================================
# Tab 1 - Leaderboard
# ======================================================================================
def board_table(top: "pd.DataFrame", role: str, compact: bool = False) -> "pd.DataFrame":
    r = pd.DataFrame({"#": top["view_rank"].astype(int), "Player": top["player_name"].map(lambda v: clip(v, 24))})
    if compact:
        r["Team"] = top.apply(team_label, axis=1)
    else:
        r["Country"] = top["country"].map(lambda v: "–" if pd.isna(v) else clip(v, 16)) if "country" in top else "–"
        r["Franchise"] = top["franchise"].map(lambda v: "–" if pd.isna(v) else clip(v, 22)) if "franchise" in top else "–"
    r["Rating"] = top["rating"].map(lambda v: fnum(v, 1))
    if role == "Batter":
        r["HP SR"] = top["hp_strike_rate"].map(lambda v: fnum(v, 1))
        if not compact:
            r["Base SR"] = top["base_strike_rate"].map(lambda v: fnum(v, 1))
        r["Δ SR"] = top["delta_kpi"].map(lambda v: "–" if pd.isna(v) else f"{v:+.1f}")
        if not compact:
            r["HP Bnd %"] = top["hp_boundary_pct"].map(lambda v: fnum(v, 1))
            r["HP Dot %"] = top["hp_dot_pct"].map(lambda v: fnum(v, 1))
    else:
        r["HP Econ"] = top["hp_economy"].map(lambda v: fnum(v, 2))
        if not compact:
            r["Base Econ"] = top["base_economy"].map(lambda v: fnum(v, 2))
        r["Δ Econ"] = top["delta_kpi"].map(lambda v: "–" if pd.isna(v) else f"{v:+.2f}")
        if not compact:
            r["HP Dot %"] = top["hp_dot_pct"].map(lambda v: fnum(v, 1))
            r["Wkts"] = top["hp_wickets"].map(lambda v: fnum(v, 0)) if "hp_wickets" in top else "–"
    r["HP balls"] = top["hp_n"].map(lambda v: fnum(v, 0))
    r["Consist."] = top["cons_rate"].map(lambda v: "–" if pd.isna(v) else f"{v * 100:.0f}%")
    return r


def render_board(df: "pd.DataFrame", role: str, key: str, compact: bool) -> None:
    elig = df[df["eligible"]].sort_values("final_z", ascending=False).reset_index(drop=True)
    elig["view_rank"] = elig.index + 1
    top = elig.head(10)
    st.markdown(f"### Top 10 {role}s Under Pressure")
    if top.empty:
        st.info("No eligible players for this filter.")
        return
    pick = st.selectbox(f"Spotlight {role.lower()}", top["player_name"].tolist(), key=f"spot_{key}")
    s = top[top["player_name"] == pick].iloc[0]
    d = s["delta_kpi"]
    if role == "Batter":
        kpi_row(kpi("Rating", fnum(s["rating"], 1), f"Rank #{int(s['view_rank'])} of {len(elig)} eligible"),
                kpi("HP Strike Rate", fnum(s["hp_strike_rate"], 1), f"baseline {fnum(s['base_strike_rate'], 1)}", accent="gold"),
                kpi("Δ vs Baseline", "–" if pd.isna(d) else f"{d:+.1f}", "SR points under pressure", "good" if d > 0 else "bad", "blue"))
    else:
        kpi_row(kpi("Rating", fnum(s["rating"], 1), f"Rank #{int(s['view_rank'])} of {len(elig)} eligible"),
                kpi("HP Economy", fnum(s["hp_economy"], 2), f"baseline {fnum(s['base_economy'], 2)}", accent="gold"),
                kpi("Δ vs Baseline", "–" if pd.isna(d) else f"{d:+.2f}", "runs/over · negative is better", "good" if d < 0 else "bad", "blue"))
    st.markdown(df_to_html(board_table(top, role, compact), highlight=("Rating",)), unsafe_allow_html=True)

    t = top.iloc[::-1]
    bar = go.Figure(go.Bar(x=t["rating"], y=t["player_name"].map(lambda v: clip(v, 30)), orientation="h",
                           marker=dict(color=t["rating"], colorscale=[[0, BLUE], [1, PINK]], line=dict(width=0)),
                           text=t["rating"].round(1), textposition="outside", textfont=dict(color=TEXT), cliponaxis=False,
                           hovertemplate="<b>%{y}</b><br>Pressure rating: %{x:.1f}<extra></extra>"))
    bar.update_layout(height=420, xaxis_title="Pressure rating (50 = average eligible player)", yaxis_title=None)
    rr_layout(bar, title=f"Top 10 {role.lower()}s: pressure rating", margin=dict(l=160, r=40, t=40, b=40))
    plot(bar, f"bar_{key}")

    # Scatter: no text on every point; rich hover for all, call-outs for the Top 5 only
    xc, yc = ("base_strike_rate", "hp_strike_rate") if role == "Batter" else ("base_economy", "hp_economy")
    lab, hp_lab, b_lab = ("strike rate", "HP SR", "Baseline SR") if role == "Batter" else ("economy", "HP Econ", "Baseline Econ")
    f = ".1f" if role == "Batter" else ".2f"
    balls_lab = "High-pressure balls faced" if role == "Batter" else "High-pressure balls bowled"
    hover = ("<b>%{customdata[0]}</b><br>Pressure rating: %{customdata[1]:.1f}"
             f"<br>{hp_lab}: " + "%{customdata[2]:" + f + "}" + f"<br>{b_lab}: " + "%{customdata[3]:" + f + "}"
             f"<br>{balls_lab}: " + "%{customdata[4]:.0f}<extra></extra>")
    cd = lambda fr: fr[["player_name", "rating", yc, xc, "hp_n"]].to_numpy(dtype=object).tolist()
    callouts = [clip(n, 18) if i < 5 else "" for i, n in enumerate(top["player_name"])]
    sc = go.Figure()
    sc.add_trace(go.Scatter(x=elig[xc], y=elig[yc], mode="markers", name="Eligible pool", customdata=cd(elig), hovertemplate=hover,
                            marker=dict(size=np.clip(elig["hp_n"].fillna(30) / 8, 6, 20), color=BLUE, opacity=0.55, line=dict(width=0))))
    sc.add_trace(go.Scatter(x=top[xc], y=top[yc], mode="markers+text", name="Top 10 (labels: Top 5)", text=callouts,
                            textposition="top center", textfont=dict(size=11, color=TEXT), customdata=cd(top), hovertemplate=hover,
                            marker=dict(size=14, color=GOLD, line=dict(width=1.5, color=PINK))))
    lo, hi = float(np.nanmin(elig[[xc, yc]].values)), float(np.nanmax(elig[[xc, yc]].values))
    sc.add_shape(type="line", x0=lo, y0=lo, x1=hi, y1=hi, line=dict(color=MUTED, dash="dot", width=1))
    sc.update_layout(height=460, xaxis_title=f"Baseline {lab}", yaxis_title=f"High-pressure {lab}")
    rr_layout(sc, title=f"Baseline vs pressure {lab} (above the dotted line = {'better' if role == 'Batter' else 'worse'} under pressure)", legend_bottom=True)
    plot(sc, f"sc_{key}")

def tab_leaderboard(P: dict, sel: list) -> None:
    st.markdown("## RR SupeRR Selector Leaderboard")
    c1, c2 = st.columns(2)
    split = c1.radio("Tournament split", ["All", "IPL", "T20I"], horizontal=True,
                     help="Players are assigned to IPL or T20I by where most of their high-pressure balls were faced.")
    view = c2.radio("Layout", ["Side by side", "Batters", "Bowlers"], horizontal=True)
    st.caption("Ratings come from the full IPL + T20I pool and are not re-fitted by filters. Ranks, tables and charts below reflect the current "
               "tournament split and country/team selection.")

    def board(role, key, compact):
        df = P.get(role)
        if df is None:
            st.warning(f"{role} metrics not loaded.")
            return
        df = apply_team_filter(df, sel)
        if split != "All":
            df = df[df["comp_group"] == split]
        render_board(df, role, key, compact)

    if view == "Side by side":
        l, r = st.columns(2, gap="large")
        with l:
            board("Batter", "b1", True)
        with r:
            board("Bowler", "w1", True)
    elif view == "Batters":
        board("Batter", "b2", False)
    else:
        board("Bowler", "w2", False)


# ======================================================================================
# Tab 2 - Player deep-dive
# ======================================================================================
def metric_defs(role: str) -> list:
    if role == "Batter":
        return [("Strike rate", "hp_strike_rate", "base_strike_rate", True), ("Boundary %", "hp_boundary_pct", "base_boundary_pct", True),
                ("Dot ball %", "hp_dot_pct", "base_dot_pct", False), ("Dismissals/100", "hp_wkt100", "base_wkt100", False)]
    return [("Economy", "hp_economy", "base_economy", False), ("Dot ball %", "hp_dot_pct", "base_dot_pct", True),
            ("Boundaries conceded %", "hp_boundary_conceded_pct", "base_boundary_conceded_pct", False),
            ("Wickets/100", "hp_wkt100", "base_wkt100", True)]


def tab_deep_dive(P: dict, cfg: dict, sel: list) -> None:
    st.markdown("## Player Pressure Deep-Dive")
    roles = [r for r in ("Batter", "Bowler") if r in P]
    if not roles:
        st.warning("No player metrics loaded.")
        return
    c1, c2 = st.columns([1, 2], gap="large")
    role = c1.radio("Role", roles, horizontal=True)
    full = P[role]
    df = apply_team_filter(full, sel).sort_values("player_name").reset_index(drop=True)
    if df.empty:
        st.info("No players match the current country/team filter.")
        return
    labels = {f"{clip(r.player_name, 30)}{'' if r.eligible else ' · low sample'}  (#{r.player})": i for i, r in df.iterrows()}
    choice = c2.selectbox("Search player (type to filter)", list(labels), key=f"pl_{role}_{team_sig(sel)}")
    s = df.loc[labels[choice]]
    pool = full[full["eligible"]]

    n = s.get("hp_n", np.nan)
    thr = cfg["thresholds"]["min_hp_balls"]
    tier = ("Robust sample", "pink") if n >= 2.5 * thr else (("Adequate sample", "blue") if n >= thr else ("Thin sample: interpret with caution", ""))
    cons_pct = pct_rank(pool["cons_rate"], s.get("cons_rate", np.nan), True)
    cons_b = ("Consistency n/a", "") if pd.isna(cons_pct) else ("High consistency", "gold") if cons_pct >= 75 else (("Average consistency", "blue") if cons_pct >= 40 else ("Volatile", ""))
    unit = "balls faced" if role == "Batter" else "balls bowled"
    st.markdown(
        badge(f"{fnum(n, 0)} high-pressure {unit}", tier[1]) + badge(tier[0], tier[1]) +
        badge(f"{fnum(s.get('hp_matches'), 0)} pressure matches", "blue") + badge(cons_b[0], cons_b[1]) +
        badge("Eligible for ranking" if s["eligible"] else "Below eligibility thresholds", "pink" if s["eligible"] else "") +
        "".join(badge(str(s.get(c)), "blue") for c in ("country", "franchise") if pd.notna(s.get(c))),
        unsafe_allow_html=True)

    cons_rate = s.get("cons_rate", np.nan)
    kpi_row(kpi("Rating", fnum(s.get("rating"), 1), f"final z {fnum(s.get('final_z'), 2)}"),
            kpi("Consistency score", "–" if pd.isna(cons_rate) else f"{cons_rate * 100:.0f}%",
                f"{fnum(s.get('cons_matches'), 0)} matches judged" + ("" if pd.isna(cons_pct) else f" · top {max(1, 100 - cons_pct):.0f}%"), accent="gold"),
            kpi("Pressure level (z)", fnum(s.get("z_hp"), 2), "vs eligible peers", accent="blue"),
            kpi("Vs own baseline (z)", fnum(s.get("z_delta"), 2), "high pressure minus usual", accent="gold"))

    defs = metric_defs(role)
    fig = make_subplots(rows=1, cols=4, subplot_titles=[d[0] for d in defs], horizontal_spacing=0.07)
    for i, (nm, hpc, bc, _) in enumerate(defs, start=1):
        hv, bv = s.get(hpc, np.nan), s.get(bc, np.nan)
        fig.add_trace(go.Bar(x=["Baseline", "High pressure"], y=[bv, hv], marker_color=[BLUE, PINK], marker_line_width=0,
                             text=[fnum(bv, 1), fnum(hv, 1)], textposition="outside", textfont=dict(color=TEXT),
                             showlegend=False, cliponaxis=False), row=1, col=i)
    fig.update_layout(height=370)
    rr_layout(fig, title="High-pressure execution vs the player's own baseline")
    plot(fig, f"dd_bar_{role}")

    cats, hp_p, b_p = [], [], []
    for nm, hpc, bc, hb in defs:
        cats.append(nm)
        hp_p.append(pct_rank(pool[hpc], s.get(hpc, np.nan), hb))
        b_p.append(pct_rank(pool[bc], s.get(bc, np.nan), hb))
    rad = go.Figure()
    rad.add_trace(go.Scatterpolar(r=b_p + b_p[:1], theta=cats + cats[:1], name="Baseline", fill="toself",
                                  line=dict(color=BLUE, width=2.5), fillcolor="rgba(37,99,235,0.28)"))
    rad.add_trace(go.Scatterpolar(r=hp_p + hp_p[:1], theta=cats + cats[:1], name="High pressure", fill="toself",
                                  line=dict(color=PINK, width=2.5), fillcolor="rgba(234,26,133,0.30)"))
    rad.update_layout(height=440, polar=dict(radialaxis=dict(range=[0, 100], tickvals=[25, 50, 75, 100])))
    rr_layout(rad, title="Percentile vs eligible peers (100 = best; flipped where lower is better)", legend_bottom=True)
    plot(rad, f"dd_rad_{role}")

    with st.expander("All computed metrics for this player"):
        t = s.dropna().rename("value").to_frame().reset_index().rename(columns={"index": "metric"})
        t["value"] = t["value"].map(lambda v: f"{v:,.4g}" if isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, bool) else str(v))
        st.markdown(df_to_html(t.rename(columns={"metric": "Metric", "value": "Value"}), name_cols=("Metric",)), unsafe_allow_html=True)


# ======================================================================================
# Tab 3 - Head-to-head
# ======================================================================================
def h2h_spec(role: str) -> list:
    """(label, column, higher_is_better, formatter, baseline column or None, treat NaN as +inf)"""
    f1, f2 = (lambda v: fnum(v, 1)), (lambda v: fnum(v, 2))
    pct = lambda v: "–" if pd.isna(v) else f"{v * 100:.0f}%"
    if role == "Batter":
        return [("Pressure rating", "rating", True, f1, None, False),
                ("HP strike rate", "hp_strike_rate", True, f1, "base_strike_rate", False),
                ("Δ vs own baseline", "delta_kpi", True, lambda v: "–" if pd.isna(v) else f"{v:+.1f}", None, False),
                ("HP dot ball %", "hp_dot_pct", False, f1, "base_dot_pct", False),
                ("HP boundary %", "hp_boundary_pct", True, f1, "base_boundary_pct", False),
                ("Balls per dismissal", "hp_balls_per_dismissal", True, f1, None, True),
                ("Consistency score", "cons_rate", True, pct, None, False),
                ("HP balls faced", "hp_n", True, lambda v: fnum(v, 0), None, False)]
    return [("Pressure rating", "rating", True, f1, None, False),
            ("HP economy", "hp_economy", False, f2, "base_economy", False),
            ("Δ vs own baseline", "delta_kpi", False, lambda v: "–" if pd.isna(v) else f"{v:+.2f}", None, False),
            ("HP dot ball %", "hp_dot_pct", True, f1, "base_dot_pct", False),
            ("HP boundaries conceded %", "hp_boundary_conceded_pct", False, f1, "base_boundary_conceded_pct", False),
            ("Balls per wicket", "hp_balls_per_wicket", False, f1, None, True),
            ("Consistency score", "cons_rate", True, pct, None, False),
            ("HP balls bowled", "hp_n", True, lambda v: fnum(v, 0), None, False)]


def cmp_winner(a, b, higher: bool, nan_is_inf: bool) -> str | None:
    def v(x):
        return (float("inf") if nan_is_inf else float("nan")) if pd.isna(x) else float(x)
    va, vb = v(a), v(b)
    if np.isnan(va) or np.isnan(vb) or va == vb:
        return None
    return "A" if (va > vb) == higher else "B"


def pct_vector(s: "pd.Series", pool: "pd.DataFrame", role: str) -> tuple[list, list]:
    defs = metric_defs(role)
    cats = [d[0] for d in defs] + ["Consistency", "Pressure level"]
    vals = [pct_rank(pool[d[1]], s.get(d[1], np.nan), d[3]) for d in defs]
    vals += [pct_rank(pool["cons_rate"], s.get("cons_rate", np.nan), True), pct_rank(pool["z_hp"], s.get("z_hp", np.nan), True)]
    return cats, [float(v) for v in np.nan_to_num(np.array(vals, dtype=float), nan=0.0)]


def tab_h2h(P: dict, cfg: dict, sel: list) -> None:
    st.markdown("## Player vs Player (Head-to-Head)")
    roles = [r for r in ("Batter", "Bowler") if r in P]
    if not roles:
        st.warning("No player metrics loaded.")
        return
    role = st.radio("Compare", roles, horizontal=True, format_func=lambda r: f"{r}s", key="h2h_role")
    full = P[role]
    pool = full[full["eligible"]]
    view = apply_team_filter(full, sel).sort_values(["eligible", "final_z"], ascending=[False, False]).reset_index(drop=True)
    if len(view) < 2:
        st.info("Fewer than two players match the current country/team filter.")
        return
    labels, seen = {}, set()
    for i, r in view.iterrows():
        lab = f"{clip(r.player_name, 28)} · {team_label(r)}" + ("" if r.eligible else " · low sample")
        if lab in seen:
            lab += f" (#{r.player})"
        seen.add(lab)
        labels[lab] = i
    keys = list(labels)
    sig = f"{role}_{team_sig(sel)}"
    ca, cb = st.columns(2, gap="large")
    la = ca.selectbox("Player A", keys, index=0, key=f"h2h_a_{sig}")
    lb = cb.selectbox("Player B", keys, index=1, key=f"h2h_b_{sig}")
    if la == lb:
        st.warning("Pick two different players.")
        return
    sA, sB = view.loc[labels[la]], view.loc[labels[lb]]

    spec = h2h_spec(role)
    winners = [cmp_winner(sA.get(c), sB.get(c), hb, inf) for _, c, hb, _, _, inf in spec]
    tiles = {"A": [], "B": []}
    for (label, col, hb, fmt, basecol, _), w in zip(spec, winners):
        for side, s in (("A", sA), ("B", sB)):
            sub = f"baseline {fmt(s.get(basecol))}" if basecol else ""
            tone = ""
            if col == "delta_kpi" and pd.notna(s.get(col)):
                tone = "good" if ((s[col] > 0) == hb) else "bad"
            tiles[side].append(kpi(label, fmt(s.get(col)), sub, tone, "gold" if col in ("rating", "cons_rate") else "", win=(w == side)))
    for col, s, side, cls in ((ca, sA, "A", "a"), (cb, sB, "B", "b")):
        with col:
            teams = " · ".join(str(s.get(c)) for c in ("country", "franchise") if pd.notna(s.get(c))) or "Team n/a"
            st.markdown(f'<div class="rr-phead {cls}"><div class="nm">{html.escape(str(s["player_name"]))}</div>'
                        f'<div class="tm">{html.escape(teams)}</div></div>', unsafe_allow_html=True)
            kpi_row(*tiles[side], cls="two")

    perf = winners[:-1]  # the sample-size tile is context, not a performance metric
    wa, wb = perf.count("A"), perf.count("B")
    zA, zB = float(sA.get("final_z", np.nan)), float(sB.get("final_z", np.nan))
    thr = cfg["thresholds"]["min_hp_balls"]
    if np.isnan(zA) or np.isnan(zB) or abs(zA - zB) < 0.15:
        verdict = f"Too close to call: A wins {wa} and B wins {wb} of {len(perf)} pressure metrics, ratings {fnum(sA['rating'])} vs {fnum(sB['rating'])}."
    else:
        lead, other = (sA, sB) if zA > zB else (sB, sA)
        lw, ow = (wa, wb) if zA > zB else (wb, wa)
        verdict = (f"{lead['player_name']} is the more reliable player under pressure: rating {fnum(lead['rating'])} vs {fnum(other['rating'])}, "
                   f"winning {lw} of {len(perf)} pressure metrics (against {ow}).")
    thin = [str(s["player_name"]) for s in (sA, sB) if s.get("hp_n", 0) < thr]
    caution = f" Caution: small high-pressure sample for {', '.join(thin)}." if thin else ""
    st.markdown(f'<div class="rr-note"><b>Verdict.</b> {html.escape(verdict + caution)}</div>', unsafe_allow_html=True)

    cats, vA = pct_vector(sA, pool, role)
    _, vB = pct_vector(sB, pool, role)
    nA, nB = clip(sA["player_name"], 22), clip(sB["player_name"], 22)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        rad = go.Figure()
        rad.add_trace(go.Scatterpolar(r=vA + vA[:1], theta=cats + cats[:1], name=nA, fill="toself", line=dict(color=PINK, width=2.5), fillcolor="rgba(234,26,133,0.28)"))
        rad.add_trace(go.Scatterpolar(r=vB + vB[:1], theta=cats + cats[:1], name=nB, fill="toself", line=dict(color=BLUE, width=2.5), fillcolor="rgba(37,99,235,0.30)"))
        rad.update_layout(height=470, polar=dict(radialaxis=dict(range=[0, 100], tickvals=[25, 50, 75, 100])))
        rr_layout(rad, title="Percentile vs eligible peers (radar)", legend_bottom=True)
        plot(rad, f"h2h_rad_{sig}")
    with c2:
        bars = go.Figure()
        for nm, vals, colr in ((nA, vA, PINK), (nB, vB, BLUE)):
            bars.add_trace(go.Bar(y=cats, x=vals, name=nm, orientation="h", marker=dict(color=colr, line=dict(width=0)),
                                  text=[f"{v:.0f}" for v in vals], textposition="outside", textfont=dict(color=TEXT), cliponaxis=False))
        bars.update_layout(barmode="group", height=470, xaxis=dict(range=[0, 112], title="Percentile (100 = best)"), yaxis=dict(autorange="reversed"))
        rr_layout(bars, title="Metric-by-metric percentile", legend_bottom=True, margin=dict(l=160, r=40, t=40, b=90))
        plot(bars, f"h2h_bar_{sig}")
    st.caption("Percentiles are measured against all eligible players of the same role (scales flipped where lower is better), "
               "so the two profiles are directly comparable even though the raw metrics have different units.")


# ======================================================================================
# Tab 4 - Match pressure worm
# ======================================================================================
NEEDED_BALL_COLS = ["match_id", "innings", "legal_before", "runs_before", "total", "PI", "runs_bat", "wkt_team", "is_wide"]


def short_comp(name: str, fmt: str) -> str:
    n = str(name)
    if "Indian Premier League" in n:
        yr = "".join(ch for ch in n if ch.isdigit())[-4:]
        return f"IPL {yr}".strip()
    for junk in (" T20I Series", " Series", " T20I", " Tour"):
        n = n.replace(junk, "")
    return clip(n, 30)


def match_options(balls: "pd.DataFrame", meta: dict) -> "pd.DataFrame":
    ids = balls[["match_id"]].drop_duplicates()
    m, comps = meta.get("matches"), meta.get("comps")
    if m is None:
        ids["label"] = "Match " + ids["match_id"].astype(str)
        ids["date"], ids["fmt"], ids["result"], ids["home"], ids["away"] = "", "", "", "", ""
        return ids
    m = m.copy()
    if comps is not None:
        m = m.merge(comps[["comp_id", "comp_name", "match_format"]], on="comp_id", how="left")
    else:
        m["comp_name"], m["match_format"] = "", ""
    m = ids.merge(m, on="match_id", how="left")
    m["date"] = m["match_date"].astype(str).str[:10]
    m["fmt"] = np.where(m["match_format"].astype(str) == "T20I", "T20I", "IPL")
    m["home"], m["away"] = m["home_team"].astype(str), m["away_team"].astype(str)
    comp = [short_comp(n, f) for n, f in zip(m["comp_name"], m["fmt"])]
    m["label"] = [clip(f"{d} | {h} vs {a} ({c})", 88) for d, h, a, c in zip(m["date"], m["home"], m["away"], comp)]
    dup = m["label"].duplicated(keep=False)
    m.loc[dup, "label"] = m.loc[dup, "label"] + " #" + m.loc[dup, "match_id"].astype(str)
    m["result"] = m["result"].astype(str) if "result" in m.columns else ""
    return m.sort_values("date", ascending=False)


def name_lookup(meta: dict) -> dict:
    mp = meta.get("map")
    return {} if mp is None else dict(zip(mp["player_id"].astype(str), mp["player_name"].astype(str)))


def tab_worm(balls: "pd.DataFrame | None", meta: dict, cfg: dict) -> None:
    st.markdown("## Match Pressure Worm")
    if balls is None:
        st.warning("`ball_pressure.parquet` not found in the Step-2 folder; run the Step-2 script first.")
        return
    miss = [c for c in NEEDED_BALL_COLS if c not in balls.columns]
    if miss:
        st.error(f"ball_pressure is missing columns: {miss}")
        return
    opts = match_options(balls, meta)

    c1, c2 = st.columns(2)
    fmt = c1.radio("Competition", ["All", "IPL", "T20I"], horizontal=True)
    inn = c2.radio("Innings", [1, 2], horizontal=True, format_func=lambda i: "1st innings (set)" if i == 1 else "2nd innings (chase)")
    if fmt != "All" and "fmt" in opts:
        opts = opts[opts["fmt"] == fmt]
    if opts.empty:
        st.info("No matches for this filter.")
        return
    label = st.selectbox("Match", opts["label"].tolist(), help="date | home vs away (competition), newest first")
    c3, c4 = st.columns([2, 1])
    thr = c3.slider("High-pressure threshold (PI ≥)", 0.40, 0.90, float(cfg.get("high_pi", HIGH_PI_DEFAULT)), 0.01)
    show_all = c4.checkbox("Show events outside high pressure", value=False)
    row = opts[opts["label"] == label].iloc[0]

    g = balls[(balls["match_id"] == row["match_id"]) & (balls["innings"] == inn)].copy()
    g = g[g["PI"].notna()]
    if g.empty:
        st.info("Pressure Index is not available for this innings (e.g. missing first-innings data for a chase).")
        return
    g = g.sort_values(["legal_before"] + (["row_idx"] if "row_idx" in g else []))
    g["x"] = g["legal_before"] / 6.0
    g["cum"] = g["runs_before"] + g["total"]
    names = name_lookup(meta)

    def nm(v):
        if isinstance(v, (int, float, np.integer, np.floating)) and not pd.isna(v):
            return names.get(str(int(v)), str(int(v)))
        return names.get(str(v), str(v))

    g["bat_n"] = g["batter"].map(nm) if "batter" in g else ""
    g["bowl_n"] = g["bowler"].map(nm) if "bowler" in g else ""
    g["hover"] = ("Over " + g["x"].map("{:.1f}".format) + " · " + g["bat_n"].astype(str) + " v " + g["bowl_n"].astype(str) +
                  "<br>Score " + g["cum"].map("{:.0f}".format) + " · PI " + g["PI"].map("{:.2f}".format))
    hp = g["PI"] >= thr
    is_w = g["wkt_team"] == 1
    is_b = g["runs_bat"].isin([4, 6]) & (g["is_wide"] == 0)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_shape(type="rect", xref="paper", x0=0, x1=1, yref="y2", y0=thr, y1=1, fillcolor="rgba(245,158,11,0.09)", line_width=0, layer="below")
    fig.add_trace(go.Scatter(x=g["x"], y=g["PI"], name="Pressure Index", mode="lines", line=dict(color=PINK, width=2.2),
                             fill="tozeroy", fillcolor="rgba(234,26,133,0.16)", hovertext=g["hover"], hoverinfo="text"), secondary_y=True)
    fig.add_trace(go.Scatter(x=g["x"], y=g["cum"], name="Cumulative runs", mode="lines", line=dict(color=BLUE, width=3.4),
                             hovertext=g["hover"], hoverinfo="text"), secondary_y=False)
    fig.add_shape(type="line", xref="paper", x0=0, x1=1, yref="y2", y0=thr, y1=thr, line=dict(color=GOLD, dash="dash", width=1.5))
    if inn == 2 and "target" in g.columns and g["target"].notna().any():
        tg = float(g["target"].dropna().iloc[0])
        fig.add_shape(type="line", xref="paper", x0=0, x1=1, yref="y", y0=tg, y1=tg, line=dict(color=TEXT2, dash="dot", width=1))
        fig.add_annotation(xref="paper", x=0.01, yref="y", y=tg, text=f"Target {tg:.0f}", showarrow=False, yshift=10, font=dict(color=TEXT2, size=11))
    if show_all:
        for mask, sym, nmx in ((is_w & ~hp, "x", "Wicket (other)"), (is_b & ~hp, "star", "Boundary (other)")):
            d = g[mask]
            fig.add_trace(go.Scatter(x=d["x"], y=d["cum"], mode="markers", name=nmx, hovertext=d["hover"], hoverinfo="text",
                                     marker=dict(symbol=sym, size=7, color=MUTED, opacity=0.55)), secondary_y=False)
    dw, db = g[is_w & hp], g[is_b & hp]
    fig.add_trace(go.Scatter(x=dw["x"], y=dw["cum"], mode="markers", name="Wicket at high pressure", hovertext=dw["hover"], hoverinfo="text",
                             marker=dict(symbol="x", size=14, color=TEXT, line=dict(width=2, color=PINK))), secondary_y=False)
    fig.add_trace(go.Scatter(x=db["x"], y=db["cum"], mode="markers", name="Boundary at high pressure", hovertext=db["hover"], hoverinfo="text",
                             marker=dict(symbol="star", size=13, color=GOLD, line=dict(width=1, color=BG))), secondary_y=False)
    fig.update_yaxes(title_text="Cumulative runs", secondary_y=False)
    fig.update_yaxes(title_text="Pressure Index", range=[0, 1], secondary_y=True, showgrid=False)
    fig.update_xaxes(title_text="Over", dtick=2)
    fig.update_layout(height=560, hovermode="x unified")
    short = f"{row.get('home', '')} vs {row.get('away', '')} · {row.get('date', '')} · innings {inn}" if row.get("home") else f"Match {row['match_id']} · innings {inn}"
    rr_layout(fig, title=clip(short, 80), legend_bottom=True)
    plot(fig, "worm")

    pk = g.loc[g["PI"].idxmax()]
    kpi_row(kpi("Score", f"{g['cum'].iloc[-1]:.0f}/{int(g['wkt_team'].sum())}", "final innings total"),
            kpi("Balls at high pressure", f"{int(hp.sum())}", f"{hp.mean() * 100:.0f}% of the innings", accent="gold"),
            kpi("Peak PI", f"{pk['PI']:.2f}", f"at over {pk['x']:.1f}", accent="blue"),
            kpi("Wickets at HP", str(int((is_w & hp).sum())), f"of {int(is_w.sum())} total"),
            kpi("Boundaries at HP", str(int((is_b & hp).sum())), f"of {int(is_b.sum())} total", accent="gold"))
    if row.get("result") and str(row["result"]) not in ("nan", ""):
        st.markdown(f'<div class="rr-note"><b>Result:</b> {html.escape(str(row["result"]))}</div>', unsafe_allow_html=True)


# ======================================================================================
# Tab 5 - Methodology
# ======================================================================================
def tab_method(balls: "pd.DataFrame | None", cfg: dict, cfg_found: bool, P: dict) -> None:
    st.markdown("## Methodology & Evaluation Defense")
    if not cfg_found:
        st.caption("pressure_config.json not found; showing the default parameters used in the Step-2 script.")
    wc, wf, fw, th = cfg["weights_chase"], cfg["weights_first"], cfg["final_weights"], cfg["thresholds"]

    st.markdown("### 1 · What counts as pressure?")
    st.markdown(
        "Pressure is the *state* a delivery is bowled in, measured **before** the ball so nothing about its outcome leaks in. "
        "Balls left and wickets in hand are folded into one currency, **runs**, using an empirical curve "
        "$E(B,w)$ = expected runs still to come with $B$ balls left and $w$ wickets down (fitted on first innings, venue-adjusted, "
        "monotone in $w$). Every pressure term is then expressed against what those resources can realistically deliver.")
    st.markdown("**2nd innings (chase)**, with $R$ = runs needed and $\\rho = R/E_v(B,w)$:")
    st.latex(r"PI_{2}=%.2f\,\sigma(%.0f\ln\rho)+%.2f\,\sigma\!\left(\tfrac{RRR-CRR}{%.0f}\right)+%.2f\left(1-\tfrac{B}{N}\right)^{%.1f}+%.2f\,e^{-(\ln\rho)^2/(2\cdot %.1f^2)}"
             % (wc["state"], cfg["k_state"], wc["rate"], cfg["rate_scale"], wc["late"], cfg["late_pow"], wc["close"], cfg["close_sigma"]))
    st.markdown("**1st innings (setting a total)**, with $r$ runs, $w$ wickets lost and $par_v$ the venue-adjusted mean total:")
    st.latex(r"PI_{1}=%.2f\,\sigma\!\left(\tfrac{par_v-(r+E_v)}{0.5\,sd_{total}}\right)+%.2f\,\sigma\big(w-\bar w_{over}\big)+%.2f\left(1-\tfrac{B}{N}\right)^{%.1f}"
             % (wf["par"], wf["coll"], wf["late"], cfg["late_pow"]))
    st.markdown(
        f"- **σ** is the logistic function, so every term lies in [0, 1] and the weights sum to 1: PI ∈ [0, 1] (PI = 0 once a chase is won).\n"
        f"- *Collapse* is wickets lost relative to the normal wickets lost at that stage, not a fixed “3 down” rule.\n"
        f"- *Closeness* peaks when the chase is exactly on par ($\\rho=1$) and fades for lost or won games, so garbage-time hitting is not rewarded.\n"
        f"- **Bands:** High ≥ {cfg['high_pi']:.2f} · Medium {cfg['med_pi']:.2f}–{cfg['high_pi']:.2f} · Low < {cfg['med_pi']:.2f}.")

    st.markdown("### 2 · Does PI separate pressure from ordinary play?")
    if balls is not None and "band" in balls.columns:
        v = balls[balls["PI"].notna()]
        t = v.groupby("band").agg(balls=("PI", "size"), runs_per_ball=("total", "mean"),
                                  dot=("total", lambda s: (s == 0).mean() * 100),
                                  boundary=("runs_bat", lambda s: s.isin([4, 6]).mean() * 100),
                                  wicket=("wkt_team", lambda s: s.mean() * 100)).reindex(["Low", "Medium", "High"]).reset_index()
        t = pd.DataFrame({"Band": t["band"], "Deliveries": t["balls"].map("{:,.0f}".format), "Runs/ball": t["runs_per_ball"].map("{:.2f}".format),
                          "Dot %": t["dot"].map("{:.1f}".format), "Boundary %": t["boundary"].map("{:.1f}".format), "Wicket %": t["wicket"].map("{:.2f}".format)})
        st.markdown(df_to_html(t, name_cols=("Band",)), unsafe_allow_html=True)
        st.caption("Computed live from ball_pressure.parquet: run, dot, boundary and wicket profiles by pressure band.")
    else:
        st.info("Load ball_pressure.parquet to see the band validation table.")

    st.markdown("### 3 · Player scoring")
    st.markdown("Each delivery is compared with the league expectation for the **same format × phase × (high / not-high)** cell, so "
                "death-over hitting is never mistaken for clutch. Per player:")
    st.latex(r"\text{Final}=%.2f\,z(\text{HP vs peers})+%.2f\,z(\text{HP}-\text{own baseline})+%.2f\,z(\text{consistency})" % (fw["hp"], fw["delta"], fw["cons"]))
    st.markdown(
        "- **HP vs peers:** PI-weighted mean residual on High-pressure balls (batters: runs/ball, boundary %, dot %, dismissal rate; "
        "bowlers: runs conceded, boundary conceded %, dot %, wicket rate).\n"
        "- **Δ vs own baseline:** that residual minus the same player's residual on non-High balls.\n"
        "- **Consistency:** share of pressure matches (≥ 6 High balls) whose standardised composite is positive, shrunk toward the league rate.")

    st.markdown("### 4 · Bayesian (empirical-Bayes) shrinkage")
    st.latex(r"\hat\theta_i=\mu+\frac{\tau^2}{\tau^2+se_i^2}\,(x_i-\mu),\qquad se_i^2=\frac{\sigma^2}{n_{eff,i}},\qquad \tau^2=\max\!\big(\mathrm{Var}_{between}-\overline{se^2},\,0.1\,\mathrm{Var}_{between}\big)")
    st.markdown("A player with few high-pressure balls has a large $se_i^2$, so his raw number is pulled hard toward the average; a player with a large sample keeps most of his signal. "
                "$\\tau^2$ is estimated from the data (method of moments), not hand-picked.")
    rows = []
    for role, key in (("Batter", "batter"), ("Bowler", "bowler")):
        c = cfg.get(key)
        if not c:
            continue
        for m, sp in c.get("metrics", {}).items():
            s = c.get("shrinkage", {}).get(f"hp_{m}", {})
            rows.append({"Role": role, "Metric": m, "Direction": "higher better" if sp["sign"] > 0 else "lower better",
                         "Weight": f"{sp['weight']:.2f}", "τ²": f"{s.get('tau2', float('nan')):.2e}",
                         "Avg. signal kept": f"{s.get('avg_shrink_factor', float('nan')) * 100:.0f}%"})
    if rows:
        st.markdown(df_to_html(pd.DataFrame(rows), name_cols=("Role", "Metric")), unsafe_allow_html=True)
    else:
        st.caption("Shrinkage diagnostics appear here once pressure_config.json is present.")
    for role in ("Batter", "Bowler"):
        df = P.get(role)
        if df is not None and "hp_runs" in df and "hp_runs_sh" in df and "hp_n" in df:
            f = go.Figure(go.Scatter(x=df["hp_runs"], y=df["hp_runs_sh"], mode="markers", text=df["player_name"],
                                     marker=dict(size=7, color=np.log10(df["hp_n"].clip(1)), colorscale=[[0, BLUE], [0.5, PINK], [1, GOLD]],
                                                 colorbar=dict(title=dict(text="log10 HP balls", font=dict(color=TEXT2)), tickfont=dict(color=MUTED),
                                                               outlinewidth=0), opacity=0.85),
                                     hovertemplate="%{text}<br>raw %{x:.3f} → shrunk %{y:.3f}<extra></extra>"))
            f.update_layout(height=350, xaxis_title="Raw residual", yaxis_title="Shrunk residual")
            rr_layout(f, title=f"{role}s: raw vs shrunk runs-per-ball residual (small samples collapse toward the mean)")
            plot(f, f"shr_{role}")

    st.markdown("### 5 · Decision rules")
    st.markdown(
        f"1. **Eligibility:** ≥ {th['min_hp_balls']} high-pressure balls, ≥ {th['min_hp_matches']} high-pressure matches and ≥ {th['min_base_balls']} baseline balls.\n"
        "2. **Ranking:** descending *Final* score among eligible players. The Top 10 per role are submitted.\n"
        "3. **IPL + T20I:** both are pooled; expectations are format-specific, so a T20I ball is judged against T20I peers.\n"
        "4. **No look-ahead:** PI uses only the state before the ball; super overs are excluded; rain-reduced innings use the revised overs and target.\n"
        "5. **Reproducibility:** every parameter is stored in `pressure_config.json`; the pipeline is deterministic.")
    st.markdown("### 6 · Limitations (stated up front)")
    st.markdown(
        "- Opposition and venue quality are not adjusted at the player level (venue only enters PI).\n"
        "- Fixed phase boundaries (overs 1–6 / 7–15 / 16–20), even in shortened matches.\n"
        "- A near-hopeless chase can still score High PI; closeness down-weights it but does not remove it.\n"
        "- Weights are expert-set; report sensitivity to ±0.05 on the weights and to the 0.65 cut-off alongside the final ranking.")


# ======================================================================================
# Main
# ======================================================================================
def main() -> None:
    register_plotly_template()
    with st.sidebar:
        st.markdown("### Data locations")
        step2 = st.text_input("Step-2 outputs", DEFAULT_STEP2)
        data = st.text_input("Data Pack", DEFAULT_DATA)
        if st.button("Reload data"):
            st.cache_data.clear()
    st.markdown('<div class="rr-hero"><h1>🏏 RR SupeRR Selector</h1>'
                '<p>Most reliable players under pressure · IPL + T20I from 2022 · Halla Bol</p></div>', unsafe_allow_html=True)

    if not Path(step2).exists():
        st.error(f"Step-2 folder not found: `{step2}`. Fix it in the sidebar or set RR_STEP2_DIR.")
        st.stop()
    try:
        loaded = load_players(step2)
        balls = load_balls(step2)
    except Exception as e:
        st.error(f"Could not read the Step-2 outputs: {e}")
        st.stop()
    cfg, cfg_found = load_config(step2)
    meta = load_match_meta(data)
    tm = build_team_map(data)
    P = {role: attach_teams(df, tm) for role, df in loaded["data"].items()}
    for n in loaded["notes"]:
        st.warning(n)
    if meta["matches"] is None:
        st.warning(f"matches.csv not found in `{data}`; the match selector will show ids only.")
    if tm.empty:
        st.warning("competition_team_player_mapping.csv not found or empty: country/team filters are unavailable.")

    opts = team_options(P)
    chosen = st.multiselect("Filter by Country / Team (empty = All)", list(opts), key="team_filter",
                            placeholder="All players · pick countries (India, Australia, England…) or IPL franchises")
    sel = [opts[c] for c in chosen]
    if sel:
        st.caption("Filter applies to the leaderboard, scatter plots and the player pickers. Percentiles and ratings always use the full eligible pool.")

    t1, t2, t3, t4, t5 = st.tabs(["🏆 Leaderboard", "🔍 Player Deep-Dive", "⚔️ Head-to-Head", "📈 Match Worm", "📋 Methodology"])
    with t1:
        tab_leaderboard(P, sel)
    with t2:
        tab_deep_dive(P, cfg, sel)
    with t3:
        tab_h2h(P, cfg, sel)
    with t4:
        tab_worm(balls, meta, cfg)
    with t5:
        tab_method(balls, cfg, cfg_found, P)


main()