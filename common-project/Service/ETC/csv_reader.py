import pandas as pd
import chardet

class CSVReader:
    def __init__(self, path):
        self.path = path
        self.encoding = self.detect_encoding()

    def detect_encoding(self):
        """파일의 인코딩을 자동 감지"""
        try:
            with open(self.path, 'rb') as f:
                result = chardet.detect(f.read(10000))  # 일부 데이터 샘플링
                detected_encoding = result['encoding']
                print(f"감지된 인코딩: {detected_encoding}")
                return detected_encoding
        except Exception as e:
            print(f"인코딩 감지 오류: {e}")
            return 'utf-8'  # 기본값

    def read_csv(self):
        """CSV 파일을 읽어서 DataFrame 반환"""
        try:
            df = pd.read_csv(self.path, encoding=self.encoding)
            return df
        except Exception as e:
            print(f"파일을 읽는 중 오류 발생: {e}")
            return None
