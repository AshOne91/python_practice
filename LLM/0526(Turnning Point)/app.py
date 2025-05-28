import streamlit as st

from stock_info import Stock
from report_service import invesment_report
from search import stock_search

class SearchResult:
    def __init__(self, item):
        self.item = item

    @property
    def symbol(self):
        return self.item["Symbol"]
    
    @property
    def name(self):
        return self.item["Name"]
    
    def __str__(self):
        return f"{self.symbol}: {self.name}"

st.title("AI 투자 보고서 생성 서비스")
# 예외처리
try:
    search_query = st.text_input("회사명", "Apple Inc.")
    hits = stock_search(search_query)['hits']
    search_results = [SearchResult(hit) for hit in hits]
    selected = st.selectbox("검색 결과 리스트", search_results)
    stock = Stock(selected.symbol)

    tabs = ["회사 정보", "AI 투자 보고서"]
    tab1, tab2 = st.tabs(tabs)


    with tab1:
        st.header(str(selected))
        st.write(stock.get_basic_info())
        st.write(stock.get_financial_statement())

    with tab2:
        st.header("AI 투자 보고서")
        if st.button("보고서 생성"):
            with st.spinner(text="In progress..."):
                report = invesment_report(selected.name, selected.symbol)
                st.success("Done.")
            st.write(report)
except Exception as e:
    st.error(f"오류 발생: 검색하신 회사가 nasdaq에 등록되어 있지 않거나, 잘못된 입력입니다. {e}")
    st.stop()