from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from food.models import Store
import string
import random


# Create your views here.
def signup(request):
    if request.method == "GET": #GET으로 가져와야 처음 시작할때 초기화 같은 것을 한다고 생각하면 된다!!
        request.session['count']=0
        request.session['readonly']=""

    if request.method == "POST":
        request.session['username'] = request.POST.get('username')
        request.session['password1'] = request.POST.get('password1')
        request.session['password2'] = request.POST.get('password2')
        request.session['ownername'] = request.POST.get('ownername')
        request.session['ownerphone1'] = str(request.POST.get("ownerphone1"))
        request.session['ownerphone2'] = str(request.POST.get("ownerphone2"))
        request.session['ownerphone3'] = str(request.POST.get("ownerphone3"))
        request.session['storename'] = request.POST.get('storename')
        request.session['storephone1'] = str(request.POST.get("storephone1"))
        request.session['storephone2'] = str(request.POST.get("storephone2"))
        request.session['storephone3'] = str(request.POST.get("storephone3"))
        request.session['storeaddress'] = request.POST.get('storeaddress')
        request.session['storelatitude'] = float(request.POST.get('storelatitude'))
        request.session['storelongitude'] = float(request.POST.get('storelongitude'))

        content = {
            "username":request.session.get('username', ""),
            "password1":request.session.get('password1', ""),
            "password2":request.session.get('password2', ""),
            "ownername":request.session.get('ownername', ""),
            "ownerphone1":request.session.get('ownerphone1', ""),
            "ownerphone2":request.session.get('ownerphone2', ""),
            "ownerphone3":request.session.get('ownerphone3', ""),
            "storename":request.session.get('storename', ""),
            "storephone1":request.session.get('storephone1', ""),
            "storephone2":request.session.get('storephone2', ""),
            "storephone3":request.session.get('storephone3', ""),
            "storeaddress":request.session.get('storeaddress', ""),
            "storelatitude":request.session.get('storelatitude', ""),
            "storelongitude":request.session.get('storelongitude', ""),
            "readonly":request.session.get('readonly', ""),
        }

    if request.method == "POST" and 'signupforme' in request.POST:
        if request.session.get('count', "0") != 1: #중복검사를 하지 않았을 경우!!
            request.session['count'] = 0
            request.session['readonly']=""
            content["checkthesame"]="아이디 중복확인을 하세요!"
            return render(request, "signup.html", content)

        if request.POST["password1"]==request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"]
            )
            OwnerName = request.POST["ownername"]
            OwnerPhone = str(request.POST["ownerphone1"]) + "-" + str(request.POST["ownerphone2"]) + "-" + str(request.POST["ownerphone3"])  #나중에 하나하나씩 붙이는것 생각 XXXX-XXXX-XXXX 느낌
            StoreName = request.POST["storename"]
            StorePhone = str(request.POST["storephone1"]) + "-" + str(request.POST["storephone2"]) + "-" + str(request.POST["storephone3"])
            StoreAddress = request.POST["storeaddress"]
            Latitude = float(request.POST["storelatitude"])
            Longitude = float(request.POST["storelongitude"])

            profile = Profile( #사장님 회원가입 저장
                user=user,
                OwnerName=OwnerName,
                OwnerPhone=OwnerPhone,
                StoreName=StoreName,
                StorePhone=StorePhone,
                StoreAddress=StoreAddress,
                Latitude=Latitude,
                Longitude=Longitude,
                OwnerType=""
                )
            profile.save()

            store = Store( #food앱에 있는 모델의 가게 테이블에 또 저장
            StoreName=StoreName,
            StoreAddress=StoreAddress,
            StorePhone=StorePhone,
            Latitude=Latitude,
            Longitude=Longitude
            )
            store.save()

            del request.session['username'] # 다 끝나고 session 삭제!!!!
            del request.session['password1'] # 다 끝나고 session 삭제!!!!
            del request.session['password2'] # 다 끝나고 session 삭제!!!!
            del request.session['ownername'] # 다 끝나고 session 삭제!!!!
            del request.session['ownerphone1'] # 다 끝나고 session 삭제!!!!
            del request.session['ownerphone2'] # 다 끝나고 session 삭제!!!!
            del request.session['ownerphone3'] # 다 끝나고 session 삭제!!!!
            del request.session['storename'] # 다 끝나고 session 삭제!!!!
            del request.session['storephone1'] # 다 끝나고 session 삭제!!!!
            del request.session['storephone2'] # 다 끝나고 session 삭제!!!!
            del request.session['storephone3'] # 다 끝나고 session 삭제!!!!
            del request.session['storeaddress'] # 다 끝나고 session 삭제!!!!
            del request.session['storelatitude'] # 다 끝나고 session 삭제!!!!
            del request.session['storelongitude'] # 다 끝나고 session 삭제!!!!
            del request.session['readonly'] # 다 끝나고 session 삭제!!!!
            del request.session['count'] # 다 끝나고 session 삭제!!!!

            auth.login(request, user)
            
            return redirect('Ownerpage')

        else:
            content["error"]="비밀번호와 비밀번호 확인이 일치하지 않습니다."
            return render(request, "signup.html", content)

    elif request.method == "POST" and 'checksame' in request.POST:
        if len(request.POST.get('username'))<7:
            request.session['count'] = 0
            content["usernameerror"]="아이디는 7글자 이상이어야 됩니다!"
            return render(request, "signup.html", content)

        profile=Profile.objects.filter( #사장님 정보를 가져오기 위해서
            user__username=request.POST["username"]
        )

        if profile:
            request.session['count'] = 0
            content["usernameerror"]="중복한 아이디가 존재 합니다!"
        else:
            request.session['count'] = 1
            request.session['readonly']="readonly"
            content["readonly"]=request.session.get('readonly', "")
            content["usernameerror"]="사용가능한 아이디 입니다!"
        return render(request, "signup.html", content)
    return render(request, "signup.html")


def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/Ownerpage')
        else:
            return render(request, 'login.html', {"error":"사용자 아이디 혹은 비밀번호가 잘못입력되었습니다!"})
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('/')
    return render(request, 'login.html')

def findpassword(request): #비밀번호 찾기
    if request.method=="POST":
        user=User.objects.get(
            username=request.POST.get('userid')
        )

        phonenumber=str(request.POST.get("ownerphone1")) + "-" + str(request.POST.get("ownerphone2")) + "-" + str(request.POST.get("ownerphone3"))
        
        finduser=Profile.objects.get(
           user__username=request.POST.get('userid'), #다른 곳을 참조할때는 가져올라면 __해야되는구나!!
           OwnerName=request.POST.get('ownername'),
           OwnerPhone=phonenumber
        )
        if finduser:
            _LENGTH = 8 # 몇자리?
            string_pool = string.digits # "0123456789"
            result = "" # 결과 값
            for i in range(_LENGTH) : # 랜덤한 하나의 숫자를 뽑아서, 문자열 결합을 한다.
                result += random.choice(string_pool)
            user.set_password(result)
            user.save()
            return render(request, 'findpassword.html',{"error":"비밀번호는 '"+str(result)+"'로 수정되었습니다!"})
        else:
            return render(request, 'findpassword.html',{"error":"그런 정보의 사용자는 없습니다. 다시 정보를 확인해주세요!"})
    return render(request, 'findpassword.html')

def confirming(request):
    return render(request, 'confirming.html')