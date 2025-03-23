
from datetime import time
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
# 从TXT文件中读取用户信息
def load_users_from_file(filename):
    users = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    username, password = line.split(':')
                    users[username] = password
        return users
    except Exception as e:
        st.error(f"读取用户文件时出错: {e}")
        return {}

# 加载用户信息
users = load_users_from_file('users.txt')

# 如果用户未登录，显示登录表单
if not getattr(st.session_state, 'logged_in', False):
    with st.form("login_form"):
        st.subheader("请登录")
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submitted = st.form_submit_button("登录")

    # 检查用户是否登录成功
    if submitted:
        with st.spinner('loading...'):
         if username in users and users[username] == password:
            st.success("登录成功！")
            time.sleep(2)
            st.session_state.logged_in = True
            st.rerun()  # 重新运行应用以跳转到数据展示页面
         else:
            st.error("用户名或密码错误！")
            time.sleep(2)
            st.session_state.logged_in = False
            st.rerun()
else:
    st.set_page_config(page_title="平均注意力权重", page_icon="📈")
    
    add_selectbox = st.sidebar.selectbox(
        "选择注意力权重",
        ("平均值注意力权重-特征", "平均值注意力权重-时序")
    )
    
    if add_selectbox == '平均值注意力权重-时序':
    
        st.markdown("# 平均注意力权重得分")
        st.sidebar.header("平均注意力权重得分")
        st.write(
            """测试集数据注意力权重得分值取平均，展示100个时序数据点注意力权重得分值,每25个得分数据展示一次折线图！"""
        )
        excel_file_path = '1DNN-LSTM_att_3ymodel_Top25Values.xlsx'
        # 初始化进度条和状态文本
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        data_att =pd.read_excel(excel_file_path, sheet_name='average_top_100_values')
        # 模拟数据处理过程
        # 模拟数据处理过程
        for i in range(1, 101):  # 用500个测试数据
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
    else:
    
        st.markdown("# 平均注意力权重得分")
        st.sidebar.header("平均注意力权重得分")
        st.write(
            """测试集数据注意力权重得分值取平均，展示128个特征数据点注意力权重得分值,每25个得分数据展示一次折线图！"""
        )
        excel_file_path = '1DNN-LSTM_att_3ymodel_Top25Values_.xlsx'
        # 初始化进度条和状态文本
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        data_att = pd.read_excel(excel_file_path, sheet_name='average_top_128_values_')
        # 模拟数据处理过程
    
        # 模拟数据处理过程
        for i in range(1, 101):  # 用500个测试数据
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
                fig.update_layout(yaxis=dict(range=[0, 1]))
                fig.update_layout(
                    xaxis=dict(
                        range=[0, i],
                        ticktext=data_att['indices'][:i],  # 设置刻度标签
                        tickvals=list(range(len(data_att['indices'][:i]))),  # 设置刻度位置
                    )
                )
                fig.update_layout(title_text="Line Chart-att")
                fig.update_layout(xaxis_title='特征数据点', yaxis_title='平均注意力权重')
    
                # 在Streamlit中显示图表
                st.plotly_chart(fig)
    
        # 完成进度
        progress_bar.progress(1)
        status_text.text("Processing complete!")
