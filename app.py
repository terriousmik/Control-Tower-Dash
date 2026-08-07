import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정 (가볍고 넓은 화면 비율)
st.set_page_config(page_title="아시아나 중정비 Control Tower", layout="wide")
st.title("✈️ 아시아나 중정비 Control Tower Dashboard")
st.markdown("Google Sites 연동용 경량화 대시보드입니다.")

# 2. 데이터 로드 함수 (캐싱을 통해 로딩 속도 최적화)
@st.cache_data
def load_data():
    # 파일들을 읽어옵니다. (결측치가 많은 빈 열은 자동으로 제거하여 깔끔하게 만듭니다)
    def clean_csv(file_name):
        try:
            df = pd.read_csv(file_name)
            # 'Unnamed' 로 시작하는 의미 없는 빈 열 제거
            df = df.dropna(axis=1, how='all') 
            return df
        except Exception as e:
            return pd.DataFrame({'Error': [f"파일을 읽는 중 오류 발생: {e}"]})

    bay_df = clean_csv("01_BAY_진행.csv")
    db_list_df = clean_csv("01_DB_LIST.csv")
    operation_df = clean_csv("01_운영파일_원본.csv")
    maintenance_df = clean_csv("01_중정비_진형_현황_종합.csv")
    
    return bay_df, db_list_df, operation_df, maintenance_df

# 데이터 불러오기
bay_df, db_list_df, operation_df, maintenance_df = load_data()

# 3. 화면 레이아웃 구성 (탭 형태로 분리하여 가독성 향상)
tab1, tab2, tab3 = st.tabs(["📊 중정비 현황 종합", "🛠️ BAY 진행 상황", "📁 운영 및 DB 리스트"])

with tab1:
    st.subheader("중정비 진형 현황 종합")
    # 주요 컬럼 필터링 (불필요한 전체 빈 행 제거)
    clean_maintenance = maintenance_df.dropna(how='all')
    st.dataframe(clean_maintenance, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("BAY 진행 상황")
    st.dataframe(bay_df, use_container_width=True, hide_index=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("운영 파일 원본")
        st.dataframe(operation_df, use_container_width=True, hide_index=True)
    with col2:
        st.subheader("DB 리스트")
        st.dataframe(db_list_df, use_container_width=True, hide_index=True)