import httpx
import logging
from typing import Optional
from sqlalchemy.orm import Session

from ..config import settings
from ..models.task import Task
from ..models.template import Template
from ..models.report import Report
from ..models.user import User

logger = logging.getLogger(__name__)

async def generate_report_with_qwen(
    db: Session, task_id: int, user_id: int, template_id: Optional[int] = None
) -> Optional[Report]:
    """使用通义千问API生成报告"""
    # 获取任务
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.error(f"无法找到任务ID: {task_id}")
        return None
    
    # 获取模板（如果提供）
    template = None
    if template_id:
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            logger.warning(f"无法找到模板ID: {template_id}")
    
    # 构建提示词
    prompt = f"""
    你是一位专业的实训报告撰写专家，具备跨学科的写作能力，能够根据实训任务信息生成符合高等职业教育或应用型本科教学要求的标准化实训报告。

    请根据以下实验任务信息，撰写一份完整、逻辑清晰、语言书面化、结构规范的实训报告。

    【实训项目名称】
    {task.title}

    【实训任务描述】
    {task.description}

    {"【撰写模板】" + template.content if template else ""}

    请严格按照以下五个部分进行撰写，每个部分不少于规定的字数，内容应具体真实、有条理，语言规范：

    ---

    一、实训目标（不少于 150 字）
    - 明确本次实训的教学目标和专业能力目标；  
    - 描述学生通过实训应掌握的知识点、操作技能或综合素养（如设备使用、流程掌握、职业习惯等）；  
    - 强调与课程标准、职业岗位能力之间的关系。

    二、实训内容（不少于 300 字）
    - 总结实训所涉及的主要知识模块、技术工具、实验材料或场景设置；  
    - 可以包括：仪器设备、软件平台、工作流程、标准规范等；  
    - 适当补充理论支撑内容，使报告更系统。

    三、实验/实训步骤（不少于 500 字，若适用请加入关键操作或技术过程描述）
    - 按照实际操作过程，分步骤描述实验/实训的详细过程；  
    - 包括前期准备、操作流程、关键参数设定、注意事项等；  
    - 如涉及仪器设置、软件使用、绘图建模、数据采集、护理流程等，需说明关键点或配图/代码段：

    四、结果记录与分析（不少于 200 字）
    - 准确描述实训中产生的关键结果、测量数据、图纸、作品、成品、护理记录等；
    - 分析结果是否达标、存在的问题或改进空间；
    - 若出现问题，需结合原理或规范进行原因分析。

    五、个人心得与体会（不少于 200 字）

    - 总结本次实训对知识、技能、职业素养等方面的提升；
    - 可谈学习过程中的困难、反思与收获；
    - 也可对课程内容、教学组织或实训条件提出建议，体现批判性和专业成长。
"""
        
    try:
        # 调用通义千问API
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                settings.QWEN_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.QWEN_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "qwen-max-latest",
                    "input": {"prompt": prompt},
                    "parameters": {
                        "max_tokens": 4000,
                        "temperature": 0.7,
                        "top_p": 0.8
                    }
                }
            )
            
            if response.status_code != 200:
                logger.error(f"通义千问API错误: {response.text}")
                return None
            
            # 解析响应
            result = response.json()
            report_content = result.get("output", {}).get("text", "")
            if not report_content:
                logger.error("通义千问返回内容为空")
                return None
            
            # 创建报告
            report_title = f"{task.title} - 实训报告"
            new_report = Report(
                title=report_title,
                content=report_content,
                task_id=task_id,
                user_id=user_id,
                template_id=template_id
            )
            
            db.add(new_report)
            db.commit()
            db.refresh(new_report)
            
            logger.info(f"成功生成报告ID: {new_report.id}")
            return new_report
            
    except Exception as e:
        logger.error(f"生成报告时发生错误: {str(e)}")
        return None
