import streamlit as st
import pandas as pd

# 모바일 화면에 맞춘 페이지 기본 설정
st.set_page_config(page_title="데이터 뷰어", page_icon="📱", layout="centered")

st.title("📱 원격검침 데이터 조회")
st.markdown("---")

# 엑셀 데이터 불러오기 함수 (데이터를 캐싱하여 로딩 속도 향상)
@st.cache_data
def load_data():
    try:
        return pd.read_excel("data.xlsx")
    except FileNotFoundError:
        st.error("오류: 'data.xlsx' 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None and not df.empty:
    # 간편 검색 기능 추가
    search_query = st.text_input("🔍 검색어를 입력하세요", "")

    # 검색어가 있을 경우 데이터 필터링
    if search_query:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df

    st.caption(f"총 {len(filtered_df)}건의 데이터가 조회되었습니다.")

    # 🚀 핵심 수정: 15,000개를 한 번에 그리면 멈추기 때문에 최대 50개로 제한
    MAX_DISPLAY = 50 
    
    if len(filtered_df) > MAX_DISPLAY:
        st.warning(f"데이터가 너무 많습니다. 속도 저하를 막기 위해 상위 {MAX_DISPLAY}건만 표시합니다. 원하는 데이터를 보려면 '검색'을 이용해 주세요.")
        display_df = filtered_df.head(MAX_DISPLAY)
    else:
        display_df = filtered_df

    # 제한된 개수(display_df)만큼만 화면에 리스트/카드 형태로 출력
    for index, row in display_df.iterrows():
        title_col = df.columns[0]
        title_value = row[title_col]
        
        with st.expander(f"📌 {title_col}: {title_value}"):
            for col in df.columns:
                st.markdown(f"**{col}:** {row[col]}")
