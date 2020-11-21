header = [] # header
traffic_list = [] # 가져온 데이터를 넣을 리스트


def getData(filename):
  global header
  global traffic_list
  line_counter = 0


  with open(filename) as f:
    while 1:
      data = f.readline()
      if not data: break 
      if line_counter == 0:
        header = data.split(",") #맨 첫 줄은 header로 저장
        for i in range(0,4):
          del header[1] #delete '집계기준일', 'TCS차종구분명','TCS차종구분코드','TCS차종유형구분명'
        for i in range(0,3):
          del header[2] #delete 'TCS노선번호', 'TCS본부코드', 'TCS지사코드'
        del header[4] #delete '구분'
        del header[6] #delete '\n'

      else:
        traffic = data.split(",")
        for i in range(0,4):
          del traffic[1] #delete '집계기준일', 'TCS차종구분명','TCS차종구분코드','TCS차종유형구분명'
        for i in range(0,3):
          del traffic[2] #delete 'TCS노선번호', 'TCS본부코드', 'TCS지사코드'
        del traffic[4] #delete '구분'
        del traffic[6] #delete '\n'

        for i in range(0,6):
          if i == 2 or i == 5:
            continue;
          tmp = int(traffic[i])
          traffic[i] = tmp
            
        traffic_list.append(traffic)
                    
      line_counter += 1



filename1 = ".\\data\\TCS_67_04_01_270485.csv"
getData(filename1)


# for test
print(header)
print(len(traffic_list))
print(traffic_list)

