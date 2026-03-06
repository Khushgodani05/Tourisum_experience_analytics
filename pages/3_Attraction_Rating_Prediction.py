import streamlit as st
from rating_attraction_prediction.ratingpredict import predict_rating

st.set_page_config(page_title="Rating Predictor", page_icon="⭐", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root { --gold:#C9A84C; --deep:#0D1B2A; --surface:#132236; --accent:#4ECDC4; --pink:#E84393; --text:#E8EDF2; --muted:#8A9BB0; --border:rgba(201,168,76,0.2); }
html,body,[class*="css"]{ font-family:'DM Sans',sans-serif; background-color:var(--deep); color:var(--text); }
.main { background-color:var(--deep); }
section[data-testid="stSidebar"]{ background:linear-gradient(180deg,#0A1628 0%,#0D1B2A 100%); border-right:1px solid var(--border); }
section[data-testid="stSidebar"] * { color:var(--text)!important; }
#MainMenu, footer { visibility:hidden; }

.page-header { background:linear-gradient(135deg,#1e1428 0%,#160d28 100%); border:1px solid rgba(232,67,147,0.25); border-radius:16px; padding:2rem 2.2rem; margin-bottom:1.8rem; position:relative; overflow:hidden; }
.page-header::after { content:''; position:absolute; top:-30px; right:-30px; width:150px; height:150px; background:radial-gradient(circle,rgba(232,67,147,0.1) 0%,transparent 70%); border-radius:50%; }
.page-badge { display:inline-block; background:rgba(232,67,147,0.1); border:1px solid rgba(232,67,147,0.3); color:var(--pink); font-size:0.7rem; font-weight:600; letter-spacing:2px; text-transform:uppercase; padding:0.28rem 0.8rem; border-radius:20px; margin-bottom:0.8rem; }
.page-title { font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:700; color:var(--text); margin-bottom:0.3rem; }
.page-title span { color:var(--pink); }
.page-sub { font-size:0.9rem; color:var(--muted); }

.form-section { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:1.5rem; margin-bottom:1rem; }
.form-section-title { font-family:'Cormorant Garamond',serif; font-size:1.1rem; font-weight:600; color:var(--text); margin-bottom:1rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(255,255,255,0.07); }

.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div {
    background-color: #0D1B2A !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 8px !important;
    color: #E8EDF2 !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label { color: #8A9BB0 !important; font-size: 0.82rem !important; }

.rating-display {
    background: linear-gradient(135deg, #1e1428 0%, #132236 100%);
    border: 1px solid rgba(232,67,147,0.4);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
}
.rating-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 5rem;
    font-weight: 700;
    color: var(--gold);
    line-height: 1;
    margin-bottom: 0.5rem;
}
.rating-stars { font-size: 2rem; margin-bottom: 1rem; letter-spacing: 4px; }
.rating-out-of { font-size:0.8rem; color:var(--muted); letter-spacing:1px; text-transform:uppercase; margin-bottom:1.5rem; }

.metric-mini {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 0.9rem;
    text-align: center;
}
.metric-mini-val { font-family:'Cormorant Garamond',serif; font-size:1.6rem; color:var(--gold); font-weight:700; }
.metric-mini-lbl { font-size:0.72rem; color:var(--muted); margin-top:0.2rem; }

.gold-divider { border:none; border-top:1px solid var(--border); margin:1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.2rem; border-bottom:1px solid rgba(201,168,76,0.2); margin-bottom:1.2rem;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:700;color:#C9A84C;">🌍 TourismAI</div>
        <div style="font-size:0.72rem;color:#8A9BB0;margin-top:0.2rem;">Analytics Platform v2.0</div>
    </div>
    <div style="font-size:0.78rem;color:#8A9BB0;line-height:1.8;">
        <strong style="color:#E84393;">About this Model</strong><br>
        Predicts the expected star rating (1–5) a tourist will assign based on their profile, visit context, and attraction characteristics.
        <br><br>
        <strong style="color:#C9A84C;">Scale</strong><br>
        ⭐ 1 — Very Poor<br>
        ⭐⭐ 2 — Poor<br>
        ⭐⭐⭐ 3 — Average<br>
        ⭐⭐⭐⭐ 4 — Good<br>
        ⭐⭐⭐⭐⭐ 5 — Excellent
    </div>
    """, unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-badge">⭐ Module 3 — Regression</div>
    <div class="page-title">Attraction <span>Rating</span> Predictor</div>
    <div class="page-sub">Estimate the expected tourist rating for an attraction using ML regression on visitor and location features.</div>
</div>
""", unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
with st.form("ratingform"):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="form-section"><div class="form-section-title">👤 User Profile</div>', unsafe_allow_html=True)
        useridx = st.number_input("User ID", value=14)
        continent = st.text_input("Continent", "Europe")
        region = st.text_input("Region", "Southern Europe")
        usercountry = st.text_input("Country", "Portugal")
        usercity = st.text_input("City", "Lagos")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-section"><div class="form-section-title">📍 Visit Context</div>', unsafe_allow_html=True)
        transactionid = st.number_input("Transaction ID", value=5661)
        visityearx = st.number_input("Visit Year", value=2018)
        visitmonthx = st.number_input("Visit Month", value=12)
        attractionidx = st.number_input("Attraction ID", value=640)
        visitmodex = st.selectbox("Visit Mode", ["Business","Couples","Family","Friends","Solo"], index=3)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-section"><div class="form-section-title">🏝 Attraction Details</div>', unsafe_allow_html=True)
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

    submit = st.form_submit_button("⭐ Predict Rating", use_container_width=True)

# ── Prediction Result ─────────────────────────────────────────────────────────
if submit:
    input_data = {
        "useridx": useridx, "continent": continent, "region": region,
        "usercountry": usercountry, "usercity": usercity,
        "transactionid": transactionid, "visityearx": visityearx,
        "visitmonthx": visitmonthx, "attractionidx": attractionidx,
        "visitmodex": visitmodex, "attraction": attraction,
        "attractionaddress": attractionaddress, "attractiontype": attractiontype,
        "attractioncity": attractioncity, "attractioncountry": attractioncountry
    }

    with st.spinner("Predicting rating..."):
        rating = predict_rating(input_data)

    rounded = round(rating, 2)
    stars_full = int(rounded)
    stars_display = "⭐" * stars_full + ("✨" if rounded - stars_full >= 0.5 else "")

    pct = (rounded / 5.0) * 100

    if rounded >= 4.5:
        quality_label, quality_color = "Excellent", "#2ecc71"
    elif rounded >= 3.5:
        quality_label, quality_color = "Good", "#C9A84C"
    elif rounded >= 2.5:
        quality_label, quality_color = "Average", "#E8C97A"
    else:
        quality_label, quality_color = "Below Average", "#E84393"

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    r1, r2, r3 = st.columns([1, 2, 1])
    with r2:
        st.markdown(f"""
        <div class="rating-display">
            <div style="font-size:0.75rem;letter-spacing:2px;text-transform:uppercase;color:#8A9BB0;margin-bottom:0.5rem;">Predicted Rating</div>
            <div class="rating-number">{rounded}</div>
            <div class="rating-stars">{stars_display}</div>
            <div class="rating-out-of">out of 5.0</div>
            <div style="background:rgba(255,255,255,0.06);border-radius:20px;height:8px;overflow:hidden;margin-bottom:1rem;">
                <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#C9A84C,{quality_color});border-radius:20px;"></div>
            </div>
            <div style="display:inline-block;background:rgba({int(quality_color[1:3],16)},{int(quality_color[3:5],16)},{int(quality_color[5:7],16)},0.15);border:1px solid {quality_color};color:{quality_color};font-size:0.8rem;font-weight:600;letter-spacing:1px;padding:0.35rem 1rem;border-radius:20px;text-transform:uppercase;">{quality_label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    # Mini metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="metric-mini"><div class="metric-mini-val">{rounded}</div><div class="metric-mini-lbl">Raw Score</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-mini"><div class="metric-mini-val">{stars_full}/5</div><div class="metric-mini-lbl">Star Rating</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-mini"><div class="metric-mini-val">{pct:.0f}%</div><div class="metric-mini-lbl">Percentile</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-mini"><div class="metric-mini-val" style="color:{quality_color};">{quality_label}</div><div class="metric-mini-lbl">Quality Band</div></div>', unsafe_allow_html=True)