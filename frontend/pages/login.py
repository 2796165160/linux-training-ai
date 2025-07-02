import streamlit as st
from frontend.utils.api import login, register

def show_login_page():
    """登录页面"""
    # 使用列布局居中显示登录框
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <h1 style="color:#1E88E5; margin-bottom:0;">AI实训报告生成系统</h1>
            <p style="color:#757575; font-size:18px;">使用AI技术快速生成标准化实训报告</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 创建一个带样式的卡片容器
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["登录", "注册"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown('<p style="font-size:18px; font-weight:500; color:#333; text-align:center; margin-bottom:15px;">用户登录</p>', unsafe_allow_html=True)
                username = st.text_input("用户名", placeholder="请输入用户名")
                password = st.text_input("密码", type="password", placeholder="请输入密码")
                
                col1, col2 = st.columns(2)
                with col1:
                    remember = st.checkbox("记住我", value=True)
                
                submit_button = st.form_submit_button("登录", use_container_width=True)
                
                if submit_button:
                    if not username or not password:
                        st.error("请输入用户名和密码")
                    else:
                        with st.spinner("登录中..."):
                            if login(username, password):
                                st.success("登录成功!")
                                st.session_state.current_page = "main"
                                st.experimental_rerun()
                            else:
                                st.error("登录失败，请检查用户名和密码")
        
        with tab2:
            with st.form("register_form"):
                st.markdown('<p style="font-size:18px; font-weight:500; color:#333; text-align:center; margin-bottom:15px;">新用户注册</p>', unsafe_allow_html=True)
                
                reg_username = st.text_input("用户名", key="reg_username", placeholder="请设置用户名")
                reg_email = st.text_input("邮箱地址", placeholder="请输入有效的邮箱地址")
                reg_password = st.text_input("密码", type="password", key="reg_password", placeholder="请设置密码")
                reg_password_confirm = st.text_input("确认密码", type="password", placeholder="请再次输入密码")
                
                col1, col2 = st.columns(2)
                with col1:
                    reg_role = st.selectbox("选择角色", ["student", "teacher"], 
                                         format_func=lambda x: "学生" if x == "student" else "教师")
                
                st.markdown('<p style="font-size:12px; color:#757575;">注册即表示您同意我们的服务条款和隐私政策</p>', unsafe_allow_html=True)
                
                submit_reg_button = st.form_submit_button("创建账号", use_container_width=True)
                
                if submit_reg_button:
                    if not reg_username or not reg_email or not reg_password:
                        st.error("请填写所有必填信息")
                    elif reg_password != reg_password_confirm:
                        st.error("两次输入的密码不一致")
                    else:
                        with st.spinner("注册中..."):
                            if register(reg_username, reg_email, reg_password, reg_role):
                                st.success("注册成功! 请登录")
                            else:
                                st.error("注册失败，用户名或邮箱可能已被使用")
        
        # 关闭卡片容器
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 添加底部说明
        st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <p style="color:#757575; font-size:14px;">© 2025 AI实训报告生成系统 | 技术支持: CC</p>
        </div>
        """, unsafe_allow_html=True)
