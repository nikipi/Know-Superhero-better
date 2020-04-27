import pandas as pd
import numpy as np
import pymongo
import pandas as pd
import pyquery as pq
import os
import ssl
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
ssl._create_default_https_context = ssl._create_unverified_context
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)

url = 'https://raw.githubusercontent.com/makcyun/web_scraping_with_python/master/%E6%BC%AB%E5%A8%81%E7%94%B5%E5%BD%B1%E5%AE%87%E5%AE%99%E8%8B%B1%E9%9B%84%E7%BB%BC%E5%90%88%E5%AE%9E%E5%8A%9B%E5%AF%B9%E6%AF%94%E5%88%86%E6%9E%90/marvel.csv'

data = pd.read_csv(url, sep=',',engine='python')

print(data.head())

print(data.info())

data=data.fillna(0)

# weight has kg , make it as object  the measurement is not the same
data['height']=data['height'].str.replace('cm','')

row_meter=data['height'].str.contains('meters')   # str.contains 模糊筛选  返回的是FALSE AND TRUE
print(data.loc[row_meter,'height'])

data.loc[row_meter,'height'] = pd.to_numeric(data.loc[row_meter,'height'].str.replace(' meters',''))*100
#*100 means convert it to cm as the rest

data['height']=pd.to_numeric(data['height'])/100
print(data.head())

data['weight']=data['weight'].str.replace('kg','')
row_weight=data['weight'].str.contains('tons')
data.loc[row_weight,'weight']=pd.to_numeric(data.loc[row_weight,'weight'].str.replace('tons',''))*1000
data['weight']=pd.to_numeric(data['weight'])

print(data.head())

data['total_score'] = data[['intelligence','power','strength','speed','durability','combat']].sum(axis=1)
data=data.sort_values(by='total_score',ascending=False).reset_index(drop=True)
#index 跟着排序走的 所以应该 RESET.INDEX
data['score_rank']=data.index+1
print(data.head(10))

print(data.sort_values(by='score_rank')[:10][['name','publisher','total_score']])
# only print the first 10 &&& their name publisher total_socre


###############
###hist grap###
###############

name=data.sort_values(by='score_rank')[:10]['name'].values.tolist()
score=data.sort_values(by='score_rank')[:10]['total_score'].values.tolist()
data_top=pd.DataFrame({'name':name,'score':score})[::-1]
#merge two list to a dataframe

plt.style.use('ggplot')
fig,ax = plt.subplots(figsize=(8,6))

grey = '#969696'#深灰
red = '#E24A33' #红色

color = [grey, red, red, red, red, red, red, '#2A2A2A', red, grey]
barh = ax.barh(np.arange(10),
               data_top['score'],
               color=color)
for y,x in enumerate(data_top['score'].values.tolist()):
   ax.text(x-5,y-0.1,'%i'%x,
            ha='right',
            size=15,
            color='#FFFFFF')
ax.set_yticks(np.arange(10))
ax.set_yticklabels(data_top['name'].tolist(),size=15)

ax.legend(['TOP 10 score(out of 600)'],loc='lower right')
plt.tight_layout()
plt.show()

# choose the part of it
members = ['Captain Marvel','Black Panther','Star-Lord','Spider Man','Doctor Strange',
           'Ant-Man','Winter Soldier','Loki','Vision','Scarlet Witch']
marvel = pd.DataFrame({'name':members})
marvel.merge(data,how='inner',on='name')
## inner__only keep the wanted one

#############
#radar grp###
#############

fig = plt.figure(figsize=(10, 6))

names = ['Captain Marvel','Thor','Thanos']
scores = pd.DataFrame({'name':names})
## use merge to select certain id
## build a empty dataframe with id merge it with original dataframe
# 提取 A6 得分
scores = scores.merge(data,how='left',on='name')[['intelligence','power','strength','speed','durability','combat']]
scores=scores.drop(index=[1])
print(scores)

scores = scores.values.tolist()

names_cn = ['Captain Marvel','Thor','Thanos']   #标签
zipped = zip(scores,names_cn)

