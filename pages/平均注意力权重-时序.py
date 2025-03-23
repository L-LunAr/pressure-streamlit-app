from datetime import time
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(page_title="平均注意力权重", page_icon="📈")

st.markdown("#平均注意力权重得分")
st.sidebar.header("平均注意力权重得分")
st.write(
    """测试集数据注意力权重得分值取平均，展示100个时序数据点注意力权重得分值,每25个得分数据展示一次折线图！"""
)
excel_file_path = '1DNN-LSTM_att_3ymodel_Top25Values.xlsx'
# 初始化进度条和状态文本
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
data_att=pd.read_excel(excel_file_path,sheet_name='average_top_100_values')
# 模拟数据处理过程
# 模拟数据处理过程
for i in range(1, 101):
    # 更新进度条
    progress_bar.progress(i / 100)
    # 更新状态文本
    status_text.text(f"Processing step: {int(i / 100 * 100)}%")

    # 每隔25次展示一次图像
    if i % 25 == 0:
        # 更新图表数据
        # 初始化图表x=data_att['indices'][:i]
        fig = go.Figure()
        # 设置图表的宽度和高度
        fig.update_layout(width=1800, height=600)
        fig.add_trace(go.Scatter(y=data_att['values'][:i], mode='lines', name='att',
                                 line=dict(color='#FF0000', width=2)))

        # 设置纵坐标的范围
        fig.update_layout(yaxis=dict(range=[0, 0.15]))
        fig.update_layout(
            xaxis=dict(
                range=[0, i],
                ticktext=data_att['indices'][:i],  # 设置刻度标签
                tickvals=list(range(len(data_att['indices'][:i]))),  # 设置刻度位置
            )
        )
        fig.update_layout(title_text="Line Chart-att")
        fig.update_layout(xaxis_title='时序数据点', yaxis_title='平均注意力权重')

        # 在Streamlit中显示图表
        st.plotly_chart(fig)

# 完成进度
progress_bar.progress(1)
status_text.text("Processing complete!")
