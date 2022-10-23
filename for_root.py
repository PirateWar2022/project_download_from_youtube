# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox
from root_three import Ui_MainWindow
import threading
import prosses
from pytube import YouTube
import requests
import sys
from time import sleep
class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.Down.clicked.connect(self.append)
        self.Clear.clicked.connect(self.click_c)
        self.choose.clicked.connect(self.select)


    def click_d1(self):
        link2 = self.line_link.text()
        put = self.line_fail.text()
        self.th = prosses.Prosses(link2, put)



        if self.comboBox.currentText() == 'Audio':
            threading.Thread(target=self.th.download_only_audio).start()
            self.th.receiv.connect(self.progress)


        elif self.comboBox.currentText() == '1080p':
            threading.Thread(target=self.th.download_video_1080).start()
            self.th.receiv.connect(self.progress)


        elif self.comboBox.currentText() == '720p':
            threading.Thread(target=self.th.download_video_720).start()
            self.th.receiv.connect(self.progress)


        elif self.comboBox.currentText() == '480p':
            threading.Thread(target=self.th.download_video_480).start()
            self.th.receiv.connect(self.progress)



        elif self.comboBox.currentText() == '360p':
            threading.Thread(target=self.th.download_video_360).start()
            self.th.receiv.connect(self.progress)



    def click_c(self):
        self.line_link.setText('')
        self.comboBox.setCurrentText('1080p')
        self.textEdit.setText('')
        self.title_line.setText('')
        self.label_3.clear()


    def select(self):

        self.file = QtWidgets.QFileDialog.getExistingDirectory(self, "Select file")
        if self.file != "":
            self.line_fail.setText(self.file)
        else:
            pass

    def append(self):
        if self.line_link.text() == '':
            self.msg()

        put = self.line_link.text()
        video = YouTube(put)
        video_title = video.title
        video_description = video.description
        video_thumbnail = video.thumbnail_url
        video_url = video.js_url

        self.title_line.setText(video_title)
        self.textEdit.setText(video_description)
        self.textEdit.append(video_url)
        image = QImage()
        image.loadFromData(requests.get(video_thumbnail).content)
        self.label_3.setScaledContents(True)
        self.label_3.setPixmap(QtGui.QPixmap(image))

        self.ag()


    def msg(self):
        msg = QMessageBox()
        msg.setText("SOME ONE ERROR, CHECK EVERYTHING")
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)
        msg.setStyleSheet("background-color: rgb(0, 0, 0);")
        msg.setStyleSheet("text-color: rgb(255, 255, 255);")
        msg.exec_()

    def ag(self):
        msgBox = QMessageBox(
            QMessageBox.Question,
            "Continued",
            "Do you want download this video?",
            buttons=QMessageBox.Yes | QMessageBox.No,
        )
        msgBox.setDefaultButton(QMessageBox.Yes)
        msgBox.setStyleSheet("QLabel{background-color: white}")
        msgBox.exec_()
        reply = msgBox.standardButton(msgBox.clickedButton())
        if reply == QMessageBox.Yes:
            self.click_d1()
        else:
            self.click_c()

    def progress(self, size):
        self.progressBar.setValue(size)
        if size == 100:
            self.click_c()
            self.progressBar.setValue(0)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()