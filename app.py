import streamlit as st
import pandas as pd
import plotly.express as px
import ast

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="Movie Mood Finder",
    page_icon="🎬",
    layout="wide"
)

# ── Y2K 에디토리얼 CSS ────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;600;700&display=swap');

    .stApp {
        background-color: #F5F0E8;
        font-family: 'DM Sans', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background-color: #FADADD;
        border-right: 3px solid #1a1a1a;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }

    .hero-wrap {
        background: #E8F4D4;
        border: 3px solid #1a1a1a;
        border-radius: 20px;
        padding: 36px 40px 28px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .hero-tag {
        display: inline-block;
        background: #FFE44D;
        border: 2px solid #1a1a1a;
        border-radius: 30px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
        padding: 4px 14px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }
    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3.6rem;
        line-height: 1.1;
        color: #1a1a1a;
        margin: 0 0 10px 0;
    }
    .hero-sub {
        font-size: 1rem;
        color: #555;
        margin: 0;
    }

    .card {
        background: #ffffff;
        border: 2.5px solid #1a1a1a;
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 4px 4px 0px #1a1a1a;
    }
    .card-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.2rem;
        color: #1a1a1a;
        margin: 0 0 4px 0;
    }
    .card-meta {
        font-size: 0.82rem;
        color: #666;
        margin-bottom: 8px;
    }
    .card-overview {
        font-size: 0.8rem;
        color: #888;
        line-height: 1.5;
        margin-top: 6px;
    }

    .tag {
        display: inline-block;
        background: #FFE44D;
        border: 1.5px solid #1a1a1a;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 2px 10px;
        margin: 2px;
        color: #1a1a1a;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .tag.pink  { background: #FFB3C6; }
    .tag.green { background: #C8F0A0; }
    .tag.blue  { background: #A8D8EA; }

    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #999;
        margin-bottom: 4px;
    }
    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem;
        color: #1a1a1a;
        margin: 0 0 16px 0;
        border-bottom: 2.5px solid #1a1a1a;
        padding-bottom: 8px;
    }

    .chart-card {
        background: #fff;
        border: 2.5px solid #1a1a1a;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 4px 4px 0px #1a1a1a;
    }

    .result-badge {
        display: inline-block;
        background: #1a1a1a;
        color: #FFE44D;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 4px 14px;
        border-radius: 30px;
        margin-bottom: 14px;
    }

    h1, h2, h3, h4 { color: #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

# ── 감정 매핑 ─────────────────────────────────────────────────
EMOTION_MAP = {
    "comforting": ["Animation", "Family", "Comedy"],
    "emotional":  ["Drama", "Romance", "Music"],
    "exciting":   ["Action", "Adventure", "Thriller"],
    "inspiring":  ["Documentary", "History"],
    "nostalgic":  ["Romance", "Music", "History"],
    "immersive":  ["Science Fiction", "Fantasy", "Mystery"],
    "calm":       ["Documentary", "Animation"],
}

MOOD_LABELS = {
    "comforting": "😊 위로받고 싶어",
    "emotional":  "🥺 감동받고 싶어",
    "exciting":   "⚡ 짜릿한 거 보고 싶어",
    "inspiring":  "💪 동기부여 받고 싶어",
    "nostalgic":  "🌙 감성적인 거 보고 싶어",
    "immersive":  "🚀 완전 몰입하고 싶어",
    "calm":       "☁️ 조용히 힐링하고 싶어",
}

# ── 데이터 로드 ───────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("tmdb_5000_movies.csv")

    def parse_genres(g):
        try:
            return [x["name"] for x in ast.literal_eval(g)]
        except:
            return []

    df["genre_list"] = df["genres"].apply(parse_genres)
    df["genre_str"]  = df["genre_list"].apply(lambda x: ", ".join(x))

    def assign_emotions(genres):
        tags = [e for e, gs in EMOTION_MAP.items() if any(g in genres for g in gs)]
        return tags if tags else ["general"]

    df["emotions"] = df["genre_list"].apply(assign_emotions)
    df = df.dropna(subset=["title", "vote_average", "runtime"])
    df = df[(df["runtime"] > 0) & (df["vote_average"] > 0)]
    df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    return df

df = load_data()

# ── 히어로 헤더 ───────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-tag">✦ Emotion-Based Recommendation</div>
    <div class="hero-title">Movie<br>Mood Finder</div>
    <p class="hero-sub">지금 기분에 딱 맞는 영화를 찾아드려요 ✦</p>
</div>
""", unsafe_allow_html=True)

# ── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎭 지금 기분이 어때?")
    selected_mood = st.radio(
        "",
        options=list(MOOD_LABELS.keys()),
        format_func=lambda x: MOOD_LABELS[x]
    )

    st.markdown("---")
    st.markdown("### ⏱️ 얼마나 볼 수 있어?")
    runtime_option = st.select_slider(
        "",
        options=["90분 이하", "90~120분", "120분 이상", "상관없음"],
        value="상관없음"
    )

    st.markdown("---")
    st.markdown("### ⭐ 최소 평점")
    min_rating = st.slider("", 0.0, 10.0, 7.0, 0.5, format="%.1f")

# ── 필터링 ───────────────────────────────────────────────────
filtered = df[df["emotions"].apply(lambda x: selected_mood in x)]

if runtime_option == "90분 이하":
    filtered = filtered[filtered["runtime"] <= 90]
elif runtime_option == "90~120분":
    filtered = filtered[(filtered["runtime"] > 90) & (filtered["runtime"] <= 120)]
elif runtime_option == "120분 이상":
    filtered = filtered[filtered["runtime"] > 120]

filtered = filtered[filtered["vote_average"] >= min_rating]
filtered = filtered.sort_values("popularity", ascending=False).head(20)

# ── 레이아웃 ─────────────────────────────────────────────────
col_movies, col_charts = st.columns([2, 1], gap="large")

with col_movies:
    st.markdown('<div class="section-label">RESULTS</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{MOOD_LABELS[selected_mood]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-badge">✦ {len(filtered)}편 발견</div>', unsafe_allow_html=True)

    if filtered.empty:
        st.warning("조건에 맞는 영화가 없어요. 필터를 조정해봐!")
    else:
        colors = ["", "pink", "green", "blue"]
        for _, row in filtered.iterrows():
            year = int(row["release_year"]) if pd.notna(row["release_year"]) else "N/A"
            overview = str(row.get("overview", ""))[:160] + "..." if pd.notna(row.get("overview")) else ""
            tags_html = "".join(
                f'<span class="tag {colors[j % len(colors)]}">{e}</span>'
                for j, e in enumerate(row["emotions"])
            )
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🎬 {row['title']} <span style="font-size:0.9rem;color:#aaa;font-family:sans-serif;">({year})</span></div>
                <div class="card-meta">⭐ {row['vote_average']:.1f} &nbsp;·&nbsp; ⏱️ {int(row['runtime'])}분 &nbsp;·&nbsp; {row['genre_str']}</div>
                <div>{tags_html}</div>
                <div class="card-overview">{overview}</div>
            </div>
            """, unsafe_allow_html=True)

with col_charts:
    st.markdown('<div class="section-label">DATA INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">분석</div>', unsafe_allow_html=True)

    CHART_BG = "rgba(0,0,0,0)"
    CHART_FONT = "#1a1a1a"
    CHART_MARGIN = dict(l=0, r=0, t=10, b=0)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**📊 장르 분포**")
    all_genres = [g for gl in filtered["genre_list"] for g in gl]
    if all_genres:
        gc = pd.Series(all_genres).value_counts().head(8)
        fig1 = px.bar(x=gc.values, y=gc.index, orientation="h",
                      color=gc.values,
                      color_continuous_scale=["#A8D8EA", "#FFB3C6", "#FFE44D"])
        fig1.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
            font_color=CHART_FONT, showlegend=False,
            coloraxis_showscale=False, margin=CHART_MARGIN,
            xaxis_title="영화 수", yaxis_title=""
        )
        st.plotly_chart(fig1, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**⭐ 평점 분포**")
    fig2 = px.histogram(filtered, x="vote_average", nbins=10,
                        color_discrete_sequence=["#FFB3C6"])
    fig2.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
        font_color=CHART_FONT, margin=CHART_MARGIN,
        xaxis_title="평점", yaxis_title="영화 수"
    )
    st.plotly_chart(fig2, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**⏱️ 상영시간 분포**")
    fig3 = px.histogram(filtered, x="runtime", nbins=10,
                        color_discrete_sequence=["#C8F0A0"])
    fig3.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
        font_color=CHART_FONT, margin=CHART_MARGIN,
        xaxis_title="상영시간 (분)", yaxis_title="영화 수"
    )
    st.plotly_chart(fig3, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)
