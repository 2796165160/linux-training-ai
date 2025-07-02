# scripts/migrate_templates.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import Column, String, LargeBinary
from backend.app.database import engine, SessionLocal
import sqlalchemy as sa
from alembic import op

def migrate_templates_table():
    """为模板表添加DOCX存储相关字段"""
    try:
        # 添加新列
        op.add_column('templates', sa.Column('original_filename', sa.String(255), nullable=True))
        op.add_column('templates', sa.Column('docx_content', sa.LargeBinary(), nullable=True))
        
        print("模板表迁移成功，添加了新字段")
        
    except Exception as e:
        print(f"迁移失败: {str(e)}")
        
if __name__ == "__main__":
    migrate_templates_table()
