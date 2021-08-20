from django.shortcuts import render


def intro(request):
    """처음 보게 되는 홈페이지"""
    return render(request, 'base_generic.html')


def draw(request, pk):
    remains_askii = 0  # 97
    remains_hangul = 0  # 11172
    remains_jamo = 0  # 67
    context = {
        'remains_askii': remains_askii,
        'remains_hangul': remains_hangul,
        'remains_jamo': remains_jamo,
    }
    return render(request, 'draw_font.html', context)
