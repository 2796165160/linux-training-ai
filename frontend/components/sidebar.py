import streamlit as st
from typing import List, Callable

def show_sidebar(current_user_name: str, role: str, menu_options: List[str]) -> str:
    """
    显示侧边栏
    
    Args:
        current_user_name: 当前用户名
        role: 用户角色
        menu_options: 菜单选项列表
        
    Returns:
        选中的菜单项
    """
    with st.sidebar:
        st.title("AI实训报告系统")
        
        st.write(f"用户: {current_user_name}")
        st.write(f"角色: {'教师' if role == 'teacher' else '学生'}")
        
        st.divider()
        
        # 菜单选择
        selected = st.radio("功能菜单", menu_options)
        
        st.divider()
        
        # 退出登录按钮
        if st.button("退出登录", use_container_width=True):
            st.session_state.token = None
            st.session_state.role = None
            st.session_state.current_page = "login"
            st.experimental_rerun()
        
        # 调试模式开关
        debug_mode = st.checkbox("调试模式", value=st.session_state.get("debug_mode", False))
        if debug_mode != st.session_state.get("debug_mode", False):
            st.session_state.debug_mode = debug_mode
        
        st.write("---")
        st.write("© 2023 AI实训报告系统")
        
    return selected
