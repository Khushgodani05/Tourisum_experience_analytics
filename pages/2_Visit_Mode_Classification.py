import streamlit as st
from visit_mode_classification.visitmodeclassify import visitmodeclassify

st.set_page_config(page_title="Visit Mode Classifier", page_icon="🧭", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root { --gold:#C9A84C; --deep:#0D1B2A; --surface:#132236; --accent:#4ECDC4; --pink:#E84393; --text:#E8EDF2; --muted:#8A9BB0; --border:rgba(201,168,76,0.2); }
html,body,[class*="css"]{ font-family:'DM Sans',sans-serif; background-color:var(--deep); color:var(--text); }
.main { background-color:var(--deep); }
section[data-testid="stSidebar"]{ background:linear-gradient(180deg,#0A1628 0%,#0D1B2A 100%); border-right:1px solid var(--border); }
section[data-testid="stSidebar"] * { color:var(--text)!important; }
#MainMenu, footer { visibility:hidden; }

.page-header { background:linear-gradient(135deg,#132236 0%,#0D2440 100%); border:1px solid var(--border); border-radius:16px; padding:2rem 2.2rem; margin-bottom:1.8rem; position:relative; overflow:hidden; }
.page-header::after { content:''; position:absolute; top:-30px; right:-30px; width:150px; height:150px; background:radial-gradient(circle,rgba(78,205,196,0.1) 0%,transparent 70%); border-radius:50%; }
.page-badge { display:inline-block; background:rgba(78,205,196,0.1); border:1px solid rgba(78,205,196,0.3); color:var(--accent); font-size:0.7rem; font-weight:600; letter-spacing:2px; text-transform:uppercase; padding:0.28rem 0.8rem; border-radius:20px; margin-bottom:0.8rem; }
.page-title { font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:700; color:var(--text); margin-bottom:0.3rem; }
.page-title span { color:var(--accent); }
.page-sub { font-size:0.9rem; color:var(--muted); }

.form-section { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:1.5rem; margin-bottom:1rem; }
.form-section-title { font-family:'Cormorant Garamond',serif; font-size:1.1rem; font-weight:600; color:var(--text); margin-bottom:1rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(255,255,255,0.07); }

/* Streamlit input overrides */
.stTextInput > div > div > input, .stNumberInput > div > div > input {
    background-color: #0D1B2A !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 8px !important;
    color: #E8EDF2 !important;
}
.stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
    border-color: #4ECDC4 !important;
    box-shadow: 0 0 0 2px rgba(78,205,196,0.15) !important;
}
.stTextInput label, .stNumberInput label { color: #8A9BB0 !important; font-size: 0.82rem !important; }

.result-card {
    background: linear-gradient(135deg, #132236 0%, #0D2440 100%);
    border: 1px solid var(--accent);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: -40px; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(78,205,196,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.result-label { font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; color:var(--muted); margin-bottom:0.5rem; }
.result-value { font-family:'Cormorant Garamond',serif; font-size:2.8rem; font-weight:700; color:var(--accent); margin-bottom:0.5rem; }
.result-icon { font-size:3rem; margin-bottom:0.8rem; display:block; }

.mode-badge {
    display: inline-block;
    padding: 0.4rem 1.2rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 0.3rem;
}
.gold-divider { border:none; border-top:1px solid var(--border); margin:1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# Mode icon mapping
MODE_ICONS = {
    "Business": "💼",
    "Couples":  "💑",
    "Family":   "👨‍👩‍👧‍👦",
    "Friends":  "👥",
    "Solo":     "🧳",
}
MODE_COLORS = {
    "Business": "#C9A84C",
    "Couples":  "#E84393",
    "Family":   "#4ECDC4",
    "Friends":  "#2ecc71",
    "Solo":     "#9b59b6",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.2rem; border-bottom:1px solid rgba(201,168,76,0.2); margin-bottom:1.2rem;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:700;color:#C9A84C;">🌍 TourismAI</div>
        <div style="font-size:0.72rem;color:#8A9BB0;margin-top:0.2rem;">Analytics Platform v2.0</div>
    </div>
    <div style="font-size:0.78rem;color:#8A9BB0;line-height:1.8;">
        <strong style="color:#4ECDC4;">About this Model</strong><br>
        Classifies tourist visit context into one of five categories using visitor profile and attraction features.
        <br><br>
        <strong style="color:#C9A84C;">Output Classes</strong><br>
        💼 Business<br>💑 Couples<br>👨‍👩‍👧‍👦 Family<br>👥 Friends<br>🧳 Solo
    </div>
    """, unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-badge">🧭 Module 2 — Classification</div>
    <div class="page-title">Visit Mode <span>Classifier</span></div>
    <div class="page-sub">Predict the type of tourist visit — Business, Couples, Family, Friends, or Solo — using ML classification.</div>
</div>
""", unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
with st.form("visitmodeform"):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="form-section"><div class="form-section-title">👤 User Information</div>', unsafe_allow_html=True)
        useridx = st.number_input("User ID", value=73808)
        continent = st.text_input("Continent", "Australia & Oceania")
        region = st.text_input("Region", "Australia")
        usercountry = st.text_input("Country", "Australia")
        usercity = st.text_input("City", "Eastern Creek")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-section"><div class="form-section-title">📍 Visit Details</div>', unsafe_allow_html=True)
        transactionid = st.number_input("Transaction ID", value=4842)
        visityearx = st.number_input("Visit Year", value=2018)
        visitmonthx = st.number_input("Visit Month", value=4)
        attractionidx = st.number_input("Attraction ID", value=640)
        ratingx = st.number_input("Rating", value=5)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-section"><div class="form-section-title">🏝 Attraction Information</div>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    with a1:
        attraction = st.text_input("Attraction Name", "Sacred Monkey Forest Sanctuary")
        attractionaddress = st.text_input("Attraction Address", "Jl. Monkey Forest, Ubud 80571 Indonesia")
    with a2:
        attractiontype = st.text_input("Attraction Type", "Nature & Wildlife Areas")
        attractioncity = st.text_input("Attraction City", "Douala")
    with a3:
        attractioncountry = st.text_input("Attraction Country", "Cameroon")
    st.markdown('</div>', unsafe_allow_html=True)

    submit = st.form_submit_button("🚀 Predict Visit Mode", use_container_width=True)

# ── Prediction ────────────────────────────────────────────────────────────────
if submit:
    input_data = {
        "useridx": useridx, "continent": continent, "region": region,
        "usercountry": usercountry, "usercity": usercity,
        "transactionid": transactionid, "visityearx": visityearx,
        "visitmonthx": visitmonthx, "attractionidx": attractionidx,
        "ratingx": ratingx, "attraction": attraction,
        "attractionaddress": attractionaddress, "attractiontype": attractiontype,
        "attractioncity": attractioncity, "attractioncountry": attractioncountry
    }

    with st.spinner("Analysing visit pattern..."):
        prediction = visitmodeclassify(input_data)

    icon = MODE_ICONS.get(prediction, "🎯")
    color = MODE_COLORS.get(prediction, "#C9A84C")

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    r1, r2, r3 = st.columns([1, 2, 1])
    with r2:
        st.markdown(f"""
        <div class="result-card" style="border-color:{color};">
            <span class="result-icon">{icon}</span>
            <div class="result-label">Predicted Visit Mode</div>
            <div class="result-value" style="color:{color};">{prediction}</div>
            <div style="font-size:0.85rem;color:#8A9BB0;margin-top:0.5rem;">
                Based on visitor profile &amp; attraction context
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    # Show all mode tags with predicted one highlighted
    cols = st.columns(5)
    for col, (mode, ico) in zip(cols, MODE_ICONS.items()):
        mc = MODE_COLORS[mode]
        if mode == prediction:
            col.markdown(f'<div style="background:rgba({int(mc[1:3],16)},{int(mc[3:5],16)},{int(mc[5:7],16)},0.18);border:1px solid {mc};border-radius:10px;padding:0.7rem;text-align:center;font-size:0.85rem;font-weight:600;color:{mc};">{ico} {mode}<br><small style="font-size:0.65rem;letter-spacing:1px;">✓ PREDICTED</small></div>', unsafe_allow_html=True)
        else:
            col.markdown(f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.7rem;text-align:center;font-size:0.85rem;color:#8A9BB0;">{ico} {mode}</div>', unsafe_allow_html=True)