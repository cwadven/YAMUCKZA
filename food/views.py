from django.shortcuts import render,redirect
from .models import Foodmenu, Store, Dessertmenu
from login.models import Profile
from django.contrib.auth.models import User
from django.db.models import Q
import random
from math import sin, cos, sqrt, atan2, radians

# Create your views here.

def main(request):
    if request.session.get('latitude'):
        del request.session['latitude']
        del request.session['longitude']
    return render(request, 'main.html')

def Fmenu(request):
    if request.method=="POST":
        content = {
        "radius_session":request.session.get('radius'),
        "lessprice_session":request.session.get('lessprice'),
        "highprice_session":request.session.get('highprice'),
        "latitude_session":request.session.get('latitude', False),
        "longitude_session":request.session.get('longitude', False)
        }
        return render(request, 'Fmenu.html', content)

    request.session['radius'] = 0.7
    request.session['lessprice'] = 0
    request.session['highprice'] = 7000
    content = {
        "radius_session":request.session.get('radius'),
        "lessprice_session":request.session.get('lessprice'),
        "highprice_session":request.session.get('highprice'),
        "latitude_session":request.session.get('latitude', False),
        "longitude_session":request.session.get('longitude', False)
    }
    return render(request, 'Fmenu.html', content)


def Fselect(request):
    Check_category = []
    Check_category.append(request.POST.getlist('check1') or list('N')) #Check는 list로만 가져와지고 체크가 안되어있으면 값이 없어서 찾지를 못함 그래서 or "N"을 함
    Check_category.append(request.POST.getlist('check2') or list('N'))
    Check_category.append(request.POST.getlist('check3') or list('N'))
    Check_category.append(request.POST.getlist('check4') or list('N'))
    Check_category.append(request.POST.getlist('check5') or list('N'))
    Check_category.append(request.POST.getlist('check6') or list('N'))
    Check_category.append(request.POST.getlist('check7') or list('N'))
    Check_category.append(request.POST.getlist('check8') or list('N')) #리스트로 한 이유는 나중에 밑에서 더할때 리스트가 아니면 안더해짐 ㅠ
    Check_category.append(request.POST.getlist('check9') or list('N'))
    Check_category.append(request.POST.getlist('check10') or list('N'))
    Check_category.append(request.POST.getlist('check11') or list('N'))
    Check_category.append(request.POST.getlist('check12') or list('N'))


    Check_category = sum(Check_category, []) #합친다!!

    if request.method == "GET": #get일 경우 세션에서 남아있는녀석을 이용
        Check_category = request.session.get('Check_category', False)
    
    request.session['Check_category'] = Check_category

    print(request.session.get('Check_category', False))

    #default_category = ["한식", "중식", "일식", "양식", "분식", "치킨", "고기", "햄버거"] #기준을 잡아서 session해주려고
    default_category = ["한식", "중식", "일식", "양식", "분식", "치킨", "보쌈", "햄버거", "피자", "돈가스", "떡볶이", "세계음식"]
    #none_category = ["N", "N", "N", "N", "N", "N", "N", "N"]
    none_category = ["N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N"]

    for a in range(0,12):
        if(Check_category[a]==default_category[a]):
            request.session['check'+str(a+1)] = "checked"
        else:
            request.session['check'+str(a+1)] = ""

    #Check_category 안에 선택한 분류들이 리스트로 들어가있음
    if request.method == "GET": #get일 경우 세션에서 남아있는녀석을 이용
        print(request.session.get('lessprice', False))
        print(request.session.get('highprice', False))
        pass
    else:
        request.session['chk_info'] = request.POST.get('chk_info') #현재 위치 채크 했는지 확인후 세션으로 가져오기
        request.session['lessprice'] = request.POST.get('lessprice') #최소가격 가져오기 세션 저장
        request.session['highprice'] = request.POST.get('highprice') #최대가격 가져오기 세션 저장
        request.session['latitude'] = request.POST.get('latitude') #내 위도 세션 저장
        request.session['longitude'] = request.POST.get('longitude') #내 경도 세션 저장
        request.session['radius'] = request.POST.get('radius') #내 반경 세션 저장
        request.session['getpositioncheck'] = "true"
    #request.session.get('lessprice', False)
    #request.session.get('highprice', False)
    
    foodGetit = [] #필터링된 녀석들을 이용해서 리스트에 집어 넣어서 랜덤을 돌리기 위해...
    storeGetit = [] #필터링된 녀석들을 이용해서 리스트에 집어 넣어서 랜덤을 돌리기 위해... 또한 같은 메뉴이름이 나올 경우 가게를 기준으로...
    #me_to_store = find_distance(request.session.get('latitude', False),request.session.get('longitude', False),데이터베이스위도,데이터베이스경도)
    #me_to_store = round(me_to_store * 1000)

    foodmenus=Foodmenu.objects.filter(
        Category__in=request.session.get('Check_category', False),Price__gte=request.session.get('lessprice', False),Price__lte=request.session.get('highprice', False)
    ) # 필터를 

    for foods in foodmenus: #필터링 된녀석을 가지고 랜덤을 돌리기위해서 위도와 경도를 끌고와서 길이 제는 것을 이용
        me_to_store = find_distance(request.session.get('latitude', False),request.session.get('longitude', False),foods.Latitude,foods.Longitude)
        if(me_to_store<=float(request.session.get('radius', False))): #만약 반경안에 들어가면 리스트안에 집어넣는다
            foodGetit.append(foods.Menu)
            storeGetit.append(foods.StoreName)

    print(foodGetit)
    Randomlength = len(foodGetit) #집어넣은 리스트안의 크기를 조사해서 랜덤을 돌릴 값을 결정한다.

            ########## 오류일 경우 #####################

    checkinfo = "설정 완료"  #오류가 났을경우 줄 정보들!!
    content={ 
        "message2":checkinfo,
        "message":"최소가격이 최대가격보다 높을 수 없습니다!!\n가격을 다시 설정해주세요!!\n",
        "chk_info_session":request.session.get('chk_info', ""),
        "latitude_session":request.session.get('latitude', ""),
        "longitude_session":request.session.get('longitude', ""),
        "lessprice_session":request.session.get('lessprice', ""),
        "highprice_session":request.session.get('highprice', ""),
        "radius_session":request.session.get('radius', ""),
        "check_for_checked1":request.session.get('check1', ""),
        "check_for_checked2":request.session.get('check2', ""),
        "check_for_checked3":request.session.get('check3', ""),
        "check_for_checked4":request.session.get('check4', ""),
        "check_for_checked5":request.session.get('check5', ""),
        "check_for_checked6":request.session.get('check6', ""),
        "check_for_checked7":request.session.get('check7', ""),
        "check_for_checked8":request.session.get('check8', ""),
        "check_for_checked9":request.session.get('check9', ""),
        "check_for_checked10":request.session.get('check10', ""),
        "check_for_checked11":request.session.get('check11', ""),
        "check_for_checked12":request.session.get('check12', "")
    }
            
    if(int(request.session.get('lessprice', ""))>int(request.session.get('highprice', ""))): #만약 최소가격이 최대 가격보다 높을 경우
        #if request.session['radius']: #radio 설정된거 계속 가져가기 위해서!
        return render(request, 'Fmenu.html', content)

    elif(Check_category==none_category): #만약 분류를 선택하지 않았을 경우
        #if request.session['radius']: #radio 설정된거 계속 가져가기 위해서!
        content["message"] = "분류를 하나라도 선택해주세요!!\n"
        return render(request, 'Fmenu.html', content)

    elif(Randomlength==0): #만약 그런 메뉴가 없을 경우
        content["message"] = "거리에 그런 메뉴가 없어요..\n 범위를 넓혀보거나 가격을 조정하세요!!\n"
        #if request.session['radius']: #radio 설정된거 계속 가져가기 위해서!
        return render(request, 'Fmenu.html', content)

            ########## 오류일 경우 #####################

    else: ################## 정상작동 #########################
        RandomMenuNum = random.randrange(0,Randomlength)
        SelectedMenu = foodGetit[RandomMenuNum] #랜덤 수에 결정된 수를 리스트의 번째로 그녀석을 가지고 온다.
        SelectedStore = storeGetit[RandomMenuNum] #랜덤 수에 결정된 수를 리스트의 번째로 그녀석을 가지고 온다.
        foodmenus=foodmenus.filter( #랜덤으로 골라진 녀석 한번더 필터!!
            Menu=SelectedMenu,StoreName=SelectedStore
        )

        for selectedfoodurl in foodmenus:
            selectedfoodimg = selectedfoodurl.Foodurl
        #여기에 따로 또 가게 정보를 집어넣기 위해서 나중에 데이터베이스 엑셀을 임포트하고 가져올 것이다 또한 음식의 가게 번호와 가게 정보의 가게 번호랑 같은 것
        #즉 StoreName=SelectedStore로 필터링 한후에 그 필터링된 가게의 모든 것을 가져올 것이다!! 그런후 반복문 돌려서 나타내기!

    storemenus=Store.objects.filter(
        id=SelectedStore
    )

    foodmenus_all=Foodmenu.objects.filter( #모든메뉴 나오게 하기
        StoreName=SelectedStore
    )

    storelocation = Store.objects.get(id=SelectedStore) #get은 하나의 녀석을 가져올때 가져온다 filter는 레코드가 많을경우... 가게 위도 경도 가져오려고
    me_to_store = find_distance(request.session.get('latitude', False),request.session.get('longitude', False),storelocation.Latitude,storelocation.Longitude) #걸린 가게의 나와의 문제
    distance_metter=int(me_to_store*1000) #지도를 위한 정보들
    
    print(distance_metter)

    if(distance_metter>=3200): #지도의 보는 거리를 원에 따라서 설정하려고함!
        zoom=7
    elif(distance_metter>=1600):
        zoom=8
    elif(distance_metter>=800):
        zoom=9
    elif(distance_metter>=400):
        zoom=10
    elif(distance_metter>=200):
        zoom=11
    elif(distance_metter>=100):
        zoom=12
    elif(distance_metter>=50):
        zoom=13
    else:
        zoom=14

    middle_latitude=(float(request.session.get('latitude', False))+float(storelocation.Latitude))/2 #중앙값 구하기 위도 이유는 지도의 중심을 가운데에 놓기 위해서
    middle_longitude=(float(request.session.get('longitude', False))+float(storelocation.Longitude))/2

    print(middle_latitude)
    print(middle_longitude)

    content={
        "selectedfoodimg":selectedfoodimg,
        "foodmenus":foodmenus, #데베쿼리 선택된 메뉴 정보
        "storemenus":storemenus, #데베쿼리 선택된 가게 정보
        "foodmenus_all":foodmenus_all, #상점번호에 맞는 모든 메뉴 데베쿼리
        "me_to_store":distance_metter, #가게 m변환하려고 변수
        "middle_latitude":middle_latitude,
        "middle_longitude":middle_longitude,
        "get_my_latitude":request.session.get('latitude',False),
        "get_my_longitude":request.session.get('longitude',False),
        "store_latitude":storelocation.Latitude,
        "store_longitude":storelocation.Longitude,
        "zoom":zoom
    }

    return render(request, 'Fselect.html', content)    
     #랜덤으로 고른 메뉴까지 조건에 추가 나중에 같은 매뉴가 있을 수가 있는데 그 경우 위에 나중에 식당 번호까지 가져오려고 한다
    
    
    #밑은 나중에 생각했던 것들...
    #print(foodmenus.count()) #쿼리안에 몇개의 값이 있는지 확인

    #RandomMenuId = random.randrange(1,foodmenus.count()) #랜덤번째를 고른다

    #foodmenus=Foodmenu.objects.filter(
    #    (Q(Category=Check_category[0][0])|Q(Category=Check_category[1][0])|Q(Category=Check_category[2][0])|Q(Category=Check_category[3][0])|Q(Category=Check_category[4][0])|Q(Category=Check_category[5][0])|Q(Category=Check_category[6][0])|Q(Category=Check_category[7][0])),Price__gte=request.session.get('lessprice', False),Price__lte=request.session.get('highprice', False)
    #)[RandomMenuId-1:RandomMenuId] #랜덤번째 있는 녀석을 가져온다
    #Q(Category="값")은 OR 이용할때!
    #, 는 And
    #Category__lte="값" 값보다 작거나 같을경우
    #Category__gte="값" 값보다 크거나 같을경우

