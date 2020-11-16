# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AIcam.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
#Author: Andrés Puerto Lara

import cv2
import numpy as np
import time
import os 
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import smtplib
from email.mime.text import MIMEText
import ssl


labelsPath="coco.names"
yolo_conf="yolov3.cfg"
yolo_weights="yolov3.weights"

def get_detections(layerOutputs,W,H,frame,conf,threshold,alarm,class_interest):
  boxes = []
  confidences = []
  classIDs = []
  LABELS = open(labelsPath).read().strip().split("\n")
  COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
  flag=False
  for output in layerOutputs:
  
    for detection in output:
      
      scores = detection[5:]
      classID = np.argmax(scores)
      confidence = scores[classID]
   
      
      if confidence > conf:
        
        box = detection[0:4] * np.array([W, H, W, H])
        (centerX, centerY, width, height) = box.astype("int")
   
        
        x = int(centerX - (width / 2))
        y = int(centerY - (height / 2))
   
       
        boxes.append([x, y, int(width), int(height)])
        confidences.append(float(confidence))
        classIDs.append(classID)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf,threshold)
        if len(idxs) > 0:
  
          for i in idxs.flatten():
            
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
               
                  
            color = [int(c) for c in COLORS[classIDs[i]]]
            #cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
            if alarm==True and LABELS[classIDs[i]]==class_interest:
                return True

def time_conversion():
    now=datetime.datetime.now()
    now_v=str(now).split(" ")
    hour=now_v[1].split(":")
    hour_n=datetime.datetime.strptime(hour[0]+':'+hour[1],'%H:%M').strftime('%I:%M %p')
    r_hour=hour_n.split(" ")
    l_hour=r_hour[0].split(":")
    if int(l_hour[0])<10:
        l_hour[0]=str(int(l_hour[0]))
    hour_n=l_hour[0]+":"+l_hour[1]+" "+r_hour[1]
       
    return hour_n
def load_classes():
	    classes=[]
	    file=open(labelsPath)
	    classes=file.read().split("\n")
	    return classes
def send_email(sender,passwd,receiver,msg,pic):
    msg=MIMEText(msg)
    server=smtplib.SMTP('smtp.gmail.com',587)
    context=ssl.create_default_context()
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
      
    msg['Subject']="Alert from your Ipcam"
    try:
        server.login(sender,passwd)
        server.sendmail(sender,receiver,msg.as_string())
        print("Message sent")
    except Exception as e:
        print(e)

    


    return False


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(517, 410)
        Form.setWindowTitle("")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(410, 350, 91, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.ai_process)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(130, 40, 311, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 40, 121, 20))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(130, 180, 141, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(load_classes())
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 220, 311, 171))
        self.groupBox.setObjectName("groupBox")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(0, 80, 131, 17))
        self.label_6.setObjectName("label_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 70, 141, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(0, 40, 101, 17))
        self.label_5.setObjectName("label_5")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 30, 141, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 110, 141, 25))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(0, 120, 111, 17))
        self.label_7.setObjectName("label_7")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 90, 271, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 67, 17))
        self.label_3.setObjectName("label_3")
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.groupBox_2)
        self.timeEdit_2.setGeometry(QtCore.QRect(120, 50, 141, 26))
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 67, 17))
        self.label_2.setObjectName("label_2")
        self.timeEdit = QtWidgets.QTimeEdit(self.groupBox_2)
        self.timeEdit.setGeometry(QtCore.QRect(120, 20, 141, 26))
        self.timeEdit.setObjectName("timeEdit")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 67, 17))
        self.label_4.setObjectName("label_4")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(350, 110, 71, 23))
        self.checkBox.setObjectName("checkBox")
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.pushButton.raise_()
        self.lineEdit.raise_()
        self.label.raise_()
        self.comboBox.raise_()


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("Form", "Start"))
        self.label.setText(_translate("Form", "Ipcam address"))
        self.groupBox.setTitle(_translate("Form", "Communication"))
        self.label_6.setText(_translate("Form", "Password (Sender)"))
        self.label_5.setText(_translate("Form", "Email (Sender)"))
        self.label_7.setText(_translate("Form", "Email (Receiver)"))
        self.groupBox_2.setTitle(_translate("Form", "Alarm configuration"))
        self.label_3.setText(_translate("Form", "End"))
        self.label_2.setText(_translate("Form", "Start"))
        self.label_4.setText(_translate("Form", "Class"))
        self.checkBox.setText(_translate("Form", "GPU"))
    def ai_process(self):
        
        start_t=self.timeEdit.text()
        end_t=self.timeEdit_2.text()

        start_t=start_t.replace(".","")

        end_t=end_t.replace(".","")
        cap = cv2.VideoCapture(self.lineEdit.text())
        if (cap.isOpened() == False):
            print("Unable to read camera feed")
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        np.random.seed(42)
        out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        net = cv2.dnn.readNetFromDarknet(yolo_conf, yolo_weights)
        cuda=1;
        if  self.checkBox.isChecked():
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        conf=0.5
        threshold=0.3
        alarm=False
        start_splitted=start_t.split(" ")
        AM=start_splitted[1]+start_splitted[2]
        start_t=start_splitted[0]+" "+AM
        end_splitted=end_t.split(" ")
        PM=end_splitted[1]+end_splitted[2]
        end_t=end_splitted[0]+" "+PM

         
        class_interest=self.comboBox.currentText()
        print("Program started at: "+time_conversion())
        print("Object of interest : " +class_interest)
        print("Alarm starts: "+start_t)
        print("Alarm ends: "+end_t)
        #print(self.lineEdit_2.text())
        #print(self.lineEdit_3.text())
        cont_class=0
        email_time=0
        istime=True
        while(True):
            ret, frame = cap.read()

            
            if start_t==time_conversion():
                alarm=True
                #print("Alarma encendida")
            elif end_t==time_conversion():
                alarm=False
                #print("Alarma apagada")
            elif start_t==end_t:
            	alarm=True

            if ret == True:
                (H, W) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),  swapRB=True, crop=False)
                net.setInput(blob)
                layerOutputs = net.forward(ln)
                
                flag=get_detections(layerOutputs,W,H,frame,conf,threshold,alarm,class_interest)
                
                
                if flag==True and cont_class<=20:
                    
                    cv2.imwrite("detected_classes/"+class_interest+str(datetime.datetime.now())+".jpg",frame)
                    cont_class=cont_class+1
                    print(class_interest+" detected, ..")
                    msg=class_interest+" detected at "+str(datetime.datetime.now())
                    pic=0
                    
                    if alarm==True and istime==True:

                        send_email(str(self.lineEdit_2.text()),str(self.lineEdit_3.text()),str(self.lineEdit_4.text()),msg,pic)
                        #print("email enviado")
                        istime=False
                        email_time=time.time()
                        #print("se deshabilita el envio de email")

                else:
                    cont_class=0
                if time.time()-email_time>=300 and istime==False:
                    istime=True
                    #print("Se habilita el envio de email")

                out.write(frame)
                cv2.imshow('Video',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows() 

    	
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    
    sys.exit(app.exec_())
