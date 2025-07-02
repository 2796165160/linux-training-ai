#!/bin/bash
# 启动AI实训报告生成系统

# 项目根目录
PROJECT_ROOT=$(dirname "$(dirname "$(readlink -f "$0")")")
cd $PROJECT_ROOT

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

print_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

# 检查是否安装了必要的依赖
check_dependencies() {
    print_message "检查依赖..."
    
    # 检查Python版本
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]]; then
        print_message "Python版本: $python_version ✓"
    else
        print_error "需要Python 3.8或更高版本，当前版本: $python_version"
        exit 1
    fi

    # 安装依赖
    print_message "安装项目依赖..."
    pip install -r requirements.txt

    if [ $? -ne 0 ]; then
        print_error "依赖安装失败"
        exit 1
    fi
}
# 初始化数据库
initialize_database() {
    print_message "初始化数据库..."
    python3 scripts/init_db.py
    
    if [ $? -ne 0 ]; then
        print_error "数据库初始化失败"
        exit 1
    fi
}

# 启动后端服务
start_backend() {
    print_message "启动后端服务..."
    cd $PROJECT_ROOT
    
    # 使用nohup在后台运行
    nohup uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    BACKEND_PID=$!
    
    # 检查服务是否成功启动
    sleep 3
    if kill -0 $BACKEND_PID >/dev/null 2>&1; then
        print_message "后端服务运行中，PID: $BACKEND_PID"
    else
        print_error "后端服务启动失败"
        exit 1
    fi
    
    # 保存PID到文件
    echo $BACKEND_PID > backend.pid
}

# 启动前端服务
start_frontend() {
    print_message "启动前端服务..."
    cd $PROJECT_ROOT
    
    # 使用nohup在后台运行
    nohup streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 > frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    # 检查服务是否成功启动
    sleep 3
    if kill -0 $FRONTEND_PID >/dev/null 2>&1; then
        print_message "前端服务运行中，PID: $FRONTEND_PID"
    else
        print_error "前端服务启动失败"
        exit 1
    fi
    
    # 保存PID到文件
    echo $FRONTEND_PID > frontend.pid
}

# 显示访问信息
show_access_info() {
    # 获取服务器IP地址
    SERVER_IP=$(hostname -I | awk '{print $1}')
    
    print_message "==============================================="
    print_message "AI实训报告生成系统已成功启动!"
    print_message "后端API: http://$SERVER_IP:8000"
    print_message "前端界面: http://$SERVER_IP:8501"
    print_message "API文档: http://$SERVER_IP:8000/docs"
    print_message "==============================================="
    print_message "测试账户:"
    print_message "教师账号: admin / admin123"
    print_message "学生账号: student / student123"
    print_message "==============================================="
}

# 主函数
main() {
    print_message "启动AI实训报告生成系统..."
    
    # 执行初始化步骤
    check_dependencies
    initialize_database
    start_backend
    start_frontend
    show_access_info
}

# 执行主函数
main