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

# ── 다크 시네마틱 CSS ─────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #161b22; }
    .mood-title {
        font-size: 2.8rem; font-weight: 900;
        text-align: center; color: #f0c040;
        letter-spacing: 2px; padding: 10px 0;
    }
    .sub-title {
        text-align: center; color: #8b949e;
        font-size: 1rem; margin-bottom: 20px;
    }
    .movie-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        border: 1px solid #30363d;
    }
    .tag {
        background-color: rgba(240,192,64,0.15);
        color: #f0c040;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        margin: 2px;
        display: inline-block;
    }
    .movie-title { font-size: 1.1rem; font-weight: 700; color: #e6edf3; }
    .movie-meta  { font-size: 0.85rem; color: #8b949e; margin: 4px 0; }
    .overview    { font-size: 0.82rem; color: #6e7681; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

# ── 감정 태그 매핑 ────────────────────────────────────────────
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

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown('<div class="mood-title">🎬 Movie Mood Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">지금 기분에 딱 맞는 영화를 찾아드려요</div>', unsafe_allow_html=True)
st.markdown("---")

# ── 사이드바 필터 ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎭 지금 기분이 어때?")
    selected_mood = st.radio(
        "",
        options=list(MOOD_LABELS.keys()),
        format_func=lambda x: MOOD_LABELS[x]
    )

    st.markdown("---")
    st.markdown("## ⏱️ 얼마나 볼 수 있어?")
    runtime_option = st.select_slider(
        "",
        options=["90분 이하", "90~120분", "120분 이상", "상관없음"],
        value="상관없음"
    )

    st.markdown("---")
    st.markdown("## ⭐ 최소 평점")
    min_rating = st.slider("", 0.0, 10.0, 7.0, 0.5,
                           format="%.1f")

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
col_movies, col_charts = st.columns([2, 1])

# ── 왼쪽: 영화 카드 ──────────────────────────────────────────
with col_movies:
    st.markdown(f"### {MOOD_LABELS[selected_mood]}")
    st.caption(f"조건에 맞는 영화 {len(filtered)}편")

    if filtered.empty:
        st.warning("조건에 맞는 영화가 없어요. 필터를 조정해봐!")
    else:
        for _, row in filtered.iterrows():
            year = int(row["release_year"]) if pd.notna(row["release_year"]) else "N/A"
            tags_html = "".join(f'<span class="tag">{e}</span>' for e in row["emotions"])
            overview  = str(row.get("overview", ""))[:160] + "..." if pd.notna(row.get("overview")) else ""

            st.markdown(f"""
            <div class="movie-card">
                <div class="movie-title">🎬 {row['title']} ({year})</div>
                <div class="movie-meta">
                    ⭐ {row['vote_average']:.1f} &nbsp;·&nbsp;
                    ⏱️ {int(row['runtime'])}분 &nbsp;·&nbsp;
                    🎭 {row['genre_str']}
                </div>
                <div>{tags_html}</div>
                <div class="overview">{overview}</div>
            </div>
            """, unsafe_allow_html=True)

# ── 오른쪽: 차트 ─────────────────────────────────────────────
with col_charts:
    # 장르 분포
    st.markdown("### 📊 장르 분포")
    all_genres = [g for gl in filtered["genre_list"] for g in gl]
    if all_genres:
        gc = pd.Series(all_genres).value_counts().head(8)
        fig1 = px.bar(x=gc.values, y=gc.index, orientation="h",
                      color=gc.values, color_continuous_scale="Oranges")
        fig1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="white", showlegend=False, coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="영화 수", yaxis_title=""
        )
        st.plotly_chart(fig1, use_container_width=True)

    # 평점 분포
    st.markdown("### ⭐ 평점 분포")
    fig2 = px.histogram(filtered, x="vote_average", nbins=10,
                        color_discrete_sequence=["#f0c040"])
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="white", margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="평점", yaxis_title="영화 수"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 런타임 분포
    st.markdown("### ⏱️ 상영시간 분포")
    fig3 = px.histogram(filtered, x="runtime", nbins=10,
                        color_discrete_sequence=["#58a6ff"])
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="white", margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="상영시간 (분)", yaxis_title="영화 수"
    )
    st.plotly_chart(fig3, use_container_width=True)
