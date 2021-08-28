# fontforge -lang py -script (이 파일 경로) (매개변수들)
# fontforge가 PATH에 등록되어 있지 않은 경우, 'fontforge' 대신 실행 파일의 실제 위치를 명시할 것
import argparse
import os
import fontforge as ffg
import psMat

BASEPATH='./fontmaker/ff_projects/{}/{}'  # 현재 디렉토리 기준: fontforge 스크립트를 실행시키는 명령을 한 곳
VECTOR=('.svg','.eps','.glif')
BITMAP=('.bmp','.png','.xbm','.jpg')
ASCII={'\\':'BSLASH', '/':'SLASH', ':':'COLON','?':'QUEST','%':'PERCENT','*':'ASTER','|':'BAR','.':'PERIOD','<':'LT','>':'GT','"':'DOUBLE',"'":'SINGLE'}
ASCIIR={ASCII[k]:k for k in ASCII}

# ascii size data
AREA=((111.0, -9.0, 212.0, 754.0),(91.21428571428571, 460.0, 335.75, 760.0),(18.0, 6.0, 624.0, 734.0),(28.0, -104.0, 540.0, 832.0),(67.0, -18.0, 811.0, 722.0),(84.0, -18.0, 800.0, 754.0),(88.21428571428571, 460.0, 167.23076923076923, 760.0),(82.0, -85.0, 338.0, 823.0),(52.0, -85.0, 308.0, 823.0),(73.66666666666667, 163.0, 432.0833333333333, 575.0),(60.0, 120.0, 580.0, 624.0),(84.0, -141.0, 204.0, 101.0),(91.0, 351.0, 549.0, 404.0),(92.0, -16.0, 205.0, 102.0),(2.0, -72.0, 386.0, 816.0),(54.0, -14.0, 562.0, 754.0),(133.0, -1.0, 499.0, 754.0),(82.0, -3.0, 550.0, 752.0),(68.0, -18.0, 533.0, 753.0),(60.0, -1.0, 541.0, 751.0),(78.0, -16.0, 539.0, 736.0),(73.0, -18.0, 536.0, 754.0),(69.0, -18.0, 544.0, 736.0),(76.0, -18.0, 538.0, 754.0),(74.0, -20.0, 537.0, 753.0),(117.0, 108.0, 225.0, 626.0),(116.0, -30.0, 225.0, 627.0),(78.0, 6.0, 566.0, 729.0),(64.0, 247.0, 576.0, 497.0),(78.0, 6.0, 566.0, 729.0),(56.0, -18.0, 457.0, 754.0),(79.0, -68.0, 944.0, 798.0),(8.0, -1.0, 742.0, 754.0),(38.0, -1.0, 669.0, 736.0),(58.0, -18.0, 671.0, 754.0),(38.0, 1.0, 689.0, 737.0),(38.0, 1.0, 662.0, 737.0),(38.0, -1.0, 635.0, 737.0),(59.0, -18.0, 730.0, 754.0),(43.0, -1.0, 742.0, 737.0),(41.0, -1.0, 294.0, 737.0),(19.0, -16.0, 399.0, 737.0),(42.0, -1.0, 752.0, 737.0),(38.0, -1.0, 641.0, 737.0),(41.0, -8.0, 875.0, 737.0),(38.0, -4.0, 757.0, 737.0),(57.0, -17.0, 702.0, 754.0),(38.0, -1.0, 627.0, 736.0),(54.0, -115.0, 736.0, 754.0),(38.0, -1.0, 684.0, 736.0),(44.0, -16.0, 589.0, 754.0),(22.0, -3.0, 749.0, 737.0),(38.0, -18.0, 771.0, 736.0),(30.0, -18.0, 736.0, 736.0),(16.0, -18.0, 956.0, 736.0),(30.0, -1.0, 682.0, 736.0),(33.0, -1.0, 674.0, 736.0),(35.0, -1.0, 609.0, 736.0),(205.0, -81.0, 418.0, 815.0),(36.0, -18.0, 980.0, 736.0),(146.0, -81.0, 359.0, 815.0),(27.0, 511.0, 483.0, 767.0),(0.0, -89.0, 512.0, -37.0),(109.67857142857143, 565.0, 339.0, 738.3703703703703),(64.0, -18.0, 521.0, 496.0),(37.0, -18.0, 528.0, 745.0),(64.0, -18.0, 494.0, 496.0),(64.0, -18.0, 556.0, 744.0),(64.0, -18.0, 524.0, 496.0),(47.0, -1.0, 365.0, 749.0),(45.0, -145.0, 552.0, 501.0),(39.0, -1.0, 558.0, 745.0),(47.0, -1.0, 249.0, 754.0),(0.0, -145.0, 210.0, 754.0),(34.0, -1.0, 565.0, 745.0),(45.0, -1.0, 251.0, 745.0),(40.0, -1.0, 849.0, 496.0),(35.0, -1.0, 550.0, 496.0),(61.0, -18.0, 528.0, 496.0),(39.0, -145.0, 530.0, 496.0),(64.0, -145.0, 555.0, 496.0),(33.0, -1.0, 426.0, 506.0),(67.0, -20.0, 475.0, 495.0),(34.0, -17.03448275862069, 344.0, 653.0),(41.0, -18.0, 555.0, 496.0),(31.0, -18.0, 558.0, 489.0),(39.0, -18.0, 807.0, 489.0),(37.0, -1.0, 595.0, 489.0),(40.0, -141.0, 577.0, 489.0),(46.0, -1.0, 475.0, 489.0),(113.0, -78.0, 448.0, 815.0),(224.0, -84.0, 279.0, 818.0),(83.0, -76.0, 418.0, 817.0),(82.0, 293.0, 684.0, 441.0),)
WIDA=(320,427,638,574,876,853,256,386,386,512,853,299,640,299,384,610,610,610,610,610,610,610,610,610,610,341,341,640,640,640,512,1024,754,725,725,752,688,660,758,784,334,436,764,654,916,794,754,670,756,688,640,768,794,768,968,704,702,640,512,1024,512,512,512,597,555,590,555,590,590,374,597,588,296,299,586,299,866,584,597,588,588,450,532,368,580,586,828,620,602,512,512,597,512,768)
WIDH=(768,512,768,512,769,512,683,512,683,512,683,512,683,512,725,555,725,555,683,555,683,555,683,555,683,555,683,555,725,555,725,555,725,555,725,555,768,555,768,555,384,299,384,299,384,299,384,299,384,299,768)

