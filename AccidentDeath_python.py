import requests
import folium
import json
from pandas import json_normalize
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# API
url = 'http://apis.data.go.kr/B552061/AccidentDeath/getRestTrafficAccidentDeath'
params = {
    'serviceKey': 'KIEoEcas5+qEQxI+aryWfzGIcu0jQ8TPGnrwEEywckSmesrb/L8yUJhmWyrHOsPaFHn8wzeZOLsiTn88KZUxaQ==',
    'searchYear': '2021',
    'siDo': '',
    'guGun': '',
    'type': 'JSON',
    'numOfRows': '2816',
    'pageNo': '1'
}
response = requests.get(url, params=params)
json_file = json.loads(response.text)

df = json_normalize(json_file['items']['item'])  # JSON 데이터를 DataFrame으로 변환

m = folium.Map(location=[36.4563239, 127.8446978], zoom_start=8)  # 초기 위치와 줌 레벨이 설정된 맵 생성

for index, row in df.iterrows():  # DataFrame 행을 반복하며 맵에 마커 추가
    latitude = float(row['la_crd'])  # 사고 위치의 위도와 경도 가져오기
    longitude = float(row['lo_crd'])

    # 사고 유형 텍스트
    accident_type = row['acc_ty_cd']
    if accident_type == '01':
        accident_type_text = '차vs사람 - 횡단중'
    elif accident_type == '02':
        accident_type_text = '차vs사람 - 차도 통행중'
    elif accident_type == '03':
        accident_type_text = '차vs사람 - 길가장자리 구역 통행중'
    elif accident_type == '04':
        accident_type_text = '차vs사람 - 보도 통행중'
    elif accident_type == '05':
        accident_type_text = '차vs사람 - 기타'
    elif accident_type == '21':
        accident_type_text = '차vs차 - 정면충돌'
    elif accident_type == '22':
        accident_type_text = '차vs차 - 측면충돌'
    elif accident_type == '23':
        accident_type_text = '차vs차 - 추돌'
    elif accident_type == 'Z1':
        accident_type_text = '차vs차 - 진행중 추돌'
    elif accident_type == 'Z2':
        accident_type_text = '차vs차 - 주정차중 충돌'
    elif accident_type == '25':
        accident_type_text = '차vs차 - 기타'
    elif accident_type == '26':
        accident_type_text = '차vs차 - 후진중 충돌'
    elif accident_type == '32':
        accident_type_text = '차량단독 - 공작물 충돌'
    elif accident_type == '34':
        accident_type_text = '차량단독 - 도로이탈 추락'
    elif accident_type == '35':
        accident_type_text = '차량단독 - 도로이탈 기타'
    elif accident_type == '33':
        accident_type_text = '차량단독 - 주/정차 차량 충돌'
    elif accident_type == '31':
        accident_type_text = '차량단독 - 전도전복'
    elif accident_type == '37':
        accident_type_text = '차량단독 - 기타'
    elif accident_type == '36':
        accident_type_text = '차량단독 - 운전자 부재'
    elif accident_type == '38':
        accident_type_text = '차량단독 - 전도'
    elif accident_type == '39':
        accident_type_text = '차량단독 - 전복'
    elif accident_type == '41':
        accident_type_text = '철길건널목'
    elif accident_type == 'Z4':
        accident_type_text = '철길건널목 - 차단기 돌파'
    elif accident_type == 'Z5':
        accident_type_text = '철길건널목 - 경보기 무시'
    elif accident_type == 'Z6':
        accident_type_text = '철길건널목 - 직전진행'
    elif accident_type == 'Z7':
        accident_type_text = '철길건널목 - 기타 사고'
    elif accident_type == 'Z8':
        accident_type_text = '기타'

    # 도로 형태 텍스트
    road_code = row['road_frm_cd']
    if road_code == '01':
        road_text = '터널 안'
    elif road_code == '02':
        road_text = '교량 위'
    elif road_code == '03':
        road_text = '고가도로 위'
    elif road_code == '04':
        road_text = '지하차도 내'
    elif road_code == '05':
        road_text = '기타 단일로'
    elif road_code == 'Z1':
        road_text = '횡단보도 상'
    elif road_code == 'Z2':
        road_text = '횡단보도 부근'
    elif road_code == '06':
        road_text = '교차로 내'
    elif road_code == '07':
        road_text = '교차로 횡단보도 내'
    elif road_code == '08':
        road_text = '교차로 부근'
    elif road_code == '10':
        road_text = '철길건널목'
    elif road_code == '98':
        road_text = '기타'
    elif road_code == '99':
        road_text = '불명'
    elif road_code == 'Z3':
        road_text = '기타/불명'
    elif road_code == '##':
        road_text = '없음'

    # 가해자 법규 위반 텍스트
    violation_code = row['aslt_vtr_cd']
    if violation_code == '01 ':
        violation_text = '과속'
    elif violation_code == '02 ':
        violation_text = '중앙선 침범'
    elif violation_code == '03 ':
        violation_text = '신호위반'
    elif violation_code == '04 ':
        violation_text = '안전거리 미확보'
    elif violation_code == '05 ':
        violation_text = '안전운전 의무 불이행'
    elif violation_code == '06 ':
        violation_text = '교차로 통행방법 위반'
    elif violation_code == '07 ':
        violation_text = '보행자 보호의무 위반'
    elif violation_code == '99 ':
        violation_text = '기타'

    folium.Marker(
        location=[latitude, longitude],
        icon=folium.Icon(color='red'),
        popup=folium.Popup(
            f"<div style='font-size: 16px;'>"
            f"<b>사고유형</b>: {accident_type_text}<br>"
            f"<b>도로형태</b>: {road_text}<br>"
            f"<b>가해자 법규 위반</b>: {violation_text}<br>"
            f"<b>부상자 수</b>: {row['injpsn_cnt']}<br>"
            f"<b><font color='red'>사망자 수</b>: {row['dth_dnv_cnt']}<br>"
            ,
            max_width=1000
        )
    ).add_to(m)

