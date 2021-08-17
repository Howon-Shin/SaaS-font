# fontforge -lang py -script (이 파일 경로) (매개변수들)
# fontforge가 PATH에 등록되어 있지 않은 경우, 'fontforge' 대신 실행 파일의 실제 위치를 명시할 것
import argparse
import os
import fontforge as ffg
import psMat

BASEPATH='./ff_projects/{}/{}'  # 현재 디렉토리 기준: fontforge 스크립트를 실행시키는 명령을 한 곳
VECTOR=('svg','eps','glif')
BITMAP=('bmp','png','xbm','jpg')
ASCII={'\\':'BSLASH', '/':'SLASH', ':':'COLON','?':'QUEST','%':'PERCENT','*':'ASTER','|':'BAR','.':'PERIOD','<':'LT','>':'GT','"':'DOUBLE',"'":'SINGLE'}
ASCIIR={ASCII[k]:k for k in ASCII}


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
    # 추가 과정: 차지 공간 설정, 위치 표준화

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
            font=ffg.open(proj)
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
                importImg(font, proj)
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
