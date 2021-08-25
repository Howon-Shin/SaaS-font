import re
import xml.etree.ElementTree as eTree
from math import sqrt

pathCleaver=re.compile(r'[A-Za-z]|-?[0-9]+')
# 함수들 인수: 입력 좌표값 n개, 좌표 리스트(2차원)
# 리턴값: 특성리스트

def isNumOrDir(x):
    return x if x.isalpha() else int(x)

def svg2path(file): # svg의 패스의 d 데이터를 모두 가져옴
    allPaths=[]
    r=eTree.parse(file).getroot().iter('{http://www.w3.org/2000/svg}path')
    for p in r:
        allPaths.append(pathCleaver.findall(p.attrib['d']))
        allPaths[-1]=[isNumOrDir(x) for x in allPaths[-1]]
    return allPaths

def mag(x,y):
    return sqrt(x**2+y**2)

def sinCoef(x1,y1,x2,y2):
    cross=x1*y2-x2*y1
    if cross<0:
        cross=-1
    elif cross>0:
        cross=1
    dot=x1*x2+y1*y2
    try:
        dot=dot/mag(x1,y1)/mag(x2,y2)
    except ZeroDivisionError:
        dot=0
    return cross, dot

def polyLineLen(x0,y0,pl):
    ret=mag(x0-pl[0],y0-pl[1])
    i=0
    l=len(pl)-2
    while i<l:
        ret+=mag(pl[i]-pl[i+2],pl[i+1]-pl[i+3])
        i+=2
    return ret

def path2abs(d):    # 리스트로 입력된 단일 d 데이터에서 모든 값을 절대값(대문자)으로 변경
    cx=cy=0
    x0=y0=0
    omitFlag=0
    prev=''
    i=0
    l=len(d)
    while i<l:
        omitFlag=0 if type(d[i]) is str else 1
        shape=prev if omitFlag else d[i]
        if shape=='M' or shape=='m':
            x0,y0=d[i+1:i+3]
            cx,cy=x0,y0
            i+=3
        elif shape=='c':
            if omitFlag==0:
                d[i]='C'
            d[i+1-omitFlag]+=cx
            d[i+2-omitFlag]+=cy
            d[i+3-omitFlag]+=cx
            d[i+4-omitFlag]+=cy
            d[i+5-omitFlag]+=cx
            d[i+6-omitFlag]+=cy
            cx=d[i+5-omitFlag]
            cy=d[i+6-omitFlag]
            i+=7-omitFlag
        elif shape=='qs':
            if omitFlag==0:
                d[i]=d[i].upper()
            d[i+1-omitFlag]+=cx
            d[i+2-omitFlag]+=cy
            d[i+3-omitFlag]+=cx
            d[i+4-omitFlag]+=cy
            cx=d[i+3-omitFlag]
            cy=d[i+4-omitFlag]
            i+=5-omitFlag
        elif shape in 'tl':
            if omitFlag==0:
                d[i]=d[i].upper()
            d[i+1-omitFlag]+=cx
            d[i+2-omitFlag]+=cy
            cx=d[i+1-omitFlag]
            cy=d[i+2-omitFlag]
            i+=3-omitFlag
        elif shape=='h':
            if omitFlag==0:
                d[i]='H'
            d[i+1-omitFlag]+=cx
            cx=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape=='v':
            if omitFlag==0:
                d[i]='V'
            d[i+1-omitFlag]+=cy
            cy=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape in 'Zz':
            cx,cy=x0,y0
            i+=1
        elif shape=='C':
            cx=d[i+5-omitFlag]
            cy=d[i+6-omitFlag]
            i+=7-omitFlag
        elif shape in 'QS':
            cx=d[i+3-omitFlag]
            cy=d[i+4-omitFlag]
            i+=5-omitFlag
        elif shape in 'TL':
            cx=d[i+1-omitFlag]
            cy=d[i+2-omitFlag]
            i+=3-omitFlag
        elif shape=='H':
            cx=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape=='V':
            cy=d[i+1-omitFlag]
            i+=2-omitFlag
        prev=shape

