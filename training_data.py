import cv2
import numpy as np
import os
import pandas as pd


def extract_data_and_save(folder_gambar, class_label, csv_filename):
    listfile = os.listdir(folder_gambar)

    for i in range(len(listfile)):
        namafile = folder_gambar + "/" + listfile[i]
        img = cv2.imread(namafile)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array([0, 48, 33])
        upper = np.array([77, 255, 212])
        mask = cv2.inRange(hsv, lower, upper)

        areaArray = []
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        im = np.copy(img)

        for n, mask in enumerate(contours):
            area = cv2.contourArea(mask)
            areaArray.append(area)
            areaLargest1 = np.argmax(areaArray)
            areaLargestMax1 = max(areaArray)
            areaLargestCnt1 = contours[areaLargest1]
            x, y, w, h = cv2.boundingRect(areaLargestCnt1)
            if y > 5 and y < 300:
                if areaLargestMax1 > 1000:
                    boundingbox = cv2.rectangle(im, (x - 1, y - 1), (x + w, y + h), (0, 255, 255), 1)

        hasilcrop = im[y: y + h, x: x + w]
        mean = np.array(hasilcrop).mean(axis=(0, 1))
        dframe = pd.DataFrame(mean)
        df = np.transpose(dframe)
        df.to_csv(csv_filename, encoding='utf-8', index=False, index_label=False, header=False, mode='a')


# Ekstraksi data dari folder pepaya matang
matang_folder = "dataset/matang"  # Ganti dengan path folder gambar pepaya matang
matang_csv = "pepaya_matang.csv"  # Nama file CSV untuk data pepaya matang
extract_data_and_save(matang_folder, "matang", matang_csv)

# Ekstraksi data dari folder pepaya tidak matang
tidak_matang_folder = "dataset/tidakmatang"  # Ganti dengan path folder gambar pepaya tidak matang
tidak_matang_csv = "pepaya_tidakmatang.csv"  # Nama file CSV untuk data pepaya tidak matang
extract_data_and_save(tidak_matang_folder, "tidak matang", tidak_matang_csv)

# Ekstraksi data dari folder pepaya setengah matang
setengah_matang_folder = "dataset/setengahmatang"  # Ganti dengan path folder gambar pepaya setengah matang
setengah_matang_csv = "pepaya_setengahmatang.csv"  # Nama file CSV untuk data pepaya setengah matang
extract_data_and_save(setengah_matang_folder, "setengah matang", setengah_matang_csv)

