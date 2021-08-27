import base64

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse
from fontmaker.forms import UserForm
import os


def index(request):
    """처음 보게 되는 홈페이지"""
    return render(request, 'base_generic.html')


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
    data = data[22:]  # 앞에 base64 아닌부분 제거

    path = str(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/image/'))
    filename = 'image.png'

    image = open(path + filename, "wb")
    image.write(base64.b64decode(data))
    image.close()

    answer = {'category': 'notyet'}
    return JsonResponse(answer)


def draw_load_img(request, pk):
    path = str(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/image/'))
    filename = 'image.png'

    image = open(path + filename, "rb")
    return FileResponse(image)


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
