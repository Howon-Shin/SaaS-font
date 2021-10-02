import base64

from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, Http404, HttpResponseForbidden
from fontmaker.forms import *
from .models import Proj, HUser, OwnerShip
import os, time, shutil


def index(request, isWrong=False):
    """
    처음 보게 되는 홈페이지
    """
    my_proj_names = []  # 프로젝트 불러오기에 자기 프로젝트 이름 띄우기 용
    if request.user.is_authenticated:
        my_proj_names = request.user.handle.allProj()

    context = {
        'my_proj_names': my_proj_names,
        'wrong_access' : isWrong
    }

    return render(request, 'base_generic.html', context)


def new_project(request):
    if request.method == "POST" and request.user.is_authenticated:  # 일단 로그인해야 가능하게 둠, 비로그인 설정 필요
        form = ProjForm(request.POST)
        if form.is_valid():
            proj = form.save()
            proj.initialSetting()
            proj.save()

            OwnerShip(proj=proj, user=request.user.handle, level=2).save()

            return redirect('draw', pk=proj.id)
    return redirect('/')


def exist_project(request):  # 계정과 프로젝트 연결 필요
    if request.method == "POST":
        project_name = request.POST.get('name')

        proj = Proj.objects.get(name=project_name) if project_name else None
        huser = request.user.handle if request.user.is_authenticated else None
        if not (proj or huser):
            return redirect('/')

        ownership = OwnerShip.objects.filter(proj=proj, user=huser)

        if ownership:
            return redirect('draw', pk=proj.id)
        else:
            return index(request, True)  # 알림 띄우고 싶지만 잘 모르겠음


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
    try:
        proj = Proj.objects.get(id=pk)
    except:
        return HttpResponseForbidden()
    huser = request.user.handle
    owner_level = OwnerShip.objects.filter(proj=proj, user=huser)[0].level

    cur_ownerships = OwnerShip.objects.filter(proj=proj).exclude(user=huser)
    proj_members = {ownership.user.name: ownership.level for ownership in cur_ownerships}

    context = {
        'remains_ascii': remains_ascii,
        'remains_hangul': remains_hangul,
        'remains_jamo': remains_jamo,
        'owner_level': owner_level,
        'members': proj_members,
    }
    return render(request, 'draw_font.html', context)


@csrf_exempt
def draw_save_img(request, pk):
    data = request.POST['data']
    letter = request.POST['letter']
    extension = request.POST['format']
    data = data[22:]  # 앞에 base64 아닌부분 제거

    proj = Proj.objects.filter(id=pk)[0]
    proj.setImageOf(data, letter, extension)
    print(letter)

    return JsonResponse({})


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

            # HUser 연결
            huser = HUser(user=user, name=username)
            huser.ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
            huser.save()

            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})


def delete_project(request, pk):
    if request.method == "POST":
        proj = Proj.objects.get(id=pk)
        huser = request.user.handle
        is_manager = OwnerShip.objects.filter(proj=proj, user=huser)[0].level

        if request.user.is_authenticated and is_manager == 2:
            # 프로젝트 및 프로젝트 폴더 삭제
            proj.delete()
            proj_path = './fontmaker/ff_projects/{}'.format(proj.name)
            shutil.rmtree(proj_path)

            return redirect('index')  # 왜인지 모르겠지만 작동안함, ajax에 임시로 redirect기능 넣어둠

    return JsonResponse({'right': 'no'})


def exit_project(request, pk):
    if request.method == "POST":
        proj = Proj.objects.get(id=pk)
        huser = request.user.handle
        ownership = OwnerShip.objects.filter(proj=proj, user=huser)[0]

        if request.user.is_authenticated:
            ownership.delete()

            successor = ''
            if ownership.level == 2:
                proj_ownerships = OwnerShip.objects.filter(proj=proj).order_by("-level")

                if proj_ownerships:
                    # 다음으로 렙 높은 사람한테 양도
                    proj_ownerships[0].level = 2
                    proj_ownerships[0].save()
                    successor = proj_ownerships[0].user.name
                else:
                    # 프로젝트 및 프로젝트 폴더 삭제
                    proj.delete()
                    proj_path = './fontmaker/ff_projects/{}'.format(proj.name)
                    shutil.rmtree(proj_path)

                return JsonResponse({'successor': successor})

        return JsonResponse({'error': 'noerror'})

    return JsonResponse({'right': 'no'})


def invite_member(request, pk):
    if request.method == "POST":
        proj = Proj.objects.get(id=pk)
        huser = request.user.handle
        owner_level = OwnerShip.objects.filter(proj=proj, user=huser)[0].level

        member_ID = request.POST.__getitem__('memberID')
        member = HUser.objects.filter(name=member_ID)

        if request.user.is_authenticated and owner_level >= 1:
            if member and (member[0] != request.user.handle):
                OwnerShip(proj=proj, user=member[0], level=0).save()
                return JsonResponse({'error': 'noerror'})
            elif member[0] == request.user.handle:
                return JsonResponse({'error': 'selfinvite'})
            else:
                return JsonResponse({'error': 'nomember'})

    return JsonResponse({'error': 'noright'})


def manage_member(request, pk):
    if request.method == "POST":
        proj = Proj.objects.get(id=pk)
        huser = request.user.handle
        owner_level = OwnerShip.objects.filter(proj=proj, user=huser)[0].level

        member_ID = request.POST.__getitem__('memberID')
        level = eval(request.POST.__getitem__('level'))
        member = HUser.objects.get(name=member_ID)
        member_ownership = OwnerShip.objects.filter(proj=proj, user=member)[0]

        if request.user.is_authenticated and owner_level >= 2:
            if member_ownership.level == level:
                return JsonResponse({'error': 'samelevel'})
            elif 0 <= level <= 1:
                member_ownership.level = level
                member_ownership.save()
                return JsonResponse({'error': 'noerror'})
            else:
                return JsonResponse({'error': 'nolevel'})

    return JsonResponse({'error': 'noright'})


def fire_member(request, pk):
    if request.method == "POST":
        proj = Proj.objects.get(id=pk)
        huser = request.user.handle
        owner_level = OwnerShip.objects.filter(proj=proj, user=huser)[0].level

        member_ID = request.POST.__getitem__('memberID')
        member = HUser.objects.get(name=member_ID)
        member_ownership = OwnerShip.objects.get(proj=proj, user=member)

        if huser == member:
            return JsonResponse({'error': 'noright'})

        if request.user.is_authenticated and owner_level >= 2:
            if member:
                member_ownership.delete()
                return JsonResponse({'error': 'noerror'})
            else:
                return JsonResponse({'error': 'nomember'})

    return JsonResponse({'error': 'noright'})
