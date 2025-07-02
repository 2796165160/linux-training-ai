import requests

def test_endpoints(base_url):
    # 测试路径列表
    paths = [
        "/",  # 根路径
        "/docs",  # API文档
        "/api",  # API前缀
        "/api/auth/login",  # 登录端点
        "/api/auth/register",  # 注册端点
    ]
    
    print(f"测试基础URL: {base_url}")
    print("-" * 50)
    
    for path in paths:
        url = f"{base_url}{path}"
        try:
            response = requests.get(url, timeout=5)
            print(f"路径: {path} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"路径: {path} - 错误: {str(e)}")
    
    print("-" * 50)

if __name__ == "__main__":
    test_endpoints("http://localhost:8000")
