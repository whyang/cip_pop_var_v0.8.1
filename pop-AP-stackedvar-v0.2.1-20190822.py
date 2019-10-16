"""
Created on Aug. 21, 2019
@author: whyang

present the accumulated population variation between the period of time 
 
"""
# -*- coding: utf-8 -*-
import os
from cippackage.popAPstackedvar import cipStackedVar # the Analytic package for the data of CIP's population (stacked variation)

###
# function of entry point
#
def doStackedVar():
    # step 1. set configuration info.
    figurepath = '.\\figure'  # directory of output folder 
    if not os.path.isdir(figurepath):
        os.mkdir(figurepath)

    datapath = '.\\data'  # directory of input data folder 
    if not os.path.isdir(datapath):
        os.mkdir(datapath)

    tribes = ['阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族',
              '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族', 
              '拉阿魯哇族', '卡那卡那富族', '尚未申報']

    areas = ['新北市', '臺北市', '桃園市', '桃園縣', '臺中市', '臺南市', '高雄市', '宜蘭縣', '新竹縣', '苗栗縣',
             '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '臺東縣', '花蓮縣', '澎湖縣', 
             '基隆市', '新竹市', '嘉義市', '金門縣', '連江縣']

    # step 2: 要觀察那個族、那個縣市 原住民族人口變化
    print('觀察原住民族人口變化(2011年~2018年)')
    _selected = input('0.單一特定區域; 1.單一原住民族; 3.全部; 其它. Done： ')
    if _selected == '0':
        _area = input('那個縣市? ')
        if _area in areas:
            # 準備目前有的原住民族人口變化統計表格(100~102, 102~103, 103~017)
            stackedvar = cipStackedVar()
            df_100_102, df_102_103, df_103_107 = stackedvar.readPopVarCSV(datapath='.\\data')
            stackedvar.show_stackedvar_area(df_100_102, df_102_103, df_103_107, area=_area, figurepath=figurepath)
        else:
            print('縣市名稱 輸入錯誤!')
    elif _selected == '1':
        _tribe = input('那個民族? ')
        if _tribe in tribes:
            # 準備目前有的原住民族人口變化統計表格(100~102, 102~103, 103~017)
            stackedvar = cipStackedVar()
            df_100_102, df_102_103, df_103_107 = stackedvar.readPopVarCSV(datapath='.\\data')
            stackedvar.show_stackedvar_tribe(df_100_102, df_102_103, df_103_107, tribe=_tribe, figurepath=figurepath)
        else:
            print('族名 輸入錯誤!')
    elif _selected == '3':
        print('繪製各縣市之所有原住民族人口變化之圖形')
        # 準備目前有的原住民族人口變化統計表格(100~102, 102~103, 103~017)
        stackedvar = cipStackedVar()
        df_100_102, df_102_103, df_103_107 = stackedvar.readPopVarCSV(datapath='.\\data')
        for _area in areas:
            stackedvar.show_stackedvar_area(df_100_102, df_102_103, df_103_107, area=_area, figurepath=figurepath)
            print('繪製各原住民族在所有縣市人口變化之圖形')
        for _tribe in tribes:
            stackedvar.show_stackedvar_tribe(df_100_102, df_102_103, df_103_107, tribe=_tribe, figurepath=figurepath)
    else:
       print('輸入錯誤，不處理')

    print('Finish this work')

###
# main program
#
doStackedVar()
'''
if __name__ == '__main__':
    doStackedVar()
'''
    
#######################################################################################
# end of file                                                                         #
#######################################################################################