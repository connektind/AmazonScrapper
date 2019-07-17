# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'amazonscrapper.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import ctypes
from qtstyles import StylePicker
from selenium import webdriver
import json
import requests
#driver = webdriver.Chrome()
#driver.get("https://www.amazon.com/s/browse?_encoding=UTF8&node=16225009011&ref_=nav_shopall-export_nav_mw_sbd_intl_electronics")

j = 0
title_list = []
url_list = []

class Ui_MainWindow(object):

    def start_scrap(self):

        global driver
        category = self.comboBox.currentText()
        print(category)
        driver = webdriver.Chrome()

        if category == "Automotive":
            driver.get("https://www.amazon.com/s?rh=n%3A2562090011&page=2&qid=1562735887&ref=lp_2562090011_pg_2")
        elif category == "Tools & Home Improvement":
            driver.get("https://www.amazon.com/s?rh=n%3A256643011&page=2&qid=1562830852&ref=lp_256643011_pg_2")
        elif category == "Electronics":
            driver.get("https://www.amazon.com/s?i=electronics-intl-ship&rh=n%3A%2116225009011&page=2&qid=1562830927&ref=lp_16225009011_pg_2")
        elif category == "Computers":
            driver.get("https://www.amazon.com/s?rh=n%3A16225007011&page=2&qid=1562830982&ref=lp_16225007011_pg_2")
        elif category == "Health and Household":
            driver.get("https://www.amazon.com/s?i=hpc-intl-ship&rh=n%3A%2116225010011&page=2&qid=1562831025&ref=lp_16225010011_pg_2")
        elif category == "Sports and Outdoors":
            driver.get("https://www.amazon.com/s?i=sporting-intl-ship&rh=n%3A%2116225014011&page=2&qid=1562831055&ref=lp_16225014011_pg_2")

        self.get_url()


    def restart(self):
        global driver

        print("I am inside restart")

        with open('lasturl.json') as json_file:
            data = json.load(json_file)
        print(data['URL'])
        url = data['URL']

        driver = webdriver.Chrome()
        driver.get(url)
        self.get_url()






    def back_url(self):
        print("I am inside back url")
        global driver
        global current_url
        global next_button
        global end_value
        global j

        j = j + 1
        print("This is current url",current_url)
        driver.get(current_url)

        if int(j) is not int(end_value):
            next_button = driver.find_element_by_class_name("a-last")
            next_button.click()
            self.get_url()
        else:
            print("Process End")
            self.get_url()

    def get_url(self):
        print("I am inside get url")
        global next_button
        global driver
        global current_url
        global end_value
        #self.label_3.setText('Loading Website ....')


        try:
            end_value = driver.find_element_by_class_name("a-disabled").text
            print(end_value)
        except:
            print("No end value found")


        current_url = driver.current_url
        print("This is current URL", current_url)
        url_list.clear()
        data = {'URL': str(current_url)}
        with open('lasturl.json', 'w') as f:
            json.dump(data, f)

        QApplication.processEvents()
        product_title = driver.find_elements_by_class_name("a-text-normal")
        QApplication.processEvents()
        print('Reached here')
        for i in list(set(product_title)):
            ##self.label_3.setText('Scrapping Product ..')
            QApplication.processEvents()
            print(i.text)

            if str(i.get_attribute("href")) != "None":
                print("Href value found")
                ##self.label_3.setText('Scrapping Product ....')
                QApplication.processEvents()
                url_list.append(str(i.get_attribute("href")))
                title_list.append(str(i.text))
                QApplication.processEvents()

        #print(url_list)
        self.change_page()

    def change_page(self):
        global end_value
        global url_list
        print("I am inside change page")
        print(url_list)
        QApplication.processEvents()
        print(len(set(url_list)))

        #print(j,url_list)
        #self.label_3.setText("No. Of Pages Scrapped: " + str(j))
        self.label_4.setText("No. Of Products Scrapped: " + str(len(set(url_list))))

        print("1")
        #print("I am inside change page")
        global next_button
        url_list = list(set(url_list))
        print("2")
        self.tableWidget.clearContents()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(url_list))
        r = 0
        print(url_list)
        for i in range(len(url_list)):
            QApplication.processEvents()
            col = 0
            url = QtWidgets.QTableWidgetItem(str(i))
            self.tableWidget.setItem(r, col, url)

            col = 1
            url = QtWidgets.QTableWidgetItem(str(url_list[i]))
            self.tableWidget.setItem(r, col, url)

            col = 2
            url = QtWidgets.QTableWidgetItem("Not Scrapped")
            self.tableWidget.setItem(r, col, url)
            self.tableWidget.item(r, col).setBackground(QtGui.QColor(255, 100, 150))

            r = r + 1
        self.scrap_data()

        #if int(j) is not int(end_value) :
            #next_button.click()
            #self.get_url()
        #else:
            #print("Process End")


        #    driver.get(i.get_attribute("href"))

    def scrap_data(self):
        print("I am inside scrap data")
        global url_list
        feeds = []
        #print("This is url List", url_list)
        #print("This number of Items", len((url_list)))
        url_list = list(set(url_list))

        for i in range(len(url_list)):
            QApplication.processEvents()
            driver.get(url_list[i])



            QApplication.processEvents()
            self.progressBar.setProperty("value", (int(i) / int(len(url_list))) * 100)

            try:
                title = driver.find_element_by_id("productTitle")
                print("Title: ", title.text)
                title = title.text
            except:
                print("Title Not Found")


            try:
                product_price = driver.find_element_by_id("priceblock_ourprice").text
                print("Price: ", product_price)
            except:
                print("Product Price Not Found")

            try:
                image_url = driver.find_element_by_id("landingImage")
                print("Image URL: ",image_url.get_attribute('src'))
                image_url = image_url.get_attribute('src')
            except:
                print("Image URL Not Found")



            try:
                description_text = ""
                description = driver.find_element_by_xpath("//*[@id='feature-bullets']/ul")
                items = description.find_elements_by_tag_name('li')
                for item in items:
                    description_text = description_text + str(item.text)
                    print(item.text)
            except:
                print("Description Not Found")

            url = QtWidgets.QTableWidgetItem("Scrapped")
            self.tableWidget.setItem(i, 2, url)
            self.tableWidget.item(i, 2).setBackground(QtGui.QColor(100, 255, 150))
            QApplication.processEvents()

            try:
                with open('data.json', mode='w', encoding='utf-8') as feedsjson:
                    entry = {'title': title, 'ImageUrl': image_url, 'Price':product_price, 'Description':str(description_text)}
                    feeds.append(entry)
                    json.dump(feeds, feedsjson)
            except:
                print("Error Ocurred while appending data")

        try:
            url = "http://app.bookcommerce.com/api/webservice/SaveNonBookScrapperFile"
            files = {'media': open('data.json', 'rb')}
            r = requests.post(url, files=files)
            # r = requests.post(url)
            print(r.json())
        except:
            print("Error Occured")

        self.back_url()

    def frame1(self):
        global a
        global b
        global width
        global height
        global MainWindow
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        width = w
        height = h
        print(width, height)
        a = width / 2
        b = height / 1.2
        print(a, b)

    def setupUi(self, MainWindow):
        self.frame1()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1360, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, (width*1361)/1360, (height*51)/768))
        font = QtGui.QFont()
        font.setFamily("Latha")
        font.setPointSize((width*17)/1360)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setStyleSheet(("color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(83,139,174);"))

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect((width*30)/1360, (height*80)/768, (width*750)/1360, (height*80)/768))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet(("color: rgb(0, 0, 0);\n"
                                     "background-color: rgb(220,220,220);"))

        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect((width*150)/1360, (height*20)/768, (width*211)/1360, (height*41)/768))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet(("color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(83,139,174);"))
        font = QtGui.QFont()
        font.setPointSize((width*11)/1360)
        self.comboBox.setFont(font)
        self.comboBox.addItems(['Automotive','Tools & Home Improvement','Electronics','Computers','Health and Household','Sports and Outdoors'])


        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect((width*10)/1360, (height*20)/768, (width*121)/1360, (height*41)/768))
        font = QtGui.QFont()
        font.setPointSize((width*11)/1360)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect((width*380)/1360, (height*20)/768, (width*111)/1360, (height*41)/768))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(("color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(83,139,174);"))
        self.pushButton.clicked.connect(self.start_scrap)


        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect((width*530)/1360, (height*20)/768, (width*125)/1360, (height*41)/768))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet(("color: rgb(255, 255, 255);\n"
                                  "background-color: rgb(83,139,174);"))
        self.pushButton_2.clicked.connect(self.restart)

        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(width*600, 20, 91, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet(("color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(83,139,174);"))

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect((width*800)/1360, (height*80)/768, (width*500)/1360, (height*500)/768))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect((width*800)/1360, (height*600)/768, (width*500)/1360, (height*41)/768))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(("color: rgb(0, 0, 0);"))
        self.progressBar.setVisible(True)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect((width*30)/1360, (height*180)/768, (width*200)/1360, (height*41)/768))
        font = QtGui.QFont()
        font.setPointSize((width*11)/1360)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect((width*30)/1360, (height*220)/768, (width*220)/1360, (height*41)/768))
        font = QtGui.QFont()
        font.setPointSize((width*11)/1360)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("No. Of Products Scrapped: ")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1360, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Amazon Scrapper "))
        self.label_2.setText(_translate("MainWindow", "Category: "))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.setText(_translate("MainWindow", "Restart"))
        self.pushButton_3.setText(_translate("MainWindow", "Upload"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "URL"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))

        self.label_3.setText(_translate("MainWindow", "No. Of Pages Scrapped: "))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    app.setStyleSheet(StylePicker("light-blue").get_sheet())
    sys.exit(app.exec_())