m.save('AccidentDeath.html')


font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)

plt.rcParams['font.family'] = font_prop.get_name()
plt.rc('font', size=13)

# 사고 유형 텍스트 매핑
accident_type_mapping = {  
    '01': '차vs사람\n횡단중',
    '02': '차vs사람\n차도\n통행중',
    '03': '차vs사람\n길가장자리\n통행중',
    '04': '차vs사람\n보도\n통행중',
    '05': '차vs사람\n기타',
    '21': '차vs차\n정면충돌',
    '22': '차vs차\n측면충돌',
    '23': '차vs차\n추돌',
    'Z1': '차vs차\n진행중\n추돌',
    'Z2': '차vs차\n주정차중\n충돌',
    '25': '차vs차\n기타',
    '26': '차vs차\n후진중\n충돌',
    '32': '차량\n공작물\n충돌',
    '34': '차량\n도로이탈\n추락',
    '35': '차량\n도로이탈\n기타',
    '33': '차량\n주/정차\n차량충돌',
    '31': '차량\n전도전복',
    '37': '차량\n기타',
    '36': '차량\n운전자\n부재',
    '38': '차량\n전도',
    '39': '차량\n전복',
    '41': '철길건널목',
    'Z4': '철길건널목\n차단기\n돌파',
    'Z5': '철길건널목\n경보기\n무시',
    'Z6': '철길건널목\n직전진행',
    'Z7': '철길건널목\n기타 사고',
    'Z8': '기타'
}
accident_type_counts = df['acc_ty_cd'].map(accident_type_mapping).value_counts()  # 사고 유형별 발생 건수 계산
plt.bar(accident_type_counts.index, accident_type_counts.values)    # 막대 그래프 생성
plt.title('사고 유형별 교통사고 건수', fontweight='bold', fontsize=24)    # 그래프 제목과 축 이름 설정
plt.xlabel('사고 유형', fontsize=14, loc='left')
plt.ylabel('교통사고 건수\n', fontsize=14, loc='bottom')
plt.show()    # 그래프 출력

