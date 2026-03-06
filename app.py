import streamlit as st

st.set_page_config(
    page_title="Tourism Experience Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold: #C9A84C;
    --gold-light: #E8C97A;
    --deep: #0D1B2A;
    --surface: #132236;
    --surface2: #1A2E47;
    --accent: #4ECDC4;
    --pink: #E84393;
    --text: #E8EDF2;
    --muted: #8A9BB0;
    --border: rgba(201,168,76,0.2);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--deep);
    color: var(--text);
}
.main { background-color: var(--deep); }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #0D1B2A 50%, #0A1628 100%);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
#MainMenu, footer { visibility: hidden; }

.hero-container {
    background: linear-gradient(135deg, #0D1B2A 0%, #132236 40%, #0D2440 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(201,168,76,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(201,168,76,0.12);
    border: 1px solid var(--border);
    color: var(--gold);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.hero-title span { color: var(--gold); }
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 560px;
    line-height: 1.7;
    margin-bottom: 1.8rem;
}
.hero-stat { display: inline-block; margin-right: 2.5rem; text-align: center; }
.hero-stat-val {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    color: var(--gold);
    font-weight: 700;
    display: block;
}
.hero-stat-lbl { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

.feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem;
    position: relative;
    overflow: hidden;
    height: 100%;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.card-gold::before { background: linear-gradient(90deg, var(--gold), var(--gold-light)); }
.card-teal::before { background: linear-gradient(90deg, var(--accent), #2BBDB5); }
.card-pink::before { background: linear-gradient(90deg, var(--pink), #FF69B4); }
.card-purple::before { background: linear-gradient(90deg, #9b59b6, #7B2FBE); }

.feature-icon { font-size: 2rem; margin-bottom: 0.8rem; display: block; }
.feature-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.5rem;
}
.feature-desc { font-size: 0.88rem; color: var(--muted); line-height: 1.65; margin-bottom: 1rem; }
.feature-tag {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--muted);
    font-size: 0.72rem;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    margin: 0.15rem;
}

.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.4rem;
}
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.3rem;
}
.section-sub { font-size: 0.9rem; color: var(--muted); margin-bottom: 1.5rem; }
.gold-divider { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
.cap-item {
    display: flex;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.9rem;
    color: var(--text);
}
.cap-dot { width: 6px; height: 6px; background: var(--gold); border-radius: 50%; margin-right: 0.8rem; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.5rem; border-bottom:1px solid rgba(201,168,76,0.2); margin-bottom:1.5rem;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:700;color:#C9A84C;">🌍 TourismAI</div>
        <div style="font-size:0.75rem;color:#8A9BB0;margin-top:0.2rem;">Analytics Platform v2.0</div>
    </div>
    <div style="font-size:0.72rem;letter-spacing:2px;text-transform:uppercase;color:#8A9BB0;margin-bottom:0.8rem;">Navigation</div>
    """, unsafe_allow_html=True)
    st.markdown('<hr style="border-top:1px solid rgba(201,168,76,0.15);margin:1.5rem 0;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.78rem;color:#8A9BB0;line-height:1.7;">
        <strong style="color:#C9A84C;">System Status</strong><br>
        🟢 All models online<br>
        🟢 Data pipeline active<br>
        🟢 API endpoints healthy
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🤖 AI-Powered Analytics Platform</div>
    <div class="hero-title">Tourism Experience<br><span>Analytics</span> Intelligence</div>
    <div class="hero-sub">
        A unified machine learning platform for tourism pattern analysis,
        visit mode prediction, attraction rating estimation, and personalised
        destination recommendations — built for enterprise deployment.
    </div>
    <div>
        <div class="hero-stat"><span class="hero-stat-val">3K+</span><span class="hero-stat-lbl">Records Analysed</span></div>
        <div class="hero-stat"><span class="hero-stat-val">3</span><span class="hero-stat-lbl">ML Models</span></div>
        <div class="hero-stat"><span class="hero-stat-val">9+</span><span class="hero-stat-lbl">Attraction Types</span></div>
        <div class="hero-stat"><span class="hero-stat-val">6</span><span class="hero-stat-lbl">Continents</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Feature Cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Platform Modules</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Four Integrated Intelligence Systems</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Each module is independently deployable and integrates seamlessly into the analytics pipeline.</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

features = [
    ("card-gold", "📊", "EDA Insights", "Interactive exploration of tourism data — distributions, seasonality, and behavioural trends across continents."),
    ("card-teal", "🧭", "Visit Mode Classifier", "Predict whether a tourist visit is Business, Couples, Family, Friends, or Solo using contextual ML classification."),
    ("card-pink", "⭐", "Rating Predictor", "Estimate the star rating a tourist will assign to an attraction based on their profile and visit context."),
    ("card-purple", "🏝", "Recommendation Engine", "Hybrid content + collaborative filtering engine that surfaces the best-matched attractions for any user."),
]

for col, (card_cls, icon, title, desc) in zip([c1, c2, c3, c4], features):
    col.markdown(f"""
    <div class="feature-card {card_cls}">
        <span class="feature-icon">{icon}</span>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── Capabilities ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">System Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Built for Scale & Precision</div>', unsafe_allow_html=True)

cap1, cap2, cap3 = st.columns(3)
for col, caps in zip([cap1, cap2, cap3], [
    ["Tourism Data Exploration & EDA", "Multi-class Visit Mode Prediction", "Attraction Rating Regression"],
    ["Hybrid Recommendation Engine", "ML-Powered Pattern Recognition", "Interactive Analytics Dashboard"],
    ["Real-time Model Inference", "Plotly Visualisation Suite", "Enterprise-grade Architecture"],
]):
    items = "".join(f'<div class="cap-item"><div class="cap-dot"></div>{c}</div>' for c in caps)
    col.markdown(f'<div>{items}</div>', unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:1rem 0;color:#8A9BB0;font-size:0.82rem;">
    Tourism Experience Analytics Platform &nbsp;·&nbsp; Powered by Machine Learning &nbsp;·&nbsp; Enterprise Edition
</div>
""", unsafe_allow_html=True)