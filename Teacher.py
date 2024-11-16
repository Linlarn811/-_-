import datetime
import pyodbc
from connect_database import connect_to_database
#创建教师
def create_teacher(cursor):
    try:
        teacher_name = input("请输入教师姓名: ").strip()

        # 设置创建和更新时间为当前时间
        created_at = updated_at = datetime.datetime.now()

        query = "INSERT INTO Teacher (teacher_name, created_at, updated_at) VALUES (?, ?, ?)"
        cursor.execute(query, (teacher_name, created_at, updated_at))
        cursor.connection.commit()

        print("教师创建成功。")
    except pyodbc.Error as e:
        print(f"教师创建失败：{e}")
#批量创建教师
def bulk_create_teachers_from_file(cursor):
    try:
        # 用户手动输入文件路径
        file_path = input("请输入教师数据文件的路径: ").strip()

        # 从文件中读取教师数据
        with open(file_path, "r", encoding="utf-8") as file:
            teachers = [line.strip() for line in file if line.strip()]

        if not teachers:
            print("文件中没有有效的教师数据。")
            return

        # 准备插入数据库
        query = "INSERT INTO Teacher (teacher_name, created_at, updated_at) VALUES (?, ?, ?)"
        created_at = updated_at = datetime.datetime.now()
        teacher_count = 0

        for teacher_name in teachers:
            try:
                cursor.execute(query, (teacher_name, created_at, updated_at))
                teacher_count += 1
            except pyodbc.Error as e:
                print(f"教师 '{teacher_name}' 创建失败：{e}")

        # 提交事务
        cursor.connection.commit()
        print(f"成功从文件 '{file_path}' 中批量创建了 {teacher_count} 位教师。")

    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到，请检查路径是否正确。")
    except pyodbc.Error as e:
        print(f"批量创建教师失败：{e}")
#更新教师姓名
def update_teacher_name(cursor):
    try:
        # 输入教师ID
        teacher_id = input("请输入要修改的教师ID: ").strip()
        if not teacher_id.isdigit():
            print("教师ID必须是数字，请重新输入。")
            return

        # 输入新的教师姓名
        new_name = input("请输入新的教师姓名: ").strip()
        if not new_name:
            print("教师姓名不能为空，请重新输入。")
            return

        # 更新操作
        query = "UPDATE Teacher SET teacher_name = ?, updated_at = ? WHERE teacher_id = ?"
        updated_at = datetime.datetime.now()
        cursor.execute(query, (new_name, updated_at, int(teacher_id)))
        cursor.connection.commit()

        # 检查影响的行数
        if cursor.rowcount > 0:
            print(f"教师ID为 {teacher_id} 的姓名已更新为 '{new_name}'。")
        else:
            print(f"未找到教师ID为 {teacher_id} 的记录。")

    except pyodbc.Error as e:
        print(f"更新教师姓名失败：{e}")




#查询教师
def view_teachers(cursor):
    try:
        choice = input("请选择查询类型：1. 查询所有教师 2. 按教师ID查询教师 3. 按教师姓名查询教师: ").strip()

        if choice == "1":
            # 查询所有教师
            query = "SELECT teacher_id, teacher_name, created_at, updated_at FROM Teacher"
            cursor.execute(query)
            teachers = cursor.fetchall()
            if teachers:
                for teacher in teachers:
                    print(
                        f"教师ID: {teacher.teacher_id}, 姓名: {teacher.teacher_name}, 创建时间: {teacher.created_at}, 更新时间: {teacher.updated_at}")
            else:
                print("未找到教师数据。")

        elif choice == "2":
            # 按教师ID查询教师
            teacher_id = int(input("请输入教师ID: ").strip())
            query = "SELECT teacher_id, teacher_name, created_at, updated_at FROM Teacher WHERE teacher_id = ?"
            cursor.execute(query, (teacher_id,))
            teacher = cursor.fetchone()
            if teacher:
                print(
                    f"教师ID: {teacher.teacher_id}, 姓名: {teacher.teacher_name}, 创建时间: {teacher.created_at}, 更新时间: {teacher.updated_at}")
            else:
                print("未找到指定的教师。")

        elif choice == "3":
            # 按教师姓名查询教师
            teacher_name = input("请输入教师姓名: ").strip()
            query = "SELECT teacher_id, teacher_name, created_at, updated_at FROM Teacher WHERE teacher_name = ?"
            cursor.execute(query, (teacher_name,))
            teachers = cursor.fetchall()
            if teachers:
                print(f"找到 {len(teachers)} 位同名教师：")
                for teacher in teachers:
                    print(
                        f"教师ID: {teacher.teacher_id}, 姓名: {teacher.teacher_name}, 创建时间: {teacher.created_at}, 更新时间: {teacher.updated_at}")
            else:
                print("未找到指定的教师。")
        else:
            print("无效的选择，请输入1、2或3。")

    except pyodbc.Error as e:
        print(f"查询教师信息失败：{e}")

#删除教师
def delete_teacher(cursor):
    try:
        teacher_id = input("请输入要删除的教师ID: ").strip()
        if not teacher_id.isdigit():
            print("教师ID必须是数字，请重新输入。")
            return

        # 确认是否存在该教师
        query_check = "SELECT teacher_id, teacher_name FROM Teacher WHERE teacher_id = ?"
        cursor.execute(query_check, (int(teacher_id),))
        teacher = cursor.fetchone()

        if not teacher:
            print(f"未找到教师ID为 {teacher_id} 的记录。")
            return

        # 删除确认提示
        confirm = input(f"确认删除教师ID为 {teacher_id}，姓名为 {teacher.teacher_name} 的记录吗？(y/n): ").strip().lower()
        if confirm != 'y':
            print("操作已取消。")
            return

        # 删除教师
        query_delete = "DELETE FROM Teacher WHERE teacher_id = ?"
        cursor.execute(query_delete, (int(teacher_id),))
        cursor.connection.commit()

        print(f"教师ID为 {teacher_id} 的记录已删除成功。")

    except pyodbc.Error as e:
        print(f"删除教师信息失败：{e}")

#删除所有教师
def delete_all_teachers(cursor):
    try:
        # 确认是否继续删除操作
        confirm = input("确认删除所有教师记录吗？(此操作不可恢复) (y/n): ").strip().lower()
        if confirm != 'y':
            print("操作已取消。")
            return

        # 执行删除操作
        query_delete_all = "DELETE FROM Teacher"
        cursor.execute(query_delete_all)
        cursor.connection.commit()

        print("所有教师记录已成功删除。")
    except pyodbc.Error as e:
        print(f"删除所有教师信息失败：{e}")


# 主函数，用于测试教师管理功能
def main():
    # 连接到数据库
    # 创建测试数据文件

    connection = connect_to_database()
    if not connection:
        print("连接数据库失败。")
        return

    cursor = connection.cursor()

    while True:
        print("\n--- 教师管理系统 ---")
        print("1. 创建教师")
        print("2. 查询教师")
        print("3. 退出程序")
        print("4. 批量创建教师")
        print("5. 修改教师姓名")
        print("6. 删除教师")

        choice = input("请选择一个操作 (1-4): ").strip()

        if choice == "1":
            create_teacher(cursor)
        elif choice == "2":
            view_teachers(cursor)
        elif choice == "3":
            print("退出程序。")
            break
        elif choice=="4":
            bulk_create_teachers_from_file(cursor)
        elif choice=="5":
            update_teacher_name(cursor)
        elif choice=="6":
            delete_teacher(cursor)

        else:
            print("无效的选项，请重新选择。")

    # 关闭数据库连接
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()