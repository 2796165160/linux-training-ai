import streamlit as st
import requests
import pandas as pd
import time
import datetime
import random
import os

# API基础URL - 使用服务器实际IP地址
SERVER_IP = os.environ.get("SERVER_IP", "localhost") # 替换为您的服务器IP
API_BASE_URL = f"http://{SERVER_IP}:8000/api"

# 设置页面配置
st.set_page_config(
    page_title="AI实训报告生成系统",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "debug_mode" not in st.session_state:
    st.session_state.debug_mode = False

# API函数
def make_request(method, endpoint, data=None, params=None, files=None, auth=True):
    """通用API请求函数"""
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {}
    
    # 添加认证头
    if auth and "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if st.session_state.get("debug_mode", False):
            st.write(f"DEBUG - 请求: {method} {url}")
            st.write(f"DEBUG - 数据: {data}")
            st.write(f"DEBUG - 参数: {params}")
        
        if method == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=120)
        elif method == "POST":
            response = requests.post(url, json=data, params=params, files=files, headers=headers, timeout=120)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=120)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=120)
        else:
            st.error(f"不支持的请求方法: {method}")
            return None
        
        if st.session_state.get("debug_mode", False):
            st.write(f"DEBUG - 响应状态码: {response.status_code}")
            try:
                st.write(f"DEBUG - 响应内容: {response.json()}")
            except:
                st.write(f"DEBUG - 响应内容: {response.text}")
        
        # 处理认证失败
        if response.status_code == 401:
            st.error("登录已过期，请重新登录")
            st.session_state.token = None
            st.session_state.role = None
            st.session_state.current_page = "login"
            st.experimental_rerun()
            return None
        
        return response
        
    except requests.exceptions.ConnectionError as e:
        st.error(f"连接错误: 无法连接到 {url}")
        st.error(f"详细信息: {str(e)}")
        st.info(f"请确认后端服务正在运行，并且可以通过 {API_BASE_URL} 访问")
        return None
    except Exception as e:
        st.error(f"请求发生错误: {str(e)}")
        return None

