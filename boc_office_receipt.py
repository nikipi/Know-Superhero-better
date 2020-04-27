import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
movie = ['战狼2','流浪地球','复仇者联盟4','红海行动','唐人街探案2','美人鱼','我不是药神','速度与激情8','西红市首富','捉妖记']

income = [56.83,46.55,38.25,36.51,33.98,33.86,31.00,26.71,25.48,24.40]
data_movies = pd.DataFrame({'movie':movie,'income':income})[::-1] #倒序
print(data_movies)

#显示中文
plt.rcParams['font.sans-serif']=['Arial Unicode MS']
plt.rcParams['axes.unicode_minus']=False

# 绘制票房条形图
# https://stackoverflow.com/questions/37447056/different-colors-for-rows-in-barh-chart-from-pandas-dataframe-python
# 可以单独设置颜色，或者list分别设置

plt.style.use('ggplot')
# fig,ax = plt.subplots(figsize=(6,10))
fig,ax = plt.subplots(figsize=(8,6))

grey = '#969696'#深灰
red = '#E24A33' #红色

barh = ax.barh(np.arange(10),
               data_movies['income'],
               color='#969696')
# 单独为复联4和速8上色
barh[7].set_color(red)
barh[2].set_color('#EB8171')

for y,x in enumerate(data_movies['income'].values.tolist()):
   ax.text(x-1,y-0.1,'%s'%round(x,1),
            ha='right',
            size=15,
            color='#FFFFFF')
ax.set_yticks(np.arange(10))
ax.set_yticklabels(data_movies['movie'].tolist(),size=15)
# ax.set_xlim(0,62)

ax.legend(['BOX OFFICE RECEIPT)'],loc='best')
plt.tight_layout()
plt.show()

movies = ['阿凡达','泰坦尼克号','星球大战：原力觉醒','复仇者联盟3','复仇者联盟4','侏罗纪世界','复仇者联盟','速度与激情7','复仇者联盟2','黑豹']

income = [27.88,21.87,20.68,20.48,19.14,16.72,15.19,15.16,14.05,13.47,]
data_movies = pd.DataFrame({'movie':movies,'income':income})[::-1]#倒序

# 绘制票房条形图
# https://stackoverflow.com/questions/37447056/different-colors-for-rows-in-barh-chart-from-pandas-dataframe-python
# 可以单独设置颜色，或者list分别设置

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(8, 6))

grey = '#969696'  # 深灰
red = '#E24A33'  # 红色
# 批量设置颜色
color = [red, red, grey, red, grey, red, red, grey, grey, grey]

barh = ax.barh(np.arange(10),
               data_movies['income'],
               color=color)

for y, x in enumerate(data_movies['income'].values.tolist()):
    ax.text(x-1, y-0.1, '%s' % round(x, 1),
            ha='right',
            size=15,
            color='#FFFFFF')

ax.set_yticks(np.arange(10))
ax.set_yticklabels(data_movies['movie'].tolist(), size=15)
ax.set_xlim(0, 32)

ax.legend(['票房(亿美元)'], loc='best')

plt.tight_layout()
plt.savefig('/Users/apple/Desktop/CODELIKEAPRICK/global.png', dpi=200)