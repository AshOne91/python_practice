# App.py
import sys
import os

# root 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# RentCarTotalOut 클래스 가져오기
from Template.RentCarTotal.rent_car_total_out import RentCarTotalOut
import streamlit as st

# Streamlit 앱 실행
def main():
    # RentCarTotalOut 객체 생성
    rent_car = RentCarTotalOut()  # 객체 생성

    # Streamlit UI
    st.title("🚗 렌터카 업체 정보 앱")
    st.write("렌터카 업체들의 차량 보유 현황을 조회하고 출력합니다.")

    # 데이터 조회 및 출력
    rent_car.ViewDataStreamlit()  # Streamlit에서 데이터 표시

if __name__ == "__main__":
    main()
