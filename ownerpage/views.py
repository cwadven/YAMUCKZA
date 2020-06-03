from django.shortcuts import render, redirect
from food.models import Foodmenu, Store
from login.models import Profile
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.hashers import check_password

def ownerpage(request):

    if request.method=='GET':
        if str(request.user)=="AnonymousUser":
            return redirect('/')
        else:
            pass

    user = User.objects

    request.session['category'] = request.POST.get("category")

    profile=Profile.objects.filter( #사장님 정보를 가져오기 위해서
        user=request.user
    )

    for profiles in profile: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storephone = profiles.StorePhone
        ownertype = profiles.OwnerType #동의 확인

    if request.method=='GET': #동의된 사람이 아니면 나가라!!
        if ownertype!="1":
            return redirect('Confirming')
        else:
            pass

    store=Store.objects.filter( #사장님의 전화번호를 통해 전화번호에 맞는 모든 정보가져오기
        StorePhone=storephone
    )

    for stores in store: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storeid = stores.id
        storeLatitude = stores.Latitude
        storeLongitude = stores.Longitude

    foodmenu = Foodmenu.objects.filter( #가게의 id를 이용해서 필터링
        StoreName=storeid
    )

    ############################################## 밑은 메뉴 추가 기능
    default_category = ["한식", "중식", "일식", "양식", "분식", "치킨", "고기", "햄버거"]

    if(request.method=='POST'):
        for a in foodmenu: #같은 메뉴 있을 경우 오류 나오게 하기!!
            a.Menu=a.Menu.replace(" ", "")
            space_confirm=request.POST.get("Cmenu").replace(" ", "") # 가져옴 띄어쓰기는 없앰
            if a.Menu == space_confirm:
                content = {
                    "profile":profile,
                    "foodmenu":foodmenu,
                    "store":store,
                    "default_category":default_category,
                    "category":request.session.get('category', ''),
                    "error":"같은 메뉴가 존재합니다!!"
                }
                return render(request, "ownerpage.html", content)

    if(request.method=='POST'):#POST이면서 같은 메뉴가 아닐경우 데이터베이스 foodmenu에 저장
        createmenu=Foodmenu()
        createmenu.Menu=request.POST.get("Cmenu")
        createmenu.Price=request.POST.get("Cprice")
        createmenu.Foodurl=request.POST.get("Cpicture").replace(" ", "") #가져옴 띄어쓰기는 없앰
        createmenu.StoreName=storeid
        createmenu.Latitude=storeLatitude
        createmenu.Longitude=storeLongitude
        createmenu.Category=request.POST.get("category")
        createmenu.save()

        content = {
        "profile":profile,
        "foodmenu":foodmenu,
        "store":store,
        "default_category":default_category,
        "category":request.session.get('category', '')
        }
        return render(request, "ownerpage.html", content)

    content = {
        "profile":profile,
        "foodmenu":foodmenu,
        "store":store,
        "default_category":default_category,
        "category":request.session.get('category', '')
    }

    return render(request, "ownerpage.html", content)

