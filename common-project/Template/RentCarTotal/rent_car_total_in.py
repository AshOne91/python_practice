from Template.Base.base_template import BaseTemplate
from Service.ETC.csv_reader import CSVReader
from mysql import connector
import pandas as pd
import requests
import os

REGION_KEYS = {
    "서울특별시": "서울",
    "부산광역시": "부산",
    "대구광역시": "대구",
    "인천광역시": "인천",
    "광주광역시": "광주",
    "대전광역시": "대전",
    "울산광역시": "울산",
    "세종특별자치시": "세종",
    "세종특별시": "세종",
    "경기도": "경기",
    "강원특별자치도": "강원",
    "강원도": "강원",
    "충청북도": "충북",
    "충청남도": "충남",
    "전라북도": "전북",
    "전북특별자치도": "전북",
    "전라남도": "전남",
    "경상북도": "경북",
    "경상남도": "경남",
    "제주특별자치도": "제주"
}

args = {
  'host' : 'localhost',
  'user' : 'root',
  'password' : 'root1234',
  'port' : 3306,
  'database' : 'test_db'  # 접속할때 활성화할 db(스키마)명
}

def get_connection(args):
    return connector.connect(**args)  # localhost 에 접속 해서 접속 객체를 생성

def get_region_id(cursor, region_name):
    query = f"SELECT id FROM regions_table WHERE region_name = '{region_name}'"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None


class RentCarTotalIn(BaseTemplate):
    def __init__(self, name = "RentCarTotalIn"):
        super().__init__(name)
    
    def get_region(self, address):
        # 주소가 NaN이거나 None일 경우를 처리
        if not isinstance(address, str):  # 문자열이 아니면 다른 처리
            return '기타'
        
        for key, region in REGION_KEYS.items():
            if key in address:
                return region
            
        return '기타'

    def DataLoad(self, **kwargs):
        print("Load Call")
        test_dir = os.path.dirname(os.path.abspath(__file__))  
        
        # Test.py가 있는 경로에 RentCar.csv 저장
        save_path = os.path.join(test_dir, kwargs['path'])  
        csv_reader = CSVReader(save_path)  # CSV 파일 경로
        df = csv_reader.read_csv()

        # 컬럼명만 출력하기
        columns = df.columns
        print("컬럼명:", columns)

        try:
            conn = get_connection(args)  # 데이터베이스 연결
            cursor = conn.cursor()  # 커서 생성
            data_list = df.to_dict(orient='records')

            for i in range(len(data_list)):
                region = self.get_region(data_list[i]['소재지도로명주소'])  # 지역명 추출
                if region == '기타':
                    continue  # 지역이 '기타'인 경우 건너뜀
                
                region_id = get_region_id(cursor, region)  # 커서를 사용하여 region_id 조회
                if region_id is None:
                    continue  # 만약 region_id가 없다면 해당 데이터는 삽입하지 않음

                # 데이터 삽입 SQL 쿼리
                query = """
                    INSERT INTO rent_car_companies_table (company_name, region_id, sedan_vehicle_count, 
                    van_vehicle_count, electric_sedan_vehicle_count, electric_van_vehicle_count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                # 삽입할 데이터 튜플
                data_to_insert = (
                    data_list[i]['업체명'],
                    region_id,
                    data_list[i]['승용차보유대수'],
                    data_list[i]['승합차보유대수'],
                    data_list[i]['전기승용자동차보유대수'],
                    data_list[i]['전기승합자동차보유대수']
                )

                # SQL 실행
                cursor.execute(query, data_to_insert)
            
            conn.commit()  # 변경 사항 반영

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()  # 커서 닫기
            conn.close()  # 연결 종료

        