# 도로 형태 텍스트 매핑
road_mapping = {
    '01': '터널 안',
    '02': '교량 위',
    '03': '고가도로 위',
    '04': '지하차도 내',
    '05': '기타 단일로',
    'Z1': '횡단보도 상',
    'Z2': '횡단보도 부근',
    '06': '교차로 내',
    '07': '교차로\n횡단보도 내',
    '08': '교차로 부근',
    '10': '철길건널목',
    '98': '기타',
    '99': '불명',
    'Z3': '기타/불명',
    '##': '없음'
}
road_counts = df['road_frm_cd'].map(road_mapping).value_counts()
plt.bar(road_counts.index, road_counts.values)
plt.title('도로 형태별 교통사고 건수', fontweight='bold', fontsize=24)
plt.xlabel('\n도로 형태', fontsize=14, loc='left')
plt.ylabel('교통사고 건수\n', fontsize=14, loc='bottom')
plt.show()

# 가해자 법규 위반 텍스트 매핑
violation_mapping = {
    '01 ': '과속',
    '02 ': '중앙선 침범',
    '03 ': '신호위반',
    '04 ': '안전거리 미확보',
    '05 ': '안전운전 의무 불이행',
    '06 ': '교차로 통행방법 위반',
    '07 ': '보행자 보호의무 위반',
    '99 ': '기타'
}
violation_counts = df['aslt_vtr_cd'].map(violation_mapping).value_counts()
plt.bar(violation_counts.index, violation_counts.values)
plt.title('가해자 법규 위반 항목별 횟수', fontweight='bold', fontsize=24)
plt.xlabel('\n가해자 법규 위반 항목', fontsize=14, loc='left')
plt.ylabel('횟수\n', fontsize=14, loc='bottom')
plt.show()


# 엑셀 저장
df = df.drop('occrrnc_lc_sido_cd', axis=1)
df = df.drop('occrrnc_lc_sgg_cd', axis=1)
df = df.drop('acc_ty_lclas_cd', axis=1)
df = df.drop('acc_ty_mlsfc_cd', axis=1)
df = df.drop('road_frm_lclas_cd', axis=1)
df = df.drop('wrngdo_isrty_vhcty_lclas_cd', axis=1)
df = df.drop('dmge_isrty_vhcty_lclas_cd', axis=1)
df = df.drop('occrrnc_lc_x_crd', axis=1)
df = df.drop('occrrnc_lc_y_crd', axis=1)
df = df.drop('lo_crd', axis=1)
df = df.drop('la_crd', axis=1)

df = df.rename(columns={'acc_year': '사고년도'})
df = df.rename(columns={'occrrnc_dt': '발생월일시'})
df = df.rename(columns={'dght_cd': '주간/야간'})
df = df.rename(columns={'occrrnc_day_cd': '발생요일'})
df = df.rename(columns={'dth_dnv_cnt': '사망자수'})
df = df.rename(columns={'injpsn_cnt': '부상자수'})
df = df.rename(columns={'se_dnv_cnt': '중상자수'})
df = df.rename(columns={'sl_dnv_cnt': '경상자수'})
df = df.rename(columns={'wnd_dnv_cnt': '부상신고자수'})
df = df.rename(columns={'acc_ty_cd': '사고유형코드'})
df = df.rename(columns={'aslt_vtr_cd': '가해자법규위반코드'})
df = df.rename(columns={'road_frm_cd': '도로형태코드'})

df['주간/야간'] = df['주간/야간'].replace('1', '주간')
df['주간/야간'] = df['주간/야간'].replace('2', '야간')

df['발생요일'] = df['발생요일'].replace('1', '일요일')
df['발생요일'] = df['발생요일'].replace('2', '월요일')
df['발생요일'] = df['발생요일'].replace('3', '화요일')
df['발생요일'] = df['발생요일'].replace('4', '수요일')
df['발생요일'] = df['발생요일'].replace('5', '목요일')
df['발생요일'] = df['발생요일'].replace('6', '금요일')
df['발생요일'] = df['발생요일'].replace('7', '토요일')

