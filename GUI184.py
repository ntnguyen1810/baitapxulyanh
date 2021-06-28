import numpy as np
import sqlite3
import os
from tkinter import *
import tkinter
from tkinter import messagebox
import cv2
from time import sleep
from threading import Thread

import PIL.Image, PIL.ImageTk
from tkinter import ttk
from datetime import *



dateTime = datetime.now()


window = Tk()
window.title("Điểm Danh Sinh Viên")
p1 = PhotoImage(file = 'angel.png')
p2 = PhotoImage(file = 'Nguyen.png')

window.iconphoto(False, p1)


#Độ rộng của window
window.geometry("330x170")





# Cac tabs menu
tabControl = ttk.Notebook(window)
tabControl.grid(column=0, row=0)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Đăng Ký')
tabControl.add(tab2, text='Điểm Danh')
tabControl.add(tab3, text='Thông Tin')
tabControl.add(tab4, text='Dự Phòng 1')
tabControl.add(tab5, text='Dự Phòng 2')


#cac frame quan ly
frame0 = Frame(tab1)
frame0.grid(column=0, row=0)

lbr = Label(window,text="        ", font=("Times New Roman",30))
lbr.grid(column=2, row=0)

frame2 = Frame(tab2)
frame2.grid(column=0, row=0)

frame3 = Frame(tab3)
frame3.grid(column=0, row=0)

frame4 = Frame(tab5)
frame4.grid(column=0, row=0)




def Training():
    import main1
    tkinter.messagebox.showinfo(title="Thông Báo", message="Training Thành Công")
def Trainningtemp():
    thread1 = Thread(target=Training())
    thread1.start()

def AddDateTime():
    def AddColumn(DateTime):
        try:
            conn = sqlite3.connect('F:\Python\Prj\MLFaceDec\Datasebase\detectface.db')
            query =  "ALTER TABLE People ADD "+ "'"+str(DateTime)+"'" +" TEXT"
            conn.execute(query)
            conn.commit()
            conn.close()
        except: tkinter.messagebox.showwarning(title="Thông Báo", message="Bạn đã điểm danh rồi")




    DateTime = dateTime.strftime("Ng_%d_%m_%Y")
    AddColumn(DateTime)
def SuaBang(id):
            conn = sqlite3.connect('F:\Python\Prj\MLFaceDec\Datasebase\detectface.db')
            query = "UPDATE People SET "+dateTime.strftime("Ng_%d_%m_%Y")+"= "+"'Có Mặt'"+"  WHERE ID="+ str(id)
            conn.execute(query)
            conn.commit()
            conn.close()
def DangKy():
    try:
        def insertorUpdate(id, name, Class):

            conn = sqlite3.connect('F:\Python\Prj\MLFaceDec\Datasebase\detectface.db')
            query = "SELECT * FROM People WHERE ID=" + str(id)
            cussor = conn.execute(query)

            isRecordExist = 0

            for row in cussor:
                isRecordExist=1
            if(isRecordExist==0):
                query = "INSERT INTO People(ID, Name, Class) VALUES("+str(id)+",'"+ str(name)+"','"+str(Class)+"')"
            else:
                query = "UPDATE People SET Name ='"+ str(name)+"'"+","+"Class="+"'"+str(Class)+"' WHERE ID="+ str(id)
            conn.execute(query)
            conn.commit()
            conn.close()

        #load TV
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        #insert db

        id = txt2.get()
        name = txt0.get()
        Class =  txt1.get()

        insertorUpdate(id, name, Class)

        sampleNum=0

        while(1):
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for ( x,y,w,h) in faces :

                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                if not os.path.exists('dataSet'):
                    os.makedirs('dataSet')
                sampleNum +=1
                cv2.imwrite('dataSet\Image.'+ str(id)+'.'+str(sampleNum)+'.jpg',gray[y: y+h, x: x + w] )

            cv2.imshow('Dang Chup Anh',frame)
            cv2.waitKey(1)

            if sampleNum > 1000:
                break;
        cv2.destroyAllWindows()
        tkinter.messagebox.showwarning(title="Thông Báo", message="Lấy hình xong rồi nè !")
    except:tkinter.messagebox.showwarning(title="Thông Báo", message="Thao Tác Không Thành Công !")


def DangKytemp():
    try:
        thread0 = Thread(target=DangKy())
        thread0.start()
        thread0.join()
    except: tkinter.messagebox.showwarning(title="Thông Báo", message="Lỗi Hệ Thống !")

