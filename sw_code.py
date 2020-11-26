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

  line = 0
  line2 = 0
  line_counter = 0
  ex_date = "" #기준일자
  ex_cartype = "" #TCS차종유형구분코드
  ex_highway = "" #노선명
  ex_station = "" #순번
  ex_trafficsum = "" #교통량
  ex_direction = "" #방향구분코드

  #stations = {}
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

      service_level = [] #서비스 수준

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

      if ex_trafficsum <= 600:
        service_level.append('A')
      elif ex_trafficsum <= 1000:
        service_level.append('B')
      elif ex_trafficsum <= 1350:
        service_level.append('C')
      elif ex_trafficsum <= 1750:
        service_level.append('D')
      elif ex_trafficsum <= 2200:
        service_level.append('E')
      else:
        service_level.append('F')

      """
      if not ex_station in stations:
        stations[ex_station] = {
          "up" : {},
          "down" : {}
        }
      
      if traffic[5] == 'E':
        if not ex_cartype in stations[ex_station]['up']:
          stations[ex_station]['up'][ex_cartype] += traffic[4]
        stations[ex_station]['down'][ex_cartype] += traffic[4]
      else:
        if not ex_cartype in stations[ex_station]['down']:
          stations[ex_station]['down'][ex_cartype] += traffic[4]
        stations[ex_station]['down'][ex_cartype] += traffic[4]
      """
      
      if traffic[5] == 'S':
        if not ex_station in stations_S:
          line = 0
          stations_S[ex_station] = {
            "down": {}
          }
          stations_S[ex_station]['down'][line] = [ex_trafficsum]
          #stations_S[ex_station]['down'][line] = service_level[line_counter]
        else:
          stations_S[ex_station]['down'][line] = [ex_trafficsum]
          #stations_S[ex_station]['down'][line] = service_level[line_counter]
        line += 1
      else:
        line2 = 0
        if not ex_station in stations_E:
          stations_E[ex_station] = {
            "up": {}
          }
          stations_E[ex_station]['up'][line2] = [ex_trafficsum]
        else:
          stations_E[ex_station]['up'][line2] = [ex_trafficsum]
        line2 += 1
          #stations_S[ex_station]['down'][line] = service_level[line_counter]
        #line += 1
      
      
    pp = pprint.PrettyPrinter(indent=1)
    #pp.pprint(stations)
    print(ex_date, '\n\n')
    print("* S방향\n")
    pp.pprint(stations_S)
    print("\n\n* E방향\n")
    pp.pprint(stations_E)

filename1 = ".\\data\\TCS_67_04_01_270485.csv"
getData(filename1)