def Dselect(request):
    Check_category = []
    Check_category.append(request.POST.getlist('check1') or list('N')) #Check는 list로만 가져와지고 체크가 안되어있으면 값이 없어서 찾지를 못함 그래서 or "N"을 함
    Check_category.append(request.POST.getlist('check2') or list('N'))
    Check_category.append(request.POST.getlist('check3') or list('N'))
    Check_category.append(request.POST.getlist('check4') or list('N'))
    Check_category.append(request.POST.getlist('check5') or list('N'))
    Check_category.append(request.POST.getlist('check6') or list('N'))
    Check_category.append(request.POST.getlist('check7') or list('N'))
    Check_category.append(request.POST.getlist('check8') or list('N')) #리스트로 한 이유는 나중에 밑에서 더할때 리스트가 아니면 안더해짐 ㅠ

    Check_category = sum(Check_category, []) #합친다!!

    if request.method == "GET": #get일 경우 세션에서 남아있는녀석을 이용
        Check_category = request.session.get('Check_category', False)
    
    request.session['Check_category'] = Check_category

    print(request.session.get('Check_category', False))

    default_category = ["커피", "라떼", "스무디", "에이드", "차", "버블티", "빵", "아이스크림"] #기준을 잡아서 session해주려고
    none_category = ["N", "N", "N", "N", "N", "N", "N", "N"]

    for a in range(0,8):
        if(Check_category[a]==default_category[a]):
            request.session['check'+str(a+1)] = "checked"
        else:
            request.session['check'+str(a+1)] = ""

    #Check_category 안에 선택한 분류들이 리스트로 들어가있음
    if request.method == "GET": #get일 경우 세션에서 남아있는녀석을 이용
        print(request.session.get('lessprice', False))
        print(request.session.get('highprice', False))
        pass
    else:
        request.session['chk_info'] = request.POST.get('chk_info') #현재 위치 채크 했는지 확인후 세션으로 가져오기
        request.session['lessprice'] = request.POST.get('lessprice') #최소가격 가져오기 세션 저장
        request.session['highprice'] = request.POST.get('highprice') #최대가격 가져오기 세션 저장
        request.session['latitude'] = request.POST.get('latitude') #내 위도 세션 저장
        request.session['longitude'] = request.POST.get('longitude') #내 경도 세션 저장
        request.session['radius'] = request.POST.get('radius') #내 반경 세션 저장
    #request.session.get('lessprice', False)
    #request.session.get('highprice', False)
    
    foodGetit = [] #필터링된 녀석들을 이용해서 리스트에 집어 넣어서 랜덤을 돌리기 위해...
    storeGetit = [] #필터링된 녀석들을 이용해서 리스트에 집어 넣어서 랜덤을 돌리기 위해... 또한 같은 메뉴이름이 나올 경우 가게를 기준으로...
    #me_to_store = find_distance(request.session.get('latitude', False),request.session.get('longitude', False),데이터베이스위도,데이터베이스경도)
    #me_to_store = round(me_to_store * 1000)

    foodmenus=Dessertmenu.objects.filter(
        Category__in=request.session.get('Check_category', False),Price__gte=request.session.get('lessprice', False),Price__lte=request.session.get('highprice', False)
    ) # 필터를 

    for foods in foodmenus: #필터링 된녀석을 가지고 랜덤을 돌리기위해서 위도와 경도를 끌고와서 길이 제는 것을 이용
        me_to_store = find_distance(request.session.get('latitude', False),request.session.get('longitude', False),foods.Latitude,foods.Longitude)
        if(me_to_store<=float(request.session.get('radius', False))): #만약 반경안에 들어가면 리스트안에 집어넣는다
            foodGetit.append(foods.Menu)
            storeGetit.append(foods.StoreName)

    print(foodGetit)
    Randomlength = len(foodGetit) #집어넣은 리스트안의 크기를 조사해서 랜덤을 돌릴 값을 결정한다.

            ########## 오류일 경우 #####################

    checkinfo = "설정 완료"  #오류가 났을경우 줄 정보들!!
    content={ 
        "message2":checkinfo,
        "message":"최소가격이 최대가격보다 높을 수 없습니다!!\n가격을 다시 설정해주세요!!\n",
        "chk_info_session":request.session.get('chk_info', ""),
        "latitude_session":request.session.get('latitude', ""),
        "longitude_session":request.session.get('longitude', ""),
        "lessprice_session":request.session.get('lessprice', ""),
        "highprice_session":request.session.get('highprice', ""),
        "radius_session":request.session.get('radius', ""),
        "check_for_checked1":request.session.get('check1', ""),
        "check_for_checked2":request.session.get('check2', ""),
        "check_for_checked3":request.session.get('check3', ""),
        "check_for_checked4":request.session.get('check4', ""),
        "check_for_checked5":request.session.get('check5', ""),
        "check_for_checked6":request.session.get('check6', ""),
        "check_for_checked7":request.session.get('check7', ""),
        "check_for_checked8":request.session.get('check8', "")
    }
            
    if(request.session.get('lessprice', "")>request.session.get('highprice', "")): #만약 최소가격이 최대 가격보다 높을 경우
        #if request.session['radius']: #radio 설정된거 계속 가져가기 위해서!
        return render(request, 'Dmenu.html', content)

    elif(Check_category==none_category): #만약 분류를 선택하지 않았을 경우
        #if request.session['radius']: #radio 설정된거 계속 가져가기 위해서!
        content["message"] = "분류를 하나라도 선택해주세요!!\n"
        return render(request, 'Dmenu.html', content)

    elif(Randomlength==0): #만약 그런 메뉴가 없을 경우
        content["message"] = "거리에 그런 메뉴가 없어요..\n 범위를 넓혀보거나 가격을 조정하세요!!\n"
        #if request.session['radius']: #radio 설정된거 계속 가져가기 위해서!
        return render(request, 'Dmenu.html', content)

            ########## 오류일 경우 #####################

    else: ################## 정상작동 #########################
        RandomMenuNum = random.randrange(0,Randomlength)
        SelectedMenu = foodGetit[RandomMenuNum] #랜덤 수에 결정된 수를 리스트의 번째로 그녀석을 가지고 온다.
        SelectedStore = storeGetit[RandomMenuNum] #랜덤 수에 결정된 수를 리스트의 번째로 그녀석을 가지고 온다.
        foodmenus=foodmenus.filter( #랜덤으로 골라진 녀석 한번더 필터!!
            Menu=SelectedMenu,StoreName=SelectedStore
        )

        for selectedfoodurl in foodmenus:
            selectedfoodimg = selectedfoodurl.Foodurl
        #여기에 따로 또 가게 정보를 집어넣기 위해서 나중에 데이터베이스 엑셀을 임포트하고 가져올 것이다 또한 음식의 가게 번호와 가게 정보의 가게 번호랑 같은 것
        #즉 StoreName=SelectedStore로 필터링 한후에 그 필터링된 가게의 모든 것을 가져올 것이다!! 그런후 반복문 돌려서 나타내기!

    storemenus=Store.objects.filter(
        id=SelectedStore
    )

    foodmenus_all=Dessertmenu.objects.filter( #모든메뉴 나오게 하기
        StoreName=SelectedStore
    )

    storelocation = Store.objects.get(id=SelectedStore) #get은 하나의 녀석을 가져올때 가져온다 filter는 레코드가 많을경우... 가게 위도 경도 가져오려고
    me_to_store = find_distance(request.session.get('latitude', False),request.session.get('longitude', False),storelocation.Latitude,storelocation.Longitude) #걸린 가게의 나와의 문제
    distance_metter=int(me_to_store*1000) #지도를 위한 정보들

    print(distance_metter)

    if(distance_metter>=3200): #지도의 보는 거리를 원에 따라서 설정하려고함!
        zoom=7
    elif(distance_metter>=1600):
        zoom=8
    elif(distance_metter>=800):
        zoom=9
    elif(distance_metter>=400):
        zoom=10
    elif(distance_metter>=200):
        zoom=11
    elif(distance_metter>=100):
        zoom=12
    elif(distance_metter>=50):
        zoom=13
    else:
        zoom=14

    middle_latitude=(float(request.session.get('latitude', False))+float(storelocation.Latitude))/2 #중앙값 구하기 위도 이유는 지도의 중심을 가운데에 놓기 위해서
    middle_longitude=(float(request.session.get('longitude', False))+float(storelocation.Longitude))/2

    content={
        "selectedfoodimg":selectedfoodimg,
        "foodmenus":foodmenus, #데베쿼리 선택된 메뉴 정보
        "storemenus":storemenus, #데베쿼리 선택된 가게 정보
        "foodmenus_all":foodmenus_all, #상점번호에 맞는 모든 메뉴 데베쿼리
        "me_to_store":distance_metter, #가게 m변환하려고 변수
        "middle_latitude":middle_latitude,
        "middle_longitude":middle_longitude,
        "get_my_latitude":request.POST.get('latitude'),
        "get_my_longitude":request.POST.get('longitude'),
        "store_latitude":storelocation.Latitude,
        "store_longitude":storelocation.Longitude,
        "zoom":zoom
    }

    return render(request, 'Dselect.html', content)

