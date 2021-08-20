# fontforge -lang py -script (이 파일 경로) (매개변수들)
# fontforge가 PATH에 등록되어 있지 않은 경우, 'fontforge' 대신 실행 파일의 실제 위치를 명시할 것
import argparse
import os
import fontforge as ffg
import psMat

BASEPATH='./ff_projects/{}/{}'  # 현재 디렉토리 기준: fontforge 스크립트를 실행시키는 명령을 한 곳
VECTOR=('.svg','.eps','.glif')
BITMAP=('.bmp','.png','.xbm','.jpg')
ASCII={'\\':'BSLASH', '/':'SLASH', ':':'COLON','?':'QUEST','%':'PERCENT','*':'ASTER','|':'BAR','.':'PERIOD','<':'LT','>':'GT','"':'DOUBLE',"'":'SINGLE'}
ASCIIR={ASCII[k]:k for k in ASCII}
STD_C=(120,90,820,620)
STD_VV=(320,-86,715,820)
STD_HV=(54,136,962,642)

LEFT_HV=(85,190,750,370)
RIGHT_VV=(645,-90,830,820)
COMPL=(84.0, -113, 989.0, 849.0)

def transC(rect1, rect2):
    # rect1을 rect2에 맞게 조정. rect1의 비율을 유지하지 않고 rect2의 비율을 따라감
    dst=(rect2[2]-rect2[0],rect2[3]-rect2[1])
    mat=psMat.scale(dst[0]/(rect1[2]-rect1[0]),dst[1]/(rect1[3]-rect1[1]))
    tr2=psMat.translate(rect2[0]-rect1[0],rect2[1]-rect1[1])
    mat=psMat.compose(mat,tr2)
    return mat

def transV(rect1, rect2):
    # rect1을 rect2에 맞게 조정. rect1의 비율을 유지(긴 방향의 중심선 일치)
    dst=(rect2[2]-rect2[0],rect2[3]-rect2[1])
    mat=None
    if rect1[2]-rect1[0]>rect1[3]-rect1[1]:
        mat=psMat.scale(dst[0]/(rect1[2]-rect1[0]))
        #tr1=psMat.translate(0,(dst[1]+(rect1[3]-rect1[1])*dst[0]/(rect1[2]-rect1[0]))/2)
        #mat=psMat.compose(mat,tr1)
    else:
        mat=psMat.scale(dst[1]/(rect1[3]-rect1[1]))
        #tr1=psMat.translate((dst[0]+(rect1[2]-rect1[0])*dst[1]/(rect1[3]-rect1[1]))/2,0)
        #mat=psMat.compose(mat,tr1)
    tr2=psMat.translate(rect2[0]-rect1[0],rect2[1]-rect1[1])
    mat=psMat.compose(mat,tr2)
    return mat


def importImg(font, path):
    letter, ext=os.path.splitext(path)
    if ext not in VECTOR and ext not in BITMAP:
        return
    letter=letter.split('/')[-1]
    if letter in ASCIIR:
        letter=ASCIIR[letter]
    font.createChar(ord(letter),letter)
    font[letter].clear()
    font[letter].importOutlines(path)
    if ext in BITMAP:
        font[letter].autoTrace()
    setPos(font, letter)
    # 추가 과정: 차지 공간 설정, 위치 표준화

