"""
Created on Jul. 30, 2019

@author: whyang
"""
# -*- coding: utf-8 -*-
import os
import csv # deal with csv file
import pandas as pd
import numpy as np
from cippackage.popAPvar import cipFacetGrid # the Analytic package for the data of CIP's population

#######################################################################################
# declare functions                                                                   #
#######################################################################################
###
# remove leading and trailing characters of each value across all cells in dataframe
#
def trim_all_cells(df):
    # trim whitespace from ends of each value across all series in dataframe
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

###
# set output figure and input data directories
#
pathdir = '.\\figure'  # directory of output folder 
if not os.path.isdir(pathdir): 
    os.mkdir(pathdir)
datadir = '.\\data'  # directory of input data folder 
if not os.path.isdir(datadir): 
    os.mkdir(datadir)

###
# given the comparison period (from the year ybeg to the year yend )
# status quo: 
# 1. 輸入日期(年份:中華民國、西元，月份，日歷天數)都一致轉為只有西元年-12-31
# 2. 限定兩個年度期間: 起始年(ybeg)、結束年(yend)，yend > ybeg
#
print('觀察比較原住民族人口變化：年度1 vs 年度2 (e.g., 2011, 2013)')
year1 = input('年度1:')
year2 = input('年度2:')
yeardict = {'2011':'2011-12-31', '2013':'2013-12-31', '2014':'2014-12-31', '2018':'2018-12-31',
            '100':'2011-12-31', '102':'2013-12-31', '103':'2014-12-31', '107':'2018-12-31'}
invyeardict = {'2011-12-31':'100', '2013-12-31':'102', '2014-12-31':'103', '2018-12-31':'107'}
if yeardict[year1] > yeardict[year2]:
    ybeg = yeardict[year2]
    yend = yeardict[year1]
else:
    ybeg = yeardict[year1]
    yend = yeardict[year2]
# still needs to deal with wrong doing of input process
print(ybeg, '~', yend)
    