def path2rel(d):    # 리스트로 입력된 단일 d 데이터에서 모든 값을 상대값(소문자)으로 변경
    cx=cy=0
    x0=y0=0
    omitFlag=0
    prev=''
    i=0
    l=len(d)
    while i<l:
        omitFlag=0 if type(d[i]) is str else 1
        shape=prev if omitFlag else d[i]
        if shape=='M' or shape=='m':
            x0,y0=d[i+1:i+3]
            cx,cy=x0,y0
            i+=3
        elif shape=='c':
            cx+=d[i+5-omitFlag]
            cy+=d[i+6-omitFlag]
            i+=7-omitFlag
        elif shape=='qs':
            cx+=d[i+3-omitFlag]
            cy+=d[i+4-omitFlag]
            i+=5-omitFlag
        elif shape in 'tl':
            cx+=d[i+1-omitFlag]
            cy+=d[i+2-omitFlag]
            i+=3-omitFlag
        elif shape=='h':
            cx+=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape=='v':
            cy+=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape in 'Zz':
            cx,cy=x0,y0
            i+=1
        elif shape=='C':
            if omitFlag==0:
                d[i]='c'
            d[i+1-omitFlag]-=cx
            d[i+2-omitFlag]-=cy
            d[i+3-omitFlag]-=cx
            d[i+4-omitFlag]-=cy
            d[i+5-omitFlag]-=cx
            d[i+6-omitFlag]-=cy
            cx+=d[i+5-omitFlag]
            cy+=d[i+6-omitFlag]
            i+=7-omitFlag
        elif shape in 'QS':
            if omitFlag==0:
                d[i]=d[i].lower()
            d[i+1-omitFlag]-=cx
            d[i+2-omitFlag]-=cy
            d[i+3-omitFlag]-=cx
            d[i+4-omitFlag]-=cy
            cx+=d[i+3-omitFlag]
            cy+=d[i+4-omitFlag]
            i+=5-omitFlag
        elif shape in 'TL':
            if omitFlag==0:
                d[i]=d[i].lower()
            d[i+1-omitFlag]-=cx
            d[i+2-omitFlag]-=cy
            cx+=d[i+1-omitFlag]
            cy+=d[i+2-omitFlag]
            i+=3-omitFlag
        elif shape=='H':
            if omitFlag==0:
                d[i]='h'
            d[i+1-omitFlag]-=cx
            cx+=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape=='V':
            if omitFlag==0:
                d[i]='v'
            d[i+1-omitFlag]-=cy
            cy+=d[i+1-omitFlag]
            i+=2-omitFlag
        prev=shape

