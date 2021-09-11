import base64

from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, Http404
from fontmaker.forms import *
from .models import Proj, HUser, OwnerShip
import os, time


def index(request):
    """
    처음 보게 되는 홈페이지
    """
    my_proj_names = []  # 프로젝트 불러오기에 자기 프로젝트 이름 띄우기 용
    if request.user.is_authenticated:
        huser = HUser.objects.filter(user=request.user)[0]
        ownerships = OwnerShip.objects.filter(user=huser)

        for ownership in ownerships:
            my_proj_names.append(ownership.proj.name)

    context = {
        'my_proj_names': my_proj_names,
    }

    return render(request, 'base_generic.html', context)


def new_project(request):
    if request.method == "POST" and request.user.is_authenticated:  # 일단 로그인해야 가능하게 둠, 비로그인 설정 필요
        form = ProjForm(request.POST)
        if form.is_valid():
            proj = form.save()
            proj.initialSetting()
            proj.save()

            owner_ship = OwnerShip()
            owner_ship.proj = proj
            huser = HUser.objects.filter(user=request.user)[0]
            owner_ship.user = huser
            owner_ship.level = 2
            owner_ship.save()

            return redirect('draw', pk=proj.id)
    return redirect('/')


def exist_project(request):  # 계정과 프로젝트 연결 필요
    if request.method == "POST":
        project_name = request.POST.get('name')

        proj = Proj.objects.filter(name=project_name) if project_name else None
        huser = HUser.objects.filter(user=request.user) if request.user.is_authenticated else None
        if not (proj or huser):
            return redirect('/')

        ownership = OwnerShip.objects.filter(proj=proj[0], user=huser[0])

        if ownership:
            return redirect('draw', pk=proj[0].id)
        else:
            return redirect('/')  # 알림 띄우고 싶지만 잘 모르겠음


def undone_chars(request, pk):
    proj = Proj.objects.filter(id=pk)[0]

    if proj:
        undones = proj.unDone().split()

        return JsonResponse({'data': undones})


def draw(request, pk):
    """
    폰트 그리는 페이지
    """
    remains_ascii = 0  # 97
    remains_hangul = 0  # 11172
    remains_jamo = 0  # 67
    context = {
        'remains_ascii': remains_ascii,
        'remains_hangul': remains_hangul,
        'remains_jamo': remains_jamo,
    }
    return render(request, 'draw_font.html', context)


@csrf_exempt
def draw_save_img(request, pk):
    data = request.POST.__getitem__('data')
    letter = request.POST.__getitem__('letter')
    data = data[22:]  # 앞에 base64 아닌부분 제거

    proj = Proj.objects.filter(id=pk)[0]
    filename = './fontmaker/ff_projects/{}/{}'.format(proj.name, letter + '.png')

    image = open(filename, "wb")
    image.write(base64.b64decode(data))
    image.close()

    answer = {'category': 'notyet'}

    proj.setImageOf(filename)
    os.remove(filename)

    return JsonResponse(answer)


def draw_load_img(request, pk, letter):
    proj = Proj.objects.filter(id=pk)[0]
    image = proj.getImageOf(letter, '.png')
    try:
        imagef = open(image, 'rb')
    except:
        raise Http404
    res = HttpResponse(imagef.read(), content_type="image/png")
    res['Cache-Control']='no-cache, no-store, must-revalidate'
    imagef.close()
    os.remove(image)
    # print('load ' + letter)
    return res
    

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인

            # HUser 연결, name 저렇게 하면되나?
            huser = HUser()
            huser.user = user
            huser.name = username
            huser.ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
            huser.save()

            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})
