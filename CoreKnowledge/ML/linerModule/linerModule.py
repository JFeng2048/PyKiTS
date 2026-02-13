# -*- coding:utf-8 -*-
# file:linerModule.py
"""
线型模拟

测试数据：模拟机器生成的数据

进行房价预测

参考文献：机器学习实践（第二版） 李轩涯 、计湘婷、曹焯然 编著
"""

# 导入模块
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


#加载数据
df = pd.read_csv('chinese_house_data.csv')

#设置特征值
X = df.drop(['price'],axis=1)

#设置模型预测值
y = df['price']

# 标准化归一化处理
ss = StandardScaler()
X = ss.fit_transform(X=X)

# 使用train_test_split进行分割为测试集和训练集
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

line_model = linear_model.LinearRegression()
# 训练模型
line_model.fit(X_train,y_train)

# 模型预测
y_predict = line_model.predict(X_test)


for i in range(len(y_predict)):
    error = y_predict[i]-y_test.iloc[i]
    print("预测值：",y_predict[i],"\t真实值：",y_test.iloc[i],"\t误差：",error)

# 模型评估
print("训练集模型评估结果为：",line_model.score(X_train,y_train))
print("测试集模型评估结果为：",line_model.score(X_test,y_test))

plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# 模型结果可视化
# 绘制预测值和真实值
plt.scatter(y_test, y_predict, alpha=0.6, color='blue', s=50)              #绘制散点图
# 添加理想预测线（完美预测时y=x）
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--',
         linewidth=2, label='理想预测线')
plt.xlabel('实际值')
plt.ylabel('预测值')
plt.title('预测值 vs 实际值')
plt.legend()
plt.grid(True, alpha=0.3)

plt.show()

