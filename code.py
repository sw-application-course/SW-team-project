import pprint

header = [] # header
traffic_list = [] # 가져온 데이터를 넣을 리스트
current_ammount = 0 #한시간 동안 그 도로를 지나간 차량 대수
MSF_i = [] #서비스 수준 i에서 차로 당 최대 서비스 교통량
c_j = [] #설계속도의 용량
Vc_i = [] #서비스 수준 i에서 교통량 대 용량비
SF_i = [] #서비스 수준 i에서 주어진 도로 및 교통 조건에 대한 서비스 교통량
N = [] #편도차로수
f_W = [] #차로폭 및 측방여유폭 보정계수
f_HV = [] #중차량 보정계수


def getData(filename):
  global header
  global traffic_list

  global current_ammount
  global MSF_i
  global c_j
  global Vc_i
  global SF_i
  global N
  global f_W
  global f_HV

  car = 0
  trafficsum = 0
  line_counter = 0

  ex_date = "" #기준일자
  ex_cartype = "" #TCS차종유형구분코드
  ex_highway = "" #노선명
  ex_station = "" #순번
  ex_trafficsum = "" #교통량
  ex_direction = "" #방향구분코드

  stations_S = {}
  stations_E = {}
  
  with open(filename) as f:
    while 1:
      data = f.readline()
      if not data: break 
      
      traffic = data.split(",")
      for i in range(0,4):
        del traffic[1] #delete '집계기준일', 'TCS차종구분명','TCS차종구분코드','TCS차종유형구분명'
      for i in range(0,3):
        del traffic[2] #delete 'TCS노선번호', 'TCS본부코드', 'TCS지사코드'
      del traffic[3] #delete '순번'
      del traffic[6] #delete '\n'

      line_counter += 1
      if line_counter == 1:
        continue

      service_level = 0 #서비스 수준

      for i in range(0,6):
        if i == 2 or i ==3 or i == 5:
          continue;
        traffic[i] = int(traffic[i])

      ex_date = traffic[0]
      ex_cartype = traffic[1]
      ex_highway = traffic[2]
      ex_station = traffic[3]
      ex_trafficsum = traffic[4]
      ex_direction = traffic[5]
      
      traffic_list.append(traffic)

      if ex_cartype == 1:
        car = 0
      elif ex_cartype == 2:
        car = 1
      else:
        car = 2

      if traffic[5] == 'S':
        if not ex_station in stations_S:
          stations_S[ex_station] = {
            "down": {}
          }
          stations_S[ex_station]['down'] = [0,0,0,0,0,0,0] #소형, 중형, 대형차 수, 교통량 합, 서비스수준, Vc비, MSF
        stations_S[ex_station]['down'][car] = [ex_trafficsum]
        stations_S[ex_station]['down'][3] += traffic[4]
        trafficsum = stations_S[ex_station]['down'][3] / 24 #1일 교통량을 1시간 단위로 나눔
      
      else:
        if not ex_station in stations_E:
          stations_E[ex_station] = {
            "up": {}
          }
          stations_E[ex_station]['up'] = [0,0,0,0,0,0,0] #소형, 중형, 대형차 수, 교통량 합, 서비스수준, Vc비, MSF
        stations_E[ex_station]['up'][car] = [ex_trafficsum]
        stations_E[ex_station]['up'][3] += traffic[4]
        trafficsum = stations_E[ex_station]['up'][3] / 24 #1일 교통량을 1시간 단위로 나눔

      #서비스 수준 구하기(교통량만으로 계산한 것)
      if trafficsum <= 600:
        service_level = 'A'
        #c_j = 600
        Vc_i = round(trafficsum / 600, 2) #소수점 둘째자리까지만 표시
      elif trafficsum <= 1000:
        service_level = 'B'
        #c_j = 1000
        Vc_i = round(trafficsum / 1000, 2)
      elif trafficsum <= 1350:
        service_level = 'C'
        #c_j = 1350
        Vc_i = round(trafficsum / 1350, 2)
      elif trafficsum <= 1750:
        service_level = 'D'
        #c_j = 1750
        Vc_i = round(trafficsum / 1750, 2)
      elif trafficsum <= 2200:
        service_level = 'E'
        #c_j = 2200
        Vc_i = round(trafficsum / 2200, 2)
      else:
        service_level = 'F'
        #c_j = 2200
        Vc_i = round(trafficsum / 2200, 2) #용량 미정(2200이상이라서 일단 2200으로 잡아둠)
      c_j = 2200
      MSF_i = round(c_j * Vc_i, 2)

      if traffic[5] == 'S':
        stations_S[ex_station]['down'][4] = service_level
        stations_S[ex_station]['down'][5] = Vc_i
        stations_S[ex_station]['down'][6] = MSF_i

      else:
        stations_E[ex_station]['up'][4] = service_level
        stations_E[ex_station]['up'][5] = Vc_i
        stations_E[ex_station]['up'][6] = MSF_i
    
    pp = pprint.PrettyPrinter(indent=1)
    print(ex_date, '\n\n')
    print("* S방향\n")
    pp.pprint(stations_S)
    print("\n\n* E방향\n")
    pp.pprint(stations_E)
    
    print('\n\n\n\n------서비스교통량 구하기------\n')

    ex_station = input('도로명을 입력해주세요 : ')
    N = int(input('편도차로수 : '))
    f_W = float(input('차로폭 및 측방여유폭 보정계수 : '))
    f_HV = float(input('중차량 보정계수 : '))

    if ex_station in stations_S:
      trafficsum = stations_S[ex_station]['down'][3]
      Vc_i = stations_S[ex_station]['down'][5]
    else:
      trafficsum = stations_E[ex_station]['up'][3]
      Vc_i = stations_E[ex_station]['up'][5]

    SF_i = float(MSF_i * N * f_W * f_HV)
    print('서비스 교통량(vph) : ', SF_i)

filename1 = ".\\data\\TCS_67_04_01_270485.csv"
getData(filename1)