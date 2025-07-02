import requests
import streamlit as st
import json
from typing import Any, Dict, List, Optional, Union

# API基础URL
API_BASE_URL = "http://localhost:8000/api"

def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
    auth: bool = True,
) -> Optional[requests.Response]:
    """
    通用API请求函数
    
    Args:
        method: 请求方法 (GET, POST, PUT, DELETE)
        endpoint: API端点
        data: 请求数据
        params: URL参数
        files: 文件数据
        auth: 是否需要认证
        
    Returns:
        Response对象或None（如果请求失败）
    """
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {}
    
    # 添加认证头
    if auth and "token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if st.session_state.get("debug_mode", False):
            st.write(f"DEBUG - 请求: {method} {url}")
            st.write(f"DEBUG - 数据: {data}")
            st.write(f"DEBUG - 参数: {params}")
        
        if method == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, params=params, files=files, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
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
        
    except Exception as e:
        st.error(f"请求发生错误: {str(e)}")
        return None

def login(username: str, password: str) -> bool:
    """
    用户登录
    
    Args:
        username: 用户名
        password: 密码
        
    Returns:
        是否登录成功
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            data={"username": username, "password": password},
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

def register(username: str, email: str, password: str, role: str) -> bool:
    """
    用户注册
    
    Args:
        username: 用户名
        email: 邮箱
        password: 密码
        role: 角色
        
    Returns:
        是否注册成功
    """
    data = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }
    
    response = make_request("POST", "auth/register", data=data, auth=False)
    return response and response.status_code == 200

def get_user_info() -> Optional[Dict[str, Any]]:
    """获取当前用户信息"""
    response = make_request("GET", "users/me")
    if response and response.status_code == 200:
        return response.json()
    return None

def get_tasks(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """获取任务列表"""
    response = make_request("GET", f"tasks?skip={skip}&limit={limit}")
    if response and response.status_code == 200:
        return response.json()
    return []

def create_task(title: str, description: str) -> Optional[Dict[str, Any]]:
    """创建新任务"""
    data = {"title": title, "description": description}
    response = make_request("POST", "tasks", data=data)
    if response and response.status_code == 201:
        return response.json()
    return None

def get_templates(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """获取模板列表"""
    response = make_request("GET", f"templates?skip={skip}&limit={limit}")
    if response and response.status_code == 200:
        return response.json()
    return []

def create_template(name: str, content: str) -> Optional[Dict[str, Any]]:
    """创建新模板"""
    data = {"name": name, "content": content}
    response = make_request("POST", "templates", data=data)
    if response and response.status_code == 201:
        return response.json()
    return None

def generate_report(task_id: int, template_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """生成报告"""
    data = {"task_id": task_id}
    if template_id:
        data["template_id"] = template_id
        
    response = make_request("POST", "reports/generate", data=data)
    if response and response.status_code == 200:
        return response.json()
    return None

def get_reports(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """获取报告列表"""
    response = make_request("GET", f"reports?skip={skip}&limit={limit}")
    if response and response.status_code == 200:
        return response.json()
    return []

def update_report(report_id: int, content: str) -> Optional[Dict[str, Any]]:
    """更新报告内容"""
    data = {"content": content}
    response = make_request("PUT", f"reports/{report_id}", data=data)
    if response and response.status_code == 200:
        return response.json()
    return None

