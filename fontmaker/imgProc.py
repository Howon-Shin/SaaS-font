import cv2
import numpy as np

def padOut(fileName):
    def pad(base: np.ndarray):
        h,w,_=base.shape  # AttributeError: 'NoneType' object has no attribute 'shape'
        # 나한텐 여기서 에러생김
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

    base=pad(cv2.imread(fileName))
    cv2.imwrite(fileName, base)
