from datetime import time
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
excel_file_path1 = r'D:\LunAr-chengxu\jupyter-L\1DNN-LSTM-Att-3y.xlsx'
excel_file_path2=r'D:\LunAr-chengxu\jupyter-L\y_test10000.xlsx'
predict_y= pd.read_excel(excel_file_path1)# 指定Excel文件路径
real_y=pd.read_excel(excel_file_path2)# 指定Excel文件路径
y_predict1_1 = predict_y[0]
y_predict1_2 = predict_y[1]
y_predict1_3= predict_y[2]
y_test_1=real_y['Col1']
y_test_2=real_y['Col2']
y_test_3=real_y['Col3']
st.set_page_config(page_title="井筒储集系数拟合效果", page_icon="📈")

st.markdown("#井筒储集系数拟合效果")
st.sidebar.header("井筒储集系数拟合效果")
st.write(
    """展示了500个测试数据的井筒储集系数拟合效果的绘图和动画组合,每50个测试数据展示一次！"""
)
# 初始化进度条
# 初始化空的DataFrame
chart_data3 = pd.DataFrame(columns=['pre3', 'real3'])
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
for i in range(1, 501):  # 用500个测试数据
    # 更新进度条
    progress_bar.progress(i / 500)

    # 更新状态文本
    status_text.text(f"Processing step: {int(i / 500 * 100)}%")

    # 更新折线图数据
    new_data = pd.DataFrame({'pre3': [y_predict1_3[i-1]], 'real3': [y_test_3[i-1]]})
    chart_data3 = pd.concat([chart_data3, new_data], ignore_index=True)

    # 每隔50次展示一次图像
    if i % 50 == 0 :
        # 使用Plotly绘制折线图，并设置纵坐标的范围
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data3.index, y=chart_data3['pre3'], mode='lines', name='pre3',line=dict(color='#FF0000', width=2)))
        fig.add_trace(go.Scatter(x=chart_data3.index, y=chart_data3['real3'], mode='lines', name='real3',line=dict(color='#0000FF', width=2)))
        fig.update_layout(yaxis=dict(range=[2.2, 3.1]))  # 设置纵坐标的范围
        fig.update_layout(xaxis=dict(range=[0, i]))
        fig.update_layout(title_text="Line Chart-井筒储集系数")
        fig.update_layout(xaxis_title='数据点', yaxis_title='井筒储集系数')
        # 在Streamlit中显示图表
        st.plotly_chart(fig)


# 完成进度
progress_bar.progress(1)
status_text.text("Processing complete!")