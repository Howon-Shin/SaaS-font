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
    with eTree.parse(file).getroot() as r:
        for p in r.findall('{http://www.w3.org/2000/svg}path'):
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
    dot=dot/mag(x1,y1)/mag(x2,y2)
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
    l=len(d)
    i=0
    pl=0    # polyline length
    x0=0
    y0=0
    cx=0    # current x coord
    cy=0    # current y coord
    cdx=1   # current direction
    cdy=0   # current direction
    while i<l:  # 최적화를 위해 해시형식 사용하는 것 고려
        if d[i]=='M' or d[i]=='m':
            cx, cy=d[i+1:i+3]
            x0,y0=cx,cy
            i+=3
        elif d[i]=='C':
            cdx,cdy=d[i+5]-d[i+3], d[i+6]-d[i+4]
            pl=polyLineLen(cx,cy,d[i+1:i+7])
            cross, dot=sinCoef(
                d[i+1]-cx, d[i+2]-cy, 
                cdx,cdy
            )
            cx,cy=d[i+5:i+7]
            i+=7
        elif d[i]=='c':
            cdx,cdy=d[i+5]-d[i+3], d[i+6]-d[i+4]
            pl=polyLineLen(0,0,d[i+1:i+7])
            cross, dot=sinCoef(
                d[i+1], d[i+2],
                cdx,cdy
            )
            cx+=d[i+5]
            cy+=d[i+6]
            i+=7
        elif d[i]=='T':
            pl=polyLineLen(cx,cy,(cx+cdx,cy+cdy,d[i+1],d[i+2]))
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1]-cx-cdx, d[i+2]-cy-cdy
            )
            cdx, cdy=d[i+1]-cx-cdx, d[i+2]-cy-cdy
            cx,cy=d[i+1:i+3]
            i+=3
        elif d[i]=='t':
            pl=polyLineLen(0,0,(cdx,cdy,d[i+1],d[i+2]))
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1]-cdx, d[i+2]-cdy
            )
            cdx, cdy=d[i+1]-cdx, d[i+2]-cdy
            cx+=d[i+1]
            cy+=d[i+2]
            i+=3
        elif d[i]=='Q':
            pl=polyLineLen(cx,cy,d[i+1:i+5])
            cdx,cdy=d[i+3]-d[i+1], d[i+4]-d[i+2]
            cross, dot=sinCoef(
                d[i+1]-cx, d[i+2]-cy,
                cdx,cdy
            )
            cx,cy=d[i+3:i+5]
            i+=5
        elif d[i]=='q':
            pl=polyLineLen(0,0,d[i+1:i+5])
            cdx,cdy=d[i+3]-d[i+1], d[i+4]-d[i+2]
            cross, dot=sinCoef(
                d[i+1], d[i+2],
                cdx,cdy
            )
            cx+=d[i+3]
            cy+=d[i+4]
            i+=5
        elif d[i]=='L':
            pl=mag(cx-d[i+1],cy-d[i+2])
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1]-cx,d[i+2]-cy
            )
            cdx,cdy=d[i+1]-cx,d[i+2]-cy
            cx,cy=d[i+1:i+3]
            i+=3
        elif d[i]=='l':
            pl=mag(d[i+1],d[i+2])
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1],d[i+2]
            )
            cdx,cdy=d[i+1],d[i+2]
            cx+=d[i+1]
            cy+=d[i+2]
            i+=3
        elif d[i]=='H':
            pl=abs(d[i+1]-cx)
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1]-cx,0
            )
            cdx,cdy=d[i+1]-cx,0
            cx=d[i+1]
            i+=2
        elif d[i]=='h':
            pl=abs(d[i+1])
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+1],0
            )
            cdx,cdy=d[i+1],0
            cx+=d[i+1]
            i+=2
        elif d[i]=='V':
            pl=abs(d[i+1]-cy)
            cross, dot=sinCoef(
                cdx,cdy,
                0,d[i+1]-cy
            )
            cdx,cdy=0,d[i+1]-cy
            cy=d[i+1]
            i+=2
        elif d[i]=='v':
            pl=abs(d[i+1])
            cross, dot=sinCoef(
                cdx,cdy,
                0,d[i+1]
            )
            cdx,cdy=0,d[i+1]
            cy+=d[i+1]
            i+=2
        elif d[i]=='S':
            pl=polyLineLen(cx,cy,(cx+cdx,cy+cdy,d[i+1],d[i+2],d[i+3],d[i+4]))
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+3]-d[i+1], d[i+4]-d[i+2]
            )
            cdx,cdy=d[i+3]-d[i+1], d[i+4]-d[i+2]
            cx, cy=d[i+3:i+5]
            i+=5
        elif d[i]=='s':
            pl=polyLineLen(0,0,(cdx,cdy,d[i+1],d[i+2],d[i+3],d[i+4]))
            cross, dot=sinCoef(
                cdx,cdy,
                d[i+3]-d[i+1], d[i+4]-d[i+2]
            )
            cdx,cdy=d[i+3]-d[i+1], d[i+4]-d[i+2]
            cx+=d[i+3]
            cy+=d[i+4]
            i+=5
        elif d[i] in 'Zz':
            pl=mag(cx-x0,cy-y0)
            cross, dot=sinCoef(
                cdx,cdy,
                x0-cx, y0-cy
            )
            cdx,cdy=x0-cx, y0-cy
            cx,cy=x0,y0
            i+=1
        # cross, dot usage code
    # 1. Noticing overall size(rectangle area)
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