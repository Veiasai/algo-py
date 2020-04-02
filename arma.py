# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import base64
import io
import json

from statsmodels.tsa.arima_model import ARMA


def arma(paras):     # {data: bytes .csv, length: number}
    df = pd.read_csv(paras['data'])  #读取csv文件
    #read load
    data = df['data']
    length = paras['length']
    model = ARMA(data, order =(1,1))
    result_arma = model.fit(disp=-1, method='css')
    prediction = result_arma.predict(len(data),len(data)+length-1)   #start end   
    prediction.columns = ['id', 'data']
    fig = plt.Figure()
    ax = fig.subplots()
    ax.plot(prediction, 'r', label='prediction')

    ax.legend(loc='best')
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    return {'img': img, 'prediction': prediction.to_csv()}

if __name__ == "__main__":
    f = open('./arma_mini.csv')
    length = 10
    ret = arma({'data': f, 'length': length})
    # print(json.dumps(ret))
    img = open('./arma.png', 'w')
    img.write(ret['img'])
    img.close()
'''
输入：在软件里以excel格式上传历史数据；输入需要预测的天数
输出：直接输出预测数据结果（最好可以实现把结果直接生成excel）；预测数据图像
'''