import re
import xml.etree.ElementTree as eTree
from math import sqrt

pathCleaver=re.compile(r'[A-Za-z]|[0-9]+')
# 함수들 인수: 입력 좌표값 n개, 좌표 리스트(2차원)
# 리턴값: 특성리스트

def isNumOrDir(x):
    return int(x) if x.isnumeric() else x

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

def path2ch(d): # 단일 d 데이터의 특성 추출(표면 데이터[전체], 정점-꺾임 데이터[음소별], 배치 데이터[글자별])
    ch=[]
    prev=''
    omitFlag=0
    l=len(d)
    dot=1
    cross=1
    i=0
    pl=0    # polyline length
    spl=0   # sum of several polyline length
    top=bot=lpo=rpo=0
    x0=0
    y0=0
    cx=0    # current x coord
    cy=0    # current y coord
    cdx=1   # current direction
    cdy=0   # current direction
    while i<l:  # 최적화를 위해 해시형식 사용하는 것 고려
        omitFlag=0 if type(d[i]) is str else 1
        if omitFlag:
            shape=prev
        else:
            shape=d[i]
        if shape=='M' or shape=='m':
            cx, cy=d[i+1:i+3]
            x0,y0=cx,cy
            top=bot=y0
            lpo=rpo=x0
            i+=3
        elif shape=='C':
            cdx,cdy=d[i+5-omitFlag]-d[i+3-omitFlag], d[i+6-omitFlag]-d[i+4-omitFlag]
            pl=polyLineLen(cx,cy,d[i+1:i+7])
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
        elif shape == 'Z' or 'z':
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
        # cross, dot usage code
        if dot<=0.5:
            ch.append((spl,cross,dot))
            spl=0
        #elif dot<0.87:
            #pass
        else:
            spl+=pl


    return ch

    # 1. Noticing overall size(rectangle area or total spline length)
    # 2. Find significant splines
    # 3. classify(ex: 4 90 deg: rectangle, 0 significant: circle, etc.)

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
