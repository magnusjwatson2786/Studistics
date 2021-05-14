from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QColor
import sys, random, io, shutil, calendar
import matplotlib
from datetime import timedelta
from datetime import datetime as dt
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
# import matplotlib.pyplot as figr
from PyQt5.QtWidgets import QApplication, QWidget

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#353535')#xkcd:mint green')
        self.axes = fig.add_subplot(111)
        fig.subplots_adjust(top=0.935,
                            bottom=0.125,
                            left=0.05,
                            right=0.96,
                            hspace=0.2,
                            wspace=0.2) 
        self.axes.set_facecolor('#353535')
        self.axes.grid(color='#666666',)
        self.axes.set_xlabel("Dates")
        self.axes.set_ylabel("Hours")
        self.axes.xaxis.label.set_color("#f2f2f2")
        self.axes.yaxis.label.set_color("#f2f2f2")
        self.axes.tick_params(axis='x', colors='#d9d9d9')
        self.axes.tick_params(axis='y', colors='#d9d9d9')
        # params = {'axes.labelsize': 32,'axes.titlesize':20,'legend.fontsize': 20}
            # 'axes.xmargin': 0.99,
            # 'axes.ymargin': 0.99,
            # 'axes.zmargin': 0.99,}#, 'xtick.labelsize': 28, 'ytick.labelsize': 40}
        # matplotlib.rcParams.update(params)
        # print(matplotlib.rcParams.keys())
        super(MplCanvas, self).__init__(fig)

