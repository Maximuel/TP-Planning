import os
from datetime import date
from tkinter import ttk
from selenium import webdriver
import time
from tkinter import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pynput.keyboard import Key, Controller
import tkinter as tk
import tkinter.font as tkFont
from tkcalendar import DateEntry


class main(object):
    addedRequests = [[],[],[],[],[]]
    addedRequestsList = []
    request_col = ["Project name", "Country", "Test item", "Due date", "Comment"]
    keyboard = Controller()

    def __init__(self, master):

        def defocus(event):
            event.widget.master.focus_set()

        def on_entry_click(event):
            """function that gets called whenever entry is clicked"""
            if self.commentList.get("1.0", 'end-1c') == 'Enter comment here...':
                self.commentList.delete("1.0", END)  # delete all the text in the entry
                self.commentList.insert("1.0", '')  # Insert blank for user input
                self.commentList.config(fg='black')

        def on_focusout(event):
            if self.commentList.get("1.0",END) == '':
                self.commentList.insert(0, 'Enter comment here...')
                self.commentList.config(fg='grey')

        # buttonsFrame = Frame(top,borderwidth=4, relief="raised")
        # buttonsFrame.place(x=300, y=500, width=120, height=20)

        # Project entry frame
        projectFrame = Frame(top, borderwidth=4, relief="raised")
        projectFrame.place(x=30, y=245, width=227, height=100)

        # Calendar frame
        calendarFrame = Frame(top, borderwidth=4, relief="raised")
        calendarFrame.place(x=267, y=245, width=210, height=100)

        # country
        frame = Frame(top, borderwidth=4, relief="raised")
        frame.place(x=30, y=355, width=447, height=200)

        # test type frame
        testTypeFrame = Frame(top, borderwidth=4, relief="raised")
        testTypeFrame.place(x=487, y=355, width=447, height=200)

        # Request button frame
        addProjectFrame = Frame(top)
        addProjectFrame.place(x=30, y=565, width=900, height=70)

        # Request button frame
        sendRequestFrame = Frame(top)
        sendRequestFrame.place(x=30, y=645, width=900, height=70)

        # List
        #listFrame = Frame(top, borderwidth=4, relief="raised")
        #listFrame.place(x=30, y=30, width=904, height=205)

        # Comment
        commentFrame = Frame(top, borderwidth=4, relief="raised")
        commentFrame.place(x=487, y=245, width=447, height=100)

        self.commentList = Text(commentFrame, height=100, width=667)
        self.commentList.insert(END, "Enter comment here...")
        self.commentList.bind('<FocusIn>', on_entry_click)
        self.commentList.bind('<FocusOut>', on_focusout)
        self.commentList.config(fg='grey')
        self.commentList.pack(side="left")
        self.commentList.pack()

        self.testTypeLabel = Label(testTypeFrame, text="Select test item")
        self.testTypeLabel.pack()

        self.countryLabel = Label(frame, text="Country")
        self.countryLabel.pack()

        self.projectEntry = Label(projectFrame, text="Project")
        self.projectEntry.place(x=88, y=15)
        self.projectEntry = ttk.Combobox(projectFrame, state="readonly", width=26, values=["SM-J105F_MEA_XSG", "SM-A515F_EUR_XX"])
        self.projectEntry.place(x=20, y=40)
        self.projectEntry.bind("<FocusIn>", defocus)

        self.calendar = Label(calendarFrame, text="Due date")
        self.calendar.place(x=72, y=15)
        self.calendar = MyDateEntry(top, date_pattern='yyyy-MM-dd')
        self.calendar._set_text(self.calendar._date.strftime('%Y-%m-%d'))
        self.calendar.place(x=322,y=287)

        self.listBoxRequests = MultiColumnListbox()

        #=====================================================================================================
        #                      Country checkboxes
        self.chbPoland = BooleanVar()
        self.countryCheckBox1 = Checkbutton(frame, variable=self.chbPoland, text="Poland")
        self.countryCheckBox1.place(x=5, y=10)

        self.chbItaly = BooleanVar()
        self.countryCheckBox2 = Checkbutton(frame, variable=self.chbItaly, text="Italy")
        self.countryCheckBox2.place(x=5, y=30)

        self.chbGermany = BooleanVar()
        self.countryCheckBox3 = Checkbutton(frame, variable=self.chbGermany, text="Germany")
        self.countryCheckBox3.place(x=5, y=50)

        self.chbFrance = BooleanVar()
        self.countryCheckBox4 = Checkbutton(frame, variable=self.chbFrance, text="France")
        self.countryCheckBox4.place(x=5, y=70)

        self.chbUK = BooleanVar()
        self.countryCheckBox5 = Checkbutton(frame, variable=self.chbUK, text="U.K.")
        self.countryCheckBox5.place(x=5, y=90)

        self.chbSpain = BooleanVar()
        self.countryCheckBox6 = Checkbutton(frame, variable=self.chbSpain, text="Spain")
        self.countryCheckBox6.place(x=5, y=110)

        self.chbSweden = BooleanVar()
        self.countryCheckBox7 = Checkbutton(frame, variable=self.chbSweden, text="Sweden")
        self.countryCheckBox7.place(x=5, y=130)

        #----------------------
        #select all button
        self.chAllButton = Button(frame, text="Check ALL",
                                    command=lambda: self.checkAllcountry())
        self.chAllButton.place(x=93 ,y=510)
        #----------------------
        #deselectALL
        self.chAllButton = Button(frame, text="Clear",
                                  command=lambda: self.uncheckAllcountry())
        self.chAllButton.place(x=163, y=275)

        self.buttonAdd = Button(addProjectFrame, width=140, height=30, text="Add request",
                                command=lambda: self.printlist())
        self.buttonAdd.pack()
        self.buttonRequest = Button(sendRequestFrame, width=140, height=30, text="Start planning",
                                    command=lambda: self.request())
        self.buttonRequest.pack()

        #===================================================================================================

        # =====================================================================================================
        #                      TestItems checkboxes
        self.chbIOT = BooleanVar()
        self.testItemCheckBox1 = Checkbutton(testTypeFrame, variable=self.chbIOT, text="IOT")
        self.testItemCheckBox1.place(x=5, y=10)

        self.chbFullTC = BooleanVar()
        self.testItemCheckBox2 = Checkbutton(testTypeFrame, variable=self.chbFullTC, text="Full Test Case")
        self.testItemCheckBox2.place(x=5, y=30)

        self.chbWA = BooleanVar()
        self.testItemCheckBox3 = Checkbutton(testTypeFrame, variable=self.chbWA, text="Widget/Application Test")
        self.testItemCheckBox3.place(x=5, y=50)

        self.chbEurExtra = BooleanVar()
        self.testItemCheckBox4 = Checkbutton(testTypeFrame, variable=self.chbEurExtra, text="EUR Extra Test")
        self.testItemCheckBox4.place(x=5, y=70)

        self.chbNetworkCheckList = BooleanVar()
        self.testItemCheckBox5 = Checkbutton(testTypeFrame, variable=self.chbNetworkCheckList, text="Network Check List")
        self.testItemCheckBox5.place(x=5, y=90)

        self.chbBMICT = BooleanVar()
        self.testItemCheckBox6 = Checkbutton(testTypeFrame, variable=self.chbBMICT, text="Base Model Issue")
        self.testItemCheckBox6.place(x=5, y=110)

        self.chbSimCardAt = BooleanVar()
        self.testItemCheckBox7 = Checkbutton(testTypeFrame, variable=self.chbSimCardAt, text="Sim Card AT")
        self.testItemCheckBox7.place(x=5, y=130)

        # ----------------------
        # select all button
        self.chAllButton = Button(frame, text="Check All",
                                  command=lambda: self.checkAllcountry())
        self.chAllButton.place(x=270, y=147, width=70, height=30)
        # ----------------------
        # deselectALL
        self.chAllButton = Button(frame, text="Clear",
                                  command=lambda: self.uncheckAllcountry())
        self.chAllButton.place(x=350, y=147, width=70, height=30)

        # ===================================================================================================

        # select all button
        self.chAllButton = Button(testTypeFrame, text="Check All",
                                  command=lambda: self.checkAllitems())
        self.chAllButton.place(x=270, y=147, width=70, height=30)
        # ----------------------
        # deselectALL
        self.chAllButton = Button(testTypeFrame, text="Clear",
                                  command=lambda: self.uncheckAllitems())
        self.chAllButton.place(x=350, y=147, width=70, height=30)

        # ===================================================================================================

    def checkAllcountry(self):
        self.countryCheckBox1.select()
        self.countryCheckBox2.select()
        self.countryCheckBox3.select()
        self.countryCheckBox4.select()
        self.countryCheckBox5.select()
        self.countryCheckBox6.select()
        self.countryCheckBox7.select()
    def uncheckAllcountry(self):
        self.countryCheckBox1.deselect()
        self.countryCheckBox2.deselect()
        self.countryCheckBox3.deselect()
        self.countryCheckBox4.deselect()
        self.countryCheckBox5.deselect()
        self.countryCheckBox6.deselect()
        self.countryCheckBox7.deselect()

    def checkAllitems(self):
        self.testItemCheckBox1.select()
        self.testItemCheckBox2.select()
        self.testItemCheckBox3.select()
        self.testItemCheckBox4.select()
        self.testItemCheckBox5.select()
        self.testItemCheckBox6.select()
        self.testItemCheckBox7.select()

    def uncheckAllitems(self):
        self.testItemCheckBox1.deselect()
        self.testItemCheckBox2.deselect()
        self.testItemCheckBox3.deselect()
        self.testItemCheckBox4.deselect()
        self.testItemCheckBox5.deselect()
        self.testItemCheckBox6.deselect()
        self.testItemCheckBox7.deselect()


    def createListOfRequest(self,project, chbPoland,chbItaly,chbGermany,chbFrance,chbUK,chbSpain,chbSweden,
                            chbFullTC,chbIOT,chbWA,chbEurExtra,chbNetworkCheckList,chbBMICT,chbSimCardAt,
                            dueDate, comment):
        listofrequest = [[], [], [], [], []]

        if chbPoland is True:
            if chbFullTC is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Poland")
                listofrequest[2].append("Full Test Case")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbIOT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Poland")
                listofrequest[2].append("IOT")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbWA is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Poland")
                listofrequest[2].append("Widgets/Applications Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbEurExtra is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Poland")
                listofrequest[2].append("EUR Extra Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbNetworkCheckList is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Poland")
                listofrequest[2].append("Network Checklist Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbBMICT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Poland")
                listofrequest[2].append("Base Model Issue Checking Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbSimCardAt is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Poland")
                listofrequest[2].append("SIM card AT Functionalities")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)

        if chbItaly is True:
            if chbFullTC is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Italy")
                listofrequest[2].append("Full Test Case")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbIOT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Italy")
                listofrequest[2].append("IOT")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbWA is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Italy")
                listofrequest[2].append("Widgets/Applications Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbEurExtra is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Italy")
                listofrequest[2].append("EUR Extra Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbNetworkCheckList is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Italy")
                listofrequest[2].append("Network Checklist Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbBMICT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Italy")
                listofrequest[2].append("Base Model Issue Checking Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbSimCardAt is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Italy")
                listofrequest[2].append("SIM card AT Functionalities")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)

        if chbGermany is True:
            if chbFullTC is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Germany")
                listofrequest[2].append("Full Test Case")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbIOT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Germany")
                listofrequest[2].append("IOT")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbWA is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Germany")
                listofrequest[2].append("Widgets/Applications Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbEurExtra is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Germany")
                listofrequest[2].append("EUR Extra Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbNetworkCheckList is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Germany")
                listofrequest[2].append("Network Checklist Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbBMICT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Germany")
                listofrequest[2].append("Base Model Issue Checking Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbSimCardAt is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Germany")
                listofrequest[2].append("SIM card AT Functionalities")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)

        if chbFrance is True:
            if chbFullTC is True:
                listofrequest[0].append(project)
                listofrequest[1].append("France")
                listofrequest[2].append("Full Test Case")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbIOT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("France")
                listofrequest[2].append("IOT")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbWA is True:
                listofrequest[0].append(project)
                listofrequest[1].append("France")
                listofrequest[2].append("Widgets/Applications Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbEurExtra is True:
                listofrequest[0].append(project)
                listofrequest[1].append("France")
                listofrequest[2].append("EUR Extra Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbNetworkCheckList is True:
                listofrequest[0].append(project)
                listofrequest[1].append("France")
                listofrequest[2].append("Network Checklist Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbBMICT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("France")
                listofrequest[2].append("Base Model Issue Checking Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbSimCardAt is True:
                listofrequest[0].append(project)
                listofrequest[1].append("France")
                listofrequest[2].append("SIM card AT Functionalities")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)

        if chbUK is True:
            if chbFullTC is True:
                listofrequest[0].append(project)
                listofrequest[1].append("UK")
                listofrequest[2].append("Full Test Case")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbIOT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("UK")
                listofrequest[2].append("IOT")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbWA is True:
                listofrequest[0].append(project)
                listofrequest[1].append("UK")
                listofrequest[2].append("Widgets/Applications Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbEurExtra is True:
                listofrequest[0].append(project)
                listofrequest[1].append("UK")
                listofrequest[2].append("EUR Extra Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbNetworkCheckList is True:
                listofrequest[0].append(project)
                listofrequest[1].append("UK")
                listofrequest[2].append("Network Checklist Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbBMICT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("UK")
                listofrequest[2].append("Base Model Issue Checking Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbSimCardAt is True:
                listofrequest[0].append(project)
                listofrequest[1].append("UK")
                listofrequest[2].append("SIM card AT Functionalities")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)

        if chbSpain is True:
            if chbFullTC is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Spain")
                listofrequest[2].append("Full Test Case")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbIOT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Spain")
                listofrequest[2].append("IOT")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbWA is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Spain")
                listofrequest[2].append("Widgets/Applications Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbEurExtra is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Spain")
                listofrequest[2].append("EUR Extra Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbNetworkCheckList is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Spain")
                listofrequest[2].append("Network Checklist Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbBMICT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Spain")
                listofrequest[2].append("Base Model Issue Checking Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbSimCardAt is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Spain")
                listofrequest[2].append("SIM card AT Functionalities")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)

        if chbSweden is True:
            if chbFullTC is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Sweden")
                listofrequest[2].append("Full Test Case")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbIOT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Sweden")
                listofrequest[2].append("IOT")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbWA is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Sweden")
                listofrequest[2].append("Widgets/Applications Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbEurExtra is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Sweden")
                listofrequest[2].append("EUR Extra Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbNetworkCheckList is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Sweden")
                listofrequest[2].append("Network Checklist Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbBMICT is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Sweden")
                listofrequest[2].append("Base Model Issue Checking Test")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)
            if chbSimCardAt is True:
                listofrequest[0].append(project)
                listofrequest[1].append("Sweden")
                listofrequest[2].append("SIM card AT Functionalities")
                listofrequest[3].append(dueDate)
                listofrequest[4].append(comment)

        return listofrequest

    def printlist(self):
        del self.addedRequestsList[:]
        listofrequest= self.createListOfRequest(self.projectEntry.get(), self.chbPoland.get(), self.chbItaly.get(),self.chbGermany.get(),self.chbFrance.get(),self.chbUK.get(),self.chbSpain.get(),self.chbSweden.get(),
                                                                         self.chbFullTC.get(),self.chbIOT.get(),self.chbWA.get(),self.chbEurExtra.get(),
                                                self.chbNetworkCheckList.get(),self.chbBMICT.get(),self.chbSimCardAt.get(),
                                                self.calendar.get(), comment=self.commentList.get("1.0", END))

        for i in range(len(listofrequest)):
            self.addedRequests[i].extend(listofrequest[i])

        for i in range(len(self.addedRequests[0])):
            self.addedRequestsList.append((self.addedRequests[0][i],self.addedRequests[1][i],self.addedRequests[2][i],self.addedRequests[3][i],self.addedRequests[4][i]))

        self.listBoxRequests = MultiColumnListbox()

    def request(self):

        ieCapabilities = DesiredCapabilities.INTERNETEXPLORER.copy()
        ieCapabilities.values()
        ieCapabilities["nativeEvents"] = False
        ieCapabilities["ignoreProtectedModeSettings"] = True
        ieCapabilities["disable-popup-blocking"] = True
        ieCapabilities["enablePersistentHover"] = True

        driver = webdriver.Ie(capabilities=ieCapabilities, executable_path=r'IEDriverServer.exe')
        driver.get("http://mdvh.sec.samsung.net/swvh/pjt/info/viewSwvhProjectList.do")
        driver.maximize_window()

        time.sleep(5)
        #driver.find_element_by_xpath("//a[@name='SET_PROJECT']").click()
        #time.sleep(2)
        driver.find_element_by_id("devModelNm").clear()
        driver.find_element_by_id("devModelNm").send_keys("J105F_MEA_XSG") #Model project name zmienna pobierana
        driver.find_element_by_id("b2_pjtRegisterDateStart").click() #czyszczenie daty mozna zostawic albo czyscic
        driver.find_element_by_id("searchBtn").click() # przycisk search
        time.sleep(2)
        driver.find_element_by_xpath("//tbody[@id='resultTableBody']/tr/td[2]/a/span").click() #project pierwszy z listy
        driver.find_element_by_xpath("/html/body/div/div/div[1]/ul/li[3]/a").click() #request test

        #switch na nowe okno
        #--------------------------------------
        time.sleep(10)
        print("sleep 10")
        driver.switch_to.window(driver.window_handles[1])
        print("nowe okno")
        time.sleep(10)
        print("sleep 10")
        #select = Select(driver.find_element_by_xpath("//select[@id='searchAreaCd']"))
        #print("szuka test regionu")
        #select.select_by_visible_text("[FTE]EUR") #wybieranie fte eur jako test region
        #print("zmiana na fte eur")
        #driver.find_element_by_id("searchBtn").click()  # przycisk search
        #print("klika search")
        #------------TEST ITEM I KRAJ--------------------------------
        testItems = driver.find_elements_by_xpath("//tbody[@id='view_list']/*/td[4]")
        country = driver.find_elements_by_xpath("//tbody[@id='view_list']/*/td[3]")
        #print("searching for "+self.testType.get() + " country "  + self.country.get())
        '''LISTOFREQUEST = self.createListOfRequest(self.chbPoland.get(), self.chbItaly.get(),self.chbGermany.get(),self.chbFrance.get(),self.chbUK.get(),self.chbSpain.get(),self.chbSweden.get(),
                                                                         self.chbFullTC.get(),self.chbIOT.get(),self.chbWA.get(),self.chbEurExtra.get()
                                                 ,self.chbNetworkCheckList.get(),self.chbBMICT.get(),self.chbSimCardAt.get())'''
        LISTOFREQUEST=self.addedRequests
        print(len(LISTOFREQUEST))
        print(len(testItems))
        print(LISTOFREQUEST)
        even=0
        odd=1

        for j in range(0,len(LISTOFREQUEST)):
            for i in range(len(testItems)):
                print("+++++++++++++++++++++++")
                #print(LISTOFREQUEST[0][j])
                #print(LISTOFREQUEST[1][j])
                print(testItems[i].text)
                print("======================")
                if LISTOFREQUEST[even][j] in country[i].text and LISTOFREQUEST[odd][j] in testItems[i].text:

                        """---------------------------"""
                        driver.find_element_by_xpath("/html/body/form/div[2]/div[5]/table/tbody/tr["+str(i+1)+"]/td[1]/input").click()
                        driver.find_element_by_xpath("//form[@id='planLayerForm']/div[2]/div[6]/div/div/span[2]/span/a").click()
                        time.sleep(4)
                        driver.switch_to.window(driver.window_handles[2])
                        time.sleep(4)
                        driver.find_element_by_xpath("//textarea[@name='saveList[0].pjtTestRequestVo.requestContent']").send_keys("jakis komentarz")
                        time.sleep(4)
                        driver.close()
                        #driver.find_element_by_xpath("//form[@id='listForm']/div/div/div/div/span/a[@onclick]").click()#close button
                        print("close")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.find_element_by_xpath("/html/body/form/div[2]/div[5]/table/tbody/tr[" + str(i + 1) + "]/td[1]/input").click()
                        break
                even+=2
                odd+=2

        #_____________KONIEC TEST ITEMU___________________

        #driver.find_element_by_xpath("//form[@id='planLayerForm']/div[2]/div[6]/div/div/span[2]/span/a").click() #request button





class ABC(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

def onExit(top):
    os.startfile("end.vbs")
    top.destroy()

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

class MyDateEntry(DateEntry):
    def __init__(self, master=None, **kw):
        DateEntry.__init__(self, master=None, **kw)
        # add black border around drop-down calendar
        self._top_cal.configure(bg='black', bd=1)
        self._top_cal.configure()
        # add label displaying today's date below
        tk.Label(self._top_cal, bg='gray90', anchor='w',
                 text='Today: %s' % date.today().strftime('%Y-%m-%d')).pack(fill='x')

    def _select(self, event=None):
        date = self._calendar.selection_get()
        if date is not None:
            self._set_text(date.strftime('%Y-%m-%d'))
            self.event_generate('<<DateEntrySelected>>')
        self._top_cal.withdraw()

        if 'readonly' not in self.state():
                self.focus_set()

class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    """def delete(self):
        selected_item = self.tree.selection()[0]  ## get selected item
        self.tree.delete(selected_item)
        selected = selected_item[-1]

        print("Przed usunieciem addedRequests: " + str(len(main.addedRequests)))
        print("Przed usunieciem request_planning_list: " + str(len(main.request_planning_list)))
        print("Przed usunieciem finalLinks: " + str(len(main.finalLinks)))
        del main.addedRequests[int(selected)-1]
        del main.request_planning_list[int(selected)-1]
        del main.finalLinks[int(selected)-1]
        print("Po usunieciu addedRequests: " + str(len(main.addedRequests)))
        print("Po usunieciem request_planning_list: " + str(len(main.request_planning_list)))
        print("Po usunieciem finalLinks: " + str(len(main.finalLinks)))
        print(main.request_planning_list)"""

    def _setup_widgets(self):
        container = ttk.Frame(borderwidth=4, relief="raised")
        container.place(x=30, y=30, width=905, height=205)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=main.request_col, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        """hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)"""
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        #hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
    def _build_tree(self):
        for col in main.request_col:
            self.tree.heading(col, text=col.title())
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))
            

        for item in main.addedRequestsList:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                """if self.tree.column(main.request_planning_col[ix],width=None)<col_w:
                    self.tree.column(main.request_planning_col[ix], width=col_w)"""

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

top = Tk()
top.protocol("WM_DELETE_WINDOW", lambda: onExit(top))

# Gets the requested values of the height and width.
windowWidth = top.winfo_reqwidth()
windowHeight = top.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(top.winfo_screenwidth() / 4 - windowWidth / 2)
positionDown = int(top.winfo_screenheight() / 4 - windowHeight / 2)

# Positions the window in the center of the page.
top.geometry("+{}+{}".format(positionRight, positionDown))
top.configure()
obj = main(top)
app = ABC(master=top)
app.master.title("Zastopic TP automatem")
top.geometry("964x745")
top.resizable(0, 0)

top.mainloop()
