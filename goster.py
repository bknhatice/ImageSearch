from skimage.measure import structural_similarity as ssim
import os
import numpy as np

import cv2
from PIL import Image
import imagehash
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

ekle=[]
ssim1 = []
ssimgoster=[]
mse1 = []
msegoster=[]
resimler=[]
app = Flask(__name__, static_folder="/home/hatice/PycharmProjects/Flask/static")

def resim_getir(gelen=""):
    dosyalar = []
    sozluk = []

    dizin = "./static/pictures"
    for root, dirs, files in os.walk(dizin):
        dosyalar.append([root, files])

    for k in range(1, len(dosyalar)):

        boyut = len(dosyalar[k])
        for l in range(1, boyut):

            boyut2 = len(dosyalar[k][l])
            for j in range(boyut2):
                name = str(dosyalar[k][0]) + "/" + str(dosyalar[k][l][j])
                hash = imagehash.dhash(Image.open(gelen))
                otherhash = imagehash.dhash(Image.open(name))
                fark = hash - otherhash
                sozluk.append([fark, name])
    temp = 0
    for i in range(len(sozluk)):
        for j in range(len(sozluk)):
            if (j == len(sozluk) - 1):
                break
            else:
                if (sozluk[j][0] < sozluk[j + 1][0]):
                    continue
                elif (sozluk[j][0] >= sozluk[j + 1][0]):
                    temp = sozluk[j]
                    sozluk[j] = sozluk[j + 1]
                    sozluk[j + 1] = temp
    for i in range(0, 8):
        ekle.append(sozluk[i][1])
    print(ekle)
def ssim_mse(img=""):
    dosyalar=[]
    sozluk=[]
    sozluk2 = []
    dizin = "./static/pictures"
    for root, dirs, files in os.walk(dizin):
        dosyalar.append([root, files])

    for k in range(1, len(dosyalar)):
        # print dosyalar[k]
        boyut = len(dosyalar[k])
        for l in range(1, boyut):
            # print dosyalar[k][l]
            boyut2 = len(dosyalar[k][l])
            for j in range(boyut2):
                #print dosyalar[k]+"/"+dosyalar[k][l][j]
                name = str(dosyalar[k][0]) + "/" + str(dosyalar[k][l][j])
                resimler.append(name)


    for k in range(len(resimler)):

        name = resimler[k]

        imageB = cv2.imread(name)
        dim = (150, 150)
        resizedB = cv2.resize(imageB, dim, interpolation=cv2.INTER_AREA)

        imageA = cv2.imread(img)
        resizedA = cv2.resize(imageA, dim, interpolation=cv2.INTER_AREA)

        resizedA = cv2.cvtColor(resizedA,cv2.COLOR_BGR2GRAY)
        resizedB = cv2.cvtColor(resizedB, cv2.COLOR_BGR2GRAY)
        # if resizedA.shape[0]<resizedB.shape[0]:
        #     if resizedA.shape[1]<resizedB.shape[1]:
        m = mse(resizedA, resizedB)
        s = ssim(resizedA, resizedB)

        sozluk.append([m, resimler[k]])
        sozluk2.append([s, resimler[k]])

    temp = 0
    for i in range(len(sozluk)):
        for j in range(len(sozluk)):
            if (j == len(sozluk) - 1):
                break
            else:
                if (sozluk[j][0] < sozluk[j + 1][0]):
                    continue
                elif (sozluk[j][0] >= sozluk[j + 1][0]):
                    temp = sozluk[j]
                    sozluk[j] = sozluk[j + 1]
                    sozluk[j + 1] = temp
    for i in range(0, 4):
        mse1.append(sozluk[i][1])
        msegoster.append(sozluk[i][0])

    temp1 = 0
    for i in range(len(sozluk2)):
        for j in range(len(sozluk2)):
            if (j == len(sozluk2) - 1):
                break
            else:
                if (sozluk2[j][0] >= sozluk2[j + 1][0]):
                    continue
                elif (sozluk2[j][0] < sozluk2[j + 1][0]):
                    temp1 = sozluk2[j]
                    sozluk2[j] = sozluk2[j+1]
                    sozluk2[j+1] = temp1
    for i in range(0, 4):
        ssim1.append(sozluk2[i][1])
        ssimgoster.append(sozluk2[i][0])
def mse(imageA, imageB):

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

@app.route('/upload')
def sayfa():
    return render_template('flask.html')

@app.route('/uploader',methods= ['POST','GET'])
def yukle():
    if request.method=='POST' or request.method=='GET':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        selected = request.form.get("algoritmalar")

        if selected == "image":
            resim_getir(f)
            return render_template("flask.html", gelen="resim", image="./static/" +f.filename,
                                   image1=ekle[0], image2=ekle[1],image3=ekle[2],image4=ekle[3],
                                   image5=ekle[4],image6=ekle[5],image7=ekle[6],image8=ekle[7],
                                   mesaj1="En benzer ", mesaj2="En benzer ", mesaj3="En benzer ", mesaj4="En benzer ",
                                   mesaj5="En benzer ", mesaj6="En benzer ", mesaj7="En benzer",mesaj8="En benzer")

        elif selected == "ssim":
            ssim_mse("./static/"+f.filename)
            # print ssimgoster[0],ssimgoster[1]
            # print msegoster[0], msegoster[1]

            return render_template("flask.html", gelen="ssim mse secildi", image="./static/" +f.filename,
                                   image1=ssim1[0],image2=ssim1[1],image3=ssim1[2],image4=ssim1[3],
                                   image5=mse1[0], image6=mse1[1], image7=mse1[2], image8=mse1[3],
                                   goster1=ssimgoster[0],goster2=ssimgoster[1], goster3=ssimgoster[2], goster4=ssimgoster[3],
                                   goster5=msegoster[0], goster6=msegoster[1], goster7=msegoster[2],goster8=msegoster[3],
                                   mesaj1="En benzer(SSIM) ",mesaj2="En benzer(SSIM) ",mesaj3="En benzer(SSIM) ",mesaj4="En benzer(SSIM) ",
                                   mesaj5="En az fark(MSE) ",mesaj6="En az fark(MSE) ",mesaj7="En az fark(MSE) ",mesaj8="En az fark(MSE)")


if __name__ == '__main__':
    app.run(debug=True, port=8090)