def ownerupdate(request): #회원정보 수정
    request.session['category'] = request.POST.get("category")
    default_category = ["한식", "중식", "일식", "양식", "분식", "치킨", "고기", "햄버거"]
    user = User.objects

    profile=Profile.objects.filter( #사장님 정보를 가져오기 위해서
        user=request.user
    )

    for profiles in profile: #필터링 된 녀석의 값을 필터링에 쓰는 것과 input에 값이 넣어져있는 상태로 만들기 위해서
        storephone = profiles.StorePhone
        ownerphone = profiles.OwnerPhone
        ownername = profiles.OwnerName
        ownerstorename= profiles.StoreName
        ownerstoreaddress = profiles.StoreAddress
        ownerlatitude = profiles.Latitude
        ownerlongitude = profiles.Longitude

    storephone_slice = storephone.split('-')  # 전화번호 쪼개기 - 구간별로
    ownerphone_slice = ownerphone.split('-')

    store=Store.objects.filter( #사장님의 전화번호를 통해 전화번호에 맞는 모든 정보가져오기
        StorePhone=storephone
    )

    for stores in store: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storeid = stores.id
        storeLatitude = stores.Latitude
        storeLongitude = stores.Longitude

    foodmenu = Foodmenu.objects.filter( #가게의 id를 이용해서 필터링
        StoreName=storeid
    )
    if request.method == "POST":
        OwnerPhone = str(request.POST.get("ownerphone1")) + "-" + str(request.POST.get("ownerphone2")) + "-" + str(request.POST.get("ownerphone3"))
        StorePhone = str(request.POST.get("store_phone1")) + "-" + str(request.POST.get("store_phone2")) + "-" + str(request.POST.get("store_phone3"))
        OwnerName = request.POST.get("ownername")
        StoreName = request.POST.get("store_name")
        StoreAddress = request.POST.get("store_address")
        StoreLatitude = float(request.POST.get("store_latitude"))
        StoreLongitude = float(request.POST.get("store_longitude"))

        for update_profile in profile:
            update_profile.OwnerName=OwnerName
            update_profile.StorePhone=StorePhone
            update_profile.OwnerPhone=OwnerPhone
            update_profile.StoreName=StoreName
            update_profile.StoreAddress=StoreAddress
            update_profile.Latitude=StoreLatitude
            update_profile.Longitude=StoreLongitude
            update_profile.save()

        for update_menu in foodmenu:
            update_menu.Latitude = StoreLatitude #사용자 기준으로 필터링된 음식 id를 기준으로 가져옴
            update_menu.Longitude = StoreLongitude # Menu 수정 id를 기준으로 가져옴
            update_menu.save()

        for update_store in store:
            update_store.StoreName = StoreName
            update_store.StorePhone = StorePhone
            update_store.StoreAddress = StoreAddress
            update_store.Latitude = StoreLatitude #사용자 기준으로 필터링된 음식 id를 기준으로 가져옴
            update_store.Longitude = StoreLongitude # Menu 수정 id를 기준으로 가져옴
            update_store.save()

        return redirect('/Ownerpage')
        
    content = {
        "profile":profile,
        "foodmenu":foodmenu,
        "store":store,
        "storephone1":storephone_slice[0],
        "storephone2":storephone_slice[1],
        "storephone3":storephone_slice[2],
        "ownerphone1":ownerphone_slice[0],
        "ownerphone2":ownerphone_slice[1],
        "ownerphone3":ownerphone_slice[2],
        "ownername":ownername,
        "ownerstorename":ownerstorename,
        "ownerstoreaddress":ownerstoreaddress,
        "ownerlatitude":ownerlatitude,
        "ownerlongitude":ownerlongitude,
        "default_category":default_category,
        "category":request.session.get('category', '')
    }

    return render(request, "ownerupdate.html", content)

def ownerpassword(request):
    if request.method == 'POST':
        current_password = request.POST.get("currentpw")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("changepw1")
            password_confirm = request.POST.get("changepw2")
            if new_password == password_confirm: #새로운 비밀번호와 비밀번호 확인비교
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect('/Ownerpage')
            else:
                return render(request, "ownerpassword.html", {"error":"새로운 비밀번호와 비밀번호 확인이 다릅니다!"})
        else:
            return render(request, "ownerpassword.html", {"error1":"현재 비밀번호가 다릅니다!"})
    return render(request, "ownerpassword.html")

