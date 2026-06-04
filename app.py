import streamlit as st
import pandas as pd

# 모바일 화면에 맞춘 페이지 기본 설정
st.set_page_config(page_title="유량계정보 조회", page_icon="📱", layout="centered")

# 기존 st.title 대신 HTML 적용하여 글자 크기를 2/3 수준으로 축소 (한 줄에 맞춤)
st.markdown("<h2 style='font-size: 1.6rem; font-weight: bold; margin-bottom: 0;'>📱 원격검침 데이터 조회</h2>", unsafe_allow_html=True)
st.markdown("---")

# 엑셀 데이터 불러오기 함수 (데이터를 캐싱하여 로딩 속도 향상)
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data.xlsx")
        
        # 🚀 [핵심 최적화] 검색 속도를 위해 모든 열의 데이터를 합친 '검색전용_문자열' 열을 미리 생성
        # 에러 방지: 엑셀의 빈칸(NaN)을 빈 문자열('')로 채운 뒤 확실하게 문자열로 변환하여 합침
        df['_search_string'] = df.fillna('').astype(str).apply(' '.join, axis=1).str.lower()
        
        return df
    except FileNotFoundError:
        st.error("오류: 'data.xlsx' 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None and not df.empty:
    # 간편 검색 기능 (사용자가 엔터를 치거나 입력을 멈추면 작동)
    search_query = st.text_input("🔍 검색어를 입력하세요 (입력 후 Enter)", "")

    # 검색어가 있을 경우 데이터 필터링
    if search_query:
        # 검색어도 소문자로 변환하여 대소문자 상관없이 검색되도록 처리
        query = search_query.lower()
        
        # 미리 만들어둔 '_search_string' 단일 열에서만 검색하므로 딜레이가 거의 없음
        mask = df['_search_string'].str.contains(query, na=False)
        filtered_df = df[mask]
    else:
        filtered_df = df

    st.caption(f"총 {len(filtered_df)}건의 데이터가 조회되었습니다.")

    # 15,000개를 한 번에 그리면 화면이 멈추기 때문에 최대 50개로 제한
    MAX_DISPLAY = 50 
    
    if len(filtered_df) > MAX_DISPLAY:
        st.warning(f"결과가 너무 많습니다. 속도 저하를 막기 위해 상위 {MAX_DISPLAY}건만 표시합니다. 더 자세한 검색어를 입력해 주세요.")
        display_df = filtered_df.head(MAX_DISPLAY)
    else:
        display_df = filtered_df

    # 화면에 보여줄 실제 열 이름들 (검색용으로 만든 _search_string 열은 화면에서 숨김)
    display_columns = [col for col in df.columns if col != '_search_string']

    # 제한된 개수(display_df)만큼만 화면에 리스트/카드 형태로 출력
    for index, row in display_df.iterrows():
        # 첫 번째 열을 제목으로 사용
        title_col = display_columns[0]
        title_value = row[title_col]
        
        with st.expander(f"📌 {title_col}: {title_value}"):
            for col in display_columns:
                st.markdown(f"**{col}:** {row[col]}")