def setPos(font, letter):
    code=ord(letter)
    if letter.isascii():    # 개별 위치선정
        pass
    elif code>=12593 and code<=12622:
        font[letter].transform(transC(font[letter].boundingBox(),STD_C), ('round'))
    elif code>=44032 and code<=55203:
        font[letter].transform(transC(font[letter].boundingBox(),COMPL), ('round'))
    elif letter in 'ㅏㅐㅑㅒㅓㅔㅕㅖ':
        font[letter].transform(transC(font[letter].boundingBox(),STD_VV), ('round'))
    elif letter in 'ㅗㅛㅜㅠ':
        font[letter].transform(transC(font[letter].boundingBox(),STD_HV), ('round'))
    elif letter in 'ㅘㅙㅚㅝㅞㅟㅢ':
        font[letter].transform(transC(font[letter].boundingBox(),COMPL), ('round'))
    else:
        pass

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('-e',help="다른 모든 작업 후 뽑아낼 폰트 파일 이름을 말합니다. 명시된 확장자로 정리됩니다.")
    ap.add_argument('-a',help="이미지 파일을 글리프로 추가합니다. 이미지 이름에서는, 확장자를 제외한 이름이 반드시 그 문자여야 합니다. 파일 이름으로 사용할 수 없는 문자는 이름이 따로 정해져 있으므로 참고하시기 바랍니다. 공백으로 와일드카드를 사용할 수 있습니다. 이미 있던 경우 덮어씁니다.")
    ap.add_argument('-p',help="해당 문자의 png 파일을 추출합니다.")
    ap.add_argument('-v',help="해당 문자의 svg 파일을 추출합니다. wc인 경우 현재 있는 모든 한글 글리프에 대하여 추출합니다.")
    ap.add_argument('-o',help="프로젝트 이름입니다. 해당 프로젝트에 sfd 파일이 없는 경우 새로 만들어집니다.")
    ap.add_argument('--h',help="프로젝트에 한글 글리프가 추가됩니다.", action='store_true')
    ap.add_argument('--ua',help="채워지지 않은 모든 아스키 문자를 단일 공백 구분으로 stdout에 출력합니다.", action='store_true')
    ap.add_argument('--uk',help="채워지지 않은 모든 한글 문자를 단일 공백 구분으로 stdout에 출력합니다.", action='store_true')
    ns=ap.parse_args()
    if ns.o:
        proj=BASEPATH.format(ns.o,'project.sfd')
        if os.path.isfile(proj):
            font=ffg.open(proj) # 비 아스키 문자가 파일 경로에 있는 경우 열리지 않으니 주의!!!
        else:
            font=ffg.font()
            font.createChar(ord(' '),' ')
        if ns.h:
            for x in range(12593, 12644):
                font.createChar(x,chr(x))
            for x in range(44032,55204):
                font.createChar(x,chr(x))
        if ns.a:
            if ns.a != ' ':
                importImg(font, ns.a)
            else:
                for x in os.scandir(BASEPATH.format(ns.o,'')):
                    importImg(font, x.path)
        if ns.p:
            try:
                if ns.p in ASCII:
                    font[ns.p].export(BASEPATH.format(ns.o,ASCII[ns.p]+'.png'))
                else:
                    font[ns.p].export(BASEPATH.format(ns.o,ns.p+'.png'))
            except:
                pass
        if ns.v:
            if ns.v=='wc':
                for g in font.glyphs:
                    if g.glyphname.isascii():
                        continue
                    g.export(BASEPATH.format(ns.o,g.glyphname+'.svg'))
            try:
                if ns.v in ASCII:
                    font[ns.v].export(BASEPATH.format(ns.o,ASCII[ns.v]+'.svg'))
                else:
                    font[ns.v].export(BASEPATH.format(ns.o,ns.v+'.svg'))
            except:
                pass

        unFilled=''
        if ns.ua:
            for x in range(26,127):
                try:
                    if not font[chr(x)].isWorthOutputting():
                        unFilled+=chr(x)+' '
                except TypeError:
                    unFilled+=chr(x)+' '
        if ns.uk:
            for x in range(12593, 12644):
                try:
                    if not font[chr(x)].isWorthOutputting():
                        unFilled+=chr(x)+' '
                except TypeError:
                    unFilled+=chr(x)+' '
            for x in range(44032,55204):
                try:
                    if not font[chr(x)].isWorthOutputting():
                        unFilled+=chr(x)+' '
                except TypeError:
                    unFilled+=chr(x)+' '
        if unFilled:
            print(unFilled)
            
        if ns.e:
            name=os.path.splitext(ns.e)[0]
            font.version=1.0
            font.fontname=name
            font.familyname=name
            font.fullname=name
            font.default_base_filename=name
            font.generate(BASEPATH.format(ns.o,ns.e))
        font.save(proj)
