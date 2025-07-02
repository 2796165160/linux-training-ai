import streamlit as st
import pandas as pd
from frontend.utils.api import get_reports, update_report
import time


# API基础URL - 使用服务器实际IP地址
SERVER_IP = "8.130.92.212"  # 替换为您的服务器IP
API_BASE_URL = f"http://{SERVER_IP}:8000/api"


def show_reports_page():
    """报告管理页面"""
    st.header("实训报告管理")
    
    # 加载报告列表
    with st.spinner("加载报告中..."):
        reports = get_reports()
    
    if not reports:
        st.info("暂无报告，请先生成报告")
    else:
        # 创建报告数据表格
        report_data = []
        for report in reports:
            report_data.append({
                "ID": report["id"],
                "标题": report["title"],
                "创建时间": report["created_at"].split("T")[0] if "T" in report["created_at"] else report["created_at"]
            })
        
        df = pd.DataFrame(report_data)
        
        # 处理新生成的报告高亮
        if "generated_report_id" in st.session_state:
            st.success(f"报告 #{st.session_state.generated_report_id} 已成功生成!")
            # 清除会话状态中的报告ID
            del st.session_state.generated_report_id
        
        st.dataframe(df, use_container_width=True)
        
        # 选择报告查看详情
        selected_report_id = st.selectbox("选择报告以查看/编辑", 
                                        options=[report["id"] for report in reports],
                                        format_func=lambda id: next((r["title"] for r in reports if r["id"] == id), ""))
        
        if selected_report_id:
            selected_report = next((r for r in reports if r["id"] == selected_report_id), None)
            if selected_report:
                st.subheader(f"报告详情: {selected_report['title']}")
                created_at = selected_report['created_at'].split('T')[0] if 'T' in selected_report['created_at'] else selected_report['created_at']
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
                
                # 使用服务器IP替换localhost
                server_ip = SERVER_IP  # 使用全局变量SERVER_IP
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <a href="http://{server_ip}:8000/api/reports/{selected_report_id}/export/docx" target="_blank">
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
                    st.markdown(f"""
                    <a href="http://{server_ip}:8000/api/reports/{selected_report_id}/export/pdf" target="_blank">
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
                            HTML预览(可打印为PDF)
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                
                # 添加直接下载功能作为备选
                with st.expander("文本下载选项"):
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

