let traffic = [];
let highway = {};
let fileName = [];

let selected_highway;
let selected_direction;
let selected_SF_i; //서비스 교통량
let selected_N; //편도차로수
let selected_f_W; //차로폭 및 측방여유폭 보정계수
let selected_f_HV; //중차량 보정계수

$(document).ready(function() {
  $.ajax({
    type: "GET",
    url: "./data/TCS_67_04_01_270485.csv",
    dataType: "text",
    contentType: "application/x-www-form-urlencoded; charset=euc-kr",
    beforeSend: function(jqXHR){
      jqXHR.overrideMimeType('application/x-www-form-urlencoded;charset=euc-kr');
    },
    success: function(data) {
      processData(data);
      getNeededValue();
      putHighway();
    }
  });
});

    
function processData(allText) {
  //let traffic_list = [];
  let current_ammount = 0;

  let car = 0;
  let trafficsum = 0;
  let line_counter = 0;

  let ex_date; //기준일자
  let ex_cartype; //TCS차종유형구분코드
  let ex_highway; //노선명
  let ex_station; //순번
  let ex_trafficsum; //교통량
  let ex_direction; //방향구분코드

  var allTextLines = allText.split(/\r\n|\n/);
  var headers = allTextLines[0].split(',');
  for (var i = 0; i < 4; i++) {
    headers.splice(1, 1);
  }
  for (var i = 0; i < 3; i++) {
    headers.splice(2, 1);
  }
  headers.splice(3, 1);
  headers.splice(6, 1);

  for (var i = 1; i < allTextLines.length; i++) {
    var traffic = allTextLines[i].split(',');
    for (var j = 0; j < 4; j++) {
      traffic.splice(1, 1);
    }
    for (var j = 0; j < 3; j++) {
      traffic.splice(2, 1);
    }
    traffic.splice(3, 1);
    traffic.splice(6, 1);

    for (var j = 0; j < 6; j++) { //char->int
      if (j == 2 || j == 3 || j == 5) {
        continue;
      }
      traffic[j] = parseInt(traffic[j]);
    }

    ex_date = traffic[0]; //기준일자
    ex_cartype = traffic[1]; //TCS차종유형구분코드
    ex_highway = traffic[2]; //노선명
    ex_station = traffic[3]; //구분(방향문자열)
    ex_trafficsum = traffic[4]; //교통량
    ex_direction = traffic[5]; //방향구분코드

    if (ex_cartype == 1) {
      car = 0; //소형
    } else if (ex_cartype == 2) {
      car = 1; //중형
    } else {
      car = 2; //대형
    }

    if(!(ex_highway in highway)){
      highway[ex_highway] = {};
    }
    if(!(ex_station in highway[ex_highway])){
      highway[ex_highway][ex_station] = [0,0,0,0,0,0,0];
    }
    
    highway[ex_highway][ex_station][car] = ex_trafficsum;
    ex_trafficsum /= 24; //1일 교통량을 1시간 단위로 나눔
    highway[ex_highway][ex_station][3] += ex_trafficsum;

  }
}

//service level, Vc_i, MSF_i 구하기
function getNeededValue() {

  for(var key1 in highway){
    for(var key2 in highway[key1]){
      let service_level;
      let Vc_i;

      if (highway[key1][key2][3] <= 600) {
        service_level = 'A';
        Vc_i = parseFloat((highway[key1][key2][3] / 600).toFixed(2)); //소수점 둘째자리까지만 표시
      }
      else if (highway[key1][key2][3] <= 1000) {
        service_level = 'B';
        Vc_i = parseFloat((highway[key1][key2][3] / 1000).toFixed(2));
      }
      else if (highway[key1][key2][3] <= 1350) {
        service_level = 'C';
        Vc_i = parseFloat((highway[key1][key2][3] / 1350).toFixed(2));
      }
      else if (highway[key1][key2][3] <= 1750) {
        service_level = 'D';
        Vc_i = parseFloat((highway[key1][key2][3] / 1750).toFixed(2));
      }
      else if (highway[key1][key2][3] <= 2200) {
        service_level = 'E';
        Vc_i = parseFloat((highway[key1][key2][3] / 2200).toFixed(2));
      }
      else {
        service_level = 'F';
        Vc_i = parseFloat((highway[key1][key2][3] / 2200).toFixed(2));
      }
      const c_j = 2200;
      const MSF_i = parseFloat((c_j * Vc_i).toFixed(2));

      highway[key1][key2][4] = service_level;
      highway[key1][key2][5] = Vc_i;
      highway[key1][key2][6] = MSF_i;

      console.log(highway[key1][key2]);
      console.log("<br>");
    }
  }
}


function putHighway(){
  for(var key in highway){
    var option = document.createElement('option');
    option.textContent = key;
    option.value = key;
    document.getElementById('highwaySelect').append(option);
  }
}

function putDirection(){
  var slcHighway = document.getElementById('highwaySelect');
  var slcDirection = document.getElementById('directionSelect');
  slcDirection.options.length=1; 
  var selectValue = slcHighway.options[slcHighway.selectedIndex].value;
  selected_highway = selectValue;
  for(var key in highway[selectValue]){
    var option = document.createElement('option');
    option.textContent = key;
    option.value = key;
    slcDirection.append(option);
  }
}

//선택된 direction을 받아옴
function getDirection(){
  var slcDirection = document.getElementById('directionSelect');
  var selectValue = slcDirection.options[slcDirection.selectedIndex].value;
  selected_direction = selectValue;
}

function calServiceTraffic(){
  const output_servicelevel = highway[selected_highway][selected_direction][4] //서비스 수준
  const output_MSF_i = highway[selected_highway][selected_direction][6] //서비스 수준 i에서 차로 당 최대 서비스 교통량
  const output_SF_i = parseFloat(output_MSF_i * selected_N * selected_f_W * selected_f_HV); //서비스 교통량

  document.getElementById("servicelevel").innerHTML = output_servicelevel;
  document.getElementById("MSF_i").innerHTML = output_MSF_i;
  document.getElementById("SF_i").innerHTML = output_SF_i;

  $("container").load(window.location.href + "container");
}

function getValue(){
  getDirection();
  selected_N = document.getElementById('NSelect').value;
  selected_f_W = document.getElementById('f_wSelect').value;
  selected_f_HV = document.getElementById('f_HVSelect').value;

  calServiceTraffic();
}