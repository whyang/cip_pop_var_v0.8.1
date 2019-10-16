"""
Created on Aug. 21, 2019

@author: whyang
"""
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#######################################################################################
# declare functions
#######################################################################################
###
# remove leading and trailing characters of each value across all cells in dataframe
#
def trim_all_cells(df):
    # trim whitespace from ends of each value across all series in dataframe
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

#######################################################################################
# declare Analytic classes for CIP's population data                                      #
#######################################################################################
###
# create the cipStackedVar figure in Matplotlib for the sake of analyzing the population variation
#
class cipStackedVar:
    def __init__(self):
        pass       
    ###
    # 準備目前有的原住民族人口變化統計表格(100~102, 102~103, 103~017)
    #
    def readPopVarCSV(self, datapath='.\\data'):
        # 準備目前有的原住民族人口變化統計表格(100~102, 102~103, 103~017)    
        # 1: period between year of 100 and year of 102
        with open(datapath+'\\'+'population-var-100-102.csv', 'r', encoding='utf-8', newline='') as csvfile:
            df_100_102 = pd.read_csv(
                csvfile,
                header = 0,
                usecols = ['日期區間', '區域別', '總計', 
                           '阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族',
                           '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族',
                           '拉阿魯哇族', '卡那卡那富族', '尚未申報'],
                verbose = True,
                skip_blank_lines = True)
            df_100_102 = trim_all_cells(df_100_102) # trim whitespace from each cell in dataframe
        
        # 2: period between year of 102 and year of 103
        with open(datapath+'\\'+'population-var-102-103.csv', 'r', encoding='utf-8', newline='') as csvfile:
            df_102_103 = pd.read_csv(
                csvfile,
                header = 0,
                usecols = ['日期區間', '區域別', '總計',
                           '阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族',
                           '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族',
                           '拉阿魯哇族', '卡那卡那富族', '尚未申報'],
                verbose = True,
                skip_blank_lines = True)
            df_102_103 = trim_all_cells(df_102_103) # trim whitespace from each cell in dataframe    

        # 3: period between year of 103 and year of 107
        with open(datapath+'\\'+'population-var-103-107.csv', 'r', encoding='utf-8', newline='') as csvfile:
            df_103_107 = pd.read_csv(
                csvfile,
                header = 0,
                usecols = ['日期區間', '區域別', '總計',
                           '阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族',
                           '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族',
                           '拉阿魯哇族', '卡那卡那富族', '尚未申報'],
                verbose = True,
                skip_blank_lines = True)
            df_103_107 = trim_all_cells(df_103_107) # trim whitespace from each cell in dataframe
    
        return df_100_102, df_102_103, df_103_107

    ###
    # 呈現原住民族人口歷年變化(那個縣市內所有族)
    #
    def show_stackedvar_area(self, df_100_102, df_102_103, df_103_107, area='新北市', figurepath='.\\figure'):
        x = ['阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族', '雅美族', '邵族',
             '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族', '拉阿魯哇族', '卡那卡那富族', '尚未申報']
        # to deal with two counties' names (桃園縣 and 桃園市)
        # in the year of 100~102 and 102~103, 桃園縣 is collected in the dataset (while 桃園市 is not included because it is 省轄市)
        # however, 桃園市(直轄市) contains the number of the both of 桃園縣 and 桃園市(省轄市) in the year of 103~107
        arearule1 = lambda name, replace_name: '桃園縣' if name == replace_name else name # rule 1 for the year of 100~102 and 102~103
        arearule2 = lambda name, replace_name: '桃園市' if name == replace_name else name # rule 2 for the year of 103~107
        
        # 100年~102年
        '''
        if (area == '桃園市'):
            area_1 = '桃園縣'
        else:
            area_1 = area
        '''
        filter = df_100_102['區域別'] == arearule1(area, '桃園市') #area_1
        
        y_100_102 = [df_100_102.loc[filter, '阿美族'].values[0],
                df_100_102.loc[filter, '泰雅族'].values[0],
                df_100_102.loc[filter, '排灣族'].values[0],
                df_100_102.loc[filter, '布農族'].values[0],
                df_100_102.loc[filter, '魯凱族'].values[0],
                df_100_102.loc[filter, '卑南族'].values[0],
                df_100_102.loc[filter, '鄒族'].values[0],
                df_100_102.loc[filter, '賽夏族'].values[0],
                df_100_102.loc[filter, '雅美族'].values[0],
                df_100_102.loc[filter, '邵族'].values[0],
                df_100_102.loc[filter, '噶瑪蘭族'].values[0],
                df_100_102.loc[filter, '太魯閣族'].values[0],
                df_100_102.loc[filter, '撒奇萊雅族'].values[0],
                df_100_102.loc[filter, '賽德克族'].values[0],
                df_100_102.loc[filter, '拉阿魯哇族'].values[0],
                df_100_102.loc[filter, '卡那卡那富族'].values[0],
                df_100_102.loc[filter, '尚未申報'].values[0]
                ]
        
        # 102年~103年
        '''
        if (area == '桃園市'):
            area_1 = '桃園縣'
        else:
            area_1 = area
        '''            
        #
        filter = df_102_103['區域別'] == arearule1(area, '桃園市') #area_1
        y_102_103 = [df_102_103.loc[filter, '阿美族'].values[0],
                df_102_103.loc[filter, '泰雅族'].values[0],
                df_102_103.loc[filter, '排灣族'].values[0],
                df_102_103.loc[filter, '布農族'].values[0],
                df_102_103.loc[filter, '魯凱族'].values[0],
                df_102_103.loc[filter, '卑南族'].values[0],
                df_102_103.loc[filter, '鄒族'].values[0],
                df_102_103.loc[filter, '賽夏族'].values[0],
                df_102_103.loc[filter, '雅美族'].values[0],
                df_102_103.loc[filter, '邵族'].values[0],
                df_102_103.loc[filter, '噶瑪蘭族'].values[0],
                df_102_103.loc[filter, '太魯閣族'].values[0],
                df_102_103.loc[filter, '撒奇萊雅族'].values[0],
                df_102_103.loc[filter, '賽德克族'].values[0],
                df_102_103.loc[filter, '拉阿魯哇族'].values[0],
                df_102_103.loc[filter, '卡那卡那富族'].values[0],
                df_102_103.loc[filter, '尚未申報'].values[0]
                ]
            
        # 103年~107年
        '''
        if (area == '桃園縣'):
            area_1 = '桃園市'
        else:
            area_1 = area
        '''
        #
        filter = df_103_107['區域別'] == arearule2(area, '桃園縣') #area_1
        y_103_107 = [df_103_107.loc[filter, '阿美族'].values[0],
                df_103_107.loc[filter, '泰雅族'].values[0],
                df_103_107.loc[filter, '排灣族'].values[0],
                df_103_107.loc[filter, '布農族'].values[0],
                df_103_107.loc[filter, '魯凱族'].values[0],
                df_103_107.loc[filter, '卑南族'].values[0],
                df_103_107.loc[filter, '鄒族'].values[0],
                df_103_107.loc[filter, '賽夏族'].values[0],
                df_103_107.loc[filter, '雅美族'].values[0],
                df_103_107.loc[filter, '邵族'].values[0],
                df_103_107.loc[filter, '噶瑪蘭族'].values[0],
                df_103_107.loc[filter, '太魯閣族'].values[0],
                df_103_107.loc[filter, '撒奇萊雅族'].values[0],
                df_103_107.loc[filter, '賽德克族'].values[0],
                df_103_107.loc[filter, '拉阿魯哇族'].values[0],
                df_103_107.loc[filter, '卡那卡那富族'].values[0],
                df_103_107.loc[filter, '尚未申報'].values[0]
                ]
            
        # generate figure
        y = np.vstack([y_100_102, y_102_103, y_103_107])
        labels = ['100年-102年', '102年-103年', '103年-107年']
        plt.clf()
        fig, ax = plt.subplots()
        ax.stackplot(x, y, labels=labels, baseline='zero')
        ax.set_xticklabels(x, rotation=300)
        ax.set_xlabel('原住民族')
        ax.set_ylabel('人口變化數')
        ax.legend(loc='best')
        ax.set_title('原住民族人口變化(2011年~2018年): ' + area)
        # store the figue into folder
        figfile='AP-stackvar-' + area + '-tribe.png'
        plt.savefig(figurepath + '\\' + figfile, dpi=300, bbox_inches='tight')
        
        plt.plot(x, y_103_107, color='red', linewidth=5)
        
        plt.show()

    ###
    # 呈現原住民族人口歷年變化(那個族在各縣市)
    #
    def show_stackedvar_tribe(self, df_100_102, df_102_103, df_103_107, tribe='阿美族', figurepath='.\\figure'):
        x = ['新北市', '臺北市', '桃園市\\縣', '臺中市', '臺南市', '高雄市', '宜蘭縣', '新竹縣', '苗栗縣',
             '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '臺東縣', '花蓮縣', '澎湖縣',
             '基隆市', '新竹市', '嘉義市', '金門縣', '連江縣']
        # 100年~102年
        y_100_102 = [df_100_102.loc[(df_100_102['區域別'] == '新北市'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '臺北市'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '桃園縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '臺中市'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '臺南市'), tribe].values[0],                           
                df_100_102.loc[(df_100_102['區域別'] == '高雄市'), tribe].values[0],                           
                df_100_102.loc[(df_100_102['區域別'] == '宜蘭縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '新竹縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '苗栗縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '彰化縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '南投縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '雲林縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '嘉義縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '屏東縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '臺東縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '花蓮縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '澎湖縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '基隆市'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '新竹市'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '嘉義市'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '金門縣'), tribe].values[0],
                df_100_102.loc[(df_100_102['區域別'] == '連江縣'), tribe].values[0]
                ]
        # 102年~103年
        y_102_103 = [df_102_103.loc[(df_102_103['區域別'] == '新北市'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '臺北市'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '桃園縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '臺中市'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '臺南市'), tribe].values[0],                           
                df_102_103.loc[(df_102_103['區域別'] == '高雄市'), tribe].values[0],                           
                df_102_103.loc[(df_102_103['區域別'] == '宜蘭縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '新竹縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '苗栗縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '彰化縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '南投縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '雲林縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '嘉義縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '屏東縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '臺東縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '花蓮縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '澎湖縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '基隆市'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '新竹市'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '嘉義市'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '金門縣'), tribe].values[0],
                df_102_103.loc[(df_102_103['區域別'] == '連江縣'), tribe].values[0]
                ]
        # 103年~107年
        y_103_107 = [df_103_107.loc[(df_103_107['區域別'] == '新北市'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '臺北市'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '桃園市'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '臺中市'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '臺南市'), tribe].values[0],                           
                df_103_107.loc[(df_103_107['區域別'] == '高雄市'), tribe].values[0],                           
                df_103_107.loc[(df_103_107['區域別'] == '宜蘭縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '新竹縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '苗栗縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '彰化縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '南投縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '雲林縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '嘉義縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '屏東縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '臺東縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '花蓮縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '澎湖縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '基隆市'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '新竹市'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '嘉義市'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '金門縣'), tribe].values[0],
                df_103_107.loc[(df_103_107['區域別'] == '連江縣'), tribe].values[0]
                ]
        # generate figure
        y = np.vstack([y_100_102, y_102_103, y_103_107])
        labels = ['100年-102年', '102年-103年', '103年-107年']
        plt.clf()
        fig, ax = plt.subplots()
        ax.stackplot(x, y, labels=labels, baseline='zero')
        ax.set_xticklabels(x, rotation=300)
        ax.set_xlabel('區域別')
        ax.set_ylabel('人口變化數')
        ax.legend(loc='best')
        ax.set_title('原住民族人口變化(2011年~2018年):' + tribe)
        # store the figue into folder
        figfile='AP-stackvar-' + tribe + '-area.png'
        fig.savefig(figurepath + '\\' + figfile, dpi=300, bbox_inches='tight')
        
        plt.plot(x, y_103_107, color='red', linewidth=5)
        
        plt.show()

#
# end of cipStackedVar
###

#######################################################################################
# end of file                                                                         #
#######################################################################################