df['사고유형코드'] = df['사고유형코드'].replace('01', '횡단중')
df['사고유형코드'] = df['사고유형코드'].replace('02', '차도통행중')
df['사고유형코드'] = df['사고유형코드'].replace('03', '길가장자리구역통행중')
df['사고유형코드'] = df['사고유형코드'].replace('04', '보도통행중')
df['사고유형코드'] = df['사고유형코드'].replace('05', '기타')
df['사고유형코드'] = df['사고유형코드'].replace('21', '정면충돌')
df['사고유형코드'] = df['사고유형코드'].replace('22', '측면충돌')
df['사고유형코드'] = df['사고유형코드'].replace('23', '추돌')
df['사고유형코드'] = df['사고유형코드'].replace('Z1', '진행중 추돌')
df['사고유형코드'] = df['사고유형코드'].replace('Z2', '주정차중 충돌')
df['사고유형코드'] = df['사고유형코드'].replace('25', '기타')
df['사고유형코드'] = df['사고유형코드'].replace('26', '후진중충돌')
df['사고유형코드'] = df['사고유형코드'].replace('32', '공작물충돌')
df['사고유형코드'] = df['사고유형코드'].replace('24', '도로이탈 추락')
df['사고유형코드'] = df['사고유형코드'].replace('25', '도로이탈 기타')
df['사고유형코드'] = df['사고유형코드'].replace('33', '주/정차차량 충돌')
df['사고유형코드'] = df['사고유형코드'].replace('31', '전도전복')
df['사고유형코드'] = df['사고유형코드'].replace('37', '기타')
df['사고유형코드'] = df['사고유형코드'].replace('36', '운전자부재')
df['사고유형코드'] = df['사고유형코드'].replace('38', '전도')
df['사고유형코드'] = df['사고유형코드'].replace('39', '전복')
df['사고유형코드'] = df['사고유형코드'].replace('41', '철길건널목')
df['사고유형코드'] = df['사고유형코드'].replace('Z4', '차단기돌파')
df['사고유형코드'] = df['사고유형코드'].replace('Z5', '경보기 무시')
df['사고유형코드'] = df['사고유형코드'].replace('Z6', '직전진행')
df['사고유형코드'] = df['사고유형코드'].replace('Z7', '기타')
df['사고유형코드'] = df['사고유형코드'].replace('Z8', '기타')
df['사고유형코드'] = df['사고유형코드'].replace('##', '없음')

df['도로형태코드'] = df['도로형태코드'].replace('01', '터널안')
df['도로형태코드'] = df['도로형태코드'].replace('02', '교량위')
df['도로형태코드'] = df['도로형태코드'].replace('03', '고가도로위')
df['도로형태코드'] = df['도로형태코드'].replace('04', '지하차도내')
df['도로형태코드'] = df['도로형태코드'].replace('05', '기타단일로')
df['도로형태코드'] = df['도로형태코드'].replace('Z1', '횡단보도상')
df['도로형태코드'] = df['도로형태코드'].replace('Z2', '횡단보도부근')
df['도로형태코드'] = df['도로형태코드'].replace('06', '교차로내')
df['도로형태코드'] = df['도로형태코드'].replace('07', '교차로횡단보도내')
df['도로형태코드'] = df['도로형태코드'].replace('08', '교차로부근')
df['도로형태코드'] = df['도로형태코드'].replace('10', '철길건널목')
df['도로형태코드'] = df['도로형태코드'].replace('98', '기타')
df['도로형태코드'] = df['도로형태코드'].replace('99', '불명')
df['도로형태코드'] = df['도로형태코드'].replace('Z3', '기타/불명')
df['도로형태코드'] = df['도로형태코드'].replace('##', '없음')

df['가해자법규위반코드'] = df['가해자법규위반코드'].replace('01 ', '과속')
df['가해자법규위반코드'] = df['가해자법규위반코드'].replace('02 ', '중앙선 침범')
df['가해자법규위반코드'] = df['가해자법규위반코드'].replace('03 ', '신호위반')
df['가해자법규위반코드'] = df['가해자법규위반코드'].replace('04 ', '안전거리 미확보')
df['가해자법규위반코드'] = df['가해자법규위반코드'].replace('05 ', '안전운전 의무 불이행')
df['가해자법규위반코드'] = df['가해자법규위반코드'].replace('06 ', '교차로 통행방법 위반')
df['가해자법규위반코드'] = df['가해자법규위반코드'].replace('07 ', '보행자 보호의무 위반')
df['가해자법규위반코드'] = df['가해자법규위반코드'].replace('99 ', '기타')

df.to_csv('AccidentDeath.csv', index=False, encoding='utf-8-sig')