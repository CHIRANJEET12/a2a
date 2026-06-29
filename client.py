import streamlit as st
import requests
import time
import html

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Debate AI · Powered by Claude",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Theme tokens ─────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "name": "Dark",
        "canvas":      "#0A0A0F",
        "surface":     "#14141F",
        "surface2":    "#1E1E30",
        "border":      "#2A2A42",
        "border2":     "#3A3A55",
        "text":        "#E8D5C4",
        "text2":       "#A89888",
        "text3":       "#6B5F55",
        "pro":         "#CC785C",
        "pro_dim":     "#2A1A14",
        "pro_mid":     "#8B4F3A",
        "against":     "#7C6AF7",
        "against_dim": "#16142A",
        "against_mid": "#4A3FAA",
        "green":       "#5CB88A",
        "green_dim":   "#0D2A1A",
        "yellow":      "#D4A843",
        "yellow_dim":  "#2A200A",
        "red":         "#E05C5C",
        "red_dim":     "#2A0A0A",
        "gradient":    "linear-gradient(135deg, #CC785C 0%, #A05CF0 100%)",
    },
    "light": {
        "name": "Light",
        "canvas":      "#FAF9F7",
        "surface":     "#FFFFFF",
        "surface2":    "#F3F1EE",
        "border":      "#E2DED9",
        "border2":     "#C8C4BE",
        "text":        "#1A1814",
        "text2":       "#5C5550",
        "text3":       "#9C9590",
        "pro":         "#B8623A",
        "pro_dim":     "#FEF0EB",
        "pro_mid":     "#D4886A",
        "against":     "#5C4ED4",
        "against_dim": "#EEF0FE",
        "against_mid": "#8070E8",
        "green":       "#3A9E6A",
        "green_dim":   "#E8F6EE",
        "yellow":      "#B8882A",
        "yellow_dim":  "#FDF5E0",
        "red":         "#C44A4A",
        "red_dim":     "#FEE8E8",
        "gradient":    "linear-gradient(135deg, #B8623A 0%, #7C6AF7 100%)",
    },
    "claude": {
        "name": "Claude",
        "canvas":      "#1A1410",
        "surface":     "#231E18",
        "surface2":    "#2E2820",
        "border":      "#3D3528",
        "border2":     "#52473A",
        "text":        "#F0E6D8",
        "text2":       "#B8A898",
        "text3":       "#7A6A5A",
        "pro":         "#E8935A",
        "pro_dim":     "#2E1E0E",
        "pro_mid":     "#A0623A",
        "against":     "#9B8AE8",
        "against_dim": "#1E1A30",
        "against_mid": "#6A5AB8",
        "green":       "#7ACA9A",
        "green_dim":   "#0E2A1A",
        "yellow":      "#E8C468",
        "yellow_dim":  "#2A200A",
        "red":         "#E87A7A",
        "red_dim":     "#2A0E0E",
        "gradient":    "linear-gradient(135deg, #E8935A 0%, #9B8AE8 100%)",
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None

T = THEMES[st.session_state.theme]

# ─── Inject CSS ───────────────────────────────────────────────────────────────
def inject_css(t):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [class*="css"], .stApp {{
    background-color: {t['canvas']} !important;
    color: {t['text']} !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}}

/* ── Nuke all Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton {{ visibility: hidden !important; display: none !important; }}
.stDecoration {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}
section[data-testid="stSidebar"] {{ display: none !important; }}

.block-container {{
    max-width: 860px !important;
    padding: 0 1.5rem 5rem !important;
    margin: 0 auto !important;
}}

/* ── Typography ── */
.d-title {{
    font-family: 'Lora', Georgia, serif;
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.1;
    background: {t['gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.d-sub {{
    font-size: 0.95rem;
    color: {t['text2']};
    margin-top: 0.5rem;
    line-height: 1.6;
}}
.eyebrow {{
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {t['text3']};
}}

/* ── Layout ── */
.top-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.8rem 0 0;
    border-bottom: 1px solid {t['border']};
    margin-bottom: 2.5rem;
    padding-bottom: 1.2rem;
}}
.logo-area {{ display: flex; align-items: center; gap: 0.7rem; }}
.logo-icon {{
    width: 36px; height: 36px;
    border-radius: 9px;
    background: {t['gradient']};
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    color: white;
    flex-shrink: 0;
}}
.logo-name {{
    font-family: 'Lora', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: {t['text']};
}}
.theme-pills {{
    display: flex;
    gap: 0.35rem;
    background: {t['surface2']};
    border: 1px solid {t['border']};
    border-radius: 8px;
    padding: 0.25rem;
}}
.theme-pill {{
    padding: 0.28rem 0.7rem;
    border-radius: 5px;
    font-size: 0.72rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    color: {t['text2']};
    border: none;
    background: transparent;
}}
.theme-pill.active {{
    background: {t['surface']};
    color: {t['text']};
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}

/* ── Input panel ── */
.input-panel {{
    background: {t['surface']};
    border: 1px solid {t['border']};
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
}}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background: {t['surface2']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 8px !important;
    color: {t['text']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 0.9rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
    line-height: 1.5 !important;
}}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {{
    color: {t['text3']} !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {t['pro']} !important;
    box-shadow: 0 0 0 3px {t['pro']}22 !important;
    outline: none !important;
}}
.stTextInput label, .stTextArea label {{
    color: {t['text2']} !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}}
[data-baseweb="base-input"] {{ background: transparent !important; }}

/* ── Button ── */
.stButton > button {{
    background: {t['gradient']} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.15s, transform 0.1s !important;
    box-shadow: 0 2px 12px {t['pro']}33 !important;
    width: 100% !important;
}}
.stButton > button:hover {{ opacity: 0.88 !important; transform: translateY(-1px) !important; }}
.stButton > button:active {{ transform: translateY(0) !important; }}

/* ── Status box ── */
[data-testid="stStatusWidget"] {{
    background: {t['surface']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    color: {t['text']} !important;
}}

/* ── Transcript ── */
.transcript-wrap {{
    position: relative;
    padding: 0;
}}
.vs-spine {{
    position: absolute;
    left: 50%;
    top: 0; bottom: 0;
    width: 1px;
    background: linear-gradient(180deg, transparent, {t['border2']} 20%, {t['border2']} 80%, transparent);
    transform: translateX(-50%);
}}
.vs-badge {{
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    background: {t['surface2']};
    border: 1px solid {t['border2']};
    border-radius: 20px;
    padding: 0.25rem 0.6rem;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: {t['text3']};
}}

.msg-row {{
    display: flex;
    gap: 1rem;
    margin-bottom: 1.2rem;
    animation: fadeUp 0.3s ease both;
}}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.msg-row.pro-row  {{ justify-content: flex-start; padding-right: 52%; }}
.msg-row.against-row {{ justify-content: flex-end; padding-left: 52%; }}
.msg-row.center-row  {{ justify-content: center; }}

.bubble {{
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    max-width: 100%;
    position: relative;
}}
.bubble-pro {{
    background: {t['pro_dim']};
    border: 1px solid {t['pro']}44;
    border-left: 3px solid {t['pro']};
}}
.bubble-against {{
    background: {t['against_dim']};
    border: 1px solid {t['against']}44;
    border-right: 3px solid {t['against']};
}}
.bubble-center {{
    background: {t['surface']};
    border: 1px solid {t['border']};
    max-width: 70%;
    text-align: center;
}}
.agent-label {{
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}}
.label-pro     {{ color: {t['pro']}; }}
.label-against {{ color: {t['against']}; }}
.label-center  {{ color: {t['text3']}; }}
.bubble-body {{
    font-size: 0.875rem;
    line-height: 1.65;
    color: {t['text']};
    white-space: pre-wrap;
    word-break: break-word;
}}

/* ── Section header ── */
.section-head {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid {t['border']};
}}
.section-head-icon {{
    width: 28px; height: 28px;
    border-radius: 7px;
    background: {t['surface2']};
    border: 1px solid {t['border']};
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}}

/* ── Verdict ── */
.verdict-outer {{
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid {t['border']};
    margin-bottom: 1rem;
}}
.verdict-banner {{
    padding: 1.6rem;
    text-align: center;
}}
.verdict-banner-pro     {{ background: linear-gradient(135deg, {t['pro_dim']}, {t['surface2']}); border-bottom: 1px solid {t['pro']}33; }}
.verdict-banner-against {{ background: linear-gradient(135deg, {t['against_dim']}, {t['surface2']}); border-bottom: 1px solid {t['against']}33; }}
.verdict-eyebrow {{ color: {t['text3']}; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; }}
.verdict-winner-text {{
    font-family: 'Lora', serif;
    font-size: 1.6rem;
    font-weight: 600;
    margin: 0.3rem 0;
}}
.verdict-winner-pro     {{ color: {t['pro']}; }}
.verdict-winner-against {{ color: {t['against']}; }}
.verdict-reason {{
    font-size: 0.85rem;
    color: {t['text2']};
    line-height: 1.6;
    margin-top: 0.5rem;
}}
.verdict-scores {{
    padding: 1.2rem 1.6rem;
    background: {t['surface']};
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
}}
.score-row {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
}}
.score-side {{
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    width: 60px;
    flex-shrink: 0;
}}
.score-side-pro     {{ color: {t['pro']}; }}
.score-side-against {{ color: {t['against']}; }}
.score-track {{
    flex: 1;
    height: 5px;
    background: {t['surface2']};
    border-radius: 3px;
    overflow: hidden;
}}
.score-fill {{ height: 100%; border-radius: 3px; }}
.fill-pro     {{ background: {t['pro']}; }}
.fill-against {{ background: {t['against']}; }}
.score-num {{
    font-size: 0.82rem;
    font-weight: 600;
    color: {t['text']};
    width: 28px;
    text-align: right;
    flex-shrink: 0;
}}

/* ── Evidence ── */
.evidence-card {{
    background: {t['surface']};
    border: 1px solid {t['border']};
    border-radius: 14px;
    overflow: hidden;
}}
.evidence-top {{
    padding: 1.2rem 1.5rem;
    border-bottom: 1px solid {t['border']};
    background: {t['surface2']};
}}
.evidence-body {{ padding: 1.2rem 1.5rem; }}
.evidence-item {{
    display: flex;
    gap: 0.75rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid {t['border']};
    align-items: flex-start;
}}
.evidence-item:last-child {{ border-bottom: none; }}
.ev-dot {{
    width: 5px; height: 5px;
    border-radius: 50%;
    background: {t['green']};
    margin-top: 0.5rem;
    flex-shrink: 0;
}}
.ev-text {{ font-size: 0.86rem; color: {t['text2']}; line-height: 1.6; }}
.conf-pill {{
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 12px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 0.9rem;
}}
.conf-high   {{ background: {t['green_dim']};  color: {t['green']};  border: 1px solid {t['green']}44; }}
.conf-med    {{ background: {t['yellow_dim']}; color: {t['yellow']}; border: 1px solid {t['yellow']}44; }}
.conf-low    {{ background: {t['red_dim']};    color: {t['red']};    border: 1px solid {t['red']}44; }}

/* ── Error ── */
.err-box {{
    background: {t['red_dim']};
    border: 1px solid {t['red']}55;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.875rem;
    color: {t['red']};
    margin: 1rem 0;
}}

/* ── Progress step ── */
.progress-step {{
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.38rem 0;
    font-size: 0.85rem;
    color: {t['text3']};
    transition: color 0.2s;
}}
.progress-step.live {{ color: {t['text']}; }}
.progress-step.done {{ color: {t['green']}; }}
.step-icon {{ font-size: 0.9rem; width: 18px; text-align: center; }}

/* ── Thin divider ── */
.thin-div {{
    border: none;
    height: 1px;
    background: {t['border']};
    margin: 2rem 0;
}}

/* ── Reset link button ── */
.stButton.reset > button {{
    background: {t['surface2']} !important;
    color: {t['text2']} !important;
    box-shadow: none !important;
    border: 1px solid {t['border']} !important;
    font-weight: 500 !important;
}}
</style>
""", unsafe_allow_html=True)

inject_css(T)

# ─── Constants ────────────────────────────────────────────────────────────────
API_URL = "https://a2a-eqlk.onrender.com/api/v1/debate"
API_TIMEOUT_SECONDS = 120

STAGES = [
    ("🔍", "Researching the topic"),
    ("🎙️", "Moderator setting scope"),
    ("✊", "PRO opening argument"),
    ("🛡️", "AGAINST counter-argument"),
    ("⚔️",  "Rebuttals exchanged"),
    ("⚖️", "Judge evaluating"),
    ("📋", "Extracting key evidence"),
]

AGENT_MAP = {
    "pro":        ("PRO",        "pro"),
    "against":    ("AGAINST",    "against"),
    "moderator":  ("MODERATOR",  "center"),
    "researcher": ("RESEARCHER", "center"),
    "system":     ("SYSTEM",     "center"),
}

# ─── Render helpers ───────────────────────────────────────────────────────────
def bubble(agent, message):
    label, side = AGENT_MAP.get(agent, ("UNKNOWN", "center"))
    message = html.escape(str(message))
    if side == "pro":
        st.markdown(f"""
        <div class="msg-row pro-row">
          <div class="bubble bubble-pro">
            <div class="agent-label label-pro">{label}</div>
            <div class="bubble-body">{message}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    elif side == "against":
        st.markdown(f"""
        <div class="msg-row against-row">
          <div class="bubble bubble-against">
            <div class="agent-label label-against">{label}</div>
            <div class="bubble-body">{message}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        if agent == "system":
            return
        st.markdown(f"""
        <div class="msg-row center-row">
          <div class="bubble bubble-center">
            <div class="agent-label label-center">{label}</div>
            <div class="bubble-body">{message}</div>
          </div>
        </div>""", unsafe_allow_html=True)


def verdict_block(v):
    winner = v.get("winner", "").lower()
    is_pro = winner == "pro"
    banner_cls  = "verdict-banner-pro"     if is_pro else "verdict-banner-against"
    winner_cls  = "verdict-winner-pro"     if is_pro else "verdict-winner-against"
    winner_text = "PRO wins the debate"    if is_pro else "AGAINST wins the debate"
    ps  = float(v.get("pro_score", 0))
    ags = float(v.get("against_score", 0))
    reasoning = html.escape(str(v.get("reasoning", "")))
    st.markdown(f"""
    <div class="verdict-outer">
      <div class="verdict-banner {banner_cls}">
        <div class="verdict-eyebrow">⚖️ Judge's verdict</div>
        <div class="verdict-winner-text {winner_cls}">{winner_text}</div>
        <div class="verdict-reason">{reasoning}</div>
      </div>
      <div class="verdict-scores">
        <div class="score-row">
          <span class="score-side score-side-pro">PRO</span>
          <div class="score-track"><div class="score-fill fill-pro" style="width:{ps*10}%"></div></div>
          <span class="score-num">{ps:.1f}</span>
        </div>
        <div class="score-row">
          <span class="score-side score-side-against">AGAINST</span>
          <div class="score-track"><div class="score-fill fill-against" style="width:{ags*10}%"></div></div>
          <span class="score-num">{ags:.1f}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def evidence_block(e):

    argument = html.escape(str(e.get("argument", "")))

    items = e.get("evidence", [])

    confidence = float(e.get("confidence", 0))
    pct = int(confidence * 100)

    if confidence >= 0.7:
        conf_cls, conf_txt = "conf-high", f"✓ {pct}% confidence"
    elif confidence >= 0.4:
        conf_cls, conf_txt = "conf-med", f"~ {pct}% confidence"
    else:
        conf_cls, conf_txt = "conf-low", f"! {pct}% confidence"

    items_html = ""
    if isinstance(items, list):
        for it in items:
        if isinstance(it, dict):
            text = html.escape(str(it.get("text", "")))
            url = html.escape(str(it.get("url", "")), quote=True)

            link_html = ""
            if url:
                link_html = f"""
                <a href="{url}" target="_blank"
                   style="color:#3b82f6;text-decoration:none;word-break:break-all;">
                    🔗 {url}
                </a>
                """

            items_html += f"""
            <div class="evidence-item">
                <div class="ev-dot"></div>
                <div class="ev-text">
                    <div>{text}</div>
                    {link_html}
                </div>
            </div>
            """

        else:
            text = html.escape(str(it))
            items_html += f"""
            <div class="evidence-item">
                <div class="ev-dot"></div>
                <div class="ev-text">{text}</div>
            </div>
            """
            
    else:
        items_html = f"""
    <div class="evidence-item">
        <div class="ev-dot"></div>
        <div class="ev-text">{html.escape(str(items))}</div>
    </div>
    """

    st.markdown(f"""
    <div class="evidence-card">
        <div class="evidence-top">
            <div class="eyebrow" style="margin-bottom:0.4rem;">Strongest argument</div>
            <div style="font-size:0.88rem; line-height:1.6; color:{T['text']}">
                {argument}
            </div>
            <span class="conf-pill {conf_cls}">{conf_txt}</span>
        </div>

            {items_html}
    </div>
    """, unsafe_allow_html=True)

# ─── Top bar ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
  <div class="logo-area">
    <div class="logo-icon">⚖️</div>
    <span class="logo-name">Debate AI</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Theme switcher via Streamlit columns (real buttons)
th_cols = st.columns([1, 1, 1, 5])
for i, (key, meta) in enumerate(THEMES.items()):
    with th_cols[i]:
        if st.button(
            meta["name"],
            key=f"theme_{key}",
            type="primary" if st.session_state.theme == key else "secondary",
        ):
            st.session_state.theme = key
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─── Input panel ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="input-panel">
  <div class="eyebrow" style="margin-bottom:0.3rem;">Start a debate</div>
  <div class="d-title">What should they argue about?</div>
  <div class="d-sub">Enter any topic — Debate AI will research it, argue both sides, and declare a winner.</div>
</div>
""", unsafe_allow_html=True)

# Inputs — inside a clean visual card (we use the already-injected CSS)
col_l, col_r = st.columns([3, 2], gap="medium")
with col_l:
    topic = st.text_area(
        "TOPIC",
        placeholder="e.g. Universal Basic Income will do more harm than good",
        height=100,
        key="topic_input",
        label_visibility="visible",
    )
with col_r:
    api_key = st.text_input(
        "GROQ API KEY",
        placeholder="gsk_••••••••••••••••",
        type="password",
        key="api_key_input",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("⚡  Run Debate", key="run_btn")

# ─── Execute ──────────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.markdown('<div class="err-box">Enter a topic to debate.</div>', unsafe_allow_html=True)
    elif not api_key.strip():
        st.markdown('<div class="err-box">Enter your Groq API key.</div>', unsafe_allow_html=True)
    else:
        st.session_state.result = None
        st.session_state.error  = None
        st.markdown('<hr class="thin-div">', unsafe_allow_html=True)

        with st.status("Running debate…", expanded=True) as status:
            for icon, label in STAGES:
                st.markdown(
                    f'<div class="progress-step live"><span class="step-icon">{icon}</span>{label}</div>',
                    unsafe_allow_html=True,
                )
                time.sleep(0.2)

            try:
                resp = requests.post(
                    API_URL,
                    json={"topic": topic.strip(), "groq_api_key": api_key.strip()},
                    timeout=API_TIMEOUT_SECONDS,
                )
                resp.raise_for_status()
                data = resp.json()
                if data.get("success"):
                    st.session_state.result = data["data"]
                    status.update(label="Debate complete ✓", state="complete", expanded=False)
                else:
                    st.session_state.error = data.get("message", "Server returned an error.")
                    status.update(label="Debate failed", state="error", expanded=False)
            except requests.exceptions.ConnectionError:
                st.session_state.error = "Cannot connect to https://a2a-eqlk.onrender.com — is your backend deployed and reachable?"
                status.update(label="Connection failed", state="error", expanded=False)
            except requests.exceptions.Timeout:
                st.session_state.error = (
                    "The debate is taking too long. This is usually a provider timeout "
                    "or Groq quota/rate-limit wait. Please try a shorter topic or retry later."
                )
                status.update(label="Debate timed out", state="error", expanded=False)
            except requests.exceptions.HTTPError as exc:
                try:
                    error_body = exc.response.json()
                    detail = error_body.get("message") or error_body.get("detail") or str(exc)
                except Exception:
                    detail = str(exc)
                st.session_state.error = detail
                status.update(label="Server error", state="error", expanded=False)
            except Exception as exc:
                st.session_state.error = str(exc)
                status.update(label="Unexpected error", state="error", expanded=False)

# ─── Error ────────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f'<div class="err-box">⚠ {st.session_state.error}</div>', unsafe_allow_html=True)

# ─── Results ──────────────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result
    transcript  = res.get("transcript", [])
    verdict     = res.get("verdict", {})
    evidence    = res.get("supporting_evidence", {})

    # ── Transcript ──
    st.markdown(f"""
    <div class="section-head">
      <div class="section-head-icon">💬</div>
      <span class="eyebrow">Debate transcript</span>
    </div>
    <div class="transcript-wrap">
      <div class="vs-spine"></div>
    """, unsafe_allow_html=True)

    for msg in transcript:
        agent   = msg.get("agent", "system")   if isinstance(msg, dict) else getattr(msg, "agent", "system")
        message = msg.get("message", "")       if isinstance(msg, dict) else getattr(msg, "message", "")
        bubble(agent, message)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Verdict + Evidence ──
    st.markdown('<hr class="thin-div">', unsafe_allow_html=True)
    col_v, col_e = st.columns(2, gap="large")

    with col_v:
        st.markdown(f"""
        <div class="section-head">
          <div class="section-head-icon">⚖️</div>
          <span class="eyebrow">Verdict</span>
        </div>""", unsafe_allow_html=True)
        if verdict:
            verdict_block(verdict)
        else:
            st.markdown('<div class="err-box">No verdict returned.</div>', unsafe_allow_html=True)

    with col_e:
        st.markdown(f"""
        <div class="section-head">
          <div class="section-head-icon">🔬</div>
          <span class="eyebrow">Evidence summary</span>
        </div>""", unsafe_allow_html=True)
        if evidence:
            evidence_block(evidence)
        else:
            st.markdown('<div class="err-box">No evidence returned.</div>', unsafe_allow_html=True)

    # ── New debate ──
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([2, 1, 2])
    with mid:
        if st.button("↩  New debate", key="reset_btn"):
            st.session_state.result = None
            st.session_state.error  = None
            st.rerun()
