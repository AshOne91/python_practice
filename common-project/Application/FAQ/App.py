import sys
import os

# root 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Template.FAQ.faq_in import FaqIn

faq_in = FaqIn()
faq_in.DataLoad()