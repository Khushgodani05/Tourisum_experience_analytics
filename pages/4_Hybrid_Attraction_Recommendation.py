import streamlit as st
from attraction_reccomendation.hybrid_based_recemmonder.hybrid import model

st.set_page_config(page_title="Recommendation Engine", page_icon="🏝", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root { --gold:#C9A84C; --deep:#0D1B2A; --surface:#132236; --accent:#4ECDC4; --pink:#E84393; --purple:#9b59b6; --text:#E8EDF2; --muted:#8A9BB0; --border:rgba(201,168,76,0.2); }
html,body,[class*="css"]{ font-family:'DM Sans',sans-serif; background-color:var(--deep); color:var(--text); }
.main { background-color:var(--deep); }
section[data-testid="stSidebar"]{ background:linear-gradient(180deg,#0A1628 0%,#0D1B2A 100%); border-right:1px solid var(--border); }
section[data-testid="stSidebar"] * { color:var(--text)!important; }
#MainMenu, footer { visibility:hidden; }

.page-header { background:linear-gradient(135deg,#121428 0%,#0D1B2A 100%); border:1px solid rgba(155,89,182,0.3); border-radius:16px; padding:2rem 2.2rem; margin-bottom:1.8rem; position:relative; overflow:hidden; }
.page-header::after { content:''; position:absolute; top:-30px; right:-30px; width:150px; height:150px; background:radial-gradient(circle,rgba(155,89,182,0.12) 0%,transparent 70%); border-radius:50%; }
.page-badge { display:inline-block; background:rgba(155,89,182,0.12); border:1px solid rgba(155,89,182,0.35); color:var(--purple); font-size:0.7rem; font-weight:600; letter-spacing:2px; text-transform:uppercase; padding:0.28rem 0.8rem; border-radius:20px; margin-bottom:0.8rem; }
.page-title { font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:700; color:var(--text); margin-bottom:0.3rem; }
.page-title span { color:var(--purple); }
.page-sub { font-size:0.9rem; color:var(--muted); }

.search-container { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:2rem; margin-bottom:1.5rem; }
.search-title { font-family:'Cormorant Garamond',serif; font-size:1.15rem; font-weight:600; color:var(--text); margin-bottom:0.8rem; }

.stTextArea > div > div > textarea, .stTextInput > div > div > input {
    background-color: #0D1B2A !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 10px !important;
    color: #E8EDF2 !important;
    font-size: 0.92rem !important;
}
.stTextArea label, .stTextInput label { color: #8A9BB0 !important; font-size: 0.82rem !important; }

.method-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--muted);
    font-size: 0.78rem;
    padding: 0.35rem 0.9rem;
    border-radius: 20px;
    margin: 0.25rem;
}

.results-header { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:1rem; display:flex; align-items:center; justify-content:space-between; }
.results-count { font-family:'Cormorant Garamond',serif; font-size:1.6rem; font-weight:700; color:var(--gold); }
.results-label { font-size:0.8rem; color:var(--muted); }

.stDataFrame { border-radius: 12px; overflow: hidden; }

.info-card { background:rgba(155,89,182,0.06); border:1px solid rgba(155,89,182,0.2); border-radius:12px; padding:1.2rem; }
.info-card-title { font-size:0.78rem; letter-spacing:1.5px; text-transform:uppercase; color:var(--purple); margin-bottom:0.6rem; font-weight:600; }
.info-item { font-size:0.87rem; color:var(--muted); padding:0.3rem 0; border-bottom:1px solid rgba(255,255,255,0.04); }
.info-item:last-child { border-bottom:none; }
.info-item span { color:var(--text); }

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
        <strong style="color:#9b59b6;">About this Engine</strong><br>
        A hybrid recommendation system combining content-based and collaborative filtering to surface the most relevant attractions.
        <br><br>
        <strong style="color:#C9A84C;">Methods Used</strong><br>
        📄 Content-Based Filtering<br>
        👥 Collaborative Filtering<br>
        🔀 Hybrid Score Fusion
    </div>
    """, unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-badge">🏝 Module 4 — Recommendation</div>
    <div class="page-title">Hybrid Attraction <span>Recommender</span></div>
    <div class="page-sub">AI-powered destination discovery using content-based and collaborative filtering in a unified hybrid engine.</div>
</div>
""", unsafe_allow_html=True)

# ── Method Tags ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:1.5rem;">
    <span class="method-badge">📄 Content-Based Filtering</span>
    <span class="method-badge">👥 Collaborative Filtering</span>
    <span class="method-badge">🔀 Hybrid Score Fusion</span>
    <span class="method-badge">🤖 ML-Powered Ranking</span>
</div>
""", unsafe_allow_html=True)

# ── Search Interface ──────────────────────────────────────────────────────────
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.markdown('<div class="search-title">🔍 Search Parameters</div>', unsafe_allow_html=True)

s1, s2 = st.columns([2, 1])
with s1:
    desc = st.text_area(
        "Attraction Description",
        "@@@Sacred Monkey Forest Sanctuary !!!!",
        height=100,
        help="Enter the attraction description. The model uses this for content-based matching."
    )
with s2:
    city = st.text_input(
        "Attraction City",
        "douala",
        help="City name used for geographic filtering."
    )
    st.markdown('<br>', unsafe_allow_html=True)
    generate = st.button("🔎 Generate Recommendations", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ── Results ───────────────────────────────────────────────────────────────────
if generate:
    with st.spinner("Running hybrid recommendation engine..."):
        results = model.reccomend(desc, city)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    # Results header
    n_results = len(results)
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:1.5rem;background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;">
        <div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:700;color:#C9A84C;">{n_results}</div>
            <div style="font-size:0.75rem;color:#8A9BB0;text-transform:uppercase;letter-spacing:1px;">Recommendations Found</div>
        </div>
        <div style="flex:1;height:1px;background:rgba(255,255,255,0.06);"></div>
        <div style="font-size:0.82rem;color:#8A9BB0;">
            🏙️ City: <strong style="color:#E8EDF2;">{city.title()}</strong> &nbsp;·&nbsp;
            🔀 Engine: <strong style="color:#9b59b6;">Hybrid</strong> &nbsp;·&nbsp;
            ✅ Status: <strong style="color:#2ecc71;">Complete</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top 3 highlight badges
    if n_results >= 3:
        st.markdown('<div style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:#C9A84C;margin-bottom:0.6rem;">🏆 Top Recommendations</div>', unsafe_allow_html=True)
        medals = ["🥇", "🥈", "🥉"]
        top_cols = st.columns(min(3, n_results))
        for i, (col, medal) in enumerate(zip(top_cols, medals)):
            row = results.iloc[i]
            name_col = results.columns[0] if len(results.columns) > 0 else "Attraction"
            name = str(row[name_col]) if name_col in results.columns else f"Attraction {i+1}"
            col.markdown(f"""
            <div style="background:rgba(201,168,76,0.07);border:1px solid rgba(201,168,76,0.2);border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.5rem;margin-bottom:0.3rem;">{medal}</div>
                <div style="font-size:0.85rem;font-weight:600;color:#E8EDF2;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{name[:30]}{"..." if len(str(name)) > 30 else ""}</div>
                <div style="font-size:0.72rem;color:#8A9BB0;margin-top:0.2rem;">Rank #{i+1}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)

    # ── Full-Width List Cards ─────────────────────────────────────────────────
    st.markdown('<p style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:#8A9BB0;margin:1.4rem 0 1rem;">Recommended Attractions</p>', unsafe_allow_html=True)

    rank_icons  = ["🥇", "🥈", "🥉"] + ["🏅"] * max(0, n_results - 3)
    rank_colors = ["#C9A84C", "#A8A9AD", "#CD7F32"] + ["#4ECDC4"] * max(0, n_results - 3)

    for i, (_, row) in enumerate(results.iterrows()):
        icon  = rank_icons[i]
        color = rank_colors[i]

        # Pull the three key fields from model output
        name    = str(row.get("attraction",        row.get("attractionname", row.iloc[0]))).strip()
        address = str(row.get("attractionaddress", row.get("address", "—"))).strip()
        ratingx = str(row.get("ratingx",           row.get("rating",  row.get("avgrating", "—")))).strip()
        if ratingx in ("nan", "None", ""):  ratingx = "—"
        if address in ("nan", "None", ""):  address  = "Not available"

        # Build star display
        try:
            r       = float(ratingx)
            filled  = "⭐" * int(round(r))
            empty   = "☆"  * max(0, 5 - int(round(r)))
            stars   = filled + empty
            r_label = f"{r:.1f} / 5"
        except (ValueError, TypeError):
            stars   = ""
            r_label = ratingx

        card = (
            f'<div style="background:linear-gradient(135deg,#132236 0%,#1A2E47 100%);'
            f'border:1px solid rgba(201,168,76,0.15);border-left:4px solid {color};'
            f'border-radius:14px;padding:1.4rem 2rem;margin-bottom:0.85rem;'
            f'display:flex;align-items:center;gap:2rem;">'

            f'<div style="min-width:3rem;text-align:center;flex-shrink:0;">'
            f'<div style="font-size:1.8rem;line-height:1;">{icon}</div>'
            f'<div style="font-size:0.65rem;color:{color};font-weight:700;letter-spacing:1px;margin-top:0.2rem;">#{i+1}</div>'
            f'</div>'

            f'<div style="width:1px;height:56px;background:rgba(255,255,255,0.07);flex-shrink:0;"></div>'

            f'<div style="flex:1;min-width:0;">'
            f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.2rem;font-weight:700;'
            f'color:#E8EDF2;line-height:1.3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'
            f'margin-bottom:0.35rem;">{name}</div>'
            f'<div style="font-size:0.82rem;color:#8A9BB0;">📍&nbsp;'
            f'<span style="color:#E8EDF2;">{address}</span></div>'
            f'</div>'

            f'<div style="width:1px;height:56px;background:rgba(255,255,255,0.07);flex-shrink:0;"></div>'

            f'<div style="text-align:center;flex-shrink:0;min-width:8rem;">'
            f'<div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:1.5px;color:#8A9BB0;margin-bottom:0.3rem;">Rating</div>'
            f'<div style="font-size:1.4rem;line-height:1;margin-bottom:0.25rem;">{stars if stars else "—"}</div>'
            f'<div style="font-size:0.9rem;font-weight:700;color:{color};">{r_label}</div>'
            f'</div>'

            f'</div>'
        )
        st.markdown(card, unsafe_allow_html=True)

    st.markdown(
        f'<p style="text-align:center;padding:1rem;font-size:0.8rem;color:#8A9BB0;margin-top:0.3rem;">'
        f'✦ Generated {n_results} personalised recommendations using the Hybrid Attraction Engine ✦</p>',
        unsafe_allow_html=True
    )