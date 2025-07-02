import sys
import os
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import Base, engine, check_db_connection
from backend.app.models.user import User
from backend.app.models.task import Task
from backend.app.models.report import Report
from backend.app.models.template import Template
from backend.app.utils.security import get_password_hash
from sqlalchemy.orm import Session, sessionmaker

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def init_db():
    """初始化数据库"""
    logger.info("开始初始化数据库...")
    
    # 检查数据库连接
    if not check_db_connection():
        logger.error("数据库连接失败")
        return False
    
    try:
        # 创建数据库表
        logger.info("创建数据库表...")
        Base.metadata.create_all(bind=engine)
        
        # 创建会话
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 检查是否需要创建初始用户
        if db.query(User).count() == 0:
            logger.info("创建初始管理员用户...")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                role="teacher"
            )
            db.add(admin_user)
            
            # 添加示例学生用户
            student_user = User(
                username="student",
                email="student@example.com",
                hashed_password=get_password_hash("student123"),
                role="student"
            )
            db.add(student_user)
            
            db.commit()
            logger.info("初始用户创建成功")
            
            # 为示例用户创建示例模板
            logger.info("创建示例模板...")
            example_template = Template(
                name="标准实训报告模板",
                content="""# 实训报告

## 1. 实训目标
[在这里描述本次实训的目标和要求]

## 2. 实训内容
[简要介绍本次实训的主要内容和意义]

## 3. 实验环境
- 硬件环境：[描述使用的计算机硬件配置]
- 软件环境：[描述使用的操作系统、软件版本等]

## 4. 实验步骤
### 4.1 [步骤1标题]
[详细描述步骤1的操作过程]

### 4.2 [步骤2标题]
[详细描述步骤2的操作过程]

## 5. 实验结果
[描述实验结果，可以包含截图、数据表格等]

## 6. 问题与解决方案
[描述实验中遇到的问题以及解决方法]

## 7. 心得体会
[分享通过本次实训所学到的知识和技能，以及对实训内容的理解和感悟]

## 8. 参考资料
1. [列出参考的文档、书籍或网站]
2. [参考资料2]
""",
                user_id=student_user.id
            )
            db.add(example_template)
            
            # 创建示例任务
            logger.info("创建示例任务...")
            example_task = Task(
                title="Web应用开发实训",
                description="""本次实训要求使用Flask框架开发一个简单的博客系统，实现以下功能：
1. 用户注册与登录
2. 文章的发布、编辑和删除
3. 评论功能
4. 文章分类和标签
5. 简单的用户权限管理

技术要求：
- 使用Python 3.8+和Flask 2.0+
- 数据库使用SQLite或MySQL
- 前端使用Bootstrap框架
- 代码需添加适当注释
- 提交完整源代码和部署文档
                """,
                user_id=student_user.id
            )
            db.add(example_task)
            db.commit()
            
            logger.info("示例数据创建成功!")
        else:
            logger.info("数据库已包含用户数据，跳过初始化")
        
        logger.info("数据库初始化完成")
        return True
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