###
# read into the amount of aboriginal peoples' population
#
with open(datadir+'\\'+'population-sum-ETL.csv', 'r', encoding='utf-8', newline='') as csvfile:
    df = pd.read_csv(
            csvfile,
            header = 0,
            usecols = ['日期', '身分', '區域別', '總計',
                       '阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族',
                       '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族',
                       '拉阿魯哇族', '卡那卡那富族',
                       '尚未申報'],
            verbose = True,
            skip_blank_lines = True,
            )
    df = trim_all_cells(df) # trim whitespace from each cell in dataframe
       
    ###
    # 各縣市不分平地山地身分的人口總數(依照原住民族)
    # selecting the accumulated records(rows) in order to the needs of analysis
    # add the 'selected' column as the mark: True and null
    # drop the rows that are marked as 'null' (nan)
    #
    df.loc[(df.身分 == '不分平地山地'), 'selected'] = np.nan # mark all of the rows as null
    df.loc[(df.身分 != '不分平地山地'), 'selected'] = np.nan # mark all of the rows as null
    df.loc[((df.日期 == ybeg) | (df.日期 == yend)) & ( # filtered by the period of time ybeg~yend
                    (df.區域別 == '新北市') | (df.區域別 == '臺北市') | (df.區域別 == '臺中市') |
                    (df.區域別 == '臺南市') | (df.區域別 == '高雄市') | (df.區域別 == '桃園市') | # 桃園縣 promote as 桃園市
                    (df.區域別 == '宜蘭縣') | (df.區域別 == '桃園縣') | (df.區域別 == '新竹縣') |
                    (df.區域別 == '苗栗縣') | (df.區域別 == '彰化縣') | (df.區域別 == '南投縣') |
                    (df.區域別 == '雲林縣') | (df.區域別 == '嘉義縣') | (df.區域別 == '屏東縣') |
                    (df.區域別 == '臺東縣') | (df.區域別 == '花蓮縣') | (df.區域別 == '澎湖縣') |
                    (df.區域別 == '基隆市') | (df.區域別 == '新竹市') | (df.區域別 == '嘉義市') |
                    (df.區域別 == '金門縣') | (df.區域別 == '連江縣') ), 
                    'selected'] = True # 只取各區域的合計資料(row)
    df.dropna(subset=['selected'], inplace=True) # conduct dropping of the row that are marked as null
    df.drop(columns=['selected'], inplace=True) # remove the "selected' column 
    df.reset_index(inplace=True) # let index be the sequence order

    ###
    # transform to array format applied for presenting the figures with profile
    #    
    df1 = pd.DataFrame(columns=['日期區間', # indicate the statistic period of the populaton variation, start year-finish year
                                '區域別', '總計',
                                '阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族',
                                '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族',
                                '拉阿魯哇族', '卡那卡那富族', '尚未申報'])   
    # Notes：
    # 1. 桃園縣-桃園市 資料動應時間點產生的落差(與其它縣市)，且舊桃園市(省轄市)在升格前資料未納入，升格後直接併入桃園市(直轄市)
    # 2. 拉阿魯哇族、卡那卡那富族 正式產生資料時間點問題(未成立前直接被補植為0)
    #
    
    # mapping table for area
    areadict = {'新北市':0, '臺北市':1, '桃園縣':2, '桃園市':2, # align 桃園縣 with 桃園市 (數字計算錯誤-誤差來自於舊的桃園市-省轄市 和桃園縣市分開計算)  
                '臺中市':3, '臺南市':4, '高雄市':5, '宜蘭縣':6, '新竹縣':7,
                '苗栗縣':8, '彰化縣':9, '南投縣':10, '雲林縣':11, '嘉義縣':12, '屏東縣':13, '臺東縣':14, '花蓮縣':15,
                '澎湖縣':16, '基隆市':17, '新竹市':18, '嘉義市':19, '金門縣':20, '連江縣':21}
    # construct a temporary dataframe for keeping the data of the year ybeg  
    data = np.zeros((22,18), dtype=np.int)   
    basedf = pd.DataFrame({'阿美族':data[:,0], '泰雅族':data[:,1], '排灣族':data[:,2],
                        '布農族':data[:,3], '魯凱族':data[:,4], '卑南族':data[:,5],
                        '鄒族':data[:,6], '賽夏族':data[:,7], '雅美族':data[:,8],
                        '邵族':data[:,9], '噶瑪蘭族':data[:,10], '太魯閣族':data[:,11],
                        '撒奇萊雅族':data[:,12], '賽德克族':data[:,13], '拉阿魯哇族':data[:,14],
                        '卡那卡那富族':data[:,15], '尚未申報':data[:,16], '總計':data[:,17]}) 
    ###
    # construct dataframe(df1) for keeping the transformed variation numbers
    #  
    offset = 0 # the base point for the dataframe of df1 used as the statistical population variation
    base = 0 # the base point for the dataframe of df1 used as the transformed data
    for i in range(0, len(df.index)):
        if df.at[i, '日期'] == ybeg: 
            offset = areadict[df.at[i, '區域別']] # indicate the row number corresponding to the sequence of areas (i.e., areadict)
            basedf.at[offset, '阿美族'] = df.at[i, '阿美族']
            basedf.at[offset, '泰雅族'] = df.at[i, '泰雅族']
            basedf.at[offset, '排灣族'] = df.at[i, '排灣族']
            basedf.at[offset, '布農族'] = df.at[i, '布農族']
            basedf.at[offset, '魯凱族'] = df.at[i, '魯凱族']
            basedf.at[offset, '卑南族'] = df.at[i, '卑南族']
            basedf.at[offset, '鄒族'] = df.at[i, '鄒族']
            basedf.at[offset, '賽夏族'] = df.at[i, '賽夏族']
            basedf.at[offset, '雅美族'] = df.at[i, '雅美族']
            basedf.at[offset, '邵族'] = df.at[i, '邵族']
            basedf.at[offset, '噶瑪蘭族'] = df.at[i, '噶瑪蘭族']
            basedf.at[offset, '太魯閣族'] = df.at[i, '太魯閣族']
            basedf.at[offset, '撒奇萊雅族'] = df.at[i, '撒奇萊雅族']
            basedf.at[offset, '賽德克族'] = df.at[i, '賽德克族']
            basedf.at[offset, '拉阿魯哇族'] = df.at[i, '拉阿魯哇族']           
            basedf.at[offset, '卡那卡那富族'] = df.at[i, '卡那卡那富族']
            basedf.at[offset, '尚未申報'] = df.at[i, '尚未申報']
            basedf.at[offset, '總計'] = df.at[i, '總計']
        else:
            offset = areadict[df.at[i, '區域別']] # indicate the row number corresponding to the sequence of areas (i.e., areadict)]
            df1.at[base, '日期區間'] = invyeardict[ybeg]+'-'+invyeardict[yend]
            df1.at[base, '區域別'] = df.at[i, '區域別']
            df1.at[base, '總計'] = df.at[i, '總計'] - basedf.at[offset, '總計']
            df1.at[base, '阿美族'] = df.at[i, '阿美族'] - basedf.at[offset, '阿美族']
            df1.at[base, '泰雅族'] = df.at[i, '泰雅族'] - basedf.at[offset, '泰雅族']
            df1.at[base, '排灣族'] = df.at[i, '排灣族']- basedf.at[offset, '排灣族']
            df1.at[base, '布農族'] = df.at[i, '布農族']- basedf.at[offset, '布農族']
            df1.at[base, '魯凱族'] = df.at[i, '魯凱族']- basedf.at[offset, '魯凱族']
            df1.at[base, '卑南族'] = df.at[i, '卑南族']- basedf.at[offset, '卑南族']
            df1.at[base, '鄒族'] = df.at[i, '鄒族']- basedf.at[offset, '鄒族']
            df1.at[base, '賽夏族'] = df.at[i, '賽夏族']- basedf.at[offset, '賽夏族']
            df1.at[base, '雅美族'] = df.at[i, '雅美族']- basedf.at[offset, '雅美族']
            df1.at[base, '邵族'] = df.at[i, '邵族']- basedf.at[offset, '邵族']
            df1.at[base, '噶瑪蘭族'] = df.at[i, '噶瑪蘭族']- basedf.at[offset, '噶瑪蘭族']
            df1.at[base, '太魯閣族'] = df.at[i, '太魯閣族']- basedf.at[offset, '太魯閣族']
            df1.at[base, '撒奇萊雅族'] = df.at[i, '撒奇萊雅族']- basedf.at[offset, '撒奇萊雅族']
            df1.at[base, '賽德克族'] = df.at[i, '賽德克族']- basedf.at[offset, '賽德克族']
            df1.at[base, '拉阿魯哇族'] = df.at[i, '拉阿魯哇族']- basedf.at[offset, '拉阿魯哇族']
            df1.at[base, '卡那卡那富族'] = df.at[i, '卡那卡那富族']- basedf.at[offset, '卡那卡那富族']
            df1.at[base, '尚未申報'] = df.at[i, '尚未申報']- basedf.at[offset, '尚未申報']
            base += 1             
   
