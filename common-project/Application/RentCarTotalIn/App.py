import sys
import os

# root 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Template.RentCarTotal.rent_car_total_in import RentCarTotalIn

rent_car = RentCarTotalIn()
# ent_car.DataLoad(path = 'RentCar.csv')