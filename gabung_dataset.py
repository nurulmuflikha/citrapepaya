import csv
import cv2
import os

def extract_data(folder_path, class_label):
    data = []
    class_mapping = {"matang": 0, "tidak matang": 1, "setengah matang": 2}
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)

            # Ekstraksi komponen warna
            blue_channel = image[:, :, 0]
            green_channel = image[:, :, 1]
            red_channel = image[:, :, 2]

            # Menambahkan data ke dalam list
            for blue, green, red in zip(blue_channel.flatten(), green_channel.flatten(), red_channel.flatten()):
                data.append([blue, green, red, class_mapping[class_label]])

    return data

def extract_all_data():
    data = []
    # Ekstraksi data untuk pepaya matang
    matang_folder = "dataset/matang/"  # Ganti dengan path folder gambar pepaya matang
    matang_data = extract_data(matang_folder, "matang")
    data.extend(matang_data)

    # Ekstraksi data untuk pepaya tidak matang
    tidak_matang_folder = "dataset/tidakmatang/"  # Ganti dengan path folder gambar pepaya tidak matang
    tidak_matang_data = extract_data(tidak_matang_folder, "tidak matang")
    data.extend(tidak_matang_data)

    # Ekstraksi data untuk pepaya setengah matang
    setengah_matang_folder = "dataset/setengahmatang/"  # Ganti dengan path folder gambar pepaya setengah matang
    setengah_matang_data = extract_data(setengah_matang_folder, "setengah matang")
    data.extend(setengah_matang_data)

    return data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Blue", "Green", "Red", "Class"])
        writer.writerows(data)
    print("Data berhasil disimpan ke", filename)

# Memanggil fungsi untuk ekstraksi data dari semua folder
data = extract_all_data()

# Menyimpan data ke dalam file CSV
save_to_csv(data, "data.csv")
