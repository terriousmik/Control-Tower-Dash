import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="아시아나 중정비 Control Tower", layout="wide")

# 2. 커스텀 CSS 적용 (강제 화이트 모드 & 고급스러운 카드 레이아웃 적용)
st.markdown("""
<style>
    /* 전체 배경 화이트 고정 & 텍스트 색상 어둡게 처리 */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
        color: #212529 !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
    }
    p, span, h1, h2, h3, h4, h5, h6, div {
        color: #212529 !important;
    }

    /* Bay 카드 전체 컨테이너 (그림자 및 라운드 처리) */
    .bay-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #E9ECEF;
        overflow: hidden;
        margin-bottom: 20px;
        transition: transform 0.2s ease-in-out;
    }
    .bay-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    /* Bay 헤더 (그라데이션 블루) */
    .bay-header {
        background: linear-gradient(135deg, #0A58CA, #04419A);
        color: #FFFFFF !important;
        text-align: center;
        font-weight: 900;
        padding: 15px;
        font-size: 1.2rem;
        letter-spacing: 1px;
    }

    /* Bay 행(Row) 디자인 */
    .bay-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 20px;
        border-bottom: 1px solid #F1F3F5;
    }
    .bay-row:last-child {
        border-bottom: none;
    }
    
    /* 레이블 및 값 텍스트 스타일 */
    .bay-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #6C757D !important;
    }
    .bay-value {
        font-size: 1.1rem;
        font-weight: 800;
    }

    /* 상태별 배경 및 텍스트 색상 */
    .bg-green { background-color: #E8F5E9 !important; }
    .bg-yellow { background-color: #FFFDE7 !important; }
    .val-red { color: #DC3545 !important; }
    .val-dark { color: #212529 !important; }

    /* 섹션 타이틀 (하단 밑줄 포인트) */
    .section-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #04419A !important;
        margin-top: 30px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #0A58CA;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수 (DB_List, 운영파일 제외)
@st.cache_data
def load_data():
    def clean_csv(file_name):
        try:
            df = pd.read_csv(file_name)
            df = df.dropna(axis=1, how='all') 
            return df
        except Exception as e:
            return pd.DataFrame()

    bay_df = clean_csv("01_BAY_진행.csv")
    maintenance_df = clean_csv("01_중정비_진형_현황_종합.csv")
    
    return bay_df, maintenance_df

bay_df, maintenance_df = load_data()

# 4. 탭 구성
tab1, tab2 = st.tabs(["📊 중정비 현황 종합", "🛠️ BAY 진행 상황"])

# ==========================================
# 탭 1: 중정비 현황 종합
# ==========================================
with tab1:
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown("<h2 style='color: #04419A !important; font-weight: 900;'>중정비 진행 현황 (종합)</h2>", unsafe_allow_html=True)
        st.markdown("**1. 일일 중정비 보고**")
    with col2:
        st.markdown("<div style='text-align: right; font-weight: bold; padding-top: 15px; color: #495057 !important;'>관리자: <br> 26. 08. 07.</div>", unsafe_allow_html=True)

    # ▶ 자체 중정비
    st.markdown("<div class='section-title'>▶ 자체 중정비</div>", unsafe_allow_html=True)
    if not maintenance_df.empty:
        clean_maintenance = maintenance_df.dropna(how='all').fillna("")
        st.dataframe(clean_maintenance, use_container_width=True, hide_index=True)
    else:
        st.info("데이터를 불러올 수 없습니다.")

    # ▶ 외주 중정비 (더미 데이터 구조 생성 - 추후 실제 데이터로 연결 가능)
    st.markdown("<div class='section-title'>▶ 외주 중정비</div>", unsafe_allow_html=True)
    outsource_df = pd.DataFrame(columns=["기번", "기종", "작업 내용", "작업 기간 (From)", "작업 기간 (To)", "TAT", "외주", "복귀 일정"])
    outsource_df.loc[0] = ["HL7626", "A380", "12Y(1+2+4GC)+LG", "26.02.21", "26.06.09", "109", "GAMECO", "2026.06.09 (화) /"]
    st.dataframe(outsource_df, use_container_width=True, hide_index=True)

    # ▶ 비계획 정비
    st.markdown("<div class='section-title'>▶ 비계획 정비</div>", unsafe_allow_html=True)
    unplanned_df = pd.DataFrame(columns=["기번", "기종", "작업 내용", "작업 기간 (From)", "작업 기간 (To)", "TAT", "Bay", "비고"])
    unplanned_df.loc[0] = ["-", "-", "-", "-", "-", "-", "-", "-"]
    st.dataframe(unplanned_df, use_container_width=True, hide_index=True)


# ==========================================
# 탭 2: BAY 진행 상황 (비주얼 개선된 카드 UI)
# ==========================================
with tab2:
    st.markdown("<h3 style='margin-bottom: 20px; font-weight: 800;'>2. Bay 별 중정비 진행 현황 종합</h3>", unsafe_allow_html=True)
    
    bays = st.columns(4)
    
    # 각 Bay 별 데이터
    bay_data = [
        {"name": "Bay 1", "rate1": "진행 중", "rate2": "진행 중", "rate_val": "4.0%", "bg": "bg-yellow", "red": False, "tat": "🟢", "plan": "800.0"},
        {"name": "Bay 2", "rate1": "대기", "rate2": "대기", "rate_val": "0.0%", "bg": "", "red": False, "tat": "🔴", "plan": "0.8"},
        {"name": "Bay 3", "rate1": "완료", "rate2": "완료", "rate_val": "103.6%", "bg": "bg-green", "red": True, "tat": "🟢", "plan": "0.8"},
        {"name": "Bay 4", "rate1": "초과", "rate2": "초과", "rate_val": "696.9%", "bg": "bg-green", "red": True, "tat": "🟢", "plan": "20:00"}
    ]

    for idx, col in enumerate(bays):
        data = bay_data[idx]
        val_class = "val-red" if data["red"] else "val-dark"
        
        # 카드 형태의 UI 렌더링
        html_content = f"""
        <div class="bay-card">
            <div class="bay-header">{data['name']}</div>
            <div class="bay-row">
                <span class="bay-label">▣ 공정 진행율</span>
                <span class="bay-value">{data['rate1']}</span>
            </div>
            <div class="bay-row">
                <span class="bay-label">▣ 공정 진행율</span>
                <span class="bay-value">{data['rate2']}</span>
            </div>
            <div class="bay-row {data['bg']}">
                <span class="bay-label" style="color: #495057 !important;">▣ 인원 투입율</span>
                <span class="bay-value {val_class}">{data['rate_val']}</span>
            </div>
            <div class="bay-row">
                <span class="bay-label">▣ TAT 진행율</span>
                <span class="bay-value" style="font-size: 1.5rem;">{data['tat']}</span>
            </div>
            <div class="bay-row" style="background-color: #F8F9FA;">
                <span class="bay-label">계획 / 진행</span>
                <span class="bay-value val-red">{data['plan']}</span>
            </div>
        </div>
        """
        col.markdown(html_content, unsafe_allow_html=True)
