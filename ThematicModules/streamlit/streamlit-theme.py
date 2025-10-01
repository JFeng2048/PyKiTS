# -*- coding:utf-8 -*-
# file:streamlit-theme.py

"""
pip install streamlit

"""

import streamlit as st

# --- 初始化 session_state ---
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'Light'
if 'layout' not in st.session_state:
    st.session_state['layout'] = 'Single Column'

# --- 语言包 ---
text_dict = {
    "English": {
        "title": "Multilingual App",
        "welcome": "Welcome!",
        "theme_label": "Theme",
        "layout_label": "Layout",
        "single_col": "Single Column",
        "two_col": "Two Columns"
    },
    "中文": {
        "title": "多语言应用",
        "welcome": "欢迎！",
        "theme_label": "主题",
        "layout_label": "布局",
        "single_col": "单列布局",
        "two_col": "双列布局"
    }
}

# --- 侧边栏控制 ---
with st.sidebar:
    # 语言切换
    current_lang = st.session_state['language']
    selected_lang = st.selectbox("Language", options=list(text_dict.keys()), index=list(text_dict.keys()).index(current_lang))
    if selected_lang != current_lang:
        st.session_state['language'] = selected_lang
        st.rerun() # 切换语言后重新运行

    current_text = text_dict[st.session_state['language']] # 获取当前文本

    # 主题切换
    selected_theme = st.selectbox(current_text['theme_label'], ["Light", "Dark"], index=0 if st.session_state['theme'] == 'Light' else 1)
    if selected_theme != st.session_state['theme']:
        st.session_state['theme'] = selected_theme

    # 布局切换
    selected_layout = st.selectbox(current_text['layout_label'], [current_text['single_col'], current_text['two_col']])
    if selected_layout == current_text['single_col']:
        new_layout = 'Single Column'
    else:
        new_layout = 'Two Columns'
    if new_layout != st.session_state['layout']:
        st.session_state['layout'] = new_layout
        st.rerun()

# --- 应用主题 ---
if st.session_state['theme'] == "Dark":
    st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    /* 你可以继续添加其他元素的暗色样式 */
    </style>
    """, unsafe_allow_html=True)
# 否则默认使用 Light 主题

# --- 应用布局和内容 ---
st.title(current_text['title'])
st.write(current_text['welcome'])

if st.session_state['layout'] == 'Single Column':
    st.write("📝 " + current_text['single_col'] + " 的内容区域 A")
    st.write("📊 " + current_text['single_col'] + " 的内容区域 B")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.write("📝 " + current_text['two_col'] + " 的左列内容")
    with col2:
        st.write("📊 " + current_text['two_col'] + " 的右列内容")



