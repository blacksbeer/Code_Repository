# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 00:17:23 2024

@author: black
"""

from lib import main
from gui import mainwindow, option
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
import json
import sys
import webbrowser
import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.windows = []
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
        
    #初始化
    def initUI(self):
        now = datetime.datetime.now()
        self.ui.lineEdit_time.setText(f'{now.year}{now.month:02d}{now.day:02d}{now.hour:02d}')
        self.ui.progressBar.setProperty("value", 0)
        self.ui.label_processinfo.setText('就緒')
        
        #連接訊號
        self.ui.pushButton_option.clicked.connect(self.openOptionDialog)
        self.ui.lineEdit_time.textChanged.connect(self.checkInputData)
        self.ui.pushButton_openfolder.clicked.connect(self.OpenOutputFolder)
        self.ui.pushButton_run.clicked.connect(self.program)
        self.ui.pushButton_run.setEnabled(True)
        
        if self.ui.radioButton_QPF.isChecked():
            self.ui.pushButton_openfolder.setEnabled(False)
        if self.ui.radioButton_WRF.isChecked():
            self.ui.pushButton_openfolder.setEnabled(False)
            
    #開啟設定視窗
    def openOptionDialog(self):
        window = OptionDialog()
        self.windows.append(window)
        window.show()
    
    def program(self):
        def subprogram(self):
            #執行「依選取位置抓取資料」程序
            try:
                txtfiles = self.mains.Txtfiles()
                dicts = dict()
                
                if len(txtfiles) > 0:
                    #批次讀txt檔
                    for i,j in enumerate(txtfiles):
                        dat, txt = self.mains.ReadTxtfile(j)
                        dicts[dat] = txt
                        n = j.split("\\")[-1]
                        self.ui.label_processinfo.setText(rf'讀取{n}...')
                        
                        if self.mean_calc == True:
                            calcbar = 40
                        else:
                            calcbar = 50
                            
                        if self.download == True:
                            self.ui.progressBar.setProperty("value", 
                                                            50+(calcbar*((i+1)/len(txtfiles))))
                        else:
                            self.ui.progressBar.setProperty("value", 
                                                            (50+calcbar)*((i+1)/len(txtfiles)))
        
                    intensity_by_location, predict_time = self.mains.GetDatafromLocation(dicts)
                    if self.mean_calc == True:
                        self.mains.MeanCalculate(intensity_by_location, predict_time)
                    
                    self.ui.progressBar.setProperty("value", 100)
                    self.ui.pushButton_openfolder.setEnabled(True)
                    self.ui.label_processinfo.setText('執行完成！')
                else:
                    self.ui.progressBar.setProperty("value", 0)
                    self.ui.label_processinfo.setText('執行失敗：無TXT檔案！')
            except:
                self.ui.label_processinfo.setText('執行失敗！')
        
        self.dates = self.ui.lineEdit_time.text()
        self.mean_calc = self.ui.checkBox_calcmean.isChecked()
        self.download = self.ui.checkBox_downloadraw.isChecked()
        
        if self.ui.radioButton_QPF.isChecked():
            self.types = self.ui.radioButton_QPF.text()
        if self.ui.radioButton_WRF.isChecked():
            self.types = self.ui.radioButton_WRF.text()
        
        self.mains = main.Main(types=self.types, dates=self.dates)
           
        #執行「下載原始資料」程序
        if self.download == True:
            try:
                zipfiles = self.mains.Zipfiles()
                if len(zipfiles) < 1:
                    raise
                for i,j in enumerate(zipfiles):
                    self.mains.Downloader(i, j)
                    self.ui.label_processinfo.setText(rf'下載{j}...')
                    self.ui.progressBar.setProperty("value", 
                                                    50*((i+1)/len(zipfiles)))
                self.ui.label_processinfo.setText('下載完成！')
                subprogram(self)
            except:
                self.ui.label_processinfo.setText('下載失敗！')
        else:
            subprogram(self)

    #檢查編輯資訊有無完整
    def checkInputData(self):
        if len(self.ui.lineEdit_time.text()) == 10:
            self.ui.pushButton_run.setEnabled(True)
        else:
            self.ui.pushButton_run.setEnabled(False)
            self.ui.pushButton_openfolder.setEnabled(False)
        
    #打開輸出資料夾
    def OpenOutputFolder(self):
        self.dates = self.ui.lineEdit_time.text()
        
        if self.ui.radioButton_QPF.isChecked():
            self.types = self.ui.radioButton_QPF.text()
        if self.ui.radioButton_WRF.isChecked():
            self.types = self.ui.radioButton_WRF.text()
        
        with open('config.json', encoding="utf-8") as f:
            config = json.load(f)
            
        paths = rf"{config['output_folder']}\{self.types}\{self.dates}"
        webbrowser.open(paths)


class OptionDialog(QtWidgets.QDialog):
    def __init__(self):
        super(OptionDialog, self).__init__()
        self.OptionDialog = option.Ui_Dialog()
        self.OptionDialog.setupUi(self)
        
        self.initUI()
        self.OptionDialog.pushButton_true.clicked.connect(self.SaveOption)
        self.OptionDialog.pushButton_true.clicked.connect(self.close)
        
    def initUI(self):
        #初始化
        with open('config.json', encoding="utf-8") as f:
            config = json.load(f)
        self.OptionDialog.lineEdit_databaseurl.setText(config['url'])
        self.OptionDialog.lineEdit_outputdir.setText(config['output_folder'])
        
        rowCount = self.OptionDialog.tableWidget_location.rowCount()
        columnCount = self.OptionDialog.tableWidget_location.columnCount()
        for i in range(rowCount):
            for j in range(columnCount):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.OptionDialog.tableWidget_location.setItem(i, j, item)
                
        for i in range(len(config['location'])):
            for j in range(len(config['location'][i])):
                self.OptionDialog.tableWidget_location.item(i, j).setText(
                    f"{config['location'][i][j]:.4f}")
     
    #儲存設定值
    def SaveOption(self):
        location = []
        rowCount = self.OptionDialog.tableWidget_location.rowCount()
        for i in range(rowCount):
            try:
                location.append([float(self.OptionDialog.tableWidget_location.item(i, 0).text()),
                                  float(self.OptionDialog.tableWidget_location.item(i, 1).text())])
            except:
                break
        
        config = {'url': self.OptionDialog.lineEdit_databaseurl.text(),
                  'output_folder': self.OptionDialog.lineEdit_outputdir.text(),
                  'location':location
                  }
        print(config['url'])
        print(config['output_folder'])
        print(config['location'])
        #覆寫設定值
        with open('config.json', "w", encoding='utf-8') as outfile:
            json.dump(config, outfile, indent=3, ensure_ascii=False)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
