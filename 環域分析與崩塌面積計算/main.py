# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 00:12:08 2022
@author: Steven Kuo
@version: 0.10
"""

from osgeo import gdal, ogr
import geopandas as gpd
import pandas as pd
import numpy as np
from os import path, makedirs

gdal.SetConfigOption( "GDAL_FILENAME_IS_UTF8", "YES")
gdal.SetConfigOption( "SHAPE_ENCODING", "utf-8")

#建立任務資料夾
def Create_Folders(place):
    folders = [r'{}\雨量站環域'.format(place), r'{}\崩塌環域切割'.format(place)]
    generator = lambda x: makedirs(x) if not path.exists(x) else 0
    for i in folders:
        generator(i)

#環域分析
def Buffer(place, name, point, bufferDistance):
    folder = lambda x: makedirs(x) if not path.exists(x) else 0
    folder(r"{}\雨量站環域\{}".format(place, bufferDistance))
    pt = ogr.CreateGeometryFromWkt(point)
    poly = pt.Buffer(bufferDistance)
    
    wkt = [poly.ExportToWkt()]
    df = gpd.GeoDataFrame(geometry=gpd.GeoSeries.from_wkt(wkt), crs="EPSG:3826")
    df['ID'] = name.split('_')[0]
    df['Name'] = name.split('_')[1]
    df['Distance'] = bufferDistance
    #df.to_file(r"{}\雨量站環域\{}\{}_{}.shp".format(place, bufferDistance, name, bufferDistance), encoding='utf-8')
    return poly
    
#輸出環域圖資
def OutputBufferData(place, distance):
    stations = gpd.read_file(r'{}\雨量站\{}.shp'.format(place, place), encoding='utf-8')
    geoms = stations.geometry.astype(str)
    station_name = ['{}_{}'.format(i,j) for i,j in zip(stations['站號'], stations['站名'])]
    
    poly = []
    idn = []
    name = []
    dist = []
    for i,j in enumerate(geoms):
        obj = Buffer(place, station_name[i], j, distance)
        name.append(stations['站名'][i])
        idn.append(stations['站號'][i])
        dist.append(distance)
        poly.append(obj.ExportToWkt())
        if i != len(geoms)-1:
            print('\r{}/{} ({:.2f}%)'.format(i+1,len(geoms),((i+1)/len(geoms)*100)), flush=True, end='\r')
        else:
            print('\r{}/{} ({:.2f}%)'.format(i+1,len(geoms),((i+1)/len(geoms)*100)), flush=True, end='\n')
    
    df = gpd.GeoDataFrame(geometry=gpd.GeoSeries.from_wkt(poly), crs="EPSG:3826")
    df['ID'] = idn
    df['Name'] = name
    df['Distance'] = dist
    df.area
    df.to_file(r"{}\雨量站環域\Buffer_{}.shp".format(place, distance), encoding='utf-8')

def DistanceSuitableCheck(place, distance):
    #適合範圍檢測 (覆蓋率與重疊率的概念...)
    #資訊僅供參考，若同個位置無重複測站則具有參考價值
    county = gpd.read_file(r'{}\縣市\{}.shp'.format(place, place)) #縣市圖層
    distance_buffer = gpd.read_file(r'{}\雨量站環域\Buffer_{}.shp'.format(place, distance)) #縣市圖層#環域分析之範圍圖資
    clip = gpd.clip(county, distance_buffer)
    union = distance_buffer.unary_union

    cover = clip.area[0]/county.area[0] #覆蓋率，愈高愈佳
    overlap = (sum(distance_buffer.area)-union.area)/sum(distance_buffer.area) #重疊率，愈低愈佳 (以union面積與所有環域圈面積相比，若之間無重疊則面積比為0)
    score = cover+(1-overlap)
    return pd.DataFrame(dict(distance=distance,cover=cover, overlap=overlap, score=score), index=[0])

#分割環域範圍內崩塌圖資
def ClipLandslide(place, year, distance):
    from shapely.validation import make_valid
    print('切割崩塌地...')
    folder = lambda x: makedirs(x) if not path.exists(x) else 0
    folder(r"{}\崩塌環域切割\{}".format(place, distance))
    
    info = pd.DataFrame(dict(ID=[], Name=[], Year=[], Distance=[], Area=[]))
    gdb = r'{}\新增崩塌.gdb'.format(place)
    large = gpd.read_file(gdb, layer='New_{}'.format(year))
    large['geometry'] = large['geometry'].apply(make_valid) ##Debug## 修復invalid圖層
    small = gpd.read_file(r'屏東縣\雨量站環域\Buffer_{}.shp'.format(distance))

    for i in range(len(small)):
        n = small.filter(items=[i], axis=0).reset_index(drop=True)
        arr = np.array(n.T)
        smallClip = gpd.clip(large, n)
        if len(smallClip) != 0:     
            smallClip_explode = smallClip['geometry'].explode(index_parts=True)
            gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(smallClip_explode))
            gdf.reset_index(inplace=True)
            gdf = gdf.drop(columns=[i for i in gdf.columns if i not in ['geometry']], axis=1)
            gdf['FID'] = gdf.index
            gdf['Area'] = gdf.area
            gdf.to_file(r"{}\崩塌環域切割\{}\{}_{}_{}.shp".format(place, distance, arr[0][0], arr[1][0], year), encoding='utf-8')
            dt = {'ID': arr[0][0], 'Name':arr[1][0], 
                  'Year':year, 'Distance': distance, 'Area': sum(gdf['Area'])}
            info = info.append(dt, ignore_index=True)

        else: #範圍內無崩塌者
            dt = {'ID': arr[0][0], 'Name':arr[1][0], 
                  'Year':year, 'Distance': distance, 'Area': 0}
            info = info.append(dt, ignore_index=True)
            pass
        print(dt)
    
    if path.exists(r'{}\崩塌面積.csv'.format(place)):
        with open(r'{}\崩塌面積.csv'.format(place), 'a+', newline='') as save:
            info.to_csv(save, encoding='utf-8', index=False, header=0)
    else:
        with open(r'{}\崩塌面積.csv'.format(place), 'w', newline='') as save:
            info.to_csv(save, encoding='utf-8', index=False)

#Running
if __name__ == '__main__':
    place = '屏東縣'
    Create_Folders(place)
    print('環域分析...')
    dis = pd.DataFrame()
    for d in range(500,8001,500):
        print('Distance: {} meter...'.format(d))
        OutputBufferData(place, d)
        dis = dis.append(DistanceSuitableCheck(place, d))
    dis = dis.reset_index(drop=True)
    with open(r'{}\合適範圍檢測.csv'.format(place), 'w', newline='') as save:
        dis.to_csv(save, encoding='utf-8', index=False)
    print(dis)
    
    #選用最合適範圍
    usedist = int(dis[dis['score']== max(dis['score'])].T.values[0,0])
    print('合適範圍: {} meter'.format(usedist))
    for y in range(2004, 2018, 1):
        ClipLandslide(place, y, usedist)
