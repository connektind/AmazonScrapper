# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'amazonscrapper.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import ctypes
from qtstyles import StylePicker
from selenium import webdriver
import json
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import time
#driver = webdriver.Chrome()
#driver.get("https://www.amazon.com/s/browse?_encoding=UTF8&node=16225009011&ref_=nav_shopall-export_nav_mw_sbd_intl_electronics")

j = 0
title_list = []
url_list = []
from selenium import webdriver
import xml.etree.ElementTree as ET
#driver = webdriver.Chrome()
#driver.get("https://www.amazon.com/3M-Cartridge-Respirator-Assembly-07193/dp/B00079FOK0/ref=sr_1_1?m=A3EPRARSC3P2QP&marketplaceID=ATVPDKIKX0DER&qid=1578987286&s=merchant-items&sr=1-1")
tree = ET.parse('records.xml')
record = tree.findall('records')

urllist = []
catlist = []
for i in list(tree.iter()):

    url = i.findall('url')
    cate = i.findall('category')

    for u in url:
        print(u.text)
        urllist.append(u.text)
    for c in cate:
        catlist.append(c.text)
print(urllist)
print(catlist)

mydict = dict(zip(catlist,urllist))

class Ui_MainWindow(object):

    def get_pin_code(self):


        wait = WebDriverWait(driver, 10)
        cabutton = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id='nav-main']/div[1]/div[2]/div/div[3]/span[2]/span/input")))
        #cabutton = driver.find_element_by_xpath("//*[@id='nav-main']/div[1]/div[2]/div/div[3]/span[2]/span/input")
        cabutton.click()
        wait = WebDriverWait(driver, 10)
        text = wait.until(ec.visibility_of_element_located((By.ID,'GLUXZipUpdateInput')))
        text.send_keys('27330')
        button = driver.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input')
        button.click()
        #wait = WebDriverWait(driver, 25)
        #element = WebDriverWait(driver,20).until(
        #    ec.presence_of_element_located((By.XPATH, "//*[@id='GLUXConfirmClose']")))
        #element.click()
        button2 = driver.find_element_by_id("GLUXConfirmClose")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(button2).click(button2)
        driver.implicitly_wait(5)
        self.get_url()

    def start_scrap(self):
            #try:
            self.pushButton_2.setVisible(True)
            self.pushButton.setVisible(False)
            self.pushButton_4.setVisible(True)
            self.label_5.setVisible(False)
            QApplication.processEvents()
            global driver


            category = self.comboBox.currentText()
            print(category)
            driver = webdriver.Chrome()
            flag2 = 0
            url = mydict[str(category)]
            driver.get(str(url))
            self.get_pin_code()
            #except:
            #print("Error Ocurred")
    def stop(self):

        try:
            self.label_5.setVisible(True)

            self.pushButton_4.setVisible(False)
            self.pushButton.setVisible(True)
            self.pushButton_2.setVisible(True)

            QApplication.processEvents()
            #global j
            #j = 0
            #self.label_3.setText("No. Of Pages Scrapped: " + str(j))
            global flag
            try:
                driver.close()
                driver.quit()
                flag = 1
            except:
                pass
        except:
            print("i stopped at stop")
    def restart(self):
        global driver
        self.pushButton_2.setVisible(False)
        self.pushButton.setVisible(False)
        self.pushButton_4.setVisible(True)
        print("I am inside restart")

        #with open('lasturl.json') as json_file:
        #    data = json.load(json_file)
        #print(data['URL'])
        #url = data['URL']
        pageno = self.lineEdit.text()
        url = "https://www.amazon.com/s?i=merchant-items&me=A3SBDOAENTRT1F&page={}&marketplaceID=ATVPDKIKX0DER&qid=1590045621&ref=sr_pg_{}".format(pageno,pageno)
        driver = webdriver.Chrome()
        driver.get(url)
        self.get_pin_code()
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
        print(j)
        print(type(end_value))
        if str(j) == str(end_value):
            next_button = driver.find_element_by_class_name("a-last")
            next_button.click()
            self.get_url()
        else:
            next_button = driver.find_element_by_class_name("a-last")
            next_button.click()
            print("Process End")
            self.get_url()

    def get_url(self):
        try:
            self.label_5.setVisible(False)
            print("I am inside get url")
            global next_button
            global driver
            global current_url
            global end_value
            #self.label_3.setText('Loading Website ....')


            try:
                end_value = driver.find_element_by_class_name("a-disabled").text
                end_value = int(end_value)
                print(end_value)
            except:
                print("No end value found")


            current_url = driver.current_url
            with open("data.txt",'a+') as f:
                f.write("current url is"+str(current_url))
            print("This is current URL", current_url)
            url_list.clear()
            data = {'URL': str(current_url)}
            with open('lasturl.json', 'w') as f:
                json.dump(data, f)

            QApplication.processEvents()
            product_title = driver.find_elements_by_class_name("a-text-normal")
            QApplication.processEvents()
            print('Reached here')
            global flag
            flag = 0
            for i in list(set(product_title)):
                ##self.label_3.setText('Scrapping Product ..')
                QApplication.processEvents()
                print(i.text)
                if flag == 1:
                    raise ValueError
                    break
                if str(i.get_attribute("href")) != "None":
                    print("Href value found")
                    ##self.label_3.setText('Scrapping Product ....')
                    QApplication.processEvents()
                    url_list.append(str(i.get_attribute("href")))
                    title_list.append(str(i.text))
                    QApplication.processEvents()

            #print(url_list)
            self.change_page()
        except ValueError:
            print("raised Error caught")
            self.label_5.setVisible(False)
            #except:
            #    print("stopped at get_url")
            #    self.label_5.setVisible(False)
    def change_page(self):
        global end_value
        global url_list
        print("I am inside change page")
        print(url_list)
        QApplication.processEvents()
        print(len(set(url_list)))

        print(j,url_list)
        self.label_3.setText("No. Of Pages Scrapped: " + str(j))
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
    def define_stop(self):
        print("stopped")
        self.label_5.setVisible(False)

    def find_Asin_content(self):
        try:
            content = driver.find_elements_by_class_name('content')
            print(len(content))
            flag = 0
            for i in content:
                # print("count"+str(count)+i.text)
                if "ASIN" in i.text:
                    g = i.text
                    asinno = g.find("ASIN")
                    asin = i.text[asinno + 5:asinno + 16].lstrip()
                    flag = 1
                    return asin
            if flag == 0:
                return 0
        except:
            print("error occured in asin content")


    def get_Asin(self,text):
        listth = []
        listtr = []


        table3 = driver.find_element_by_id(str(text))
        th2 = table3.find_elements_by_tag_name('th')

        for jji in th2:
            listth.append(jji.text)
        tr2 = table3.find_elements_by_tag_name('td')
        for j in tr2:
            listtr.append(j.text)

        dict1 = dict(zip(listth, listtr))
        flag = 0
        for k, v in dict1.items():
            if k == "ASIN":
                flag = 1
                return dict1['ASIN']
        if flag == 0:
            return 0

    def asinfromcontent(self):
        content = driver.find_elements_by_class_name('content')
        print(len(content))

        for i in content:
            print("i am inside for lopp")
            # print("count"+str(count)+i.text)
            if "ASIN" in i.text:
                print("i am inside adin")
                g = i.text;
                print(g)
                asinno = g.find("ASIN");
                print(asinno)
                asin = i.text[asinno + 5:asinno + 16].lstrip();
                print(asin)
                return asin

    def scrap_data(self):
        print("I am inside scrap data")
        global url_list
        feeds = []
        #print("This is url List", url_list)
        #print("This number of Items", len((url_list)))
        url_list = list(set(url_list))

        count = 0 
        for i in range(len(url_list)):
            try:
                count += 1
                if flag == 1:
                    raise ValueError
                    self.define_stop()
                    break
                QApplication.processEvents()
                driver.get(url_list[i])



                QApplication.processEvents()
                self.progressBar.setProperty("value", (int(i) / int(len(url_list))) * 100)
                category1 = ""
                #asin  = ""
                try:
                    title = driver.find_element_by_id("productTitle")
                    print("Title: ", title.text)
                    title = title.text

                    #
                    sub = driver.find_elements_by_css_selector('a.a-link-normal.a-color-tertiary')

                    category1 = sub[0].text
                    sub = sub[1].text
                    print(sub)
                    #except Exception as e:
                    #    print("category error"+str(e))



                    product_price = driver.find_element_by_id("priceblock_ourprice").text
                    print("Price: ", product_price)



                    image_url = driver.find_element_by_id("landingImage")
                    print("Image URL: ",image_url.get_attribute('src'))
                    image_url = image_url.get_attribute('src')



                    #try:
                    description_text = ""
                    description = driver.find_element_by_xpath("//*[@id='feature-bullets']/ul")
                    items = description.find_elements_by_tag_name('li')
                    for item in items:
                        description_text = description_text + str(item.text)
                        print(item.text)

                except:
                    print("Description Not Found")


                if flag == 1:
                    raise ValueError
                    self.define_stop()
                    break
                try:

                    listtable = ['productDetails_techSpec_section_1','productDetails_detailBullets_sections1','productDetails_db_sections']
                    asin = ""
                    for ii in listtable:
                        try:
                            aa = self.get_Asin(ii)
                            if aa == 0:
                                aa = None
                            else :
                                asin = aa
                        except Exception as e:
                            print("Error occuered in"+str(i)+str(e))
                except :
                    print("error occured")
                asin1 = ""
                try:
                    bbb = self.find_Asin_content()
                    if bbb != 0:
                        asin1 = bbb;print("asin1",asin1)
                except :
                    print("error occured while getting asin from content")

                if asin1:
                    asin = asin1




                category = str(self.comboBox.currentText())
                with open("dataonlyasin.txt","a+",encoding="utf-8") as f:
                    #f.write("\ncount: "+str(count)+"\n")
                    f.write(str(asin)+"\n")
                    #time.sleep(2)
                    #f.write("Title: "+str(title)+"\n")
                    #f.write("current url"+str(driver.current_url)+"\n")
                    #f.write("category"+str(category1)+"\n")
                    #f.write("subcategory"+str(sub)+"\n")
                with open("data.txt","a+",encoding="utf-8") as f:
                    #f.write("\ncount: "+str(count)+"\n")
                    f.write("\n"+str(asin)+"\n")
                    #time.sleep(2)
                    f.write("Title: "+str(title)+"\n")
                    f.write("current url"+str(driver.current_url)+"\n")
                    f.write("category"+str(category1)+"\n")
                    f.write("subcategory"+str(sub)+"\n")
                with open('data.json', mode='w', encoding='utf-8') as feedsjson:


                    entry = {'category':category1,'subcategory':sub,'title': title, 'ImageUrl': image_url, 'Price':product_price, 'Description':str(description_text),'Data':{"ASIN":str(asin)}}
                    print("entry",entry)
                    feeds.append(entry)
                    json.dump(feeds, feedsjson)

                url = QtWidgets.QTableWidgetItem("Scrapped")
                self.tableWidget.setItem(i, 2, url)
                self.tableWidget.item(i, 2).setBackground(QtGui.QColor(100, 255, 150))
                QApplication.processEvents()

            except ValueError:
                print("raised error caught")
                self.label_5.setVisible(False)
            except:
                print("Error Ocurred while appending data")
                #url = QtWidgets.QTableWidgetItem("Error")
                #self.tableWidget.setItem(i, 2, url)
                #self.tableWidget.item(i, 2).setBackground(QtGui.QColor(255, 0, 0))
                #QApplication.processEvents()
            
                
                
        url = "http://app.bookcommerce.com/api/webservice/SaveNonBookScrapperFile"
        files = {'media': open('data.json', 'rb')}
        r = requests.post(url, files=files)
        # r = requests.post(url)
        print(r.json())

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
        self.comboBox.addItems(catlist)


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


        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect((width*500)/1360, (height*20)/768, (width*111)/1360, (height*41)/768))
        self.pushButton_4.setObjectName("pushButton_2")
        self.pushButton_4.setStyleSheet(("color: rgb(255, 255, 255);\n"
                                  "background-color: rgb(83,139,174);"))
        self.pushButton_4.setText("Stop")
        self.pushButton_4.clicked.connect(self.stop)
        self.pushButton_4.setVisible(False)

        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(
            QtCore.QRect((width * 620) / 1360, (height * 20) / 768, (width * 125) / 1360, (height * 41) / 768))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet(("color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(83,139,174);"))
        self.pushButton_2.clicked.connect(self.restart)
        self.pushButton_2.setVisible(True)



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
        self.progressBar.setStyleSheet(("color: rgb(0, 0, 0);\n"
                                         "background-color: rgb(240,240,240,50);"))
        self.progressBar.setVisible(False)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect((width*30)/1360, (height*180)/768, (width*250)/1360, (height*41)/768))
        font = QtGui.QFont()
        font.setPointSize((width*11)/1360)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect((width*30)/1360, (height*220)/768, (width*250)/1360, (height*41)/768))
        font = QtGui.QFont()
        font.setPointSize((width*11)/1360)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("No. Of Products Scrapped: ")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry((width * 30) / 1360, (height * 310) / 768, (width * 40) / 1360, (height * 40) / 768)
        self.lineEdit.setStyleSheet("background-color: rgb(190, 190, 190);")
        self.lineEdit.setObjectName("lineEdit")
        font = QtGui.QFont()
        font.setPointSize((width * 11) / 1360)
        self.lineEdit.setFont(font)

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(
            QtCore.QRect((width * 30) / 1360, (height * 250) / 768, (width * 250) / 1360, (height * 41) / 768))
        font = QtGui.QFont()
        font.setPointSize((width * 11) / 1360)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("Please Enter Page Number")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(
            QtCore.QRect((width * 0) / 1360, (height * 0) / 768, (width * 1360) / 1360, (height * 768) / 768))
        self.label_5.setStyleSheet(("color: rgb(0, 0, 0);"))
        font = QtGui.QFont()
        font.setPointSize((width * 11) / 1360)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Please Wait ...")
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setVisible(False)


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
        self.label_2.setText(_translate("MainWindow", "Sellers Name "))
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
