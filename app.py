import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="아시아나 중정비 Control Tower", layout="wide")

# 커스텀 CSS 적용 (표 스타일링 및 Bay 카드 디자인)
st.markdown("""
<style>
    .bay-header {
        background-color: #0000FF;
        color: white;
        text-align: center;
        font-weight: bold;
        padding: 5px;
        border: 1px solid #000;
    }
    .bay-cell {
        border-left: 1px solid #000;
        border-right: 1px solid #000;
        border-bottom: 1px solid #000;
        text-align: center;
        padding: 8px;
        background-color: #F8F9FA;
    }
    .bay-value {
        font-weight: bold;
        font-size: 1.1em;
    }
    .val-red { color: red; }
    .bg-green { background-color: #C8E6C9; }
    .bg-yellow { background-color: #FFF9C4; }
    .section-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. 데이터 로드 함수 (DB_List, 운영파일 제외)
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

# 3. 탭 구성 (2개 탭으로 축소)
tab1, tab2 = st.tabs(["📊 중정비 현황 종합", "🛠️ BAY 진행 상황"])

# ==========================================
# 탭 1: 중정비 현황 종합 (image_6469b1.png 레이아웃)
# ==========================================
with tab1:
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown("### 중정비 진행 현황 (종합)")
        st.markdown("**1. 일일 중정비 보고**")
    with col2:
        st.markdown("<div style='text-align: right; font-weight: bold;'>관리자: <br> 26. 08. 07.</div>", unsafe_allow_html=True)

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
    # 이미지와 동일한 예시 데이터 1줄 추가
    outsource_df.loc[0] = ["HL7626", "A380", "12Y(1+2+4GC)+LG", "26.02.21", "26.06.09", "109", "GAMECO", "2026.06.09 (화) /"]
    st.dataframe(outsource_df, use_container_width=True, hide_index=True)

    # ▶ 비계획 정비
    st.markdown("<div class='section-title'>▶ 비계획 정비</div>", unsafe_allow_html=True)
    unplanned_df = pd.DataFrame(columns=["기번", "기종", "작업 내용", "작업 기간 (From)", "작업 기간 (To)", "TAT", "Bay", "비고"])
    unplanned_df.loc[0] = ["-", "-", "-", "-", "-", "-", "-", "-"]
    st.dataframe(unplanned_df, use_container_width=True, hide_index=True)


# ==========================================
# 탭 2: BAY 진행 상황 (image_646cf3.png 레이아웃)
# ==========================================
with tab2:
    st.markdown("### 2. Bay 별 중정비 진행 현황 종합")
    
    # 4개의 Bay 컬럼 생성
    bays = st.columns(4)
    
    # 각 Bay 별 하드코딩 된 레이아웃 (추후 CSV 데이터 연동 시 변수 처리 가능)
    bay_data = [
        {"name": "Bay 1", "rate": "4.0%", "bg": "bg-yellow", "red": False, "tat": "🟢", "plan": "800.0 (계획) / 진행"},
        {"name": "Bay 2", "rate": "0.0%", "bg": "", "red": False, "tat": "🔴", "plan": "0.8 (계획) / 진행"},
        {"name": "Bay 3", "rate": "103.6%", "bg": "bg-green", "red": True, "tat": "🟢", "plan": "0.8 (계획) / 진행"},
        {"name": "Bay 4", "rate": "696.9%", "bg": "bg-green", "red": True, "tat": "🟢", "plan": "20:00 (계획) / 진행"}
    ]

    for idx, col in enumerate(bays):
        data = bay_data[idx]
        val_class = "val-red" if data["red"] else ""
        
        # HTML/CSS를 활용하여 이미지와 유사한 표 형태 구현
        html_content = f"""
        <div>
            <div class="bay-header">{data['name']}</div>
            <div class="bay-cell">▣ 공정 진행율</div>
            <div class="bay-cell">▣ 공정 진행율</div>
            <div class="bay-cell">▣ 인원 투입율</div>
            <div class="bay-cell {data['bg']}"><span class="bay-value {val_class}">{data['rate']}</span></div>
            <div class="bay-cell">▣ TAT 진행율</div>
            <div class="bay-cell" style="font-size: 24px;">{data['tat']}</div>
            <div class="bay-cell" style="font-size: 0.9em;">{data['plan']}</div>
        </div>
        """
        col.markdown(html_content, unsafe_allow_html=True)
