import cv2
import numpy as np

def encode2Png(data, fileName):
    data=np.frombuffer(data, dtype=np.uint8)
    img=cv2.imdecode(data,cv2.IMREAD_COLOR)
    if cv2.imwrite(fileName,img):
        return fileName

def reEncode(fileName, afterName):
    cv2.imwrite(afterName, cv2.imread(fileName))

def transparent2white(fileName):
    data=cv2.imread(fileName, cv2.IMREAD_UNCHANGED)
    if data.shape[2]<4:
        return
    transMask=data[:,:,3]<255
    data[transMask]=(255,255,255,255)
    cv2.cvtColor(data,cv2.COLOR_BGRA2BGR,data)
    cv2.imwrite(fileName,data)

def padOut(fileName):
    def pad(base: np.ndarray):
        h,w,_=base.shape
        lrpad=max(0,(400-w)//2)
        udpad=max(0,(400-h)//2)
        if lrpad:
            sh=list(base.shape)
            sh[1]=lrpad
            base=np.concatenate([np.zeros(sh, dtype=np.uint8)+255, base, np.zeros(sh, dtype=np.uint8)+255], axis=1)
        if udpad:
            sh=list(base.shape)
            sh[0]=udpad
            base=np.concatenate([np.zeros(sh, dtype=np.uint8)+255, base, np.zeros(sh, dtype=np.uint8)+255], axis=0)
        return base
    
    def crop(base: np.ndarray):
        h,w,_=base.shape
        nw=base.min(axis=2)
        fud=(nw.min(axis=1)==255).astype(np.uint8)
        flr=(nw.min(axis=0)==255).astype(np.uint8)
        ltip=flr.argmin()
        rtip=w-flr[::-1].argmin()
        utip=fud.argmin()
        dtip=h-fud[::-1].argmin()
        return base[utip:dtip, ltip:rtip]

    print(fileName)
    base=pad(crop(cv2.imread(fileName)))
    cv2.imwrite(fileName, base)