def path2ch(d): # 단일 d 데이터의 특성 추출(표면 데이터[전체], 정점-꺾임 데이터[음소별], 배치 데이터[글자별])
    ch=[]
    prev=''
    omitFlag=0
    l=len(d)
    dot=cross=1
    cut=i=0     # index
    pl=0    # polyline length
    spl=0   # sum of several polyline length
    top=bot=lpo=rpo=0
    x0=y0=0
    cx=cy=0    # current x, y coord
    cdx=1   # current direction
    cdy=0   # current direction
    while i<l:  # 최적화를 위해 해시형식 사용하는 것 고려
        omitFlag=0 if type(d[i]) is str else 1
        if omitFlag:
            shape=prev
        else:
            shape=d[i]
        if shape in 'Mm':
            cx, cy=d[i+1:i+3]
            x0,y0=cx,cy
            top=bot=y0
            lpo=rpo=x0
            i+=3
        elif shape=='C':
            cdx,cdy=d[i+5-omitFlag]-d[i+3-omitFlag], d[i+6-omitFlag]-d[i+4-omitFlag]
            pl=polyLineLen(cx,cy,d[i+1-omitFlag:i+7-omitFlag])
            cross, dot=sinCoef(
                d[i+1-omitFlag]-cx, d[i+2-omitFlag]-cy, 
                cdx,cdy
            )
            cx,cy=d[i+5-omitFlag:i+7-omitFlag]
            i+=7-omitFlag
        elif shape=='c':
            cdx,cdy=d[i+5-omitFlag]-d[i+3-omitFlag], d[i+6-omitFlag]-d[i+4-omitFlag]
            pl=polyLineLen(0,0,d[i+1-omitFlag:i+7-omitFlag])
            cross, dot=sinCoef(
                d[i+1-omitFlag], d[i+2-omitFlag],
                cdx,cdy
            )
            cx+=d[i+5-omitFlag]
            cy+=d[i+6-omitFlag]
            i+=7-omitFlag
        elif shape=='T':
            pl=polyLineLen(cx,cy,(cx+cdx,cy+cdy,d[i+1-omitFlag],d[i+2-omitFlag]))
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1-omitFlag]-cx-cdx, d[i+2-omitFlag]-cy-cdy
            )
            cdx, cdy=d[i+1-omitFlag]-cx-cdx, d[i+2-omitFlag]-cy-cdy
            cx,cy=d[i+1-omitFlag:i+3-omitFlag]
            i+=3-omitFlag
        elif shape=='t':
            pl=polyLineLen(0,0,(cdx,cdy,d[i+1-omitFlag],d[i+2-omitFlag]))
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1-omitFlag]-cdx, d[i+2-omitFlag]-cdy
            )
            cdx, cdy=d[i+1-omitFlag]-cdx, d[i+2-omitFlag]-cdy
            cx+=d[i+1-omitFlag]
            cy+=d[i+2-omitFlag]
            i+=3-omitFlag
        elif shape=='Q':
            pl=polyLineLen(cx,cy,d[i+1-omitFlag:i+5-omitFlag])
            cdx,cdy=d[i+3-omitFlag]-d[i+1-omitFlag], d[i+4-omitFlag]-d[i+2-omitFlag]
            cross, dot=sinCoef(
                d[i+1-omitFlag]-cx, d[i+2-omitFlag]-cy,
                cdx,cdy
            )
            cx,cy=d[i+3-omitFlag:i+5-omitFlag]
            i+=5-omitFlag
        elif shape=='q':
            pl=polyLineLen(0,0,d[i+1-omitFlag:i+5-omitFlag])
            cdx,cdy=d[i+3-omitFlag]-d[i+1-omitFlag], d[i+4-omitFlag]-d[i+2-omitFlag]
            cross, dot=sinCoef(
                d[i+1-omitFlag], d[i+2-omitFlag],
                cdx,cdy
            )
            cx+=d[i+3-omitFlag]
            cy+=d[i+4-omitFlag]
            i+=5-omitFlag
        elif shape=='L':
            pl=mag(cx-d[i+1-omitFlag],cy-d[i+2-omitFlag])
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1-omitFlag]-cx,d[i+2-omitFlag]-cy
            )
            cdx,cdy=d[i+1-omitFlag]-cx,d[i+2-omitFlag]-cy
            cx,cy=d[i+1-omitFlag:i+3-omitFlag]
            i+=3-omitFlag
        elif shape=='l':
            pl=mag(d[i+1-omitFlag],d[i+2-omitFlag])
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1-omitFlag],d[i+2-omitFlag]
            )
            cdx,cdy=d[i+1-omitFlag],d[i+2-omitFlag]
            cx+=d[i+1-omitFlag]
            cy+=d[i+2-omitFlag]
            i+=3-omitFlag
        elif shape=='H':
            pl=abs(d[i+1-omitFlag]-cx)
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1-omitFlag]-cx,0
            )
            cdx,cdy=d[i+1-omitFlag]-cx,0
            cx=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape=='h':
            pl=abs(d[i+1-omitFlag])
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1-omitFlag],0
            )
            cdx,cdy=d[i+1-omitFlag],0
            cx+=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape=='V':
            pl=abs(d[i+1-omitFlag]-cy)
            cross, dot=sinCoef(
                cdx,cdy,
                0,d[i+1-omitFlag]-cy
            )
            cdx,cdy=0,d[i+1-omitFlag]-cy
            cy=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape=='v':
            pl=abs(d[i+1-omitFlag])
            cross, dot=sinCoef(
                cdx,cdy,
                0,d[i+1-omitFlag]
            )
            cdx,cdy=0,d[i+1-omitFlag]
            cy+=d[i+1-omitFlag]
            i+=2-omitFlag
        elif shape=='S':
            pl=polyLineLen(cx,cy,(cx+cdx,cy+cdy,d[i+1-omitFlag],d[i+2-omitFlag],d[i+3-omitFlag],d[i+4-omitFlag]))
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+3-omitFlag]-d[i+1-omitFlag], d[i+4-omitFlag]-d[i+2-omitFlag]
            )
            cdx,cdy=d[i+3-omitFlag]-d[i+1-omitFlag], d[i+4-omitFlag]-d[i+2-omitFlag]
            cx, cy=d[i+3-omitFlag:i+5-omitFlag]
            i+=5-omitFlag
        elif shape=='s':
            pl=polyLineLen(0,0,(cdx,cdy,d[i+1-omitFlag],d[i+2-omitFlag],d[i+3-omitFlag],d[i+4-omitFlag]))
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+3-omitFlag]-d[i+1-omitFlag], d[i+4-omitFlag]-d[i+2-omitFlag]
            )
            cdx,cdy=d[i+3-omitFlag]-d[i+1-omitFlag], d[i+4-omitFlag]-d[i+2-omitFlag]
            cx+=d[i+3-omitFlag]
            cy+=d[i+4-omitFlag]
            i+=5-omitFlag
        elif shape in 'Zz':
            pl=mag(cx-x0,cy-y0)
            cross, dot=sinCoef(
                cdx,cdy,
                x0-cx, y0-cy
            )
            cdx,cdy=x0-cx, y0-cy
            cx,cy=x0,y0
            i+=1

        if cy>top:
            top=cy
        elif cy<bot:
            bot=cy
        if cx>rpo:
            rpo=cx
        elif cx<lpo:
            lpo=cx
        prev=shape
        spl+=pl
        # cross, dot usage code
        #if dot<=0.5:    # 60도
        #    ch.append((spl,cross,dot))
        #    spl=0
        if dot<0.87:     # 30도
            ch.append((d[cut:i],int(spl),cross,dot)) # d[cut:i]는 실제 데이터, spl은 중요도(작은 것은 변형 불가능, 기준은 대충 직사각형의 짧은 길이의 1/5), cross와 dot은 동질성을 판단하는 데 중요한 열쇠임
            # dot 참고: 0=90도, 0.17=80도, 0.34=70도, 0.5=60도, 0.64=50도, 0.77=40도, 0.87=30도. 90보다 큰 각은 물론 90 중심 대칭으로 음수
            cut=i
            spl=0

    return ch, (top, bot, lpo, rpo)

    # 도트가 0.87보다 큰 것에 대해서는 직선과 2차와 3차 각각에 대하여 얼마나 밖으로 나갔는지 파악해서 평균과 분산을 리턴할 것
    # /\ 벡터 간의 각도의 절댓값을 말함. 이를 굵기와 함께 미리 주어진 직선에 적용하는 것은 오목-볼록 번갈아, 다른 파일에서 할 일

    # 1. 커버 직사각형 범위 기록
    # 2. 전체적 윤곽을 정하는(수정이 가해질) 스플라인 그룹 파악, 그룹에 속하지 않은 부분은 유지
    # 수정의 케이스: 길이 줄임/늘림, 각도 변형, 굵기 변형(예를 글어 괅같은 데에서는 기본이 굵은 글자의 굵기가 약간 줄 필요가 있음)
    # 3. classify(ex: 4 90 deg: rectangle, 0 significant: circle, etc.)
    # 아예 입력이 없었던 글자의 생성법: 베이스 패스 기반, 굵기와 표면 특성치를 합하여 적용

def compoundCh():   # 동일한 대상을 가리키는 특성치의 조합
    pass

# 특성치에서 벡터 데이터 생성하는 건 이 파일 말고 다른 곳에
# ADT
# 휘어진 각도 기준: 1. 기울기 차, 2. 시계방향/반시계방향(=내적이 아닌 외적이 필요함)
# 줄기 형태 파악(입력값: 패스, 글자), (출력 예: 글자가 '강'인 경우 패스가 수평선/수직선/ㄱ/ㅏ/원형인지 각각 확인 가능.(ㅇ, ㅁ 등은 등고선 최소 2개 필요))
# 외부 윤곽선 형태 파악(입력값: 패스), Bayesian Inference -> get RV and realize
# 배치 파악(입력값: 패스, 글자)
# 말단 길게/짧게

def path2svg(file, w, h, p):    # 새로 만들어진 패스를 다시 svg파일에 작성
    with open(file, 'w') as f:
        f.write('<svg width={} height={} xmlns="http://www.w3.org/2000/svg">\n'.format(w,h))
        for path in p:
            f.write('\t<path d="{}" fill="black"/>\n'.format(path))
        f.write('</svg>')
