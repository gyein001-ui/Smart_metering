import streamlit as st
import pandas as pd

# 모바일 화면에 맞춘 페이지 기본 설정
st.set_page_config(page_title="데이터 뷰어", page_icon="📱", layout="centered")

st.title("📱 지하수유량계 검색")
st.markdown("---")

# 엑셀 데이터 불러오기 함수 (데이터를 캐싱하여 로딩 속도 향상)
@st.cache_data
def load_data():
    try:
        # 파일명이 다르다면 아래 "data.xlsx"를 실제 엑셀 파일 이름으로 수정하세요.
        return pd.read_excel("data.xlsx")
    except FileNotFoundError:
        st.error("오류: 'data.xlsx' 파일을 찾을 수 없습니다. 엑셀 파일이 파이썬 파일과 같은 폴더에 있는지 확인해주세요.")
        return None
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None and not df.empty:
    # 간편 검색 기능 추가
    search_query = st.text_input("🔍 검색어를 입력하세요", "")

    # 검색어가 있을 경우 데이터 필터링 (모든 열 대상)
    if search_query:
        # 데이터를 모두 문자열로 임시 변환 후 검색어가 포함된 행만 필터링
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df

    st.caption(f"총 {len(filtered_df)}건의 데이터가 조회되었습니다.")

    # 엑셀의 가로 표를 모바일 앱의 세로 '리스트/카드' 형태로 변환하여 출력
    for index, row in filtered_df.iterrows():
        # 첫 번째 열(Column)의 값을 각 항목의 메인 제목으로 사용
        title_col = df.columns[0]
        title_value = row[title_col]
        
        # st.expander를 사용해 터치 시 내용이 아래로 펼쳐지도록 구성
        with st.expander(f"📌 {title_col}: {title_value}"):
            # 나머지 모든 열의 데이터를 상세 내용으로 출력
            for col in df.columns:
                st.markdown(f"**{col}:** {row[col]}")