class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.xdta=[]
        self.ydta=[]
        self.sunIndex=0
        self.monthStartIndex=0
        self.weeklyHours=0
        self.monthlyHours=0
        self.hideAnalytics=True
        self.maxAnalyticsTabWidth=500
        self.spacerHeight=150
        self.progressBarValue=(self.weeklyHours/30)*100
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        # print(self.height,self.width)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(int(0.8*self.width), int(0.8*self.height))

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        # self.canvas.grid()
        toolbar=NavigationToolbar2QT(self.canvas,MainWindow)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.hlLayout_graphandmore = QtWidgets.QHBoxLayout()
        self.hlLayout_graphandmore.setObjectName("hlLayout_graphandmore")

        # self.label_plot = QtWidgets.QLabel(self.centralwidget)
        # self.label_plot.setObjectName("label_plot")
        self.hlLayout_graphandmore.addWidget(self.canvas)

        self.analytics = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analytics.sizePolicy().hasHeightForWidth())
        self.analytics.setSizePolicy(sizePolicy)
        self.analytics.setMinimumSize(QtCore.QSize(15, 0))
        self.analytics.setMaximumSize(QtCore.QSize(25, 16777215))
        self.analytics.setObjectName("analytics")
        self.hlLayout_graphandmore.addWidget(self.analytics)
        self.analytics.clicked.connect(self.shAnalytics)
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        # self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        font1 = QtGui.QFont()
        font1.setFamily("Bahnschrift SemiLight SemiConde")
        font1.setPointSize(23)
        font2 = QtGui.QFont()
        font2.setFamily("Bahnschrift SemiLight")
        font2.setPointSize(14)
        font3 = QtGui.QFont()
        font3.setFamily("Bahnschrift SemiLight")
        font3.setPointSize(12)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setStyleSheet("color: rgb(0, 153, 255);\n"
        "/*background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));*/\n"
        "background-color: rgb(45,45,45);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font1)
        self.label_3.setMaximumSize(QtCore.QSize(self.maxAnalyticsTabWidth, 80))
        self.verticalLayout_2.addWidget(self.label_3)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(self.maxAnalyticsTabWidth, 60))
        self.label.setFont(font2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_3")
        self.label_4.setMaximumSize(QtCore.QSize(self.maxAnalyticsTabWidth, 60))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setFont(font3)
        self.verticalLayout_2.addWidget(self.label_4)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setMaximumSize(QtCore.QSize(int(0.8*self.maxAnalyticsTabWidth), 16777215))
        self.progressBar.setProperty("value", self.progressBarValue)
        self.progressBar.setObjectName("progressBar")
        # self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.progressBar)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font2)
        self.label_2.setMaximumSize(QtCore.QSize(self.maxAnalyticsTabWidth, 60))
        self.verticalLayout_2.addWidget(self.label_2)

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setFont(font3)
        self.label_5.setObjectName("label_5")
        self.label_5.setMaximumSize(QtCore.QSize(self.maxAnalyticsTabWidth, 60))
        self.label_5.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.label_5)

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.label_6.setMinimumSize(QtCore.QSize(40, 200))
        self.verticalLayout_2.addWidget(self.label_6)

        # self.spacerItem = QtWidgets.QSpacerItem(20, self.spacerHeight, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        # self.verticalLayout_2.addItem(self.spacerItem)

        self.hlLayout_graphandmore.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.hlLayout_graphandmore)

        # self.label_toolbar = QtWidgets.QLabel(self.centralwidget)
        # self.label_toolbar.setObjectName("label_toolbar")
        self.verticalLayout.addWidget(toolbar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuOptions.addAction(self.actionExit)
        self.actionExit.triggered.connect(sys.exit)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setfiles()
        self.listData()
        self.shAnalytics()
        self.canvas.axes.plot(self.xdta, self.ydta, '#007acc', marker="s")
        self.findWeeklyHours()
        self.findMonthlyHours()
        self.progressBarHandler()

    def setfiles(self):
        stream=io.StringIO()

        def getDateString(dtobj):
            return str(dtobj.strftime('%d')+":"+dtobj.strftime("%m")+":"+dtobj.strftime("%Y"))

        def getDateObj(dtstr):
            dd=int(dtstr.split(" ")[1].split(":")[0])
            mm=int(dtstr.split(" ")[1].split(":")[1])
            yy=int(dtstr.split(" ")[1].split(":")[2])
            return dt(yy, mm, dd)

        with open("fdt4.txt","r") as inf:
            count=0
            date=dt.today()
            nxtdate=dt.today()+timedelta(days=1)
            for line in inf:
                if count==0:
                    date=getDateObj(line)
                    nxtdate=date+timedelta(days=1)
                    stream.write(line)
                    # print("ct1")
                    count+=1
                    continue
                while (getDateString(getDateObj(line))!=getDateString(nxtdate)):
                    stream.write(f"0.00 {getDateString(nxtdate)}")
                    stream.write('\n')
                    date, nxtdate = nxtdate, nxtdate+timedelta(days=1)
                date, nxtdate = nxtdate, nxtdate+timedelta(days=1)
                stream.write(line)
            
            date=dt.today()
            inf.seek(0)
            nxtdate=getDateObj(inf.readlines()[-1])
            # lastdate=nxtdate
            while (getDateString(nxtdate)!=getDateString(date)):
                nxtdate=nxtdate+timedelta(days=1)
                stream.write(f"0.00 {getDateString(nxtdate)}")
                stream.write('\n')
            
            self.sunIndex=int(nxtdate.strftime('%w'))
            self.monthStartIndex=int(nxtdate.strftime('%d'))
            # print(self.sunIndex)
            # print(nxtdate-timedelta(days=int(nxtdate.strftime('%w'))))

        with io.open("fdt4.txt","w+", encoding="utf-8") as ot:
            stream.seek(0)
            shutil.copyfileobj(stream, ot)

    def listData(self):
        with open("fdt4.txt","r") as inf:
            lines=inf.readlines()
        for line in lines:
            self.xdta.append(line.split(" ")[1][:-9]+"\n"+calendar.month_abbr[int(line.split(" ")[1][3:-6])])
            self.ydta.append(float(line.split(" ")[0]))

    def findWeeklyHours(self):
        i=0
        logBack=int(self.sunIndex*(-1))
        while i>logBack:
            i-=1
            self.weeklyHours+=self.ydta[i]
        # print(self.weeklyHours)
        self.label.setText(f"Your Weekly Hours: {self.weeklyHours} hr(s)")

    def findMonthlyHours(self):
        i=0
        logBack=int(self.monthStartIndex*(-1))
        while i>logBack:
            i-=1
            self.monthlyHours+=self.ydta[i]
        # print(self.monthlyHours)
        self.label_2.setText(f"Your Monthly Hours: {round(self.monthlyHours,2)} hr(s)")
        

    def shAnalytics(self):
        _translate = QtCore.QCoreApplication.translate
        if self.verticalLayout_2.count() == 0 :
            ################################################# ADD IN CORRECT ORDER
            self.verticalLayout_2.addWidget(self.label_3)
            self.verticalLayout_2.addWidget(self.label)
            self.verticalLayout_2.addWidget(self.label_2)
            self.verticalLayout_2.addWidget(self.label_4)
            self.verticalLayout_2.addWidget(self.progressBar)
            self.verticalLayout_2.addWidget(self.label_5)
            self.verticalLayout_2.addWidget(self.label_6)
            # self.verticalLayout_2.addWidget(self.spacerItem)
            self.hideAnalytics=False
            self.analytics.setText(_translate("MainWindow", "⫸"))
        else:
            self.label.setParent(None)
            self.label_2.setParent(None)
            self.label_3.setParent(None)
            self.label_4.setParent(None)
            self.label_5.setParent(None)
            self.label_6.setParent(None)
            self.progressBar.setParent(None)
            # self.spacerItem.setParent(None)
            self.hideAnalytics=True
            self.analytics.setText(_translate("MainWindow", "⫷"))
            # print(self.hlLayout_graphandmore.count())
        
    def progressBarHandler(self):
        self.progressBarValue=(self.weeklyHours/30)*100
        if self.progressBarValue>100:
            self.progressBarValue=100
        if self.progressBarValue==100:
            self.label_5.setText("30 hrs Marker: Completed")
        self.progressBar.setValue(int(self.progressBarValue))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Studistics"))
        # self.label_plot.setText(_translate("MainWindow", "TextLabel"))
        self.analytics.setText(_translate("MainWindow", "<>"))
        self.label_3.setText(_translate("MainWindow", "Numerical Analytics"))
        self.label.setText(_translate("MainWindow", f"Your Weekly Hours: {self.weeklyHours}"))
        self.label_4.setText(_translate("MainWindow", "Your progress out of 30 hrs a week:"))
        self.label_2.setText(_translate("MainWindow", f"Your Monthly Hours: {self.monthlyHours}"))
        self.label_5.setText(_translate("MainWindow", "30 hrs Marker: Incomplete"))
        self.label_6.setText(_translate("MainWindow", ""))
        # self.label_toolbar.setText(_translate("MainWindow", "TextLabel"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle("Fusion")

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255,255,255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255,255,255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255,255,255))
    dark_palette.setColor(QPalette.Text, QColor(255,255,255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255,255,255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(142,45,197).lighter())
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    y=input()
    sys.exit(app.exec_())
