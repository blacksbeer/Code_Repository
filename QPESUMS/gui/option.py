# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'option.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(460, 330)
        Dialog.setMinimumSize(QtCore.QSize(460, 330))
        Dialog.setMaximumSize(QtCore.QSize(460, 330))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        Dialog.setFont(font)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(110, 280, 251, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_true = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_true.setObjectName("pushButton_true")
        self.horizontalLayout_2.addWidget(self.pushButton_true)
        self.pushButton_false = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_false.setObjectName("pushButton_false")
        self.horizontalLayout_2.addWidget(self.pushButton_false)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 441, 251))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget_location = QtWidgets.QTableWidget(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tableWidget_location.setFont(font)
        self.tableWidget_location.setStyleSheet("")
        self.tableWidget_location.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhFormattedNumbersOnly)
        self.tableWidget_location.setRowCount(20)
        self.tableWidget_location.setObjectName("tableWidget_location")
        self.tableWidget_location.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_location.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_location.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_location.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tableWidget_location.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tableWidget_location.setItem(0, 1, item)
        self.tableWidget_location.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget_location.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget_location.verticalHeader().setVisible(False)
        self.tableWidget_location.verticalHeader().setDefaultSectionSize(16)
        self.tableWidget_location.verticalHeader().setMinimumSectionSize(16)
        self.gridLayout.addWidget(self.tableWidget_location, 2, 1, 1, 1)
        self.label_location = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_location.setObjectName("label_location")
        self.gridLayout.addWidget(self.label_location, 2, 0, 1, 1)
        self.lineEdit_databaseurl = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_databaseurl.setText("")
        self.lineEdit_databaseurl.setObjectName("lineEdit_databaseurl")
        self.gridLayout.addWidget(self.lineEdit_databaseurl, 0, 1, 1, 1)
        self.label_databaseurl = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_databaseurl.setObjectName("label_databaseurl")
        self.gridLayout.addWidget(self.label_databaseurl, 0, 0, 1, 1)
        self.label_outputdir = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_outputdir.setObjectName("label_outputdir")
        self.gridLayout.addWidget(self.label_outputdir, 1, 0, 1, 1)
        self.lineEdit_outputdir = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_outputdir.setObjectName("lineEdit_outputdir")
        self.gridLayout.addWidget(self.lineEdit_outputdir, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.pushButton_false.clicked.connect(Dialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "設定"))
        self.pushButton_true.setText(_translate("Dialog", "確定"))
        self.pushButton_false.setText(_translate("Dialog", "取消"))
        item = self.tableWidget_location.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "新增列"))
        item = self.tableWidget_location.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "經度"))
        item = self.tableWidget_location.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "緯度"))
        __sortingEnabled = self.tableWidget_location.isSortingEnabled()
        self.tableWidget_location.setSortingEnabled(False)
        item = self.tableWidget_location.item(0, 0)
        item.setText(_translate("Dialog", "120.111"))
        item = self.tableWidget_location.item(0, 1)
        item.setText(_translate("Dialog", "23.111"))
        self.tableWidget_location.setSortingEnabled(__sortingEnabled)
        self.label_location.setText(_translate("Dialog", "選取位置"))
        self.label_databaseurl.setText(_translate("Dialog", "資料庫網址"))
        self.label_outputdir.setText(_translate("Dialog", "輸出資料夾"))
        self.lineEdit_outputdir.setText(_translate("Dialog", "output\\"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())