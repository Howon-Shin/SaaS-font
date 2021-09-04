import base64

from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, Http404
from fontmaker.forms import *
from .models import Proj
import os, time


def index(request):
    """
    처음 보게 되는 홈페이지
    """
    return render(request, 'base_generic.html')


def new_project(request):
    if request.method == "POST":
        form = ProjForm(request.POST)
        if form.is_valid():
            proj = form.save()
            proj.initialSetting()
            proj.save()
            return redirect('draw', pk=proj.id)
    return redirect('/')


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
    res = HttpResponse(imagef.read(), content_type="application/octet-stream")
    res['Cache-Control']='no-cache, no-store, must-revalidate'
    imagef.close()
    os.remove(image)
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
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})