def ownerdelete(request):

    user = User.objects

    profile=Profile.objects.filter( #사장님 정보를 가져오기 위해서
        user=request.user
    )

    for profiles in profile: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storephone = profiles.StorePhone

    store=Store.objects.filter( #사장님의 전화번호를 통해 전화번호에 맞는 모든 정보가져오기
        StorePhone=storephone
    )

    for stores in store: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storeid = stores.id
        storeLatitude = stores.Latitude
        storeLongitude = stores.Longitude

    foodmenu = Foodmenu.objects.filter( #가게의 id를 이용해서 필터링
        StoreName=storeid
    )

    if request.method == 'POST':
        if request.POST.get("confirm") == "탈퇴": #만약 탈퇴이면 필터링된 녀석들 전부 삭제를 한다!!
            foodmenu.delete() #모든 메뉴 삭제
            store.delete() #가게 정보 삭제
            request.user.delete() #유저 삭제하면 자동적으로 참조되서 Profile은 삭제됨          
            return redirect('/')
        else:
            return render(request, "ownerdelete.html", {"error":"오타입니다. '탈퇴'를 입력해주세요."})
    return render(request, "ownerdelete.html")

def updateMenu(request):
    request.session['category'] = request.POST.get("category")
    default_category = ["한식", "중식", "일식", "양식", "분식", "치킨", "고기", "햄버거"]
    user = User.objects

    profile=Profile.objects.filter( #사장님 정보를 가져오기 위해서
        user=request.user
    )

    for profiles in profile: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storephone = profiles.StorePhone

    store=Store.objects.filter( #사장님의 전화번호를 통해 전화번호에 맞는 모든 정보가져오기
        StorePhone=storephone
    )

    for stores in store: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storeid = stores.id
        storeLatitude = stores.Latitude
        storeLongitude = stores.Longitude

    foodmenu = Foodmenu.objects.filter( #가게의 id를 이용해서 필터링
        StoreName=storeid
    )

    for update in foodmenu:
        updateMenu = Foodmenu.objects.get(id=update.id) #사용자 기준으로 필터링된 음식 id를 기준으로 가져옴
        updateMenu.Menu = request.POST.get("a"+str(update.id)) # Menu 수정 id를 기준으로 가져옴
        updateMenu.Price = request.POST.get("b"+str(update.id)) # 가격 수정 id를 기준으로 가져옴
        updateMenu.Foodurl = request.POST.get("d"+str(update.id)).replace(" ", "") #사진 수정 id를 기준으로, 가져옴 띄어쓰기는 없앰
        updateMenu.Category = request.POST.get("c"+str(update.id)) # 분류 수정 id를 기준으로 가져옴
        updateMenu.save()

    content = {
        "profile":profile,
        "foodmenu":foodmenu,
        "store":store,
        "default_category":default_category,
        "category":request.session.get('category', '')
    }

    return render(request, "ownerpage.html", content)

def deleteMenu(request):
    request.session['category'] = request.POST.get("category")
    default_category = ["한식", "중식", "일식", "양식", "분식", "치킨", "고기", "햄버거"]
    user = User.objects

    profile=Profile.objects.filter( #사장님 정보를 가져오기 위해서
        user=request.user
    )

    for profiles in profile: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storephone = profiles.StorePhone

    store=Store.objects.filter( #사장님의 전화번호를 통해 전화번호에 맞는 모든 정보가져오기
        StorePhone=storephone
    )

    for stores in store: #필터링 된 녀석의 값을 필터링 하기 위해서 변수에 집어 넣어준다
        storeid = stores.id
        storeLatitude = stores.Latitude
        storeLongitude = stores.Longitude

    foodmenu = Foodmenu.objects.filter( #가게의 id를 이용해서 필터링
        StoreName=storeid
    )

    for delete in foodmenu:
        a = request.POST.get("a"+str(delete.id))
        if(delete.Menu==a): #int로 안바꿔져서 차라리 id를 str로 바꿈
            print("a")
            deleteMenu = Foodmenu.objects.get(id=delete.id)
            deleteMenu.delete()
            break

    content = {
        "profile":profile,
        "foodmenu":foodmenu,
        "store":store,
        "default_category":default_category,
        "category":request.session.get('category', '')
    }

    return render(request, "ownerpage.html", content)