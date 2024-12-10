# -*- coding: utf-8 -*-
"""
----------------------------
QPESUMS_QPF資料擷取程式 v2.0
Copyright © 2020-2024
----------------------------
Creator: Steven Kuo
Created date: 2020-07-08
Updated date: 2024-11-01
----------------------------
"""
#2024-11-01 v2.0 GUI介面；重新改寫程式碼，提升執行速度，並改善路徑無法存取之問題

from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import pandas as pd
import json
import requests
import zipfile
import os
import glob
import datetime
import numpy as np

class Main():
    def __init__(self, types, dates):
        with open('config.json', encoding="utf-8") as f:
            self.config = json.load(f)
        
        self.types = types
        self.dates = dates
        self.archive_folder = rf"{self.config['output_folder']}\{self.types}\{self.dates}"
        
        #若資料夾不存在則新建資料夾
        if not os.path.exists(rf"{self.archive_folder}\TXT"):
            os.makedirs(rf"{self.archive_folder}\TXT")
            
    def Zipfiles(self):
        '''
        取得壓縮檔目錄
        '''
        objSoap = BeautifulSoup(requests.get(
            rf"{self.config['url']}/{self.types}/{self.dates}").text,'lxml')
        tableobj = objSoap.find('pre')
        tables = tableobj.find_all('a')
        files_zip = [i.text for i in tables if i.text[-3:] in ['zip']]
        
        return files_zip
    
    def Downloader(self, zipfile_num, zipfile_name):
        '''
        下載並解壓縮檔案
        '''   
        i = zipfile_num
        j = zipfile_name
        
        name_txt = rf"{self.archive_folder}\TXT\{self.dates}-{i+1:03d}.txt"
        name_zip = rf"{self.archive_folder}\{j[:-4]}"
        
        #下載
        urlretrieve(rf"{self.config['url']}/{self.types}/{self.dates}/{j}",
                    rf"{self.archive_folder}\{self.dates}-{i+1}.zip")
        
        #解壓縮
        zippath = zipfile.ZipFile(rf"{self.archive_folder}\{self.dates}-{i+1}.zip", 'r')
        zippath.extractall(rf"{self.archive_folder}")
        zippath.close()
        
        #重新命名（若檔案已存在則覆蓋）
        try:
            os.rename(name_zip, name_txt)
        except WindowsError:
            os.remove(name_txt)
            os.rename(name_zip, name_txt)
    
        #刪除壓縮檔
        os.remove(rf"{self.archive_folder}\{self.dates}-{i+1}.zip")
    
    def Txtfiles(self):
        '''
        呼叫全部txt檔案
        '''
        files = glob.glob(rf"{self.config['output_folder']}\{self.types}\{self.dates}\TXT\*.txt")
        return files
    
    def ReadTxtfile(self, txtfile):
        '''
        讀取txt檔案
        '''
        i = txtfile
        header = pd.read_csv(i, encoding = "utf-8", header=None)[0][0].split(" ")[0].split("預報")[-1]
        txt = np.array(pd.read_csv(i, encoding = "utf-8", sep=' ', skiprows=5, 
                          skipinitialspace=True, header=None))
        
        #文字時間轉換
        dat = datetime.datetime.strptime(header[:10], '%Y%m%d%H')
        return dat, txt
    
    def GetDatafromLocation(self, dicts):
        '''
        依位置抓取資料
        '''
        intensity_by_location = []
        for lon, lat in self.config['location']:
            predict_time = []
            intensity = []
            for i in dicts.keys():
                filters = dicts[i][(dicts[i][:,0] == lon) & 
                                   (dicts[i][:,1] == lat)]
                predict_time.append(i)
                intensity.append(filters[:,2][0])
                
            frame = pd.DataFrame(dict(predict_time=predict_time,
                                      intensity=intensity))
            intensity_by_location.append(intensity)
            
            #儲存資料
            with open(rf"{self.config['output_folder']}\{self.types}\{self.dates}\{lon:.4f}-{lat:.4f}.csv", 
                      'w', newline='') as save:
                frame.to_csv(save, encoding='utf-8', index=False)
        return intensity_by_location, predict_time
    
    def MeanCalculate(self, intensity_by_location, predict_time):
        '''
        計算平均值
        '''
        intensity_by_location = np.array(intensity_by_location).T
        mean = np.mean(intensity_by_location, axis=1)
        mean_frame = pd.DataFrame(dict(predict_time=predict_time,
                                  mean_intensity=mean))
        #儲存資料
        with open(rf"{self.config['output_folder']}\{self.types}\{self.dates}\mean.csv", 
                  'w', newline='') as save:
            mean_frame.to_csv(save, encoding='utf-8', index=False)
                
if __name__ == '__main__': 
    dates = 2024120102
    types = 'QPESUMS_QPF'       
    mains = Main()
    zipfiles = mains.Zipfiles()
    for i,j in enumerate(zipfiles):
        mains.Downloader(i, j)
        print(j)
        
    txtfiles = mains.Txtfiles()
    dicts = dict()
    
    #批次讀txt檔
    for i in txtfiles:
        dat, txt = mains.ReadTxtfile(i)
        dicts[dat] = txt
        print(i)
    
    intensity_by_location, predict_time = mains.GetDatafromLocation()
    mains.MeanCalculate(intensity_by_location, predict_time)