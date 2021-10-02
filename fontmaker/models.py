from django.db import models
from django.conf import settings
import os, subprocess

import sys, base64

sys.path.append('.')

from fontmaker import svgParser, imgProc

ASCII = {'\\': 'BSLASH', '/': 'SLASH', ':': 'COLON', '?': 'QUEST', '%': 'PERCENT', '*': 'ASTER', '|': 'BAR',
         '.': 'PERIOD', '<': 'LT', '>': 'GT', '"': 'DOUBLE', "'": 'SINGLE'}
ASCIIR = {ASCII[k]: k for k in ASCII}


class Proj(models.Model):  # fontforge 프로젝트 파일을 통한 관리.
    name = models.CharField(max_length=255)  # 프로젝트 이름
    isK = models.BooleanField()  # True: 한글 포함, False: 아스키만
    soul = models.GenericIPAddressField(
        null=True)  # 비로그인 시, 자동으로 IP와 프로젝트를 연결. 사실상 일대일 연결이며 하던 중 id를 생성하는 경우
    # 옮길 수 있도록 기능 제공하며 이게 null이 아닌 경우 Ownership 연결은 없음
    SUB = ['fontforge', '-script', './fontmaker/ff.py', '-o']  # ff.py 부분 수정 필요
    fullSet = set(chr(x) for x in range(ord('가'), ord('힣') + 1))

    def initialSetting(self):  # 데이터 생성 후 바로 적용
        vp = Proj.SUB[:]
        if self.isK:
            vp.extend([self.name, '--h'])
        else:
            vp.extend([self.name])
        out, err = subprocess.Popen(vp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        # return err  # err 없는 경우 길이는 371

    def export(self, name, format='.ttf'):  # 폰트 파일 내옴. 이런 식으로 파일을 내오는 구문은 subprocess를 이용한 IPC가 필수적
        vp = Proj.SUB[:]
        vp.extend([self.name, '-e', name + format])  # 파일 이름으로 불가능한 문자 거르는 작업 필요
        out, err = subprocess.Popen(vp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return err if err else ''  # 에러 없는 경우: 파일 위치를 리턴

    def getImageOf(self, letter, format='.svg'):  # 글자 이미지 추출
        code=letter
        letter=chr(int(code))
        vp = Proj.SUB[:]
        if format == '.svg':
            vp.extend([self.name, '-v', code])
        else:
            vp.extend([self.name, '-p', code])
        out, err = subprocess.Popen(vp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if len(err) > 371:
            return err
        else:
            fileName = self.convertFileName(letter, format)
            if format == '.png':
                imgProc.padOut(fileName)
        return fileName

    def setImageOf(self, data, letter, format='.svg'):  # 글자 세팅(벡터, 비트맵 모두 가능). 이미지가 업로드된 이후에 호출됨. format은 안 쓸 수도 있음
        vp = Proj.SUB[:]
        fileName = self.convertFileName(letter, format)

        data=base64.b64decode(data)

        if format in {'.bmp','.xbm','.jpg'}:
            fileName = self.convertFileName(letter, '.png')
            imgProc.encode2Png(data,fileName)
            format='.png'
        else:
            image = open(fileName, "wb")
            image.write(data)
            image.close()

        if format =='.png':
            imgProc.transparent2white(fileName)

        vp.extend([self.name, '-a', fileName])
        out, err = subprocess.Popen(vp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('OuT: ',out.decode('cp949'))
        print("err: ", err[371:])
        os.remove(fileName)

    def convertFileName(self, letter, format):
        if letter in ASCIIR:
            letter=ASCIIR[letter]
        letter=str(ord(letter))
        fileName = './fontmaker/ff_projects/{}/{}'.format(self.name, letter + format)

        return fileName


    def unDone(self):  # 완성되지 않은 글자 목록
        vp = Proj.SUB[:]
        vp.extend([self.name, '--ua'])
        if self.isK:
            vp.append('--uk')
        out, err = subprocess.Popen(vp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return err if len(err) > 371 else out.decode('cp949')

    def autoDraw(self):  # 자동완성. 이 함수의 본 내용물은 다른 모듈로 분리할 것, 또한 이 함수를 호출할 떄는 반드시 부 스레드를 생성한 후 부를 것
        if not self.isK:
            return
        unDone = set(self.unDone())
        unDone.discard(' ')
        unDone.discard('\n')
        done = Proj.fullSet - unDone
        feat = svgParser.CharacterFeature()
        for gl in done:
            path = self.getImageOf(gl)
            feat.addFeature(gl, path)  # 특성추출기: 음소별, 글자별, 전체
            os.remove(path)
        for gl in unDone:
            path = feat.gen(gl, self.name)
            self.setImageOf(path)
            os.remove(path)


class HUser(models.Model):  # ID와 PW로 로그인. 동일 IP에서 로그아웃된 상태로 다른 계정 생성 시도하는 경우, 기존에 존재하는 계정을 알려줄 것
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='handle')  # Django 기본 사용자 클래스
    name = models.CharField(max_length=30)  # 사용자가 직접 정하는 이름(중복 불가능)
    ip = models.GenericIPAddressField()

    def allProj(self):
        return [p.proj.name for p in self.projects.all()]


class OwnerShip(models.Model):
    proj = models.ForeignKey(Proj, related_name="coop", on_delete=models.CASCADE)  # 프로젝트
    user = models.ForeignKey(HUser, related_name="projects", on_delete=models.CASCADE)  # 사용자
    level = models.IntegerField(default=0)  # 권한
    '''
    프로젝트 주인(2): 폰트 편집, 내려받기 및 사용자 초대 및 추방 가능, 타 사용자 권한 변경 가능(최대 1), 주인이 프로젝트 포기 시 다른 사람이 주인이 되며 남은 사람이 없는 경우 프로젝트는 서버에서 제거
    1등급 프로젝트 참여자(1): 폰트 편집, 내려받기 및 사용자 초대 가능
    2등급 프로젝트 참여자(0): 폰트 편집, 내려받기 가능
    '''
