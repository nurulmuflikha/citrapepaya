# Jelaskan alur program diatas
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from sklearn.svm import SVC

ratio = 0.1
d_lower = [0, 48, 33]
d_upper = [77, 255, 212]
cek = 0

class MenuUtama(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.l_judul = tk.Label(
            self,
            text="Pilih Menu",
            height='2',
            width='300',
            bg='white'
        ).pack()
        self.b_ekstraksiFitur = tk.Button(
            self,
            text="Ekstraksi Fitur",
            command=self.ekstraksiFitur,
            height='2',
            width='30'
        ).pack(pady=20)
        self.b_realTime = tk.Button(
            self,
            text="Proses Uji",
            command=self.realTime,
            height='2',
            width='30'
        ).pack()

    def ekstraksiFitur(self):
        r_ekstraksiFitur = tk.Toplevel()
        r_ekstraksiFitur.title("Ekstraksi Fitur")
        # r_ekstraksiFitur.attributes('-zoomed', True)
        r_ekstraksiFitur.protocol("WM_DELETE_WINDOW", self.disable_event)
        w_ekstraksiFitur = EkstraksiFitur(master=r_ekstraksiFitur)

    def realTime(self):
        r_realTime = tk.Toplevel()
        r_realTime.title("Proses Uji")
        # r_realTime.attributes('-zoomed', True)
        r_realTime.protocol("WM_DELETE_WINDOW", self.disable_event)
        w_realTime = RealTime(master=r_realTime)

    def disable_event(self):
        pass


class EkstraksiFitur(tk.Frame):
    global ratio
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.initPilihGambar()
        self.initHasil()
        self.createMenus()
        r_utama.withdraw()


    def m_pilihFile(self):
        self.s_namaFile = filedialog.askopenfilename(filetypes=(('File gambar', '*.jpg'), ('All Files', '*.*')), title="Pilih gambar untuk ekstraksi fitur")
        self.e_pathGambar.insert(10, self.s_namaFile)

    def m_proses(self):
        global cek
        cek+=1
        #print(cek)
        if(self.e_pathGambar.get() != ""):
            self.f_hasilGambar.pack()
            self.f_data.pack()
            self.gambar_bgr = cv2.imread(self.e_pathGambar.get())
            self.gambar = cv2.cvtColor(self.gambar_bgr, cv2.COLOR_BGR2RGB)
            self.gambar_resize = cv2.resize(self.gambar, (0, 0), None, ratio, ratio)
            self.gambar_hsv = cv2.cvtColor(self.gambar_resize, cv2.COLOR_RGB2HSV)

            lower = np.array([d_lower[0], d_lower[1], d_lower[2]])
            upper = np.array([d_upper[0], d_upper[1], d_upper[2]])
            self.mask = cv2.inRange(self.gambar_hsv, lower, upper)

            areaArray = []
            contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.gambar_copy = np.copy(self.gambar_resize)
            for n, mask in enumerate(contours):
                area = cv2.contourArea(mask)
                areaArray.append(area)
                areaLargest1 = np.argmax(areaArray)
                areaLargestMax1 = max(areaArray)
                areaLargestCnt1 = contours[areaLargest1]
                x, y, w, h = cv2.boundingRect(areaLargestCnt1)

                if areaLargestMax1 > 200:
                    boundingbox = cv2.rectangle(self.gambar_copy, (x - 1, y - 1), (x + w, y + h), (0, 0, 255), 1)
            self.gambar_crop = self.gambar_copy[y: y + h, x:x + w]
            mean = np.array(self.gambar_crop).mean(axis=(0, 1))

            # Frame Gambar
            self.l_asli = tk.Label(self.f_hasilGambar, text="Gambar Asli").grid(row=0, column=0, padx=10)
            self.g_asli = ImageTk.PhotoImage(Image.fromarray(self.gambar_resize))
            self.l_gambarAsli = tk.Label(self.f_hasilGambar, image=self.g_asli)
            self.l_gambarAsli.grid(row=1, column=0, padx=10, pady=10)

            self.l_hsv = tk.Label(self.f_hasilGambar, text="Gambar HSV").grid(row=0, column=1, padx=10)
            self.g_hsv = ImageTk.PhotoImage(Image.fromarray(self.gambar_hsv))
            self.l_gambarHSV = tk.Label(self.f_hasilGambar, image=self.g_hsv)
            self.l_gambarHSV.grid(row=1, column=1, padx=10, pady=10)
            # self.l_gambarHSV.grid(row=1, coluImageTk.PhotoImagemn = 1, padx = 10, pady = 10)

            self.l_mask = tk.Label(self.f_hasilGambar, text="Gambar Mask").grid(row=0, column=2, padx=10)
            self.g_mask = ImageTk.PhotoImage(Image.fromarray(self.mask))
            self.l_gambarMask = tk.Label(self.f_hasilGambar, image=self.g_mask)
            self.l_gambarMask.grid(row=1, column=2, padx=10, pady=10)

            self.l_deteksi = tk.Label(self.f_hasilGambar, text="Deteksi pepaya").grid(row=0, column=3, padx=10)
            self.g_deteksi = ImageTk.PhotoImage(Image.fromarray(self.gambar_copy))
            self.l_gambarDeteksi = tk.Label(self.f_hasilGambar, image=self.g_deteksi)
            self.l_gambarDeteksi.grid(row=1, column=3, padx=10, pady=10)

            self.l_crop = tk.Label(self.f_hasilGambar, text="Crop pepaya").grid(row=0, column=4, padx=10)
            self.g_crop = ImageTk.PhotoImage(Image.fromarray(self.gambar_crop))
            self.l_gambarCrop = tk.Label(self.f_hasilGambar, image=self.g_crop)
            self.l_gambarCrop.grid(row=1, column=4, padx=10, pady=10)

            # Frame Data
            self.l_r = tk.Label(self.f_data, text="R : " + str(mean[2])).grid(row=0, column=0, padx=10)
            self.l_g = tk.Label(self.f_data, text="G : " + str(mean[1])).grid(row=1, column=0, padx=10)
            self.l_b = tk.Label(self.f_data, text="B : " + str(mean[0])).grid(row=2, column=0, padx=10)


        elif (self.e_pathGambar.get() == "") and (cek > 5):
            tk.messagebox.showwarning("Peringatan!", "Gambar belum dipilih.")

    def initPilihGambar(self):
        self.f_pilihGambar = tk.LabelFrame(
            self,
            text="Pilih Gambar",
        )
        self.f_pilihGambar.pack(
            padx=20,
            pady=5
        )

        self.f_form = tk.Frame(
            self.f_pilihGambar,
        )
        self.f_form.grid(row=0, padx=10, pady=10)

        self.f_proses = tk.Frame(
            self.f_pilihGambar,
        )
        self.f_proses.grid(row=1, padx=10, pady=10)

        # Frame form
        self.l_pilihFile = tk.Label(
            self.f_form,
            text="Path Gambar"
        )
        self.l_pilihFile.grid(row=0, column=0, padx=10, pady=10)

        self.e_pathGambar = tk.Entry(
            self.f_form,
            width=50
        )
        self.e_pathGambar.grid(row=0, column=1, padx=10)
        self.e_pathGambar.var = tk.StringVar()
        self.e_pathGambar['textvariable'] = self.e_pathGambar.var
        # self.e_pathGambar.var.trace_add('write', self.toggle_state(self))

        self.b_pilihGambar = tk.Button(
            self.f_form,
            text="Pilih",
            command=self.m_pilihFile
        )
        self.b_pilihGambar.grid(row=0, column=2, padx=10)

        # Frame button
        self.b_proses = tk.Button(
            self.f_proses,
            text="Proses",
            command=self.m_proses,
            # state='disabled'
        )
        self.b_proses.grid(row=0, column=1, sticky="nsew")

        self.b_reset = tk.Button(
            self.f_proses,
            text="Reset",
            command=self.m_reset
        )

        self.b_reset.grid(row=0, column=2, sticky="nsew")
        self.f_proses.grid_columnconfigure(0, weight=1)
        self.f_proses.grid_columnconfigure(3, weight=1)


        # ============== Lower Upper ==============
        self.f_LowerUpper = tk.LabelFrame(
            self,
            text="Lower Upper"
        )
        self.f_LowerUpper.pack(
            padx=20, pady=5
        )
        # ============== Lower ==============
        self.f_lower = tk.Frame(
            self.f_LowerUpper
        )
        self.f_lower.grid(row=0, column=0, padx=10, pady=10)
        self.l_hLower = tk.Label(self.f_lower, text="H Lower")
        self.l_hLower.grid(row=0, column=0, padx=20)
        self.s_hLower = tk.Scale(self.f_lower, from_=0, to_=255, length=300, orient='horizontal', command=self.updateLU)
        self.s_hLower.grid(row=0, column=1, padx=20)

        self.l_sLower = tk.Label(self.f_lower, text="S Lower")
        self.l_sLower.grid(row=1, column=0, padx=20)
        self.s_sLower = tk.Scale(self.f_lower, from_=0, to_=255, length=300, orient='horizontal', command=self.updateLU)
        self.s_sLower.grid(row=1, column=1, padx=20)

        self.l_vLower = tk.Label(self.f_lower, text="V Lower")
        self.l_vLower.grid(row=2, column=0, padx=20)
        self.s_vLower = tk.Scale(self.f_lower, from_=0, to_=255, length=300, orient='horizontal', command=self.updateLU)
        self.s_vLower.grid(row=2, column=1, padx=20)
        # ============== End Lower ==============

        #  ============== Upper ==============
        self.f_upper = tk.Frame(
            self.f_LowerUpper
        )
        self.f_upper.grid(row=0, column=1, padx=10, pady=10)
        self.l_hUpper = tk.Label(self.f_upper, text="H Upper")
        self.l_hUpper.grid(row=0, column=0, padx=20)
        self.s_hUpper = tk.Scale(self.f_upper, from_=0, to_=255, length=300, orient='horizontal', command=self.updateLU)
        self.s_hUpper.grid(row=0, column=1, padx=20)

        self.l_sUpper = tk.Label(self.f_upper, text="S Upper")
        self.l_sUpper.grid(row=1, column=0, padx=20)
        self.s_sUpper = tk.Scale(self.f_upper, from_=0, to_=255, length=300, orient='horizontal', command=self.updateLU)
        self.s_sUpper.grid(row=1, column=1, padx=20)

        self.l_vUpper = tk.Label(self.f_upper, text="V Upper")
        self.l_vUpper.grid(row=2, column=0, padx=20)
        self.s_vUpper = tk.Scale(self.f_upper, from_=0, to_=255, length=300, orient='horizontal', command=self.updateLU)
        self.s_vUpper.grid(row=2, column=1, padx=20)
        # ============== End Upper ==============

        # ============== Set Default Lower Upper ==============
        self.s_hLower.set(d_lower[0])
        self.s_sLower.set(d_lower[1])
        self.s_vLower.set(d_lower[2])

        self.s_hUpper.set(d_upper[0])
        self.s_sUpper.set(d_upper[1])
        self.s_vUpper.set(d_upper[2])
        # ============== END Set Default Lower Upper ==============
        # ============== END Lower Upper ==============

    def initHasil(self):
        self.f_hasilGambar = tk.LabelFrame(
            self,
            text="Hasil"
        )
        self.f_hasilGambar.pack(
            padx=20,
            pady=5
        )
        self.f_hasilGambar.pack_forget()


        self.f_gambar = tk.Frame(
            self.f_hasilGambar
        )
        self.f_gambar.grid(row=0, padx=10, pady=10)

        self.f_data = tk.LabelFrame(
            self,
            text="Data RGB"
        )
        self.f_data.pack(
            padx=20,
            pady=5
        )
        self.f_data.pack_forget()
        self.f_dataRGB = tk.Frame(
            self.f_data
        )
        self.f_dataRGB.grid(row=0, padx=10, pady=10)

    def m_reset(self):
        self.e_pathGambar.delete(0, 'end')
        self.f_hasilGambar.pack_forget()
        self.f_data.pack_forget()

    def toggle_state(*_, self):
        if self.e_pathGambar.var.get():
            self.b_proses['state'] = 'normal'
        else:
            self.b_proses['state'] = 'disabled'

    def createMenus(self):
        top = self.winfo_toplevel()
        self.menuBar = tk.Menu(top)
        top['menu'] = self.menuBar

        self.subMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Menu', menu=self.subMenu)
        self.subMenu.add_command(label='Kembali ke Main', command=self.backMain)
        self.subMenu.add_command(label='Exit', command=self.exitEkstraksiFitur)

    def updateLU(self, args):
        global d_lower, d_upper
        d_lower[0] = self.s_hLower.get()
        d_lower[1] = self.s_sLower.get()
        d_lower[2] = self.s_vLower.get()

        d_upper[0] = self.s_hUpper.get()
        d_upper[1] = self.s_sUpper.get()
        d_upper[2] = self.s_vUpper.get()

        self.m_proses()

    def backMain(self):
        r_utama.deiconify()
        self.master.destroy()

    def exitEkstraksiFitur(self):
        self.master.destroy()
        r_utama.destroy()

class RealTime(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        r_utama.withdraw()

    def createWidgets(self):
        self.initPilihData()
        self.initHasil()
        self.createMenus()

    def initPilihData(self):
        self.f_pilihData = tk.LabelFrame(
            self,
            text="Pilih Data"
        )
        self.f_pilihData.pack(
            padx=20,
            pady=5
        )
        self.f_formPilihData = tk.Frame(
            self.f_pilihData
        )
        self.f_formPilihData.grid(row=0, padx=10, pady=10)

        self.f_formTombol = tk.Frame(
            self.f_pilihData
        )
        self.f_formTombol.grid(row=1, padx=10, pady=10)

        # Frame EditText
        self.l_pilihCSV = tk.Label(
            self.f_formPilihData,
            text="Path CSV"
        )
        self.l_pilihCSV.grid(row=0, column=0, padx=10, pady=10)
        self.e_pathCSV = tk.Entry(
            self.f_formPilihData
        )
        self.e_pathCSV.grid(row=0, column=1, padx=10)
        self.e_pathCSV.var = tk.StringVar()
        self.e_pathCSV['textvariable'] = self.e_pathCSV.var
        self.b_pilihCSV = tk.Button(
            self.f_formPilihData,
            text="Pilih",
            command=self.m_pilihCSV
        )
        self.b_pilihCSV.grid(row=0, column=2, padx=10)

        self.l_pilihVideo = tk.Label(
            self.f_formPilihData,
            text="Path Gambar"
        )
        self.l_pilihVideo.grid(row=1, column=0, padx=10, pady=10)
        self.e_pathVideo = tk.Entry(
            self.f_formPilihData
        )
        self.e_pathVideo.grid(row=1, column=1, padx=10)
        self.e_pathVideo.var = tk.StringVar()
        self.e_pathVideo['textvariable'] = self.e_pathVideo.var
        self.b_pilihVideo = tk.Button(
            self.f_formPilihData,
            text="Pilih",
            command=self.m_pilihVideo
        )
        self.b_pilihVideo.grid(row=1, column=2, padx=10)
        # END Freme EditText

        # Frame Button
        self.b_proses = tk.Button(
            self.f_formTombol,
            text="Proses",
            command=self.m_proses,
            # state='disabled'
        )
        self.b_proses.grid(row=0, column=1, sticky="nsew")

        self.b_reset = tk.Button(
            self.f_formTombol,
            text="Reset",
            command=self.m_reset
        )

        self.b_reset.grid(row=0, column=2, sticky="nsew")
        self.f_formTombol.grid_columnconfigure(0, weight=1)
        self.f_formTombol.grid_columnconfigure(3, weight=1)


    def m_pilihVideo(self):
        self.s_fileVideo = filedialog.askopenfilename(filetypes=(('File Video', '*.jpg'), ('All Files', '*.*')), title="Pilih gambar uji")
        self.e_pathVideo.insert(10, self.s_fileVideo)


    def m_pilihCSV(self):
        self.s_fileData = filedialog.askopenfilename(filetypes=(('File CSV', '*.csv'), ('All Files', '*.*')), title="Pilih data fitur dalam csv")
        self.e_pathCSV.insert(10, self.s_fileData)

    def createMenus(self):
        top = self.winfo_toplevel()
        self.menuBar = tk.Menu(top)
        top['menu'] = self.menuBar

        self.subMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Menu', menu=self.subMenu)
        self.subMenu.add_command(label='Kembali ke Main', command=self.backMain)
        self.subMenu.add_command(label='Exit', command=self.exitEkstraksiFitur)

    def backMain(self):
        r_utama.deiconify()
        self.master.destroy()

    def exitEkstraksiFitur(self):
        self.master.destroy()
        r_utama.destroy()

    def m_proses(self):
        if (self.e_pathVideo.get() != "") and (self.e_pathCSV.get() != ""):
            self.f_hasilProses.pack()
            datastroberi = pd.read_csv(self.e_pathCSV.get())
            x = datastroberi.drop('Class', axis=1)
            y = datastroberi['Class']
            self.svclassifier = SVC(kernel='rbf', gamma=0.001, C=10)

            self.svclassifier.fit(x, y)
            hasilcrop = 1

            # self.l_weight = tk.Label(self.f_formData, text="Weight: " + str(self.svclassifier.coef_)).grid(row=0, column=0, padx=10)

            self.l_bias = tk.Label(self.f_formData, text="Bias: " + str(self.svclassifier.intercept_)).grid(row=1, column=0, padx=10)
            self.l_support_vector= tk.Label(self.f_formData, text="number of support vector for each class: " + str(self.svclassifier.n_support_)).grid(row=2, column=0, padx=10)
            # self.l_support_vector= tk.Label(self.f_formData, text="support vector" + str(self.svclassifier.support_)).grid(row=3, column=0, padx=10)

            self.vid = MyVideoCapture(self.e_pathVideo.get())
            self.delay = 15
            self.update()


        elif (self.e_pathCSV.get() == ""):
            tk.messagebox.showwarning("Peringatan!", "Data CSV belum dipilih.")
        elif (self.e_pathVideo.get() == ""):
            tk.messagebox.showwarning("Peringatan!", "Data gambar uji belum dipilih.")

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            ratio = .4
            frame = cv2.resize(frame, (0, 0), None, ratio, ratio)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower = np.array([0, 48, 33])
            upper = np.array([77, 255, 212])
            mask = cv2.inRange(hsv, lower, upper)

            areaArray = []
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            im = np.copy(frame)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            hsv_2 = np.copy(hsv)
            for n, mask in enumerate(contours):
                area = cv2.contourArea(mask)
                areaArray.append(area)
                areaLargest = np.argmax(areaArray)
                areaLargestMax = max(areaArray)
                areaLargestCnt = contours[areaLargest]
                x, y, w, h = cv2.boundingRect(areaLargestCnt)
                if y > 5 and y < 300:
                    if area == areaLargestMax and area > 400:

                        cv2.rectangle(im, (x - 1, y - 1), (x + w, y + h), (0, 0, 255), 1)
                        cv2.rectangle(hsv_2, (x - 1, y - 1), (x + w, y + h), (0, 0, 255), 1)
                        hasilcrop = frame[y:y + h, x:x + w]
                        mean = np.array(hasilcrop).mean(axis=(0, 1))
                        dframe = pd.DataFrame(mean)
                        df = np.transpose(dframe)

                        y_hasil = self.svclassifier.predict(df)
                        if (y_hasil[0] == 1):
                            cv2.putText(im, "matang", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                                                      (0, 0, 255), 1)
                        elif (y_hasil[0] == 2):
                            cv2.putText(im, "Setengah matang", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX,
                                                      1, (0, 0, 255), 1)
                        elif (y_hasil[0] == 3):
                            cv2.putText(im, "Belum matang", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                                                      (0, 0, 255), 1)
                        else:
                            cv2.putText(im, "Data tidak diketahui", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1,
                                                      (0, 0, 255), 1)
                        cv2.putText(im, str(mean), (0, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            self.video = ImageTk.PhotoImage(Image.fromarray(im))
            self.videoShow = tk.Label(self.f_formVideo, image=self.video)
            self.videoShow.configure(image=self.video)
            self.videoShow.grid(row=0, column=0, padx=30, pady=30)

        self.master.after(self.delay, self.update)

    def m_reset(self):
        self.e_pathVideo.delete(0, 'end')
        self.e_pathCSV.delete(0, 'end')

    def initHasil(self):
        self.f_hasilProses = tk.LabelFrame(
            self,
            text="Hasil"
        )
        self.f_hasilProses.pack(
            padx=20,
            pady=5
        )
        self.f_hasilProses.pack_forget()

        self.f_formData = tk.Frame(
            self.f_hasilProses
        )
        self.f_formData.grid(row=0, padx=10, pady=10)
        self.f_formVideo = tk.Frame(
            self.f_hasilProses
        )
        self.f_formVideo.grid(row=1, padx=10, pady=10)

class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open gambar source", video_source)

         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 return (ret, frame)
             else:
                 return (ret, None)
         else:
             return (None, None)
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()

r_utama = tk.Tk()
r_utama.title("Aplikasi Klasifikasi Kematangan Pepaya")
r_utama.geometry('300x300')
w_utama = MenuUtama(master=r_utama)
w_utama.mainloop()