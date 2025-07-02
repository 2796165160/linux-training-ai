import streamlit as st
import pandas as pd
from frontend.utils.api import get_tasks, create_task, generate_report, get_templates
from typing import Dict, Any

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
            task_data.append({
                "ID": task["id"],
                "标题": task["title"],
                "创建时间": task["created_at"].split("T")[0]
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
                st.write(f"**创建时间**: {selected_task['created_at'].split('T')[0]}")
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
                            template_id = selected_template if selected_template != 0 else None
                            result = generate_report(selected_task_id, template_id)
                            
                            if result:
                                st.success("报告生成成功!")
                                st.session_state.generated_report_id = result["id"]
                                st.session_state.current_page = "reports"
                                st.experimental_rerun()
                            else:
                                st.error("报告生成失败")
