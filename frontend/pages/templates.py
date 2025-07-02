import streamlit as st
import pandas as pd
from frontend.utils.api import get_templates, create_template

def show_templates_page():
    """模板管理页面"""
    st.header("报告模板管理")
    
    # 创建新模板
    with st.expander("创建新模板", expanded=False):
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
    
    # 模板列表
    st.subheader("我的模板列表")
    
    with st.spinner("加载模板中..."):
        templates = get_templates()
    
    if not templates:
        st.info("暂无模板，请先创建模板")
    else:
        # 创建模板数据表格
        template_data = []
        for template in templates:
            template_data.append({
                "ID": template["id"],
                "名称": template["name"],
                "创建时间": template["created_at"].split("T")[0]
            })
        
        df = pd.DataFrame(template_data)
        st.dataframe(df, use_container_width=True)
        
        # 选择模板查看详情
        selected_template_id = st.selectbox("选择模板以查看详情", 
                                          options=[template["id"] for template in templates],
                                          format_func=lambda id: next((t["name"] for t in templates if t["id"] == id), ""))
        
        if selected_template_id:
            selected_template = next((t for t in templates if t["id"] == selected_template_id), None)
            if selected_template:
                st.subheader(f"模板详情: {selected_template['name']}")
                st.write(f"**创建时间**: {selected_template['created_at'].split('T')[0]}")
                
                # 显示模板内容（带有预览）
                col1, col2 = st.columns(2)
                
                with col1:
                    st.text_area("模板内容", selected_template["content"], height=400, disabled=True)
                
                with col2:
                    st.markdown("### 预览效果")
                    st.markdown(selected_template["content"])

