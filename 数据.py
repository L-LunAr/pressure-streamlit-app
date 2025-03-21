import time

import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
#from pymysql import connect
#import pymysql
DATA_URL=r"D:\LunAr-chengxu\jupyter-L\shuju_total.csv"
#from pages import mysql_connect
st.title('均质油藏压力和压力导数数据')
@st.cache_data
# 定义加载数据的函数
def load_data(start, end):
    # 这里假设你想加载从start到end行的数据
    # 由于pandas的read_csv没有直接支持范围的参数，这里分步骤处理
    data = pd.read_csv(DATA_URL)
    data = data[start:end]
    data = np.array(data)
    data = data[:, 1:]
    data = pd.DataFrame(data, columns=["压力变化", "压力导数"])
    return data
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
users = load_users_from_file(r'D:\\LunAr-chengxu\\pycharm-L\\streamlit-1\\users.txt')

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
    # 如果用户已登录，显示数据
    data_load_state = st.text('正在加载数据...')
    data = load_data(1000000,2000000)#加载1000000到2000000之间的数据
    data_load_state.text("Done! (using data)")

    if st.checkbox('显示压力和压力导数数据'):
        st.subheader('压力和压力导数数据')
        st.dataframe(data, width=600, height=800)
