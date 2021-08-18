import re
import xml.etree.ElementTree as eTree

pathCleaver=re.compile(r'[A-Za-z]|[0-9]+')

def svg2path(file): # svg의 패스의 d 데이터를 모두 가져옴
    allPaths=[]
    with eTree.parse(file).getroot() as r:
        for p in r.findall('{http://www.w3.org/2000/svg}path'):
            allPaths.append(pathCleaver.findall(p.attrib['d']))
    return allPaths

def path2ch(): # 단일 d 데이터의 특성 추출(표면 데이터[전체], 정점-꺾임 데이터[음소별], 배치 데이터[글자별])
    pass

def compoundCh():   # 동일한 대상을 가리키는 특성치의 조합
    pass

# 특성치에서 벡터 데이터 생성하는 건 이 파일 말고 다른 곳에

def path2svg(file, w, h, p):    # 새로 만들어진 패스를 다시 svg파일에 작성
    with open(file, 'w') as f:
        f.write('<svg width={} height={} xmlns="http://www.w3.org/2000/svg">\n'.format(w,h))
        for path in p:
            f.write('\t<path d="{}" fill="black"/>\n'.format(path))
        f.write('</svg>')