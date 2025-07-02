import streamlit as st
import requests

SERVER_IP = "8.130.92.212"
API_URL = f"http://{SERVER_IP}:8000"

st.title("API连接测试")

st.write(f"尝试连接: {API_URL}")

try:
    response = requests.get(f"{API_URL}/health", timeout=5)
    st.write(f"状态码: {response.status_code}")
    st.write(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        st.success("API连接成功!")
    else:
        st.error("API返回非200状态码")
except Exception as e:
    st.error(f"连接错误: {str(e)}")

st.write("---")
st.subheader("尝试访问文档")

docs_url = f"{API_URL}/docs"
st.write(f"文档URL: {docs_url}")

# 创建一个iframe尝试嵌入文档页面
st.markdown(f"""
<iframe src="{docs_url}" width="100%" height="500px"></iframe>
""", unsafe_allow_html=True)

# 添加直接链接
st.markdown(f"[直接访问文档]({docs_url})")

st.write("---")
st.subheader("PDF导出测试")

report_id = st.number_input("报告ID", min_value=1, value=2)
pdf_url = f"{API_URL}/api/reports/{report_id}/export/pdf"
word_url = f"{API_URL}/api/reports/{report_id}/export/docx"

st.write(f"PDF URL: {pdf_url}")
st.markdown(f"[下载PDF]({pdf_url})")

st.write(f"Word URL: {word_url}")
st.markdown(f"[下载Word]({word_url})")
