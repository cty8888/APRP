import os
import sys
def clear_database():
    print("🗑️  开始清理数据库...")
    # 确保在backend目录下操作
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    # 1. 删除数据库文件
    db_file = "aprp.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"✅ 已删除数据库文件: {db_file}")
        except Exception as e:
            print(f"❌ 删除数据库文件失败: {e}")
            return False
    else:
        print(f"⚠️  数据库文件不存在: {db_file}")
    # 2. 重新创建空数据库
    try:
        print("🔧 创建新数据库...")
        
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        # 导入数据库相关模块
        from app.db.database import Base, engine
        # 导入所有模型
        from app.models.user import User
        from app.models.class_model import Class
        from app.models.assignment import Assignment
        from app.models.submission import Submission
        from app.models.student_class import StudentClass
        from app.models.teacher_class import TeacherClass
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 新数据库创建完成！")
        print("📋 已创建的表:")
        for table_name in Base.metadata.tables.keys():
            print(f"   • {table_name}")
        return True
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False

if __name__ == "__main__":
    if clear_database():
        pass
    else:
        print("\n❌ 数据库清理失败！")
        sys.exit(1)
