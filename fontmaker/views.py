from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from fontmaker.forms import UserForm


def index(request):
    """처음 보게 되는 홈페이지"""
    return render(request, 'base_generic.html')


def draw(request, pk):
    remains_ascii = 0  # 97
    remains_hangul = 0  # 11172
    remains_jamo = 0  # 67
    context = {
        'remains_ascii': remains_ascii,
        'remains_hangul': remains_hangul,
        'remains_jamo': remains_jamo,
    }
    return render(request, 'draw_font.html', context)


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