def NhanDangThanhCong():

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read("Facetrainning.yml")

    def getProfile(id):
        conn = sqlite3.connect('F:\Python\Prj\MLFaceDec\Datasebase\detectface.db')
        query = "SELECT * FROM People WHERE ID="+ str(id)
        cursor= conn.execute(query)

        profile = None

        for row in cursor:
            profile = row

        conn.close()
        return profile

    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    while 1:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)


        for ( x,y,w,h) in faces :

            cv2.rectangle(frame, (x, y), (x+w, y+h),(0, 255 ,0), 2)

            roi_gray= gray[y:y+h, x:x+w]

            id, confidence = recognizer.predict(roi_gray)

            if confidence < 40 :
                profile = getProfile(id)

                if(profile != None):
                    cv2.putText(frame, str(profile[1]),(x+10, y+h+30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

                    lbten.configure(text=str(profile[1]))
                    lblop.configure(text=str(profile[2]))
                    lbmasv.configure(text=str(profile[0]))



            else:
                 cv2.putText(frame,"Unknown",(x+10, y+h+30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                 lbten.configure(text="Unknown")
                 lblop.configure(text="Unknown")
                 lbmasv.configure(text="Unknown")



        cv2.imshow("Diem Danh",frame)
        if(cv2.waitKey(1) == ord('e')):
            break;

    cap.release()
    cv2.destroyAllWindows()

def Recogtemp():
    try:
        thread2 = Thread(target=NhanDangThanhCong())
        thread2.start()
        thread2.join()
    except: tkinter.messagebox.showwarning(title="Thông Báo", message="Lỗi Hệ Thống !")


#TAB 1

lb = Label(frame0, text= "Đăng Ký Thông Tin ", fg="black", font=("Times New Roman",15) )
lb.grid( column=1, row=0)

lb0 = Label(frame0, text= "Họ và tên: ", fg="black", font=("Times New Roman",15) )
lb0.grid( column=0, row=2)

lb1 = Label(frame0, text= "Lớp: ", fg="black", font=("Times New Roman",15) )
lb1.grid( column=0, row=3)

lb2 = Label(frame0, text= "Mã SV: ", fg="black", font=("Times New Roman",15) )
lb2.grid( column=0, row=4)
#them textbox
txt0 = Entry(frame0, width=20, font=("Times New Roman",15))
txt0.grid(column=1, row=2)

txt1 = Entry(frame0, width=20, font=("Times New Roman",15))
txt1.grid(column=1, row=3)

txt2 = Entry(frame0, width=20, font=("Times New Roman",15))
txt2.grid(column=1, row=4)

btn0 = Button(frame0, text="Xác nhận", width=20, font=("Times New Roman",10), command=DangKytemp)
btn0.grid(column=1, row=5)

#TAB2
lb = Label(frame2, text= "Thông Tin Sinh Viên", fg="black", font=("Times New Roman",15) )
lb.grid( column=1, row=0)

lb0 = Label(frame2, text= "Họ và tên: ", fg="black", font=("Times New Roman",15) )
lb0.grid( column=0, row=2)

lb1 = Label(frame2, text= "Lớp: ", fg="black", font=("Times New Roman",15) )
lb1.grid( column=0, row=3)

lb2 = Label(frame2, text= "Mã SV: ", fg="black", font=("Times New Roman",15) )
lb2.grid( column=0, row=4)

lbten = Label(frame2, text= "Chưa xác định", fg="black", font=("Times New Roman",15) )
lbten.grid( column=1, row=2)

lblop = Label(frame2, text= "Chưa xác định", fg="black", font=("Times New Roman",15) )
lblop.grid( column=1, row=3)

lbmasv = Label(frame2, text= "Chưa xác định", fg="black", font=("Times New Roman",15) )
lbmasv.grid( column=1, row=4)

#TAB3
ttk.Label(frame3, text="Môn:", font=("Times New Roman", 10)).grid(column=0, row=0)
subject = ttk.Combobox(frame3, width=27)

# Adding combobox drop down list
subject['values'] = (' Xử Lý Ảnh',
                     ' Mạng truyền thông CN',
                     ' Chuyên đề khoa học TA',
                     ' Điểu khiển quá trình',
                     ' Giao thông thông minh',
                     ' Trang bị điện- TĐH',
                     ' Hệ thống điều khiển Nhúng',
                     ' Mạng máy tính',
                     ' Điều khiển máy CNC',
                     ' Truyền động điện',
                     ' Điện tử công suất',
                     ' Mô hình hóa - mô phỏng')

subject.grid(column=1, row=0)
subject.current()

ttk.Label(frame3, text="Giảng Viên", font=("Times New Roman", 10)).grid(column=0, row=4)
gv = ttk.Combobox(frame3, width=27)

# Adding combobox drop down list
gv['values'] = (' Mai Vinh Dự',
                ' Nguyễn Văn Bình',
                ' Lê Mạnh Tuấn',
                ' Ngô Thị Thu Hương',
                ' Võ Thiện Lĩnh',
                ' Phí Văn Lâm',
                ' Cồ Như Văn',
                ' Lê Thị Thúy Nga',
                )

gv.grid(column=1, row=4)
gv.current()

# lay ngay thang nam tu he thong
#ThoiGian = dateTime.strftime("%d/%m/%Y, %H:%M:%S")
ThoiGian = dateTime.strftime("%d/%m/%Y")
ttk.Label(frame3, text="Thời gian:", font=("Times New Roman", 10)).grid(column=0, row=5)
ttk.Label(frame3, text=ThoiGian, font=("Times New Roman", 10)).grid(column=1, row=5)


def DiemDanh():
    # tabControl.select(tab2)
    #AddDateTime()
    # SuaBang(str(9999))
    #import main2
    pass

btn1 = Button(frame3, text="Điểm Danh", width=20, font=("Times New Roman",10), command=DiemDanh)
btn1.grid(column=1, row=6)

btn2 = Button(frame2, text="Trainning", width=20, font=("Times New Roman",10), command=Trainningtemp)
btn2.grid(column=0, row=6)

btn5 = Button(frame2, text="Điểm Danh", width=20, font=("Times New Roman",10), command=Recogtemp)
btn5.grid(column=1, row=6)

window.mainloop()

