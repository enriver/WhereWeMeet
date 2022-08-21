'''
참여자의 위치(위도,경도)를 받고, 그 값들의 중앙 값을 반환함으로써
참여자들끼리 만날 때, 어디서 만나면 좋을지 좌표를 알려주는 프로그램

Folium 라이브러리를 통해 지도 시각화를 통해 직관적으로 어디가 가운데인지
알 수 있게 함
'''
import requests, json
import folium
import webbrowser

# 위도와 경도 받기
def get_lat_long():
    req = requests.get("http://www.geoplugin.net/json.gp")

    if(req.status_code!=200):
        print("현재 좌표를 불러올 수 없습니다")
    else:
        location = json.loads(req.text)
        lat=location['geoplugin_latitude'] # 위도
        long=location['geoplugin_longitude'] # 경도

        print('위도 : ' + lat)
        print('경도 : ' + long)

    return float(lat), float(long)

# 지도 만들기
def make_map(location_list):
    m=folium.Map(location=[37.56,126.99],
                zoom_start=7,
                width=750,
                height=500)

    sum_lat, sum_long=0, 0
    for i in range(len(location_list)):
        lat, long = location_list[i][0], location_list[i][1]
        sum_lat+=lat
        sum_long+=long

        folium.Marker(location=[lat, long],
            icon=folium.Icon(color='red', icon='start'),
            popup=str(i+1)+'번째 위치').add_to(m)

    sum_lat = round(sum_lat/len(location_list), 2)
    sum_long= round(sum_long/len(location_list), 2)

    folium.Marker(location=[sum_lat, sum_long],
        icon=folium.Icon(color='blue', icon='start'),
        popup=str('가운데 지점 입니다')).add_to(m)

    m.save("map.html")
    print("지도가 생성되었습니다")
    print('가운데 지점은 위도 : '+str(sum_lat)+', 경도 : '+str(sum_long)+' 입니다.')

if __name__=="__main__":
    lat, long = get_lat_long() # 현재 위치의 위도와 경도 값 받기
    seoul_lat, seoul_long = 37.56, 126.99

    location_list=list()
    location_list.append([lat,long])
    location_list.append([seoul_lat, seoul_long])

    make_map(location_list)

    # 지도 띄우기
    webbrowser.open('map.html')