title = ['intelligence','power','strength','speed','durability','combat']  # 标签

for value, name in zipped:
    theta = np.linspace(0, 2*np.pi, len(value), endpoint=False)  # 将圆根据标签的个数等比分
    theta = np.concatenate((theta, [theta[0]]))  # 闭合
    value = np.concatenate((value, [value[0]]))  # 闭合
    ax = fig.add_subplot(111, polar=True)
    ax.plot(theta, value, lw=2, alpha=1, label=name)

ax.set_thetagrids(theta * 180 / np.pi, title)  # 替换标签
ax.set_ylim(0, 110)  # 设置极轴的区间
ax.set_theta_zero_location('N')  # 设置极轴方向
ax.set_title('Captain Marvel & Thor & Thanos', fontsize=20)  # 添加图描述
plt.legend(loc='lower center',ncol=6)

plt.tight_layout()
plt.show()


##############
##grap loop###
##############

plt.figure(figsize=(5, 30))

names = ['Thor', 'Iron Man', 'Captain America', 'Hulk', 'Black Widow', 'Hawkeye']
names_cn = ['Thor', 'Iron Man', 'Captain America', 'Hulk', 'Black Widow', 'Hawkeye']  # 标签
title = ['intelligence', 'power', 'strength', 'speed', 'durability', 'combat']  # 标签

# 从data查询A6 数据
scores = pd.DataFrame({'name': names})
scores = scores.merge(data, how='left', on='name')[
    ['intelligence', 'power', 'strength', 'speed', 'durability', 'combat']]
# 转换为list
scores = scores.values.tolist()

zipped = zip(scores, names_cn)

# for循环生成A6成员雷达图
for i, (value, name) in enumerate(zipped):
    ax = 'ax%s' % i
    theta = np.linspace(0, 2 * np.pi, len(value), endpoint=False)  # 将圆根据标签的个数等比分
    theta = np.concatenate((theta, [theta[0]]))  # 闭合

    value = np.concatenate((value, [value[0]]))  # 闭合

    # 这里要设置为极坐标格式
    ax = plt.subplot2grid(shape=(6, 1), loc=(i, 0), polar=True)
    ax.plot(theta, value, lw=2, alpha=1, label=name)  # 绘图
    ax.fill(theta, value, alpha=0.25)  # 填充

    ax.set_thetagrids(theta * 180 / np.pi, title)  # 替换标签
    ax.set_ylim(0, 110)  # 设置极轴的区间
    ax.set_theta_zero_location('N')  # 设置极轴方向
    ax.set_title('%s SCORE' % name, fontsize=15)  # 添加图描述

plt.tight_layout(h_pad=5.0)




plt.style.use('ggplot')
fig = plt.figure(figsize=(10, 6))

names = ['Thor', 'Iron Man', 'Captain America', 'Hulk', 'Black Widow', 'Hawkeye']  # 标签
names_cn = ['Thor', 'Iron Man', 'Captain America', 'Hulk', 'Black Widow', 'Hawkeye']  # 标签
zipped = zip(scores, names_cn)

title = ['intelligence','power','strength','speed','durability','combat']   #标签


for value, name in zipped:
    theta = np.linspace(0, 2 * np.pi, len(value), endpoint=False)  # 将圆根据标签的个数等比分
    theta = np.concatenate((theta, [theta[0]]))  # 闭合
    value = np.concatenate((value, [value[0]]))  # 闭合
# 这里一定要设置为极坐标格式
    ax = fig.add_subplot(111, polar=True)
    ax.plot(theta, value, lw=2, alpha=1, label=name)  # 绘图
#     ax.fill(theta, value, alpha=0.25)  # 填充

ax.set_thetagrids(theta * 180 / np.pi, title)  # 替换标签
ax.set_ylim(0, 110)  # 设置极轴的区间
ax.set_theta_zero_location('N')  # 设置极轴方向
ax.set_title('The Avengers', fontsize=20)  # 添加图描述

plt.legend(loc='lower center', ncol=6)
plt.tight_layout()
plt.show()

