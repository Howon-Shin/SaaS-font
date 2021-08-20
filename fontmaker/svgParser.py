import re
import xml.etree.ElementTree as eTree
from math import sqrt

pathCleaver=re.compile(r'[A-Za-z]|[0-9]+')
# 함수들 인수: 입력 좌표값 n개, 좌표 리스트(2차원)
# 리턴값: 특성리스트

def bigV():
    pass

def smallV():
    pass

def bigH():
    pass

def smallH():
    pass

def bigM():
    pass

def smallM():
    pass

def bigT():
    pass

def smallT():
    pass

def bigQ():
    pass

def smallQ():
    pass

def bigS():
    pass

def smallS():
    pass

def bigC():
    pass

def smallC():
    pass

param1={
    'V':bigV,
    'v':None,
    'H':None,
    'h':None,
}
param2={
    'M':None,
    'm':None,
    'T':None,
    't':None,
}
param4={
    'Q':None,
    'q':None,
    'S':None,
    's':None,
}
param6={
    'C':None,
    'c':None,
}

def svg2path(file): # svg의 패스의 d 데이터를 모두 가져옴
    allPaths=[]
    with eTree.parse(file).getroot() as r:
        for p in r.findall('{http://www.w3.org/2000/svg}path'):
            allPaths.append(pathCleaver.findall(p.attrib['d']))
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


def path2ch(d): # 단일 d 데이터의 특성 추출(표면 데이터[전체], 정점-꺾임 데이터[음소별], 배치 데이터[글자별])
    l=len(d)
    i=0
    while i<l:  # 최적화를 위해 해시형식 사용하는 것 고려
        if d[i]=='M' or d[i]=='m':
            pass
        elif d[i]=='C':
            pass
        elif d[i]=='c':
            pass
        elif d[i]=='T':
            pass
        elif d[i]=='t':
            pass
        elif d[i]=='Q':
            pass
        elif d[i]=='q':
            pass
        elif d[i]=='L':
            pass
        elif d[i]=='l':
            pass
        elif d[i]=='H':
            pass
        elif d[i]=='h':
            pass
        elif d[i]=='V':
            pass
        elif d[i]=='v':
            pass
        elif d[i]=='S':
            pass
        elif d[i]=='s':
            pass
        i+=1

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