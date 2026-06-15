import streamlit as st
import pandas as pd
import plotly.express as px
import ast

st.set_page_config(page_title="Movie Mood Finder", page_icon="🎬", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;600&display=swap');

/* ── 전체 배경 ── */
.stApp {
    background-color: #0a0a0f;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(180,20,20,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(30,30,80,0.15) 0%, transparent 60%);
    font-family: 'DM Sans', sans-serif;
    color: #e8e0d0;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background-color: #0f0f18;
    border-right: 1px solid #2a2a3a;
}
section[data-testid="stSidebar"] * { color: #e8e0d0 !important; }
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e63946 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 3px;
}

/* ── 히어로 ── */
.hero {
    position: relative;
    padding: 50px 48px 40px;
    margin-bottom: 32px;
    border: 1px solid #2a2a3a;
    border-radius: 4px;
    overflow: hidden;
    background: linear-gradient(135deg, #0f0f18 0%, #1a0a0a 100%);
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #e63946, #ff6b6b, #e63946);
}
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #e63946;
    margin-bottom: 14px;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5.5rem;
    line-height: 0.9;
    color: #ffffff;
    margin: 0 0 16px 0;
    letter-spacing: 3px;
}
.hero-title span { color: #e63946; }
.hero-sub {
    font-size: 0.95rem;
    color: #888;
    letter-spacing: 1px;
}
.film-strip-deco {
    position: absolute;
    right: 0; top: 0; bottom: 0;
    width: 60px;
    background: #111;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    padding: 8px 0;
    border-left: 1px solid #2a2a3a;
}
.film-hole {
    width: 16px; height: 12px;
    background: #0a0a0f;
    border-radius: 2px;
    border: 1px solid #333;
}

/* ── 영화 카드 ── */
.card {
    background: #0f0f18;
    border: 1px solid #2a2a3a;
    border-left: 3px solid #e63946;
    border-radius: 4px;
    padding: 18px 22px;
    margin-bottom: 12px;
    transition: border-color 0.2s, background 0.2s;
}
.card:hover {
    background: #14141f;
    border-left-color: #ff6b6b;
}
.card-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.8rem;
    color: #e63946;
    letter-spacing: 2px;
    margin-bottom: 4px;
}
.card-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: #ffffff;
    letter-spacing: 1px;
    margin: 0 0 6px 0;
}
.card-meta { font-size: 0.8rem; color: #666; margin-bottom: 10px; }
.card-overview { font-size: 0.8rem; color: #555; line-height: 1.6; margin-top: 8px; }

/* ── 태그 ── */
.tag {
    display: inline-block;
    border: 1px solid #e63946;
    border-radius: 2px;
    font-size: 0.62rem;
    font-weight: 600;
    padding: 2px 8px;
    margin: 2px;
    color: #e63946;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.tag.b { border-color: #4a9eff; color: #4a9eff; }
.tag.g { border-color: #4aff9e; color: #4aff9e; }
.tag.w { border-color: #aaa; color: #aaa; }

/* ── 섹션 헤더 ── */
.sec-label {
    font-size: 0.62rem; font-weight: 600;
    letter-spacing: 4px; text-transform: uppercase;
    color: #e63946; margin-bottom: 4px;
}
.sec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem; color: #ffffff;
    letter-spacing: 2px;
    margin: 0 0 18px 0;
    border-bottom: 1px solid #2a2a3a;
    padding-bottom: 10px;
}

/* ── 뱃지 ── */
.badge {
    display: inline-block;
    background: #e63946;
    color: #fff;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 16px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── 차트 카드 ── */
.chart-card {
    background: #0f0f18;
    border: 1px solid #2a2a3a;
    border-radius: 4px;
    padding: 16px;
    margin-bottom: 14px;
}
.chart-title {
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    color: #555; margin-bottom: 10px;
}

/* ── 랜덤 픽 ── */
.random-card {
    background: linear-gradient(135deg, #1a0505, #0f0f18);
    border: 1px solid #e63946;
    border-radius: 4px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.random-card::after {
    content: '★';
    position: absolute;
    right: 24px; top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    color: #e63946;
    opacity: 0.08;
}
.random-eyebrow {
    font-size: 0.65rem; letter-spacing: 4px;
    text-transform: uppercase; color: #e63946;
    margin-bottom: 8px;
}
.random-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem; color: #fff;
    letter-spacing: 2px; margin: 4px 0 8px 0;
}

/* Streamlit 버튼 */
div[data-testid="stButton"] button {
    background: #e63946 !important;
    color: white !important;
    border: none !important;
    border-radius: 2px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
}
div[data-testid="stButton"] button:hover {
    background: #ff6b6b !important;
}

h1,h2,h3,h4 { color: #fff !important; }
</style>
""", unsafe_allow_html=True)

# ── 감정 매핑 ────────────────────────────────────────────────
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
ALL_GENRES = ["Action","Adventure","Animation","Comedy","Crime","Documentary",
              "Drama","Family","Fantasy","History","Horror","Music","Mystery",
              "Romance","Science Fiction","Thriller","War","Western"]

# ── 데이터 ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("tmdb_5000_movies.csv")
    def parse_genres(g):
        try: return [x["name"] for x in ast.literal_eval(g)]
        except: return []
    df["genre_list"] = df["genres"].apply(parse_genres)
    df["genre_str"]  = df["genre_list"].apply(lambda x: ", ".join(x))
    def assign_emotions(genres):
        tags = [e for e, gs in EMOTION_MAP.items() if any(g in genres for g in gs)]
        return tags if tags else ["general"]
    df["emotions"] = df["genre_list"].apply(assign_emotions)
    df = df.dropna(subset=["title","vote_average","runtime"])
    df = df[(df["runtime"]>0)&(df["vote_average"]>0)]
    df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    return df

df = load_data()

# ── 히어로 ──────────────────────────────────────────────────
holes = "".join(['<div class="film-hole"></div>'] * 12)
st.markdown(f"""
<div class="hero">
    <div class="film-strip-deco">{holes}</div>
    <div class="hero-eyebrow">✦ Emotion-Based Recommendation</div>
    <div class="hero-title">MOVIE<br><span>MOOD</span><br>FINDER</div>
    <p class="hero-sub">지금 기분에 딱 맞는 영화를 찾아드려요</p>
</div>
""", unsafe_allow_html=True)

# ── 사이드바 ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎭 MOOD")
    selected_moods = st.multiselect(
        "기분 선택 (여러 개 가능)",
        options=list(MOOD_LABELS.keys()),
        default=["comforting"],
        format_func=lambda x: MOOD_LABELS[x]
    )
    st.markdown("---")
    st.markdown("### 🎬 GENRE")
    selected_genres = st.multiselect("장르 필터", options=ALL_GENRES)
    st.markdown("---")
    st.markdown("### 📅 YEAR")
    year_range = st.select_slider("",
        options=["~1990","1990s","2000s","2010s","2020s~","전체"], value="전체")
    st.markdown("---")
    st.markdown("### ⏱️ RUNTIME")
    runtime_option = st.select_slider(" ",
        options=["90분 이하","90~120분","120분 이상","상관없음"], value="상관없음")
    st.markdown("---")
    st.markdown("### ⭐ MIN RATING")
    min_rating = st.slider("", 0.0, 10.0, 7.0, 0.5, format="%.1f")
    st.markdown("---")
    st.markdown("### 🔍 SEARCH")
    search_query = st.text_input("", placeholder="영화 제목 검색...")

# ── 필터링 ──────────────────────────────────────────────────
filtered = df.copy()
if selected_moods:
    filtered = filtered[filtered["emotions"].apply(lambda x: any(m in x for m in selected_moods))]
if selected_genres:
    filtered = filtered[filtered["genre_list"].apply(lambda x: any(g in x for g in selected_genres))]
if year_range != "전체":
    y = {"~1990":(0,1990),"1990s":(1990,2000),"2000s":(2000,2010),"2010s":(2010,2020),"2020s~":(2020,9999)}[year_range]
    filtered = filtered[(filtered["release_year"]>=y[0])&(filtered["release_year"]<y[1])]
if runtime_option == "90분 이하": filtered = filtered[filtered["runtime"]<=90]
elif runtime_option == "90~120분": filtered = filtered[(filtered["runtime"]>90)&(filtered["runtime"]<=120)]
elif runtime_option == "120분 이상": filtered = filtered[filtered["runtime"]>120]
filtered = filtered[filtered["vote_average"]>=min_rating]
if search_query:
    filtered = filtered[filtered["title"].str.contains(search_query, case=False, na=False)]
filtered_sorted = filtered.sort_values("popularity", ascending=False)

# ── 랜덤 픽 ────────────────────────────────────────────────
if st.button("🎲  RANDOM PICK  —  오늘의 영화 추천받기"):
    if not filtered_sorted.empty:
        pick = filtered_sorted.sample(1).iloc[0]
        year = int(pick["release_year"]) if pd.notna(pick["release_year"]) else "N/A"
        ov = str(pick.get("overview",""))[:180]+"..." if pd.notna(pick.get("overview")) else ""
        st.markdown(f"""
        <div class="random-card">
            <div class="random-eyebrow">✦ TODAY'S PICK</div>
            <div class="random-title">{pick['title']}</div>
            <div style="font-size:0.82rem;color:#888;margin-bottom:10px;">
                {year} &nbsp;·&nbsp; ⭐ {pick['vote_average']:.1f} &nbsp;·&nbsp; ⏱️ {int(pick['runtime'])}분 &nbsp;·&nbsp; {pick['genre_str']}
            </div>
            <div style="font-size:0.82rem;color:#666;line-height:1.7;">{ov}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("조건에 맞는 영화가 없어요!")

st.markdown("---")

# ── 레이아웃 ────────────────────────────────────────────────
col_l, col_r = st.columns([2,1], gap="large")

TAG_COLORS = ["","b","g","w","","b","g"]

with col_l:
    st.markdown('<div class="sec-label">RESULTS</div>', unsafe_allow_html=True)
    mood_label = " + ".join([MOOD_LABELS[m] for m in selected_moods]) if selected_moods else "전체"
    st.markdown(f'<div class="sec-title">{mood_label}</div>', unsafe_allow_html=True)
    top20 = filtered_sorted.head(20)
    st.markdown(f'<div class="badge">▶ {len(filtered_sorted)}편 발견 · 상위 20편</div>', unsafe_allow_html=True)

    if top20.empty:
        st.warning("조건에 맞는 영화가 없어요. 필터를 조정해봐!")
    else:
        for i, (_, row) in enumerate(top20.iterrows()):
            year = int(row["release_year"]) if pd.notna(row["release_year"]) else "N/A"
            ov = str(row.get("overview",""))[:150]+"..." if pd.notna(row.get("overview")) else ""
            tags_html = "".join(
                f'<span class="tag {TAG_COLORS[j%len(TAG_COLORS)]}">{e}</span>'
                for j,e in enumerate(row["emotions"])
            )
            st.markdown(f"""
            <div class="card">
                <div class="card-num">NO.{i+1:02d} &nbsp;·&nbsp; {year}</div>
                <div class="card-title">{row['title']}</div>
                <div class="card-meta">⭐ {row['vote_average']:.1f} &nbsp;·&nbsp; ⏱️ {int(row['runtime'])}분 &nbsp;·&nbsp; {row['genre_str']}</div>
                <div>{tags_html}</div>
                <div class="card-overview">{ov}</div>
            </div>
            """, unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="sec-label">DATA INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">분석</div>', unsafe_allow_html=True)

    BG = "rgba(0,0,0,0)"
    FC = "#888"
    MG = dict(l=0,r=0,t=6,b=0)

    def chart_layout(fig, xt, yt=""):
        fig.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, font_color=FC,
                          showlegend=False, coloraxis_showscale=False,
                          margin=MG, xaxis_title=xt, yaxis_title=yt,
                          xaxis=dict(gridcolor="#1a1a2a"), yaxis=dict(gridcolor="#1a1a2a"))
        return fig

    st.markdown('<div class="chart-card"><div class="chart-title">GENRE DISTRIBUTION</div>', unsafe_allow_html=True)
    all_g = [g for gl in top20["genre_list"] for g in gl]
    if all_g:
        gc = pd.Series(all_g).value_counts().head(8)
        fig1 = px.bar(x=gc.values, y=gc.index, orientation="h",
                      color=gc.values, color_continuous_scale=["#2a1a1a","#e63946"])
        st.plotly_chart(chart_layout(fig1,"편수"), width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card"><div class="chart-title">RATING DISTRIBUTION</div>', unsafe_allow_html=True)
    fig2 = px.histogram(top20, x="vote_average", nbins=10, color_discrete_sequence=["#e63946"])
    st.plotly_chart(chart_layout(fig2,"평점","편수"), width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card"><div class="chart-title">RELEASE YEAR</div>', unsafe_allow_html=True)
    fig3 = px.histogram(top20.dropna(subset=["release_year"]), x="release_year",
                        nbins=15, color_discrete_sequence=["#4a9eff"])
    st.plotly_chart(chart_layout(fig3,"개봉연도","편수"), width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card"><div class="chart-title">RUNTIME</div>', unsafe_allow_html=True)
    fig4 = px.histogram(top20, x="runtime", nbins=10, color_discrete_sequence=["#4aff9e"])
    st.plotly_chart(chart_layout(fig4,"분","편수"), width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)
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
    .hero-sub { font-size: 1rem; color: #555; margin: 0; }

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
    .card-meta { font-size: 0.82rem; color: #666; margin-bottom: 8px; }
    .card-overview { font-size: 0.8rem; color: #888; line-height: 1.5; margin-top: 6px; }

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
    }
    .tag.pink  { background: #FFB3C6; }
    .tag.green { background: #C8F0A0; }
    .tag.blue  { background: #A8D8EA; }

    .section-label {
        font-size: 0.7rem; font-weight: 700;
        letter-spacing: 3px; text-transform: uppercase;
        color: #999; margin-bottom: 4px;
    }
    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem; color: #1a1a1a;
        margin: 0 0 16px 0;
        border-bottom: 2.5px solid #1a1a1a;
        padding-bottom: 8px;
    }
    .chart-card {
        background: #fff;
        border: 2.5px solid #1a1a1a;
        border-radius: 16px;
        padding: 16px; margin-bottom: 16px;
        box-shadow: 4px 4px 0px #1a1a1a;
    }
    .result-badge {
        display: inline-block;
        background: #1a1a1a; color: #FFE44D;
        font-weight: 700; font-size: 0.85rem;
        padding: 4px 14px; border-radius: 30px;
        margin-bottom: 14px;
    }
    .random-card {
        background: #FFE44D;
        border: 3px solid #1a1a1a;
        border-radius: 20px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 5px 5px 0px #1a1a1a;
    }
    .random-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.8rem; color: #1a1a1a;
        margin: 8px 0 6px 0;
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

ALL_GENRES = ["Action","Adventure","Animation","Comedy","Crime","Documentary",
              "Drama","Family","Fantasy","History","Horror","Music","Mystery",
              "Romance","Science Fiction","Thriller","War","Western"]

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
    st.markdown("### 🎭 무드 선택")
    selected_moods = st.multiselect(
        "기분을 골라봐 (여러 개 가능!)",
        options=list(MOOD_LABELS.keys()),
        default=["comforting"],
        format_func=lambda x: MOOD_LABELS[x]
    )

    st.markdown("---")
    st.markdown("### 🎬 장르 선택")
    selected_genres = st.multiselect(
        "장르 필터 (선택 안 하면 전체)",
        options=ALL_GENRES
    )

    st.markdown("---")
    st.markdown("### 📅 개봉 연도")
    year_range = st.select_slider(
        "",
        options=["~1990", "1990s", "2000s", "2010s", "2020s~", "전체"],
        value="전체"
    )

    st.markdown("---")
    st.markdown("### ⏱️ 상영시간")
    runtime_option = st.select_slider(
        "",
        options=["90분 이하", "90~120분", "120분 이상", "상관없음"],
        value="상관없음"
    )

    st.markdown("---")
    st.markdown("### ⭐ 최소 평점")
    min_rating = st.slider("", 0.0, 10.0, 7.0, 0.5, format="%.1f")

    st.markdown("---")
    st.markdown("### 🔍 제목 검색")
    search_query = st.text_input("영화 제목 검색", placeholder="예: Inception")

# ── 필터링 ───────────────────────────────────────────────────
filtered = df.copy()

# 무드 필터
if selected_moods:
    filtered = filtered[filtered["emotions"].apply(
        lambda x: any(m in x for m in selected_moods)
    )]

# 장르 필터
if selected_genres:
    filtered = filtered[filtered["genre_list"].apply(
        lambda x: any(g in x for g in selected_genres)
    )]

# 연도 필터
if year_range != "전체":
    if year_range == "~1990":
        filtered = filtered[filtered["release_year"] < 1990]
    elif year_range == "1990s":
        filtered = filtered[(filtered["release_year"] >= 1990) & (filtered["release_year"] < 2000)]
    elif year_range == "2000s":
        filtered = filtered[(filtered["release_year"] >= 2000) & (filtered["release_year"] < 2010)]
    elif year_range == "2010s":
        filtered = filtered[(filtered["release_year"] >= 2010) & (filtered["release_year"] < 2020)]
    elif year_range == "2020s~":
        filtered = filtered[filtered["release_year"] >= 2020]

# 런타임 필터
if runtime_option == "90분 이하":
    filtered = filtered[filtered["runtime"] <= 90]
elif runtime_option == "90~120분":
    filtered = filtered[(filtered["runtime"] > 90) & (filtered["runtime"] <= 120)]
elif runtime_option == "120분 이상":
    filtered = filtered[filtered["runtime"] > 120]

# 평점 필터
filtered = filtered[filtered["vote_average"] >= min_rating]

# 검색 필터
if search_query:
    filtered = filtered[filtered["title"].str.contains(search_query, case=False, na=False)]

filtered_sorted = filtered.sort_values("popularity", ascending=False)

# ── 오늘의 랜덤 픽 ───────────────────────────────────────────
st.markdown("### 🎲 오늘의 랜덤 픽")
if st.button("🎬 랜덤 영화 추천받기!", use_container_width=True):
    if not filtered_sorted.empty:
        pick = filtered_sorted.sample(1).iloc[0]
        year = int(pick["release_year"]) if pd.notna(pick["release_year"]) else "N/A"
        st.markdown(f"""
        <div class="random-card">
            <div style="font-size:0.8rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;">✦ Today's Pick</div>
            <div class="random-title">{pick['title']} ({year})</div>
            <div style="font-size:0.9rem;color:#444;">⭐ {pick['vote_average']:.1f} &nbsp;·&nbsp; ⏱️ {int(pick['runtime'])}분 &nbsp;·&nbsp; {pick['genre_str']}</div>
            <div style="font-size:0.85rem;color:#666;margin-top:10px;">{str(pick.get('overview',''))[:200]}...</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("조건에 맞는 영화가 없어요!")

st.markdown("---")

# ── 레이아웃 ─────────────────────────────────────────────────
col_movies, col_charts = st.columns([2, 1], gap="large")

# ── 왼쪽: 영화 카드 ──────────────────────────────────────────
with col_movies:
    st.markdown('<div class="section-label">RESULTS</div>', unsafe_allow_html=True)
    mood_label = " + ".join([MOOD_LABELS[m] for m in selected_moods]) if selected_moods else "전체"
    st.markdown(f'<div class="section-title">{mood_label}</div>', unsafe_allow_html=True)

    top20 = filtered_sorted.head(20)
    st.markdown(f'<div class="result-badge">✦ {len(filtered_sorted)}편 발견 · 상위 20편 표시</div>', unsafe_allow_html=True)

    if top20.empty:
        st.warning("조건에 맞는 영화가 없어요. 필터를 조정해봐!")
    else:
        colors = ["", "pink", "green", "blue"]
        for _, row in top20.iterrows():
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

# ── 오른쪽: 차트 ─────────────────────────────────────────────
with col_charts:
    st.markdown('<div class="section-label">DATA INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">분석</div>', unsafe_allow_html=True)

    BG = "rgba(0,0,0,0)"
    FC = "#1a1a1a"
    MG = dict(l=0, r=0, t=10, b=0)

    # 장르 분포
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**📊 장르 분포**")
    all_genres = [g for gl in top20["genre_list"] for g in gl]
    if all_genres:
        gc = pd.Series(all_genres).value_counts().head(8)
        fig1 = px.bar(x=gc.values, y=gc.index, orientation="h",
                      color=gc.values, color_continuous_scale=["#A8D8EA","#FFB3C6","#FFE44D"])
        fig1.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, font_color=FC,
                           showlegend=False, coloraxis_showscale=False,
                           margin=MG, xaxis_title="영화 수", yaxis_title="")
        st.plotly_chart(fig1, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # 평점 분포
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**⭐ 평점 분포**")
    fig2 = px.histogram(top20, x="vote_average", nbins=10,
                        color_discrete_sequence=["#FFB3C6"])
    fig2.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, font_color=FC,
                       margin=MG, xaxis_title="평점", yaxis_title="영화 수")
    st.plotly_chart(fig2, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # 연도별 분포
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**📅 연도별 분포**")
    year_data = top20.dropna(subset=["release_year"])
    fig3 = px.histogram(year_data, x="release_year", nbins=15,
                        color_discrete_sequence=["#C8F0A0"])
    fig3.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, font_color=FC,
                       margin=MG, xaxis_title="개봉연도", yaxis_title="영화 수")
    st.plotly_chart(fig3, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # 런타임 분포
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**⏱️ 상영시간 분포**")
    fig4 = px.histogram(top20, x="runtime", nbins=10,
                        color_discrete_sequence=["#D4A8EA"])
    fig4.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, font_color=FC,
                       margin=MG, xaxis_title="상영시간 (분)", yaxis_title="영화 수")
    st.plotly_chart(fig4, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)