def login(username, password):
    """用户登录"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            data={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.role = data["role"]
            return True
        else:
            return False
    except Exception as e:
        st.error(f"登录请求失败: {str(e)}")
        return False

def register(data):
    """用户注册"""
    
    response = make_request("POST", "auth/register", data=data, auth=False)
    return response and response.status_code == 200

def get_user_info():
    """获取当前用户信息"""
    response = make_request("GET", "users/me")
    if response and response.status_code == 200:
        return response.json()
    return None

def get_tasks(skip=0, limit=100):
    """获取任务列表"""
    response = make_request("GET", f"tasks?skip={skip}&limit={limit}")
    if response and response.status_code == 200:
        return response.json()
    return []

def create_task(title, description):
    """创建新任务"""
    data = {"title": title, "description": description}
    response = make_request("POST", "tasks", data=data)
    if response and response.status_code == 201:
        return response.json()
    return None

def get_templates(skip=0, limit=100):
    """获取模板列表"""
    response = make_request("GET", f"templates?skip={skip}&limit={limit}")
    if response and response.status_code == 200:
        return response.json()
    return []

def create_template(name, content):
    """创建新模板"""
    data = {"name": name, "content": content}
    response = make_request("POST", "templates", data=data)
    if response and response.status_code == 201:
        return response.json()
    return None

def generate_report(task_id, template_id=None):
    """生成报告"""
    data = {"task_id": task_id}
    if template_id:
        data["template_id"] = template_id
        
    response = make_request("POST", "reports/generate", data=data)
    if response and response.status_code == 200:
        return response.json()
    return None

def get_reports(skip=0, limit=100):
    """获取报告列表"""
    response = make_request("GET", f"reports?skip={skip}&limit={limit}")
    if response and response.status_code == 200:
        return response.json()
    return []

def update_report(report_id, content):
    """更新报告内容"""
    data = {"content": content}
    response = make_request("PUT", f"reports/{report_id}", data=data)
    if response and response.status_code == 200:
        return response.json()
    return None

# 页面组件函数
def show_sidebar(current_user_name, role, menu_options):
    """显示侧边栏"""
    with st.sidebar:
        # 添加Logo和标题
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h2 style="color:#1E88E5; margin:0;">📚 AI实训报告系统</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 用户信息卡片
        st.markdown(f"""
        <div style="background-color:#F3F4F6; border-radius:8px; padding:15px; margin-bottom:20px;">
            <p style="margin:0; font-size:16px; font-weight:500;">👤 {current_user_name}</p>
            <p style="margin:5px 0 0; color:#757575; font-size:14px;">{'👨‍🏫 教师' if role == 'teacher' else '👨‍🎓 学生'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-weight:500; color:#757575; font-size:14px; margin-bottom:5px;'>功能导航</p>", unsafe_allow_html=True)
        
        # 定义菜单选项及其标识符
        menu_options_display = ["🏠 主页", "📋 实训任务管理", "📊 实训报告管理", "📑 报告模板管理"]
        menu_identifiers = ["home", "tasks", "reports", "templates"]
        
        # 创建一个字典，将显示名称映射到标识符
        menu_dict = dict(zip(menu_options_display, menu_identifiers))
        
        # 从会话状态中获取预选菜单（如果有）
        index = 0
        if "menu_selection" in st.session_state:
            # 找到预选菜单的索引
            try:
                selected_id = st.session_state.menu_selection
                index = menu_identifiers.index(selected_id)
                # 使用后清除，避免在用户手动选择后仍然固定在预选项上
                del st.session_state.menu_selection
            except (ValueError, IndexError):
                index = 0
        
        # 菜单选择
        selected_display = st.radio(
            "导航菜单",
            options=menu_options_display,
            index=index,
            label_visibility="collapsed"
        )
        
        # 获取选中项的标识符
        selected = menu_dict.get(selected_display)
        
        st.divider()
        
        # 退出登录按钮
        if st.button("退出登录", use_container_width=True):
            st.session_state.token = None
            st.session_state.role = None
            st.session_state.current_page = "login"
            st.experimental_rerun()
        
        # 调试模式开关
        debug_col1, debug_col2 = st.columns([3,1])
        with debug_col1:
            st.markdown("<p style='margin-top:5px'>调试模式</p>", unsafe_allow_html=True)
        with debug_col2:
            debug_mode = st.checkbox(
                "调试模式开关", 
                value=st.session_state.get("debug_mode", False), 
                key="debug_toggle",
                label_visibility="collapsed"
            )
            if debug_mode != st.session_state.get("debug_mode", False):
                st.session_state.debug_mode = debug_mode
        
        # 底部信息
        st.write("---")
        st.write("© 2025 AI实训报告系统")
        
    return selected



def show_login_page():
    """登录页面"""
    st.title("AI实训报告生成系统")
    st.write("欢迎使用AI实训报告生成系统，请登录或注册以继续。")
    
    # 分为登录和注册两个标签页
    tab1, tab2 = st.tabs(["登录", "注册"])
    
    # 登录标签页
    with tab1:
        with st.form("login_form"):
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
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
    
    # 注册标签页
    with tab2:
        with st.form("register_form"):
            st.subheader("基本信息")
            reg_username = st.text_input("用户名*", key="reg_username", help="登录系统使用的用户名")
            reg_email = st.text_input("邮箱地址*", key="reg_email", help="用于接收通知和找回密码")
            reg_password = st.text_input("密码*", type="password", key="reg_password")
            reg_password_confirm = st.text_input("确认密码*", type="password", key="reg_password_confirm")
            reg_role = st.selectbox("角色*", ["student", "teacher"], format_func=lambda x: "学生" if x == "student" else "教师")
            
            st.divider()
            st.subheader("个人信息")
            reg_full_name = st.text_input("姓名", key="reg_full_name")
            reg_school = st.text_input("学校", key="reg_school")
            
            # 如果是学生，显示更多学生相关字段
            if reg_role == "student":
                col1, col2 = st.columns(2)
                with col1:
                    reg_college = st.text_input("学院", key="reg_college")
                    reg_class = st.text_input("班级", key="reg_class")
                with col2:
                    reg_major = st.text_input("专业", key="reg_major")
                    reg_student_id = st.text_input("学号", key="reg_student_id")
            else:
                reg_college = st.text_input("学院/部门", key="reg_college")
                reg_major = None
                reg_class = None
                reg_student_id = None
            
            st.markdown('<span style="color:#888; font-size:12px;">注册即表示您同意我们的服务条款和隐私政策</span>', unsafe_allow_html=True)
            
            submit_reg_button = st.form_submit_button("注册", use_container_width=True)
            
            if submit_reg_button:
                # 验证必填字段
                if not reg_username or not reg_email or not reg_password:
                    st.error("请填写所有必填信息（标有*的字段）")
                elif reg_password != reg_password_confirm:
                    st.error("两次输入的密码不一致")
                else:
                    # 构建注册数据
                    register_data = {
                        "username": reg_username,
                        "email": reg_email,
                        "password": reg_password,
                        "role": reg_role,
                        "full_name": reg_full_name,
                        "school": reg_school,
                        "college": reg_college,
                        "major": reg_major,
                        "class_name": reg_class,
                        "student_id": reg_student_id
                    }
                    
                    # 过滤掉None值
                    register_data = {k: v for k, v in register_data.items() if v is not None}
                    
                    with st.spinner("注册中..."):
                        if register(register_data):
                            st.success("注册成功! 请登录")
                        else:
                            st.error("注册失败，用户名或邮箱可能已被使用")


def show_home_page(user_info):
    """个性化主页"""
    st.markdown(f"<h1>欢迎，{user_info.get('full_name', user_info['username'])}！</h1>", unsafe_allow_html=True)
    
    # 显示个人信息卡片
    st.markdown("""
    <style>
    .user-info-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .info-item {
        margin-bottom: 10px;
    }
    .info-label {
        font-weight: bold;
        color: #555;
    }
    .welcome-message {
        font-size: 18px;
        color: #1976D2;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 创建信息卡片
    with st.container():
        st.markdown('<div class="user-info-card">', unsafe_allow_html=True)

        now = datetime.datetime.now()
        greeting = "早上好！" if 5 <= now.hour < 12 else "下午好！" if 12 <= now.hour < 18 else "晚上好！"
        today = now.strftime("%Y年%m月%d日")
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday_str = weekdays[now.weekday()]



        # 输出欢迎语 + 名言
        st.markdown(f"""
            <p style="font-size: 1.1em;line-height: 1.6;">
                <span style="font-weight: bold;">{greeting} 今天是 {today}（{weekday_str}）</span>
            </p>
        """, unsafe_allow_html=True)

        
        # 用户信息
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="info-item"><span class="info-label">用户名：</span>{}</div>'.format(user_info['username']), unsafe_allow_html=True)
            st.markdown('<div class="info-item"><span class="info-label">角色：</span>{}</div>'.format("学生" if user_info['role'] == "student" else "教师"), unsafe_allow_html=True)
            st.markdown('<div class="info-item"><span class="info-label">姓名：</span>{}</div>'.format(user_info.get('full_name', '未设置')), unsafe_allow_html=True)
        
        with col2:
            if user_info['role'] == "student":
                st.markdown('<div class="info-item"><span class="info-label">学校：</span>{}</div>'.format(user_info.get('school', '未设置')), unsafe_allow_html=True)
                st.markdown('<div class="info-item"><span class="info-label">专业：</span>{}</div>'.format(user_info.get('major', '未设置')), unsafe_allow_html=True)
                st.markdown('<div class="info-item"><span class="info-label">学号：</span>{}</div>'.format(user_info.get('student_id', '未设置')), unsafe_allow_html=True)
            else:
                st.markdown('<div class="info-item"><span class="info-label">学校：</span>{}</div>'.format(user_info.get('school', '未设置')), unsafe_allow_html=True)
                st.markdown('<div class="info-item"><span class="info-label">部门：</span>{}</div>'.format(user_info.get('college', '未设置')), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 系统概览部分
    st.markdown("## 系统概览")
    
    # 获取任务和报告数量
    tasks = get_tasks()
    reports = get_reports()
    templates = get_templates()
    
    task_count = len(tasks) if tasks else 0
    report_count = len(reports) if reports else 0
    template_count = len(templates) if templates else 0
    
    # 显示统计卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center; height: 150px;">
            <div style="font-size: 50px; color: #1976D2;">{}</div>
            <div style="font-size: 18px; color: #333;">实训任务</div>
        </div>
        """.format(task_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; text-align: center; height: 150px;">
            <div style="font-size: 50px; color: #43a047;">{}</div>
            <div style="font-size: 18px; color: #333;">实训报告</div>
        </div>
        """.format(report_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #fff3e0; padding: 20px; border-radius: 10px; text-align: center; height: 150px;">
            <div style="font-size: 50px; color: #f57c00;">{}</div>
            <div style="font-size: 18px; color: #333;">报告模板</div>
        </div>
        """.format(template_count), unsafe_allow_html=True)
    
    # 快速操作区
    st.markdown("## 快速操作")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("创建新实训任务", use_container_width=True):
            # 直接在这里进行跳转处理
            st.session_state.menu_selection = "tasks"  # 设置菜单选择
            st.experimental_rerun()  # 重新运行应用

    with col2:
        # 判断是否有任务可以生成报告
        disabled = task_count == 0
        button = st.button("生成实训报告", use_container_width=True, disabled=disabled)
        if button:
            # 直接在这里进行跳转处理
            st.session_state.menu_selection = "tasks"  # 设置菜单选择
            st.experimental_rerun()  # 重新运行应用
        if disabled:
            st.caption("请先创建实训任务")

    with col3:
        if st.button("管理报告模板", use_container_width=True):
            # 直接在这里进行跳转处理
            st.session_state.menu_selection = "templates"  # 设置菜单选择
            st.experimental_rerun()  # 重新运行应用

    # 显示最近的任务和报告
    st.markdown("## 最近活动")
    
    tab1, tab2 = st.tabs(["最近任务", "最近报告"])
    
    with tab1:
        if not tasks:
            st.info("暂无任务记录")
        else:
            # 显示最近的3个任务
            recent_tasks = sorted(tasks, key=lambda x: x.get("created_at", ""), reverse=True)[:3]
            for task in recent_tasks:
                created_at = task["created_at"]
                if "T" in created_at:
                    created_at = created_at.split("T")[0]
                    
                st.markdown(f"""
                <div style="border: 1px solid #e0e0e0; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
                    <div style="font-size: 16px; font-weight: bold;">{task["title"]}</div>
                    <div style="color: #757575; font-size: 12px; margin: 5px 0;">创建时间: {created_at}</div>
                    <div style="font-size: 14px; margin-top: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {task["description"][:100]}{"..." if len(task["description"]) > 100 else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        if not reports:
            st.info("暂无报告记录")
        else:
            # 显示最近的3个报告
            recent_reports = sorted(reports, key=lambda x: x.get("created_at", ""), reverse=True)[:3]
            for report in recent_reports:
                created_at = report["created_at"]
                if "T" in created_at:
                    created_at = created_at.split("T")[0]
                    
                st.markdown(f"""
                <div style="border: 1px solid #e0e0e0; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
                    <div style="font-size: 16px; font-weight: bold;">{report["title"]}</div>
                    <div style="color: #757575; font-size: 12px; margin: 5px 0;">创建时间: {created_at}</div>
                    <div style="text-align: right;">
                        <a href="http://{SERVER_IP}:8000/api/reports/{report["id"]}/export/html" target="_blank" style="text-decoration: none;">
                            <button style="background-color: #2196F3; color: white; border: none; border-radius: 4px; padding: 5px 10px; cursor: pointer;">
                                预览
                            </button>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)



def show_tasks_page():
    """任务管理页面"""
    st.header("实训任务管理")
    
    # 创建新任务
    with st.expander("创建新任务", expanded=False):
        with st.form("create_task_form"):
            task_title = st.text_input("任务标题")
            task_desc = st.text_area("任务描述", height=200)
            submit_task = st.form_submit_button("创建任务", use_container_width=True)
            
            if submit_task:
                if not task_title or not task_desc:
                    st.error("请填写任务标题和描述")
                else:
                    with st.spinner("创建中..."):
                        result = create_task(task_title, task_desc)
                        if result:
                            st.success("任务创建成功!")
                            st.experimental_rerun()
                        else:
                            st.error("任务创建失败")
    
    # 任务列表
    st.subheader("我的任务列表")
    
    with st.spinner("加载任务中..."):
        tasks = get_tasks()
    
    if not tasks:
        st.info("暂无任务，请先创建任务")
    else:
        # 创建任务数据表格
        task_data = []
        for task in tasks:
            # 处理日期格式
            created_at = task["created_at"]
            if "T" in created_at:
                created_at = created_at.split("T")[0]
                
            task_data.append({
                "ID": task["id"],
                "标题": task["title"],
                "创建时间": created_at
            })
        
        df = pd.DataFrame(task_data)
        st.dataframe(df, use_container_width=True)
        
        # 选择任务查看详情
        selected_task_id = st.selectbox("选择任务以查看详情", 
                                      options=[task["id"] for task in tasks],
                                      format_func=lambda id: next((t["title"] for t in tasks if t["id"] == id), ""))
        
        if selected_task_id:
            selected_task = next((t for t in tasks if t["id"] == selected_task_id), None)
            if selected_task:
                st.subheader(f"任务详情: {selected_task['title']}")
                created_at = selected_task['created_at']
                if "T" in created_at:
                    created_at = created_at.split("T")[0]
                st.write(f"**创建时间**: {created_at}")
                st.text_area("任务描述", selected_task["description"], height=200, disabled=True)
                
                # 生成报告
                st.divider()
                st.subheader("生成实训报告")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # 获取模板列表
                    templates = get_templates()
                    template_options = {0: "不使用模板"}
                    
                    if templates:
                        for template in templates:
                            template_options[template["id"]] = template["name"]
                    
                    selected_template = st.selectbox(
                        "选择报告模板",
                        options=list(template_options.keys()),
                        format_func=lambda x: template_options[x]
                    )
                
                with col2:
                    if st.button("生成报告", use_container_width=True):
                        with st.spinner("生成报告中，请稍候..."):
                            # 添加进度条显示
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.03)
                                progress_bar.progress(i + 1)
                                
                            template_id = selected_template if selected_template != 0 else None
                            result = generate_report(selected_task_id, template_id)
                            
                        if result:
                            st.success("报告生成成功!")
                            st.session_state.generated_report_id = result["id"]
                            st.session_state.current_page = "reports"
                            st.experimental_rerun()
                        else:
                            st.error("报告生成失败")

# def show_templates_page():
#     """模板管理页面"""
#     st.header("报告模板管理")
    
    
#     # 创建新模板
#     with st.expander("创建新模板", expanded=False):
#         with st.form("create_template_form"):
#             template_name = st.text_input("模板名称")
#             template_content = st.text_area("模板内容", height=300, 
#                                           placeholder="# 实训报告标题\n\n## 实训目标\n\n## 实训内容\n\n## 实验步骤\n\n## 实验结果\n\n## 心得体会")
#             submit_template = st.form_submit_button("创建模板", use_container_width=True)
            
#             if submit_template:
#                 if not template_name or not template_content:
#                     st.error("请填写模板名称和内容")
#                 else:
#                     with st.spinner("创建中..."):
#                         result = create_template(template_name, template_content)
#                         if result:
#                             st.success("模板创建成功!")
#                             st.experimental_rerun()
#                         else:
#                             st.error("模板创建失败")
    
#     # 模板列表
#     st.subheader("我的模板列表")
    
#     with st.spinner("加载模板中..."):
#         templates = get_templates()
    
#     if not templates:
#         st.info("暂无模板，请先创建模板")
#     else:
#         # 创建模板数据表格
#         template_data = []
#         for template in templates:
#             # 处理日期格式
#             created_at = template["created_at"]
#             if "T" in created_at:
#                 created_at = created_at.split("T")[0]
                
#             template_data.append({
#                 "ID": template["id"],
#                 "名称": template["name"],
#                 "创建时间": created_at
#             })
        
#         df = pd.DataFrame(template_data)
#         st.dataframe(df, use_container_width=True)
        
#         # 选择模板查看详情
#         selected_template_id = st.selectbox("选择模板以查看详情", 
#                                           options=[template["id"] for template in templates],
#                                           format_func=lambda id: next((t["name"] for t in templates if t["id"] == id), ""))
        
#         if selected_template_id:
#             selected_template = next((t for t in templates if t["id"] == selected_template_id), None)
#             if selected_template:
#                 st.subheader(f"模板详情: {selected_template['name']}")
#                 created_at = selected_template['created_at']
#                 if "T" in created_at:
#                     created_at = created_at.split("T")[0]
#                 st.write(f"**创建时间**: {created_at}")
                
#                 # 显示模板内容（带有预览）
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.text_area("模板内容", selected_template["content"], height=400, disabled=True)
                
#                 with col2:
#                     st.markdown("### 预览效果")
#                     st.markdown(selected_template["content"])

def parse_report_content(content):
    """解析报告内容，提取不同部分"""
    sections = {
        "全文": content,
        "标题": "",
        "实训目标": "",
        "实训内容": "",
        "实验步骤": "",
        "实验结果": "",
        "心得体会": ""
    }
    
    # 提取标题
    title_match = re.match(r'^# (.+?)$', content, re.MULTILINE)
    if title_match:
        sections["标题"] = title_match.group(1).strip()
    
    # 解析各部分内容
    parts = re.split(r'^## (.+?)$', content, flags=re.MULTILINE)
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                section_title = parts[i].strip()
                section_content = parts[i + 1].strip()
                
                # 根据标题确定对应的部分
                if "目标" in section_title:
                    sections["实训目标"] = section_content
                elif "内容" in section_title:
                    sections["实训内容"] = section_content
                elif "步骤" in section_title:
                    sections["实验步骤"] = section_content
                elif "结果" in section_title or "分析" in section_title:
                    sections["实验结果"] = section_content
                elif "心得" in section_title or "体会" in section_title:
                    sections["心得体会"] = section_content
    
    return sections


def show_templates_page():
    """模板管理页面"""
    st.header("报告模板管理")
    
    # 创建两个选项卡：创建文本模板和上传DOCX模板
    tab1, tab2 = st.tabs(["创建文本模板", "上传DOCX模板"])
    
    # 第一个选项卡：创建文本模板
    with tab1:
        with st.form("create_template_form"):
            template_name = st.text_input("模板名称")
            template_content = st.text_area("模板内容", height=300, 
                                          placeholder="# 实训报告标题\n\n## 实训目标\n\n## 实训内容\n\n## 实验步骤\n\n## 实验结果\n\n## 心得体会")
            submit_template = st.form_submit_button("创建模板", use_container_width=True)
            
            if submit_template:
                if not template_name or not template_content:
                    st.error("请填写模板名称和内容")
                else:
                    with st.spinner("创建中..."):
                        result = create_template(template_name, template_content)
                        if result:
                            st.success("模板创建成功!")
                            st.experimental_rerun()
                        else:
                            st.error("模板创建失败")
    
    # 第二个选项卡：上传DOCX模板
    with tab2:
        st.markdown("""
        ### DOCX模板上传
        
        您可以上传Word格式(.docx)的报告模板，系统将保存并允许生成报告时使用。
        
        **提示：**
        - 在DOCX模板中，您可以使用`{占位符}`格式添加动态内容
        - 例如：`{实训目标}`、`{实验步骤}`、`{实验结果}`等
        - 生成报告时，这些占位符将被对应内容替换
        """)
        
        # 上传表单
        with st.form("upload_docx_form"):
            docx_name = st.text_input("模板名称", placeholder="给模板起个名字")
            uploaded_file = st.file_uploader("选择DOCX文件", type=["docx"])
            
            col1, col2 = st.columns([1, 1])
            with col1:
                preview = st.checkbox("上传前预览", value=False)
            
            submit_upload = st.form_submit_button("上传DOCX模板", use_container_width=True)
            
            if submit_upload:
                if not docx_name:
                    st.error("请输入模板名称")
                elif not uploaded_file:
                    st.error("请选择DOCX文件")
                else:
                    # 显示上传信息
                    if preview:
                        st.info(f"文件名: {uploaded_file.name}")
                        st.info(f"文件大小: {uploaded_file.size} 字节")
                        st.info(f"文件类型: {uploaded_file.type}")
                    
                    with st.spinner("正在上传..."):
                        try:
                            # 准备表单数据和文件
                            files = {
                                "file": (uploaded_file.name, uploaded_file.getvalue(), 
                                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                            }
                            data = {"name": docx_name}
                            
                            # 发送上传请求
                            url = f"{API_BASE_URL}/templates/upload-docx"
                            headers = {"Authorization": f"Bearer {st.session_state.token}"}
                            
                            response = requests.post(
                                url=url,
                                files=files,
                                data=data,
                                headers=headers
                            )
                            
                            # 处理响应
                            if response.status_code == 200:
                                st.success("DOCX模板上传成功!")
                                result = response.json()
                                st.json(result)
                                time.sleep(1)
                                st.experimental_rerun()
                            else:
                                st.error(f"模板上传失败: {response.text}")
                                if st.session_state.get("debug_mode", False):
                                    st.write(f"状态码: {response.status_code}")
                                    st.write(f"响应内容: {response.text}")
                        except Exception as e:
                            st.error(f"上传过程出错: {str(e)}")
                            if st.session_state.get("debug_mode", False):
                                import traceback
                                st.code(traceback.format_exc())
    
    # 显示模板列表
    st.divider()
    st.subheader("我的模板列表")
    
    with st.spinner("加载模板中..."):
        templates = get_templates()
    
    if not templates:
        st.info("暂无模板，请先创建模板")
    else:
        # 创建模板数据表格
        template_data = []
        for template in templates:
            # 处理日期格式
            created_at = template["created_at"]
            if "T" in created_at:
                created_at = created_at.split("T")[0]
            
            # 添加模板类型标识
            template_type = "DOCX模板" if template.get("is_docx", False) else "文本模板"
                
            template_data.append({
                "ID": template["id"],
                "名称": template["name"],
                "类型": template_type,
                "创建时间": created_at
            })
        
        df = pd.DataFrame(template_data)
        st.dataframe(df, use_container_width=True)
        
        # 选择模板查看详情
        selected_template_id = st.selectbox("选择模板以查看详情", 
                                          options=[template["id"] for template in templates],
                                          format_func=lambda id: next((f"{t['name']} ({t['id']})" for t in templates if t["id"] == id), ""))
        
        if selected_template_id:
            selected_template = next((t for t in templates if t["id"] == selected_template_id), None)
            if selected_template:
                st.markdown(f"""
                <div style="background-color:#f0f0f0; padding:15px; border-radius:5px;">
                    <h3>{selected_template['name']}</h3>
                    <p><strong>ID:</strong> {selected_template['id']}</p>
                    <p><strong>类型:</strong> {"DOCX模板" if selected_template.get('is_docx', False) else "文本模板"}</p>
                    <p><strong>创建时间:</strong> {selected_template['created_at'].split('T')[0] if 'T' in selected_template['created_at'] else selected_template['created_at']}</p>
                    {f'<p><strong>原始文件名:</strong> {selected_template.get("original_filename", "")}</p>' if selected_template.get("is_docx", False) else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # 根据模板类型显示不同内容
                if selected_template.get("is_docx", False):
                    st.info("此模板为DOCX格式，可在报告生成时套用")
                    if st.button("删除此模板", key=f"delete_{selected_template_id}"):
                        if st.session_state.get("confirm_delete", False):
                            # 调用删除API
                            response = make_request("DELETE", f"templates/{selected_template_id}")
                            if response and response.status_code == 204:
                                st.success("模板已删除")
                                time.sleep(1)
                                st.session_state.pop("confirm_delete", None)
                                st.experimental_rerun()
                            else:
                                st.error("删除模板失败")
                            st.session_state.pop("confirm_delete", None)
                        else:
                            st.session_state.confirm_delete = True
                            st.warning("再次点击以确认删除此模板，此操作不可撤销")
                else:
                    # 文本模板显示内容和预览
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### 模板内容")
                        st.text_area("", value=selected_template["content"], height=400, disabled=True, 
                                   key=f"content_{selected_template_id}")
                    
                    with col2:
                        st.markdown("#### 预览效果")
                        st.markdown(selected_template["content"])                    
                    
def show_reports_page():
    """报告管理页面"""
    st.header("实训报告管理")
    
    # 加载报告列表
    with st.spinner("加载报告中..."):
        reports = get_reports()
    
    if not reports:
        st.info("暂无报告，请先生成报告")
    else:
        # 处理新生成的报告高亮
        if "generated_report_id" in st.session_state:
            st.success(f"报告 #{st.session_state.generated_report_id} 已成功生成!")
            # 清除会话状态中的报告ID
            del st.session_state.generated_report_id
        
        # 创建报告数据表格
        report_data = []
        for report in reports:
            # 处理日期格式
            created_at = report["created_at"]
            if "T" in created_at:
                created_at = created_at.split("T")[0]
                
            report_data.append({
                "ID": report["id"],
                "标题": report["title"],
                "创建时间": created_at
            })
        
        df = pd.DataFrame(report_data)
        st.dataframe(df, use_container_width=True)
        
        # 选择报告查看详情
        selected_report_id = st.selectbox("选择报告以查看/编辑", 
                                        options=[report["id"] for report in reports],
                                        format_func=lambda id: next((r["title"] for r in reports if r["id"] == id), ""))
        
        if selected_report_id:
            selected_report = next((r for r in reports if r["id"] == selected_report_id), None)
            if selected_report:
                st.subheader(f"报告详情: {selected_report['title']}")
                created_at = selected_report['created_at']
                if "T" in created_at:
                    created_at = created_at.split("T")[0]
                st.write(f"**创建时间**: {created_at}")
                
                # 编辑区域
                report_content = st.text_area(
                    "报告内容 (可编辑)",
                    value=selected_report["content"],
                    height=500,
                    key=f"report_content_{selected_report_id}"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("保存修改", use_container_width=True):
                        with st.spinner("保存中..."):
                            if update_report(selected_report_id, report_content):
                                st.success("报告已更新")
                                time.sleep(1)
                                st.experimental_rerun()
                            else:
                                st.error("更新失败")
                
                # 导出选项
                st.divider()
                st.subheader("导出报告")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    export_docx_url = f"http://{SERVER_IP}:8000/api/reports/{selected_report_id}/export/docx"
                    st.markdown(f"""
                    <a href="{export_docx_url}" target="_blank">
                        <button style="
                            background-color: #4CAF50;
                            border: none;
                            color: white;
                            padding: 10px 24px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 8px;
                            width: 100%;">
                            导出为Word文档
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                
                with col2:
                    export_pdf_url = f"http://{SERVER_IP}:8000/api/reports/{selected_report_id}/export/pdf"
                    st.markdown(f"""
                    <a href="{export_pdf_url}" target="_blank">
                        <button style="
                            background-color: #f44336;
                            border: none;
                            color: white;
                            padding: 10px 24px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 8px;
                            width: 100%;">
                            导出为PDF文档
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                
                with col3:
                    export_html_url = f"http://{SERVER_IP}:8000/api/reports/{selected_report_id}/export/html"
                    st.markdown(f"""
                    <a href="{export_html_url}" target="_blank">
                        <button style="
                            background-color: #673AB7;
                            border: none;
                            color: white;
                            padding: 10px 24px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 8px;
                            width: 100%;">
                            HTML预览(可打印)
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                
                # 添加文本下载选项
                with st.expander("其他导出选项"):
                    if st.button("下载为文本文件", use_container_width=True):
                        st.download_button(
                            "点击下载TXT文件",
                            data=report_content,
                            file_name=f"{selected_report['title']}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                
                # 预览区域
                st.divider()
                st.subheader("报告预览")
                st.markdown(report_content)

def main():
    """主应用函数"""
    
    # 如果未登录，显示登录页面
    if not st.session_state.token:
        show_login_page()
    else:
        # 获取当前用户信息
        user_info = get_user_info()
        if not user_info:
            st.error("获取用户信息失败，请重新登录")
            st.session_state.token = None
            st.session_state.role = None
            st.session_state.current_page = "login"
            st.experimental_rerun()
            return
        
        # 侧边栏菜单
        menu_options = ["🏠 主页", "📋 实训任务管理", "📊 实训报告管理", "📑 报告模板管理"]
        selected_menu = show_sidebar(
            current_user_name=user_info.get("full_name", user_info["username"]),
            role=user_info["role"],
            menu_options=menu_options
        )
        
        # 根据选择显示对应页面
        if selected_menu == "home":
            show_home_page(user_info)
        elif selected_menu == "tasks":
            show_tasks_page()
        elif selected_menu == "reports":
            show_reports_page()
        elif selected_menu == "templates":
            show_templates_page()

# 应用入口
if __name__ == "__main__":
    main()

