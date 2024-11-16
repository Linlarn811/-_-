from connect_database import connect_to_database
import pyodbc
import csv
import os
# 添加班级与课程实例的关联（enrollment_date 由系统自动生成）
def create_class_course_instance(cursor):
    try:
        class_id = int(input("请输入班级ID: "))
        instance_id = int(input("请输入课程实例ID: "))

        # 检查班级ID是否存在
        check_class_query = "SELECT 1 FROM Class WHERE class_id = ?"
        cursor.execute(check_class_query, (class_id,))
        if not cursor.fetchone():
            print(f"错误：班级ID {class_id} 不存在。")
            return

        # 检查课程实例ID是否存在
        check_instance_query = "SELECT 1 FROM CourseInstance WHERE instance_id = ?"
        cursor.execute(check_instance_query, (instance_id,))
        if not cursor.fetchone():
            print(f"错误：课程实例ID {instance_id} 不存在。")
            return

        # 插入数据
        query = """
            INSERT INTO ClassCourseInstance (class_id, instance_id, enrollment_date)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """
        cursor.execute(query, (class_id, instance_id))
        cursor.connection.commit()
        print("班级和课程实例的关联创建成功，登记日期已自动设置为当前时间。")

    except pyodbc.IntegrityError as e:
        if "duplicate key" in str(e).lower() or "UNIQUE KEY" in str(e).lower():
            print(f"创建失败：班级ID {class_id} 和课程实例ID {instance_id} 的关联已经存在。")
        elif "FOREIGN KEY" in str(e).lower():
            print(f"创建失败：外键约束错误，可能是班级ID或课程实例ID无效。错误详情: {e}")
        else:
            print(f"创建失败：{e}")
    except ValueError:
        print("输入错误：班级ID和课程实例ID必须是整数。")
    except pyodbc.Error as e:
        print(f"创建失败：{e}")


# 查询班级与课程实例的关联
def view_class_course_instance(cursor):
    print("查询选项：")
    print("1. 查看所有班级和课程实例的关联")
    print("2. 根据班级ID查询")
    print("3. 根据课程实例ID查询")
    choice = input("请选择查询类型 (1/2/3): ").strip()

    try:
        if choice == "1":
            query = "SELECT * FROM ClassCourseInstance"
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(f"班级ID: {row.class_id}, 课程实例ID: {row.instance_id}, 登记日期: {row.enrollment_date}")
            else:
                print("没有找到任何关联记录。")
        elif choice == "2":
            class_id = int(input("请输入班级ID: "))
            query = "SELECT * FROM ClassCourseInstance WHERE class_id = ?"
            cursor.execute(query, (class_id,))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(f"班级ID: {row.class_id}, 课程实例ID: {row.instance_id}, 登记日期: {row.enrollment_date}")
            else:
                print(f"未找到班级ID {class_id} 的关联记录。")
        elif choice == "3":
            instance_id = int(input("请输入课程实例ID: "))
            query = "SELECT * FROM ClassCourseInstance WHERE instance_id = ?"
            cursor.execute(query, (instance_id,))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(f"班级ID: {row.class_id}, 课程实例ID: {row.instance_id}, 登记日期: {row.enrollment_date}")
            else:
                print(f"未找到课程实例ID {instance_id} 的关联记录。")
        else:
            print("无效的选项，请重新选择。")
    except ValueError:
        print("输入错误：班级ID或课程实例ID必须是整数。")
    except pyodbc.Error as e:
        print(f"查询失败：{e}")


# 更新班级与课程实例的关联
def update_class_course_instance(cursor):
    try:
        class_id = int(input("请输入要更新的班级ID: "))
        instance_id = int(input("请输入要更新的课程实例ID: "))

        # 检查关联是否存在
        check_query = "SELECT * FROM ClassCourseInstance WHERE class_id = ? AND instance_id = ?"
        cursor.execute(check_query, (class_id, instance_id))
        record = cursor.fetchone()
        if not record:
            print(f"错误：未找到班级ID {class_id} 和课程实例ID {instance_id} 的关联。")
            return

        print(f"当前记录 -> 班级ID: {record.class_id}, 课程实例ID: {record.instance_id}, 登记日期: {record.enrollment_date}")

        # 暂时允许用户仅更新实例 ID 或班级 ID（enrollment_date 不变）
        new_class_id = input(f"请输入新的班级ID（当前值: {record.class_id}，按回车保持不变）: ").strip()
        new_instance_id = input(f"请输入新的课程实例ID（当前值: {record.instance_id}，按回车保持不变）: ").strip()

        # 处理输入值
        new_class_id = int(new_class_id) if new_class_id else record.class_id
        new_instance_id = int(new_instance_id) if new_instance_id else record.instance_id

        # 更新记录
        update_query = """
            UPDATE ClassCourseInstance
            SET class_id = ?, instance_id = ?
            WHERE class_id = ? AND instance_id = ?
        """
        cursor.execute(update_query, (new_class_id, new_instance_id, record.class_id, record.instance_id))
        cursor.connection.commit()
        print(f"班级ID {record.class_id} 和课程实例ID {record.instance_id} 的关联更新成功。")
    except ValueError:
        print("输入错误：班级ID和课程实例ID必须是整数。")
    except pyodbc.Error as e:
        print(f"更新失败：{e}")


# 删除班级与课程实例的关联
def delete_class_course_instance(cursor):
    try:
        class_id = int(input("请输入要删除的班级ID: "))
        instance_id = int(input("请输入要删除的课程实例ID: "))

        # 删除关联记录
        delete_query = "DELETE FROM ClassCourseInstance WHERE class_id = ? AND instance_id = ?"
        cursor.execute(delete_query, (class_id, instance_id))
        cursor.connection.commit()

        if cursor.rowcount > 0:
            print(f"班级ID {class_id} 和课程实例ID {instance_id} 的关联删除成功。")
        else:
            print(f"未找到班级ID {class_id} 和课程实例ID {instance_id} 的关联记录。")
    except ValueError:
        print("输入错误：班级ID和课程实例ID必须是整数。")
    except pyodbc.Error as e:
        print(f"删除失败：{e}")


# 主函数测试用
def main():
    connection = connect_to_database()
    if not connection:
        print("连接数据库失败。")
        return

    cursor = connection.cursor()

    while True:
        print("\n--- Class-Course Instance Management ---")
        print("1. 创建班级与课程实例的关联")
        print("2. 查看班级与课程实例的关联")
        print("3. 更新班级与课程实例的关联")
        print("4. 删除班级与课程实例的关联")
        print("5. 退出")

        choice = input("请选择一个操作 (1-5): ")

        if choice == "1":
            create_class_course_instance(cursor)
        elif choice == "2":
            view_class_course_instance(cursor)
        elif choice == "3":
            update_class_course_instance(cursor)
        elif choice == "4":
            delete_class_course_instance(cursor)
        elif choice == "5":
            print("退出程序。")
            break
        else:
            print("无效选项，请重新选择。")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