STD_C=(120,90,820,620)
STD_VV=(320,-86,715,820)
STD_HV=(54,136,962,642)

LEFT_HV=(85,190,750,370)
RIGHT_VV=(645,-90,830,820)
COMPL=(84.0, -113, 989.0, 849.0)

def transC(rect1, rect2):
    # rect1을 rect2에 맞게 조정. rect1의 비율을 유지하지 않고 rect2의 비율을 따라감
    # used on complete hangul letter.
    dst=(rect2[2]-rect2[0],rect2[3]-rect2[1])
    mat=psMat.scale(dst[0]/(rect1[2]-rect1[0]),dst[1]/(rect1[3]-rect1[1]))
    tr2=psMat.translate(rect2[0]-rect1[0],rect2[1]-rect1[1])
    mat=psMat.compose(mat,tr2)
    return mat

def transV(rect1, rect2):
    # rect1을 rect2에 맞게 조정. rect1의 비율을 유지(긴 방향의 중심선 일치)
    # used on uncomplete hangul syllables and ascii.
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
    font[letter].clear(0)
    font[letter].clear(1)
    font[letter].importOutlines(path)
    # set width and height: ascii's are on above, others are defined as 1024
    if ext in BITMAP:
        font[letter].autoTrace()
    setPos(font, letter)
    font[letter].simplify()
    font[letter].round()
    font[letter].clear(0)
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
            os.mkdir('./fontmaker/ff_projects/'+ns.o)
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
            for i in range(33,127):
                try:
                    font[i].transform(transV(font[i].boundingBox(),AREA[i-33]))
                    font[i].width=WIDA[i-33]
                except:
                    pass
            for i in range(256,307):
                try:
                    font[i].width=WIDH[i-256]   # 고정값으로 할 수도 있음
                except:
                    pass
            name=os.path.splitext(ns.e)[0]
            font.version=1.0
            font.fontname=name
            font.familyname=name
            font.fullname=name
            font.default_base_filename=name
            font.generate(BASEPATH.format(ns.o,ns.e))
        font.save(proj)
