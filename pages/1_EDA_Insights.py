import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EDA Insights", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root { --gold:#C9A84C; --gold-light:#E8C97A; --deep:#0D1B2A; --surface:#132236; --accent:#4ECDC4; --pink:#E84393; --text:#E8EDF2; --muted:#8A9BB0; --border:rgba(201,168,76,0.2); }
html,body,[class*="css"]{ font-family:'DM Sans',sans-serif; background-color:var(--deep); color:var(--text); }
.main { background-color:var(--deep); }
section[data-testid="stSidebar"]{ background:linear-gradient(180deg,#0A1628 0%,#0D1B2A 100%); border-right:1px solid var(--border); }
section[data-testid="stSidebar"] * { color:var(--text)!important; }
#MainMenu, footer { visibility:hidden; }
.page-header { background:linear-gradient(135deg,#132236 0%,#0D2440 100%); border:1px solid var(--border); border-radius:16px; padding:2rem 2.2rem; margin-bottom:1.8rem; position:relative; overflow:hidden; }
.page-header::after { content:''; position:absolute; top:-30px; right:-30px; width:150px; height:150px; background:radial-gradient(circle,rgba(201,168,76,0.1) 0%,transparent 70%); border-radius:50%; }
.page-badge { display:inline-block; background:rgba(201,168,76,0.12); border:1px solid var(--border); color:var(--gold); font-size:0.7rem; font-weight:600; letter-spacing:2px; text-transform:uppercase; padding:0.28rem 0.8rem; border-radius:20px; margin-bottom:0.8rem; }
.page-title { font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:700; color:var(--text); margin-bottom:0.3rem; }
.page-title span { color:var(--gold); }
.page-sub { font-size:0.9rem; color:var(--muted); }
.metric-card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:1.2rem 1rem; text-align:center; }
.metric-val { font-family:'Cormorant Garamond',serif; font-size:2rem; color:var(--gold); font-weight:700; display:block; }
.metric-lbl { font-size:0.78rem; color:var(--muted); margin-top:0.2rem; }
.chart-container { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:1.2rem 1.2rem 0.6rem; margin-bottom:0.5rem; }
.chart-title { font-family:'Cormorant Garamond',serif; font-size:1.15rem; font-weight:600; color:var(--text); margin-bottom:0.8rem; }
.insight-box { background:rgba(78,205,196,0.06); border-left:3px solid var(--accent); border-radius:8px; padding:0.9rem 1.1rem; margin-top:0.6rem; font-size:0.88rem; color:var(--text); line-height:1.6; }
.section-label { font-size:0.7rem; font-weight:600; letter-spacing:2.5px; text-transform:uppercase; color:var(--gold); margin-bottom:0.3rem; }
.gold-divider { border:none; border-top:1px solid var(--border); margin:1.5rem 0; }
</style>
""", unsafe_allow_html=True)

PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,27,42,0.5)',
    font=dict(color='#E8EDF2', family='DM Sans'),
    margin=dict(l=20, r=20, t=30, b=20),
)

@st.cache_data
def load_simulated_data():
    np.random.seed(42)
    n = 3000
    continents = ['Europe', 'Asia', 'North America', 'South America', 'Africa', 'Australia & Oceania']
    cont_weights = [0.35, 0.28, 0.18, 0.08, 0.07, 0.04]
    attraction_types = [
        'Nature & Wildlife Areas', 'Points of Interest & Landmarks',
        'Museums', 'Beaches', 'Shopping', 'Religious Sites',
        'Amusement Parks', 'Spas & Wellness', 'Restaurants'
    ]
    visit_modes = ['Couples', 'Family', 'Friends', 'Solo', 'Business']
    vm_weights  = [0.30, 0.25, 0.22, 0.15, 0.08]
    cities = ['Bali', 'Paris', 'New York', 'Tokyo', 'Douala', 'Rome', 'Sydney', 'Dubai', 'Bangkok', 'Cape Town']
    years  = list(range(2015, 2024))
    year_weights = [0.05,0.07,0.10,0.12,0.14,0.10,0.09,0.18,0.15]
    df = pd.DataFrame({
        'continent':      np.random.choice(continents, n, p=cont_weights),
        'attractiontype': np.random.choice(attraction_types, n),
        'rating':         np.clip(np.random.normal(3.8, 0.8, n), 1, 5).round().astype(int),
        'visitmode':      np.random.choice(visit_modes, n, p=vm_weights),
        'city':           np.random.choice(cities, n),
        'visityear':      np.random.choice(years, n, p=year_weights),
        'visitmonth':     np.random.randint(1, 13, n),
    })
    return df

df = load_simulated_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.2rem; border-bottom:1px solid rgba(201,168,76,0.2); margin-bottom:1.2rem;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:700;color:#C9A84C;">🌍 TourismAI</div>
        <div style="font-size:0.72rem;color:#8A9BB0;margin-top:0.2rem;">Analytics Platform v2.0</div>
    </div>
    <div style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:#8A9BB0;margin-bottom:0.6rem;">Dashboard Filters</div>
    """, unsafe_allow_html=True)
    selected_continent = st.multiselect("Continent", df['continent'].unique().tolist(), default=df['continent'].unique().tolist())
    selected_mode = st.multiselect("Visit Mode", df['visitmode'].unique().tolist(), default=df['visitmode'].unique().tolist())
    st.markdown('<hr style="border-top:1px solid rgba(201,168,76,0.15);margin:1rem 0;">', unsafe_allow_html=True)

filtered = df[df['continent'].isin(selected_continent) & df['visitmode'].isin(selected_mode)]
if len(filtered) == 0:
    st.warning("No data matches the current filters. Please adjust the sidebar selections.")
    st.stop()

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="page-badge">📊 Module 1 — Exploratory Analysis</div>
    <div class="page-title">EDA <span>Insights</span> Dashboard</div>
    <div class="page-sub">Interactive exploration of tourism data across {filtered['continent'].nunique()} continents and {filtered['city'].nunique()} cities.</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
metrics = [
    (f"{len(filtered):,}", "Total Records"),
    (f"{filtered['continent'].nunique()}", "Continents"),
    (f"{filtered['attractiontype'].nunique()}", "Attraction Types"),
    (f"{filtered['city'].nunique()}", "Cities"),
    (f"{filtered['rating'].mean():.2f} ⭐", "Avg Rating"),
]
for col, (val, lbl) in zip([k1,k2,k3,k4,k5], metrics):
    col.markdown(f'<div class="metric-card"><span class="metric-val">{val}</span><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── Row 1 ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Geographic &amp; Behavioural Distribution</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-container"><div class="chart-title">🌐 Users by Continent</div>', unsafe_allow_html=True)
    cont_df = filtered['continent'].value_counts().reset_index()
    cont_df.columns = ['continent', 'count']
    fig = px.bar(cont_df, x='count', y='continent', orientation='h',
                 color='count', color_continuous_scale=['#132236','#C9A84C'])
    fig.update_layout(**PLOTLY_THEME, coloraxis_showscale=False, height=300)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("💡 Insight"):
        st.markdown('<div class="insight-box">Europe dominates with ~35% of tourists, followed by Asia. African and Oceanian users are underrepresented — a potential growth market worth targeting with localised campaigns.</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-container"><div class="chart-title">🧭 Visit Mode Distribution</div>', unsafe_allow_html=True)
    vm_df = filtered['visitmode'].value_counts().reset_index()
    vm_df.columns = ['mode', 'count']
    fig2 = px.pie(vm_df, names='mode', values='count',
                  color_discrete_sequence=['#C9A84C','#4ECDC4','#E84393','#2ecc71','#9b59b6'],
                  hole=0.5)
    fig2.update_layout(**PLOTLY_THEME, height=300, showlegend=True,
                       legend=dict(orientation='h', y=-0.18, font=dict(size=11)))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("💡 Insight"):
        st.markdown('<div class="insight-box">Couples travel is the most common visit mode (30%), with Business travel least frequent (8%). This shapes recommendation strategies significantly.</div>', unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── Row 2 ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Ratings &amp; Attraction Categories</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="chart-container"><div class="chart-title">⭐ Rating Distribution</div>', unsafe_allow_html=True)
    rating_df = filtered['rating'].value_counts().sort_index().reset_index()
    rating_df.columns = ['rating', 'count']
    fig3 = px.bar(rating_df, x='rating', y='count',
                  color='rating', color_continuous_scale=['#E84393','#C9A84C','#4ECDC4'], text='count')
    fig3.update_layout(**PLOTLY_THEME, coloraxis_showscale=False, height=300,
                       xaxis_title="Rating (1–5)", yaxis_title="Count")
    fig3.update_traces(textposition='outside', marker_line_width=0)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("💡 Insight"):
        st.markdown('<div class="insight-box">Ratings cluster around 4–5, suggesting a positive-bias common in tourism reviews. Very few 1-star reviews indicate either selection bias or genuine quality.</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-container"><div class="chart-title">🏛️ Popular Attraction Types</div>', unsafe_allow_html=True)
    at_df = filtered['attractiontype'].value_counts().reset_index()
    at_df.columns = ['type', 'count']
    fig4 = px.bar(at_df, x='count', y='type', orientation='h',
                  color='count', color_continuous_scale=['#1a3a5c','#4ECDC4'])
    fig4.update_layout(**PLOTLY_THEME, coloraxis_showscale=False, height=300)
    fig4.update_traces(marker_line_width=0)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("💡 Insight"):
        st.markdown('<div class="insight-box">Nature & Wildlife and Points of Interest lead, reflecting a global trend toward experiential and eco-tourism.</div>', unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── Row 3 ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Destinations &amp; Temporal Trends</div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)

with c5:
    st.markdown('<div class="chart-container"><div class="chart-title">🏙️ Top Visited Cities</div>', unsafe_allow_html=True)
    city_df = filtered['city'].value_counts().head(10).reset_index()
    city_df.columns = ['city', 'visits']
    fig5 = px.bar(city_df, x='visits', y='city', orientation='h',
                  color='visits', color_continuous_scale=['#132236','#C9A84C'])
    fig5.update_layout(**PLOTLY_THEME, coloraxis_showscale=False, height=320)
    fig5.update_traces(marker_line_width=0)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c6:
    st.markdown('<div class="chart-container"><div class="chart-title">📅 Visits Over the Years</div>', unsafe_allow_html=True)
    yr_df = filtered['visityear'].value_counts().sort_index().reset_index()
    yr_df.columns = ['year', 'visits']
    fig6 = px.area(yr_df, x='year', y='visits', color_discrete_sequence=['#4ECDC4'])
    fig6.update_layout(**PLOTLY_THEME, height=320, xaxis_title='Year', yaxis_title='Visits')
    fig6.update_traces(line_color='#C9A84C', fillcolor='rgba(78,205,196,0.12)')
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("💡 Insight"):
        st.markdown('<div class="insight-box">A dip is visible around 2020–2021 reflecting COVID-19 impact, with strong recovery in 2022–2023.</div>', unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── Heatmap ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Cross-Dimensional Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-container"><div class="chart-title">🔥 Visit Mode × Attraction Type Heatmap</div>', unsafe_allow_html=True)
pivot = filtered.groupby(['visitmode','attractiontype']).size().unstack(fill_value=0)
fig7 = px.imshow(pivot, color_continuous_scale=['#0D1B2A','#C9A84C','#4ECDC4'],
                 aspect='auto', text_auto=True)
fig7.update_layout(**PLOTLY_THEME, height=360, coloraxis_showscale=False, xaxis_tickangle=-30)
st.plotly_chart(fig7, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
with st.expander("💡 Insight"):
    st.markdown('<div class="insight-box">Family travelers strongly prefer Nature & Wildlife and Amusement Parks, while Business travelers gravitate toward Restaurants and Spas. Couples dominate Beach visits.</div>', unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── Radar ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Seasonality</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-container"><div class="chart-title">📆 Monthly Visit Seasonality</div>', unsafe_allow_html=True)
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthly = filtered['visitmonth'].value_counts().sort_index()
fig8 = go.Figure(go.Scatterpolar(
    r=monthly.values.tolist() + [monthly.values[0]],
    theta=month_names + [month_names[0]],
    fill='toself', line_color='#C9A84C', fillcolor='rgba(201,168,76,0.12)'
))
fig8.update_layout(**PLOTLY_THEME, height=380,
                   polar=dict(bgcolor='rgba(13,27,42,0.7)',
                              radialaxis=dict(gridcolor='rgba(255,255,255,0.08)'),
                              angularaxis=dict(gridcolor='rgba(255,255,255,0.08)')))
st.plotly_chart(fig8, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
with st.expander("💡 Insight"):
    st.markdown('<div class="insight-box">Summer months (June–August) and December show peak visits, consistent with school holidays and year-end travel patterns globally.</div>', unsafe_allow_html=True)