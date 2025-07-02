# 自动化实训报告生成系统

> 基于 FastAPI + RAG + 本地大模型，结合多Agent协作机制，为职业教育信息技术类学生自动生成标准化实训报告的智能服务平台。

---

## 项目简介

本项目旨在利用最新的人工智能技术，结合职业教育领域的实际需求，开发一个自动化实训报告生成系统。系统集成了基于 Retrieval-Augmented Generation（RAG）的知识检索机制、本地部署的大语言模型（LLaMA等），以及多Agent协作推理，能够根据学生提交的实验数据和实训内容，自动生成符合规范的实训报告文档，极大提升学生的学习效率和教师的教学管理便利性。

---

## 功能特点

- **自动化实训报告生成**  
  根据输入的实验手册、实训任务书和实验数据，自动生成结构化、标准化的实训报告。

- **基于RAG的知识增强**  
  利用本地知识库进行精准语义检索，确保生成内容的专业性和准确性。

- **本地大模型推理**  
  部署LLaMA、Qwen等开源大模型，支持离线推理，保障数据安全与隐私。

- **多Agent协作机制**  
  多智能体协同工作，提升报告生成的逻辑完整性与内容丰富度。

- **API服务接口**  
  基于FastAPI提供高性能、易扩展的RESTful接口，便于集成和二次开发。

---

## 技术栈

- **后端框架**: FastAPI  
- **大语言模型**: LLaMA3、Qwen、Ollama等本地部署模型  
- **知识库与检索**: pgvector + PostgreSQL 向量数据库  
- **多Agent框架**: 自定义协作调度机制  
- **前端**: （如有，填写）  
- **容器化部署**: Docker  

---

## 快速开始

### 1. 环境准备

- Python 3.10+
- PostgreSQL 数据库
- Docker（可选）

### 2. 克隆仓库

```bash
git clone https://github.com/2796165160/linux-training-ai.git
cd linux-training-ai
```

### 3. 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 4. 配置数据库

请根据实际情况修改数据库连接配置，确保PostgreSQL正常运行。

### 5. 启动服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API示例

- 生成实训报告

请求：

```bash
POST /generate_report
Content-Type: application/json

{
  "experiment_data": "...",
  "task_description": "..."
}
```

响应：

```json
{
  "report": "自动生成的实训报告文本内容..."
}
```
---

### 项目结构

```bash

├── backend/                # 后端 FastAPI 服务代码
│   ├── main.py             # FastAPI 应用入口
│   ├── rag_service.py      # RAG检索模块
│   ├── agent_manager.py    # 多Agent协作管理
│   └── model_inference.py  # 大模型推理接口
├── knowledge_base/         # 知识库构建与管理
├── frontend/               # （如有）前端代码
├── docs/                   # 项目文档
├── requirements.txt        # Python依赖
└── README.md               # 项目说明
```
### 未来规划

- 集成更多大语言模型

- 优化多Agent协作机制

- 支持实训报告导出 Word / PDF

- 拓展更多职业教育专业场景

### 贡献

欢迎提交 issue 和 pull request，一起完善项目！

### 许可证

本项目采用 MIT 许可证，详情请见 LICENSE 文件。

### 联系方式

维护人：cc

邮箱：2796165160@qq.com

GitHub: https://github.com/2796165160/

---

需要我帮你生成更详细的文档或者示例代码也可以，随时告诉我！
