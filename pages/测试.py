from datetime import time
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import time
import numpy as np
excel_file_path20000= '1DNN-LSTM-Att-test-20000.xlsx'
y_predict=pd.read_excel(excel_file_path20000)# 指定Excel文件路径
# 读取 Excel 文件
excel_file_path20000='y_test20000.xlsx'
y_test20000=pd.read_excel(excel_file_path20000)# 指定Excel文件路径

# 将四列真实值分别提取并保存到对应的列表中
real_y1 = y_test20000[0]
real_y2 = y_test20000[1]
real_y3 = y_test20000[2]
y_predict1_1 = y_predict[0]
y_predict1_2 = y_predict[1]
y_predict1_3= y_predict[2]
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
    st.set_page_config(page_title="油藏参数拟合效果", page_icon="📈")
    add_selectbox = st.sidebar.selectbox(
        "选择均质油藏油藏参数",
        ("渗透率", "表皮系数", "井筒储集系数")
    )

    if add_selectbox =="渗透率":
        # 创建一个按钮来展示表格
        if st.button("展示渗透率真实值和预测值"):
            st.session_state.show_table1 = True
        st.markdown("# 渗透率拟合效果")
        st.sidebar.header("渗透率拟合效果")
        st.write(
            """展示了500个新数据的渗透率拟合效果的绘图和动画组合,每50个测试数据展示一次！"""
        )
        # 展示表格
        if getattr(st.session_state, 'show_table1', False):
            st.subheader("渗透率真实值与预测值")
            table_data1 = pd.DataFrame({
                'real_K': real_y1.head(500),
                'pred_k': y_predict1_1.head(500)
            })
            st.dataframe(table_data1, width=800, height=400)

            # 模拟跳转延迟
            time.sleep(2)
            # 创建一个按钮来展示折线图
        if st.button("展示渗透率拟合效果折线图"):
            # 跳转到展示折线图
            st.session_state.show_chart1 = True

        # 展示折线图
        if getattr(st.session_state, 'show_chart1', False):
            # 初始化进度条
            # 初始化空的DataFrame
            chart_data1 = pd.DataFrame(columns=['pre1', 'real1'])
            progress_bar = st.sidebar.progress(0)
            status_text = st.sidebar.empty()
            for i in range(1, 501):  # 先用500个测试数据
                # 更新进度条
                progress_bar.progress(i / 500)

                # 更新状态文本
                status_text.text(f"Processing step: {int(i / 500 * 100)}%")

                # 更新折线图数据
                new_data = pd.DataFrame({'pre1': [y_predict1_1[i - 1]], 'real1': [real_y1[i - 1]]})
                chart_data1 = pd.concat([chart_data1, new_data], ignore_index=True)

                # 每隔50次展示一次图像
                if i % 50 == 0:
                    # 使用Plotly绘制折线图，并设置纵坐标的范围
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=chart_data1.index, y=chart_data1['pre1'], mode='lines', name='pre1',
                                             line=dict(color='#FF0000', width=2)))
                    fig.add_trace(go.Scatter(x=chart_data1.index, y=chart_data1['real1'], mode='lines', name='real1',
                                             line=dict(color='#0000FF', width=2)))
                    fig.update_layout(yaxis=dict(range=[0, 5]))  # 设置纵坐标的范围
                    fig.update_layout(xaxis=dict(range=[0, i]))
                    fig.update_layout(title_text="Line Chart-渗透率")
                    fig.update_layout(xaxis_title='数据点', yaxis_title='渗透率')
                    # 在Streamlit中显示图表
                    st.plotly_chart(fig)

            # 完成进度
            progress_bar.progress(1)
            status_text.text("Processing complete!")
    elif add_selectbox =="表皮系数":
        # 创建一个按钮来展示表格
        if st.button("展示表皮系数真实值和预测值"):
            st.session_state.show_table2 = True
        st.markdown("# 表皮系数拟合效果")
        st.sidebar.header("表皮系数拟合效果")
        st.write(
            """展示了500个新数据的表皮系数拟合效果的绘图和动画组合,每50个测试数据展示一次！"""
        )
        # 展示表格
        if getattr(st.session_state, 'show_table2', False):
            st.subheader("表皮系数真实值与预测值")
            table_data2 = pd.DataFrame({
                'real_S': real_y2.head(500),
                'pred_S': y_predict1_2.head(500)
            })
            st.dataframe(table_data2, width=800, height=400)

            # 模拟跳转延迟
            time.sleep(2)
            # 创建一个按钮来展示折线图
        if st.button("展示表皮系数拟合效果折线图"):
            # 跳转到展示折线图
            st.session_state.show_chart2 = True

        # 展示折线图
        if getattr(st.session_state, 'show_chart2', False):
            # 初始化进度条
            # 初始化空的DataFrame
            chart_data2 = pd.DataFrame(columns=['pre2', 'real2'])
            progress_bar = st.sidebar.progress(0)
            status_text = st.sidebar.empty()
            for i in range(1, 501):  # 用500个测试数据
                # 更新进度条
                progress_bar.progress(i / 500)

                # 更新状态文本
                status_text.text(f"Processing step: {int(i / 500 * 100)}%")

                # 更新折线图数据
                new_data = pd.DataFrame({'pre2': [y_predict1_2[i - 1]], 'real2': [real_y2[i - 1]]})
                chart_data2 = pd.concat([chart_data2, new_data], ignore_index=True)

                # 每隔50次展示一次图像
                if i % 50 == 0:
                    # 使用Plotly绘制折线图，并设置纵坐标的范围
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=chart_data2.index, y=chart_data2['pre2'], mode='lines', name='pre2',
                                             line=dict(color='#FF0000', width=2)))
                    fig.add_trace(go.Scatter(x=chart_data2.index, y=chart_data2['real2'], mode='lines', name='real2',
                                             line=dict(color='#0000FF', width=2)))
                    fig.update_layout(yaxis=dict(range=[0, 1]))  # 设置纵坐标的范围
                    fig.update_layout(xaxis=dict(range=[0, i]))
                    fig.update_layout(title_text="Line Chart-表皮系数")
                    fig.update_layout(xaxis_title='数据点', yaxis_title='表皮系数')
                    # 在Streamlit中显示图表
                    st.plotly_chart(fig)

            # 完成进度
            progress_bar.progress(1)
            status_text.text("Processing complete!")
    else:
        # 创建一个按钮来展示表格
        if st.button("展示井筒储集系数真实值和预测值"):
            st.session_state.show_table3 = True
        st.markdown("# 井筒储集系数拟合效果")
        st.sidebar.header("井筒储集系数拟合效果")
        st.write(
            """展示了500个新数据的井筒储集系数拟合效果的绘图和动画组合,每50个测试数据展示一次！"""
        )
        # 展示表格
        if getattr(st.session_state, 'show_table3', False):
            st.subheader("井筒储集系数真实值与预测值")
            table_data3 = pd.DataFrame({
                'real_C': real_y3.head(500),
                'pred_C': y_predict1_3.head(500)
            })
            st.dataframe(table_data3, width=800, height=400)

            # 模拟跳转延迟
            time.sleep(2)
            # 创建一个按钮来展示折线图
        if st.button("展示井筒储集系数折线图"):
            # 跳转到展示折线图
            st.session_state.show_chart3 = True
        # 展示折线图
        if getattr(st.session_state, 'show_chart3', False):
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
                new_data = pd.DataFrame({'pre3': [y_predict1_3[i - 1]], 'real3': [real_y3[i - 1]]})
                chart_data3 = pd.concat([chart_data3, new_data], ignore_index=True)

                # 每隔50次展示一次图像
                if i % 50 == 0:
                    # 使用Plotly绘制折线图，并设置纵坐标的范围
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=chart_data3.index, y=chart_data3['pre3'], mode='lines', name='pre3',
                                             line=dict(color='#FF0000', width=2)))
                    fig.add_trace(go.Scatter(x=chart_data3.index, y=chart_data3['real3'], mode='lines', name='real3',
                                             line=dict(color='#0000FF', width=2)))
                    fig.update_layout(yaxis=dict(range=[1.2, 3.1]))  # 设置纵坐标的范围
                    fig.update_layout(xaxis=dict(range=[0, i]))
                    fig.update_layout(title_text="Line Chart-井筒储集系数")
                    fig.update_layout(xaxis_title='数据点', yaxis_title='井筒储集系数')
                    # 在Streamlit中显示图表
                    st.plotly_chart(fig)

            # 完成进度
            progress_bar.progress(1)
            status_text.text("Processing complete!")
