# -*- coding:utf-8 -*-
# file:streamlit-demo.py
import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
import os
from datetime import datetime
import logging

# ----------------------
# 初始化设置
# ----------------------

# 设置日志
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')




# 创建数据库连接
@st.cache_resource
def init_db():
    conn = sqlite3.connect('employee_data.db')
    c = conn.cursor()

    # 创建员工表
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT,
            position TEXT,
            salary REAL,
            hire_date TEXT,
            performance_score INTEGER,
            last_review TEXT
        )
    ''')

    # 创建部门表
    c.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            budget REAL,
            manager TEXT
        )
    ''')

    # 插入示例数据
    if not c.execute("SELECT COUNT(*) FROM employees").fetchone()[0]:
        # 员工数据
        employees = [
            (1, '张伟', '技术部', '高级工程师', 25000, '2020-05-15', 85, '2023-08-10'),
            (2, '李芳', '市场部', '市场经理', 18000, '2019-11-20', 92, '2023-07-22'),
            (3, '王明', '人力资源', 'HR专员', 12000, '2021-02-10', 78, '2023-06-15'),
            (4, '赵静', '技术部', '初级工程师', 15000, '2022-03-01', 88, '2023-07-30'),
            (5, '陈强', '财务部', '财务主管', 22000, '2018-09-05', 90, '2023-08-05'),
            (6, '杨帆', '市场部', '市场专员', 14000, '2021-07-12', 82, '2023-06-20'),
            (7, '周婷', '技术部', '技术总监', 35000, '2017-04-22', 95, '2023-07-15'),
            (8, '吴磊', '人力资源', 'HR经理', 20000, '2019-08-30', 87, '2023-08-01')
        ]
        c.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?)", employees)

        # 部门数据
        departments = [
            (1, '技术部', 1500000, '周婷'),
            (2, '市场部', 800000, '李芳'),
            (3, '人力资源', 500000, '吴磊'),
            (4, '财务部', 600000, '陈强')
        ]
        c.executemany("INSERT INTO departments VALUES (?, ?, ?, ?)", departments)

    conn.commit()
    return conn


# 初始化数据库
db_conn = init_db()

# ----------------------
# 多语言支持
# ----------------------

# 定义语言包
text_dict = {
    "中文": {
        "app_title": "企业员工数据分析平台",
        "welcome": "欢迎使用员工数据分析平台",
        "dashboard": "仪表板",
        "employee_management": "员工管理",
        "department_analysis": "部门分析",
        "salary_distribution": "薪资分布",
        "performance": "绩效评估",
        "add_employee": "添加新员工",
        "name": "姓名",
        "department": "部门",
        "position": "职位",
        "salary": "薪资",
        "hire_date": "入职日期",
        "performance_score": "绩效分数",
        "last_review": "上次评估日期",
        "submit": "提交",
        "update": "更新",
        "delete": "删除",
        "department_budget": "部门预算",
        "avg_salary": "平均薪资",
        "employee_count": "员工数量",
        "performance_distribution": "绩效分布",
        "salary_vs_performance": "薪资与绩效关系",
        "search": "搜索",
        "theme": "主题",
        "language": "语言",
        "layout": "布局",
        "light": "浅色",
        "dark": "深色",
        "sidebar": "侧边栏布局",
        "horizontal": "水平布局",
        "success": "操作成功",
        "error": "发生错误",
        "navigation": "导航菜单",
        "select": "选择"  # 添加缺失的键值
    },
    "English": {
        "app_title": "Enterprise Employee Analytics Platform",
        "welcome": "Welcome to Employee Analytics Platform",
        "dashboard": "Dashboard",
        "employee_management": "Employee Management",
        "department_analysis": "Department Analysis",
        "salary_distribution": "Salary Distribution",
        "performance": "Performance Evaluation",
        "add_employee": "Add New Employee",
        "name": "Name",
        "department": "Department",
        "position": "Position",
        "salary": "Salary",
        "hire_date": "Hire Date",
        "performance_score": "Performance Score",
        "last_review": "Last Review Date",
        "submit": "Submit",
        "update": "Update",
        "delete": "Delete",
        "department_budget": "Department Budget",
        "avg_salary": "Average Salary",
        "employee_count": "Employee Count",
        "performance_distribution": "Performance Distribution",
        "salary_vs_performance": "Salary vs Performance",
        "search": "Search",
        "theme": "Theme",
        "language": "Language",
        "layout": "Layout",
        "light": "Light",
        "dark": "Dark",
        "sidebar": "Sidebar Layout",
        "horizontal": "Horizontal Layout",
        "success": "Operation Successful",
        "error": "Error Occurred",
        "navigation": "Navigation",
        "select": "Select"  # 添加缺失的键值
    }
}

# 初始化session_state
if 'language' not in st.session_state:
    st.session_state.language = '中文'
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'layout' not in st.session_state:
    st.session_state.layout = 'sidebar'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'edit_employee_id' not in st.session_state:
    st.session_state.edit_employee_id = None


