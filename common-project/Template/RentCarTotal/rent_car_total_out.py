# RentCarTotalOut.py
import sys
import os
import streamlit as st
import pandas as pd
from mysql import connector
from Template.Base.base_template import BaseTemplate
from Service.ETC.csv_reader import CSVReader

args = {
  'host': 'localhost',
  'user': 'root',
  'password': 'root1234',
  'port': 3306,
  'database': 'test_db'  # 접속할 때 활성화할 DB(스키마)명
}

def get_connection(args):
    """데이터베이스 연결 생성"""
    return connector.connect(**args)  # localhost에 접속해서 접속 객체 생성

class RentCarTotalOut(BaseTemplate):
    def __init__(self, name="RentCarTotalOut"):
        super().__init__(name)
        self.data = None  # 데이터를 저장할 멤버 변수
        self.region_vehicle_count = None  # 지역별 차량 갯수를 저장할 변수

    def ViewData(self):
        """데이터 조회 후 self.data에 저장"""
        try:
            conn = get_connection(args)  # 데이터베이스 연결
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT r.region_name, c.company_name, c.sedan_vehicle_count, 
                       c.van_vehicle_count, c.electric_sedan_vehicle_count, 
                       c.electric_van_vehicle_count
                FROM rent_car_companies_table c
                JOIN regions_table r ON c.region_id = r.id
            """
            cursor.execute(query)
            results = cursor.fetchall()

            if results:
                self.data = results  # 조회된 데이터를 멤버 변수에 저장
                st.success("📌 데이터 조회 완료! 멤버 변수에 저장되었습니다.")
                self.get_region_vehicle_count()  # 지역별 차량 갯수 계산
            else:
                st.warning("📌 조회된 데이터가 없습니다.")

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

    def get_region_vehicle_count(self):
        """지역별 총 차량 갯수를 계산하여 딕셔너리에 저장"""
        region_count = {}

        for row in self.data:
            region = row['region_name']
            sedan_count = row['sedan_vehicle_count']
            van_count = row['van_vehicle_count']
            electric_sedan_count = row['electric_sedan_vehicle_count']
            electric_van_count = row['electric_van_vehicle_count']

            # 지역별 차량 총합 계산
            if region not in region_count:
                region_count[region] = {
                    'sedan_count': 0,
                    'van_count': 0,
                    'electric_sedan_count': 0,
                    'electric_van_count': 0
                }

            region_count[region]['sedan_count'] += sedan_count
            region_count[region]['van_count'] += van_count
            region_count[region]['electric_sedan_count'] += electric_sedan_count
            region_count[region]['electric_van_count'] += electric_van_count

        self.region_vehicle_count = region_count  # 결과를 멤버 변수에 저장
        st.success("📌 지역별 차량 갯수 계산 완료!")

    def ViewDataStreamlit(self):
        """Streamlit을 이용한 데이터 표시 (self.data 활용)"""
        st.title("🚗 렌터카 업체 정보")
        st.write("렌터카 업체의 차량 보유 현황을 조회합니다.")

        # 데이터가 없으면 자동 조회
        if self.data is None:
            st.warning("📌 데이터가 없어서 새로 조회합니다.")
            self.ViewData()

        # 데이터가 있으면 테이블로 표시
        if self.data:
            df = pd.DataFrame(self.data)
            st.dataframe(df)  # 테이블 형식으로 출력
        else:
            st.error("📌 조회된 데이터가 없습니다.")

        # 지역별 총 차량 갯수 표시
        if self.region_vehicle_count:
            region_df = pd.DataFrame(self.region_vehicle_count).T
            region_df.index.name = '지역명'
            st.write("📊 지역별 총 차량 갯수:")
            st.dataframe(region_df)