def Dmenu(request):
    if request.method=="POST":
        content = {
        "radius_session":request.session.get('radius'),
        "lessprice_session":request.session.get('lessprice'),
        "highprice_session":request.session.get('highprice'),
        "latitude_session":request.session.get('latitude', False),
        "longitude_session":request.session.get('longitude', False)
        }
        return render(request, 'Dmenu.html', content)

    request.session['radius'] = 0.7
    request.session['lessprice'] = 0
    request.session['highprice'] = 7000
    content = {
        "radius_session":request.session.get('radius'),
        "lessprice_session":request.session.get('lessprice'),
        "highprice_session":request.session.get('highprice'),
        "latitude_session":request.session.get('latitude', False),
        "longitude_session":request.session.get('longitude', False)
    }
    return render(request, 'Dmenu.html', content)

def find_distance(mylatitude, mylongitude, otherlatitude, otherlongitude): #거리구하는 함수
    R = 6373.0
    lat1 = radians(float(mylatitude)) #나의 위도
    lon1 = radians(float(mylongitude)) #나의 경도
    lat2 = radians(float(otherlatitude)) #상대 위도
    lon2 = radians(float(otherlongitude)) #상대 경도

    dlon = lon2 - lon1 #계산식
    dlat = lat2 - lat1 #계산식

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2 #계산식
    c = 2 * atan2(sqrt(a), sqrt(1 - a))  #계산식
    distance = R * c #거기 까지 거리 도출

    return distance