# 获取当前语言文本
def get_text(key):
    return text_dict[st.session_state.language][key]


# ----------------------
# 自定义主题
# ----------------------

def apply_theme():
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
            .stApp {
                background-color: #1e1e1e;
                color: #f0f0f0;
            }
            .css-18e3th9 {
                background-color: #2d2d2d;
            }
            .css-1d391kg {
                background-color: #3d3d3d;
            }
            .st-bb {
                background-color: #3d3d3d;
            }
            .st-at {
                background-color: #3d3d3d;
            }
            .css-1cpxqw2 {
                color: #f0f0f0;
            }
            /* 添加更多自定义样式 */
        </style>
        """, unsafe_allow_html=True)
    else:
        # 重置为默认浅色主题
        st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
                color: #31333F;
            }
        </style>
        """, unsafe_allow_html=True)


# ----------------------
# 数据获取函数（带缓存）
# ----------------------

@st.cache_data(ttl=3600)  # 缓存1小时
def get_employee_data():
    try:
        df = pd.read_sql_query("SELECT * FROM employees", db_conn)
        df['hire_date'] = pd.to_datetime(df['hire_date'])
        df['last_review'] = pd.to_datetime(df['last_review'])
        return df
    except Exception as e:
        logging.error(f"获取员工数据失败: {str(e)}")
        st.error(f"{get_text('error')}: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_department_data():
    try:
        return pd.read_sql_query("SELECT * FROM departments", db_conn)
    except Exception as e:
        logging.error(f"获取部门数据失败: {str(e)}")
        st.error(f"{get_text('error')}: {str(e)}")
        return pd.DataFrame()


# ----------------------
# 员工管理功能
# ----------------------

def add_employee(name, department, position, salary, hire_date, performance_score, last_review):
    try:
        c = db_conn.cursor()
        c.execute("""
                  INSERT INTO employees (name, department, position, salary, hire_date, performance_score, last_review)
                  VALUES (?, ?, ?, ?, ?, ?, ?)
                  """, (name, department, position, salary, hire_date, performance_score, last_review))
        db_conn.commit()
        st.success(get_text('success'))
        st.cache_data.clear()  # 清除缓存
        logging.info(f"添加新员工: {name}")
    except Exception as e:
        logging.error(f"添加员工失败: {str(e)}")
        st.error(f"{get_text('error')}: {str(e)}")


def update_employee(employee_id, name, department, position, salary, hire_date, performance_score, last_review):
    try:
        c = db_conn.cursor()
        c.execute("""
                  UPDATE employees
                  SET name=?,
                      department=?,
                      position=?,
                      salary=?,
                      hire_date=?,
                      performance_score=?,
                      last_review=?
                  WHERE id = ?
                  """, (name, department, position, salary, hire_date, performance_score, last_review, employee_id))
        db_conn.commit()
        st.success(f"{get_text('update')} {get_text('success')}")
        st.cache_data.clear()  # 清除缓存
        logging.info(f"更新员工信息: ID={employee_id}")
    except Exception as e:
        logging.error(f"更新员工失败: {str(e)}")
        st.error(f"{get_text('error')}: {str(e)}")


def delete_employee(employee_id):
    try:
        c = db_conn.cursor()
        c.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        db_conn.commit()
        st.success(f"{get_text('delete')} {get_text('success')}")
        st.cache_data.clear()  # 清除缓存
        logging.info(f"删除员工: ID={employee_id}")
    except Exception as e:
        logging.error(f"删除员工失败: {str(e)}")
        st.error(f"{get_text('error')}: {str(e)}")


# ----------------------
# 页面组件
# ----------------------

def dashboard_page():
    st.title(get_text('dashboard'))

    # 获取数据
    employee_df = get_employee_data()
    department_df = get_department_data()

    if employee_df.empty or department_df.empty:
        st.warning("没有可用数据")
        return

    # 关键指标
    st.subheader(get_text('department_analysis'))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(get_text('department_budget'), f"¥{department_df['budget'].sum():,.0f}")
    with col2:
        st.metric(get_text('avg_salary'), f"¥{employee_df['salary'].mean():,.0f}")
    with col3:
        st.metric(get_text('employee_count'), len(employee_df))

    # 部门分析图表
    st.subheader(get_text('department_analysis'))
    dept_summary = employee_df.groupby('department').agg(
        avg_salary=('salary', 'mean'),
        employee_count=('id', 'count')
    ).reset_index()

    dept_summary = dept_summary.merge(department_df, left_on='department', right_on='name', how='left')

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(dept_summary, x='department', y='avg_salary',
                     title=get_text('avg_salary'), color='department')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(dept_summary, names='department', values='employee_count',
                     title=get_text('employee_count'))
        st.plotly_chart(fig, use_container_width=True)

    # 绩效分析
    st.subheader(get_text('performance'))
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(employee_df, x='performance_score',
                           title=get_text('performance_distribution'), nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(employee_df, x='salary', y='performance_score', color='department',
                         title=get_text('salary_vs_performance'), hover_data=['name'])
        st.plotly_chart(fig, use_container_width=True)


def employee_management_page():
    st.title(get_text('employee_management'))

    employee_df = get_employee_data()

    # 搜索功能
    search_term = st.text_input(get_text('search'), key='employee_search')
    if search_term:
        filtered_df = employee_df[
            employee_df['name'].str.contains(search_term, case=False) |
            employee_df['department'].str.contains(search_term, case=False) |
            employee_df['position'].str.contains(search_term, case=False)
            ]
    else:
        filtered_df = employee_df

    # 显示员工表格
    st.dataframe(filtered_df, use_container_width=True)

    # 添加/编辑员工表单
    st.subheader(
        get_text('add_employee') if st.session_state.edit_employee_id is None
        else f"{get_text('update')} {get_text('employee_management')}"
    )

    with st.form("employee_form"):
        name = st.text_input(get_text('name'), key='emp_name')
        department = st.selectbox(
            get_text('department'),
            options=get_department_data()['name'].tolist(),
            key='emp_dept'
        )
        position = st.text_input(get_text('position'), key='emp_position')
        salary = st.number_input(get_text('salary'), min_value=0, step=1000, key='emp_salary')
        hire_date = st.date_input(get_text('hire_date'), key='emp_hire_date')
        performance_score = st.slider(
            get_text('performance_score'), 0, 100, 80, key='emp_perf'
        )
        last_review = st.date_input(get_text('last_review'), key='emp_review')

        submitted = st.form_submit_button(
            get_text('submit') if st.session_state.edit_employee_id is None
            else get_text('update')
        )

        if submitted:
            if st.session_state.edit_employee_id is None:
                add_employee(
                    name, department, position, salary,
                    hire_date.strftime('%Y-%m-%d'),
                    performance_score,
                    last_review.strftime('%Y-%m-%d')
                )
            else:
                update_employee(
                    st.session_state.edit_employee_id,
                    name, department, position, salary,
                    hire_date.strftime('%Y-%m-%d'),
                    performance_score,
                    last_review.strftime('%Y-%m-%d')
                )
                st.session_state.edit_employee_id = None

    # 编辑和删除按钮
    if not filtered_df.empty:
        selected_index = st.selectbox(
            f"{get_text('select')} {get_text('employee_management')}",
            filtered_df.index,
            format_func=lambda x: f"{filtered_df.loc[x, 'name']} - {filtered_df.loc[x, 'position']}"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(get_text('edit')):
                employee = filtered_df.loc[selected_index]
                st.session_state.edit_employee_id = employee['id']
                st.session_state.emp_name = employee['name']
                st.session_state.emp_dept = employee['department']
                st.session_state.emp_position = employee['position']
                st.session_state.emp_salary = employee['salary']
                st.session_state.emp_hire_date = employee['hire_date']
                st.session_state.emp_perf = employee['performance_score']
                st.session_state.emp_review = employee['last_review']
                st.rerun()

        with col2:
            if st.button(get_text('delete')):
                employee_id = filtered_df.loc[selected_index, 'id']
                delete_employee(employee_id)


# ----------------------
# 主应用布局
# ----------------------

def main():
    # 应用主题
    apply_theme()

    # 顶部控制栏
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.title(get_text('app_title'))

        with col2:
            st.session_state.language = st.selectbox(
                get_text('language'),
                options=['中文', 'English'],
                index=0 if st.session_state.language == '中文' else 1
            )

        with col3:
            st.session_state.theme = st.selectbox(
                get_text('theme'),
                options=['light', 'dark'],
                index=0 if st.session_state.theme == 'light' else 1
            )

    # 水平导航
    menu_options = {
        'dashboard': get_text('dashboard'),
        'employee_management': get_text('employee_management')
    }

    if st.session_state.layout == 'horizontal':
        selected = option_menu(
            menu_title=None,
            options=list(menu_options.values()),
            icons=['house', 'people'],
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "nav-link": {"font-size": "15px", "margin": "0px 10px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#4CAF50", "font-weight": "bold"},
            }
        )

        # 将选中的菜单项映射回key
        st.session_state.current_page = [k for k, v in menu_options.items() if v == selected][0]

    # 侧边栏布局
    else:
        with st.sidebar:
            st.subheader(get_text('navigation'))
            for page_key, page_name in menu_options.items():
                if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
                    st.session_state.current_page = page_key

            st.session_state.layout = st.selectbox(
                get_text('layout'),
                options=[get_text('sidebar'), get_text('horizontal')],
                index=0 if st.session_state.layout == 'sidebar' else 1
            )

    # 显示当前页面
    if st.session_state.current_page == 'dashboard':
        dashboard_page()
    elif st.session_state.current_page == 'employee_management':
        employee_management_page()


# ----------------------
# 运行应用
# ----------------------

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("应用运行时错误")
        st.error(f"严重错误: {str(e)}")
        st.stop()