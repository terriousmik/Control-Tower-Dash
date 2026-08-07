import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="아시아나 중정비 Control Tower", layout="wide")

# 2. 커스텀 CSS 적용 (강제 화이트 모드 및 표(Table) 스타일링)
st.markdown("""
<style>
    /* 전체 배경 및 폰트 화이트 고정 */
    [data-testid="stAppViewContainer"], .main {
        background-color: #FFFFFF !important;
        color: #212529 !important;
    }
    
    /* -------------------------------------
       보고서용 HTML 표 (Table) 스타일 가이드
       ------------------------------------- */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 30px 0;
        font-size: 0.85rem;
        font-family: 'Malgun Gothic', sans-serif;
        background-color: #FFFFFF !important;
        border: 1px solid #CCCCCC;
    }
    .styled-table thead tr {
        background-color: #F4F6F9 !important;
        color: #000000 !important;
        text-align: center;
        font-weight: bold;
        border-top: 2px solid #000000;
        border-bottom: 2px solid #000000;
    }
    .styled-table th,
    .styled-table td {
        padding: 10px;
        border: 1px solid #CCCCCC;
        text-align: center;
        vertical-align: middle;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #DDDDDD;
    }
    
    /* -------------------------------------
       Bay 카드 레이아웃 스타일 (이전과 동일)
       ------------------------------------- */
    .bay-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #DDDDDD;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .bay-header {
        background-color: #0A58CA;
        color: #FFFFFF !important;
        text-align: center;
        font-weight: bold;
        padding: 10px;
        font-size: 1.1rem;
    }
    .bay-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 15px;
        border-bottom: 1px solid #EEEEEE;
    }
    .bay-label { font-size: 0.85rem; font-weight: 600; color: #555555 !important; }
    .bay-value { font-size: 1rem; font-weight: bold; color: #000000 !important; }
    
    .bg-green { background-color: #E8F5E9 !important; }
    .bg-yellow { background-color: #FFFDE7 !important; }
    .val-red { color: #D32F2F !important; }

    .section-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #000000 !important;
        margin-top: 20px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수
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

# DataFrame을 깔끔한 HTML 표로 변환하는 헬퍼 함수
def render_html_table(df):
    if df.empty:
        st.info("데이터가 없습니다.")
        return
    # 줄바꿈(\n) 기호를 HTML의 <br> 태그로 변환하여 표 안에서 줄바꿈이 되도록 처리
    df_html = df.fillna("").astype(str).replace(r'\n', '<br>', regex=True)
    html_str = df_html.to_html(classes='styled-table', escape=False, index=False)
    st.markdown(html_str, unsafe_allow_html=True)

# 4. 탭 구성
tab1, tab2 = st.tabs(["📊 중정비 현황 종합", "🛠️ BAY 진행 상황"])

# ==========================================
# 탭 1: 중정비 현황 종합 (완전한 표 형태)
# ==========================================
with tab1:
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown("<h3 style='color: #000000 !important; font-weight: bold;'>중정비 진행 현황 (종합)</h3>", unsafe_allow_html=True)
        st.markdown("<strong style='color: #000000 !important;'>1. 일일 중정비 보고</strong>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: right; font-weight: bold; padding-top: 10px; color: #000000 !important;'>관리자: <br> 26. 08. 07.</div>", unsafe_allow_html=True)

    # ▶ 자체 중정비
    st.markdown("<div class='section-title'>▶ 자체 중정비</div>", unsafe_allow_html=True)
    if not maintenance_df.empty:
        clean_maintenance = maintenance_df.dropna(how='all')
        render_html_table(clean_maintenance)
    else:
        st.info("데이터를 불러올 수 없습니다.")

    # ▶ 외주 중정비 
    st.markdown("<div class='section-title'>▶ 외주 중정비</div>", unsafe_allow_html=True)
    outsource_df = pd.DataFrame(columns=["기번", "기종", "작업 내용", "작업 기간 (From)", "작업 기간 (To)", "TAT", "외주", "복귀 일정"])
    outsource_df.loc[0] = ["HL7626", "A380", "12Y(1+2+4GC)+LG", "26.02.21", "26.06.09", "109", "GAMECO", "2026.06.09 (화) /"]
    render_html_table(outsource_df)

    # ▶ 비계획 정비
    st.markdown("<div class='section-title'>▶ 비계획 정비</div>", unsafe_allow_html=True)
    unplanned_df = pd.DataFrame(columns=["기번", "기종", "작업 내용", "작업 기간 (From)", "작업 기간 (To)", "TAT", "Bay", "비고"])
    unplanned_df.loc[0] = ["-", "-", "-", "-", "-", "-", "-", "-"]
    render_html_table(unplanned_df)


# ==========================================
# 탭 2: BAY 진행 상황
# ==========================================
with tab2:
    st.markdown("<h3 style='margin-bottom: 20px; font-weight: bold; color: #000000 !important;'>2. Bay 별 중정비 진행 현황 종합</h3>", unsafe_allow_html=True)
    
    bays = st.columns(4)
    
    bay_data = [
        {"name": "Bay 1", "rate1": "진행 중", "rate2": "진행 중", "rate_val": "4.0%", "bg": "bg-yellow", "red": False, "tat": "🟢", "plan": "800.0"},
        {"name": "Bay 2", "rate1": "대기", "rate2": "대기", "rate_val": "0.0%", "bg": "", "red": False, "tat": "🔴", "plan": "0.8"},
        {"name": "Bay 3", "rate1": "완료", "rate2": "완료", "rate_val": "103.6%", "bg": "bg-green", "red": True, "tat": "🟢", "plan": "0.8"},
        {"name": "Bay 4", "rate1": "초과", "rate2": "초과", "rate_val": "696.9%", "bg": "bg-green", "red": True, "tat": "🟢", "plan": "20:00"}
    ]

    for idx, col in enumerate(bays):
        data = bay_data[idx]
        val_class = "val-red" if data["red"] else "val-dark"
        
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
                <span class="bay-label">▣ 인원 투입율</span>
                <span class="bay-value {val_class}">{data['rate_val']}</span>
            </div>
            <div class="bay-row">
                <span class="bay-label">▣ TAT 진행율</span>
                <span class="bay-value" style="font-size: 1.2rem;">{data['tat']}</span>
            </div>
            <div class="bay-row" style="background-color: #F4F6F9;">
                <span class="bay-label">계획 / 진행</span>
                <span class="bay-value val-red">{data['plan']}</span>
            </div>
        </div>
        """
        col.markdown(html_content, unsafe_allow_html=True)
