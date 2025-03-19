from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from Template.Base.base_template import BaseTemplate
from Service.ETC.csv_reader import CSVReader
from mysql import connector
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import requests
import os

args = {
  'host' : 'localhost',
  'user' : 'root',
  'password' : 'root1234',
  'port' : 3306,
  'database' : 'test_db'  # 접속할때 활성화할 db(스키마)명
}

def get_connection(args):
    return connector.connect(**args)  # localhost 에 접속 해서 접속 객체를 생성

class FaqIn(BaseTemplate):
    def __init__(self, name = "FaqIn"):
        super().__init__(name)
        self.df = pd.DataFrame(columns=['브랜드명', '질문', '답변'])  # 빈 데이터프레임 생성
        self.brand_map = {
            "현대": 1,  # Hyundai (car_company_table ID)
            "기아": 2   # Kia (car_company_table ID)
        }

    def DataLoad(self, **kwargs):
        print("Load Call")
        print("현대 클로링 start")
        self.hyndai_in()
        print("현대 클로링 end")
        # 기아
        print("기아 클로링 start")
        self.kia_in()
        print("기아 클로링 end")
        print("db insert start")
        self.insert_to_db()
        print("db insert end")

    def kia_in(self):
        url = 'https://www.kia.com/kr/customer-service/center/faq'

        # 브라우저 열기
        wd = webdriver.Chrome()

        # 웹페이지 열기
        wd.get(url) 
        wd.find_element(By.XPATH, "//span[text()='전체']").click()
        time.sleep(10)

        result = []    
        for i in range(4):
            for j in range(1, 6):

                html = wd.page_source 
                soup = BeautifulSoup(html, 'html.parser') 
                faq_items = soup.find_all("div", class_="cmp-accordion__item")
                
                for item in faq_items:  # faqitems -> faq_items 로 수정
                    title = item.find("span", class_="cmp-accordion__title").text.strip()
                    content = item.find("div", class_="faqinner__wrap").text.strip()
                    result.append(("기아",title, content))
                if j != 5:  
                    dropdown = wd.find_element(By.XPATH,f'//*[@id="contents"]/div/div[3]/div/div/div[4]/div/ul/li[{j+1}]/a')
                    dropdown.click()
                    time.sleep(3)
            if i == 0 :
                dropdown = wd.find_element(By.XPATH,f'//*[@id="contents"]/div/div[3]/div/div/div[4]/div/button')
            else:
                dropdown = wd.find_element(By.XPATH,f'//*[@id="contents"]/div/div[3]/div/div/div[4]/div/button[2]')
            dropdown.click()
            time.sleep(1)

        wd.quit()
        df_kia = pd.DataFrame(result, columns=['브랜드명', '질문', '답변'])
        self.df = pd.concat([self.df, df_kia], ignore_index=True)


    def hyndai_in(self):
        url = 'https://www.hyundai.com/kr/ko/e/customer/center/faq'
        # 브라우저 열기
        wd = webdriver.Chrome()

        # 웹페이지 열기
        wd.get(url) 
        result = []
        title = ''
        content = ''

        html = wd.page_source
        soup = BeautifulSoup(html, 'html.parser') # html 정보를 파싱

        buttons = wd.find_elements(By.CSS_SELECTOR, 'ul.tab-menu__icon-wrapper li button')

        for button in tqdm(buttons):
            wd.execute_script("arguments[0].click();", button)
            time.sleep(1)

            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser') # html 정보를 파싱
            for i in range(1, 11):
                try:
                    dropdown = wd.find_element(By.XPATH,f'//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[1]/div[{i}]/button')
                    wd.execute_script("arguments[0].click();", dropdown)
                    time.sleep(3)
                    question_element = wd.find_element(By.XPATH, f'//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[1]/div[{i}]/button/div/span[2]')
                    title = question_element.text.strip()
                    element = wd.find_element(By.CSS_SELECTOR,'div.conts')
                    content = element.text.strip()
                    # 브랜드명 '현대' 추가
                    result.append(["현대", title, content])
                except Exception as e:
                    pass
        wd.quit()

        # 새 데이터프레임 생성 후 기존 멤버 변수 df와 병합
        df_hyundai = pd.DataFrame(result, columns=['브랜드명', '질문', '답변'])
        self.df = pd.concat([self.df, df_hyundai], ignore_index=True)

    def insert_to_db(self):
        """크롤링한 FAQ 데이터를 MySQL에 삽입 (전역 get_connection(args) 사용)"""
        conn = get_connection(args)  # 전역 DB 연결 함수 사용
        cursor = conn.cursor()

        # 🚗 브랜드명 → DB 외래키 ID 변환
        for _, row in self.df.iterrows():
            brand_name = row['브랜드명']
            question = row['질문']
            answer = row['답변']

            car_company_id = self.brand_map.get(brand_name)  # 브랜드명에 따른 ID 가져오기
            
            if car_company_id:  # 유효한 브랜드만 INSERT 실행
                sql = """
                INSERT INTO faq_table (car_company_id, question, answer)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (car_company_id, question, answer))

        # DB 반영 및 연결 종료
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ 데이터베이스 저장 완료!")

    def get_faq_data(self):
        """수집된 FAQ 데이터를 반환"""
        return self.df