###
# restore the transformed population variation info. to a specific file
#
df1.reset_index(inplace=True)
df1.drop(columns=['index'], inplace=True) # remove the "index' column thus will not appear in the output file 
df1.to_csv(datadir+'\\'+'population-var-'+invyeardict[ybeg]+'-'+invyeardict[yend]+'.csv', index=False, encoding='cp950') # for windows environment (encoding as ANSI format)

###
# prepare the dataframe(df2) for showing up the population variation figure
#
df2 = pd.DataFrame(columns=['日期區間', # indicate the statistic period of the populaton variation, start year-finish year
                            '區域別', '原住民族', '人口變化數'])

# temporary mapping table (dictionary structure)
dict = {'身分':'', '日期區間':'', '區域別':'', '原住民族':'', '人口變化數':0}
# the sequence of tribes in dataframe(df1)
col = {0:'阿美族', 1:'泰雅族', 2:'排灣族', 3:'布農族', 4:'魯凱族', 5:'卑南族', 6:'鄒族', 7:'賽夏族',
       8:'雅美族', 9:'邵族', 10:'噶瑪蘭族', 11:'太魯閣族', 12:'撒奇萊雅族', 13:'賽德克族',
       14:'拉阿魯哇族', 15:'卡那卡那富族', 16:'尚未申報'}

# transform the dataframe(df1) to the dataframe(df2) for the sake of presenting figure's structure 
base = 0 # the base point for the dataframe of df1 used as the transformed data
for i in range(0, len(df1.index)):
    for j in range(0, 17, 1): # currently, there are 16 tribes and one as 尚未申報
        df2.at[base + j, '日期區間'] = df1.at[i, '日期區間'] # retrieve the field of 日期
        dict['區域別'] = df1.at[i, '區域別']
        if dict['區域別'] == '桃園縣':
            dict['區域別'] = '桃園市' # to align 桃園縣 with 桃園市 for the convenience of analyzing 
        df2.at[base + j, '區域別'] = dict['區域別'] # retrieve the field of 區域別(縣市)
        dict['原住民族'] = col[j]
        df2.at[base + j, '原住民族'] = str(dict['原住民族']) # retrieve the field of 原住民族(tribe's name)
        dict['人口變化數'] = df1.at[i, col[j]]
        df2.at[base + j, '人口變化數'] = dict['人口變化數'] # retrieve the field of 人口數 (amount of people)
    # adjust base location by the placement
    base += 17 # the placement is 17 (each tribe is flatten to one row, totaly 16 tribes plus 1 undecisive)

###
# prepare the figures in which population distribution is illustrated
# corresponding to the period of date, location area, and tribe
#
# figure1: illustrate the spatial distribution that the people of the specified tribe
grid1 = cipFacetGrid(df2, row='日期區間', col='原住民族', margin_titles=True,
                 plotkind='line', x='區域別', y='人口變化數',
                 tribe=['阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族'],
                 area=['新北市', '臺北市', '高雄市', '屏東縣', '臺東縣', '花蓮縣'],
                 title='原住民族(身分:不分山地平地)人口變化(局部)：'+invyeardict[ybeg]+'-'+invyeardict[yend],
                 figfile=pathdir+'\\'+'AP-var '+invyeardict[ybeg]+'-'+invyeardict[yend]+'-tribe-area(partial).png')
grid1.plot(rotation=30)


# figure2: illustrate the amount of each tribe in the specified area
grid2 = cipFacetGrid(df2, row='日期區間', col='區域別', margin_titles=True,
                 plotkind='bar', x='原住民族', y='人口變化數',
                 tribe=['阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族'],
                 area=['新北市', '臺北市', '高雄市', '屏東縣', '臺東縣', '花蓮縣'],
                 title='各縣市原住民族(身分:不分山地平地)人口變化(局部)：'+invyeardict[ybeg]+'-'+invyeardict[yend],
                 figfile=pathdir+'\\'+'AP-var '+invyeardict[ybeg]+'-'+invyeardict[yend]+'-area-tribe(partial).png')
grid2.plot(rotation=300)
     
#######################################################################################
# end of file                                                                         #
#######################################################################################