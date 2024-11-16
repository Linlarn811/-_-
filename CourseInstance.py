import datetime
import pyodbc
from connect_database import connect_to_database
# 创建课程实例
def create_course_instance(cursor):
    try:
        course_id = int(input("请输入课程ID: "))
        teacher_id = int(input("请输入教师ID: "))

        # 输入并检查日期格式
        while True:
            start_date = input("请输入课程开始日期 (格式: YYYY-MM-DD): ").strip()
            end_date = input("请输入课程结束日期 (格式: YYYY-MM-DD): ").strip()
            try:
                start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

                if end_date_obj <= start_date_obj:
                    print("错误：结束日期必须晚于开始日期，请重新输入或输入 'n' 退出。")
                    retry = input("是否继续输入日期？(y/n): ").strip().lower()
                    if retry != 'y':
                        print("已退出课程实例创建。")
                        return
                else:
                    break  # 日期格式正确且结束日期晚于开始日期
            except ValueError:
                print("日期格式错误，请确保日期格式为 YYYY-MM-DD。")
                retry = input("是否继续输入日期？(y/n): ").strip().lower()
                if retry != 'y':
                    print("已退出课程实例创建。")
                    return

        # 输入考试ID
        exam_id_input = input("请输入考试ID (如果没有，请留空): ").strip()
        exam_id = int(exam_id_input) if exam_id_input else None

        # 设置创建和更新时间为当前时间
        created_at = updated_at = datetime.datetime.now()

        query = """
            INSERT INTO CourseInstance (course_id, teacher_id, start_date, end_date, created_at, updated_at, exam_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (course_id, teacher_id, start_date, end_date, created_at, updated_at, exam_id))
        cursor.connection.commit()
        print("课程实例创建成功。")
    except pyodbc.IntegrityError as e:
        if "UNIQUE KEY" in str(e):
            print("创建失败：违反唯一约束，可能是考试ID重复或其他字段冲突，请检查输入数据。")
        elif "FOREIGN KEY" in str(e):
            print("创建失败：外键约束错误，请确保课程ID或教师ID在相应表中存在。")
        else:
            print(f"创建失败：{e}")
    except ValueError:
        print("输入错误：请确保课程ID、教师ID和考试ID是整数，日期格式正确。")
    except pyodbc.Error as e:
        print(f"课程实例创建失败：{e}")

#查看已开课程实例
#1.查看全部已开课程，2.输入课程id，查看这个课程下的所有课程实例3.输入课程实例id查找对应的课程实例
def view_course_instances(cursor):
    try:
        print("\n请选择查询类型：")
        print("1. 查看所有课程实例")
        print("2. 输入课程ID，查看该课程的所有课程实例")
        print("3. 输入课程实例ID，查看对应的课程实例信息")
        choice = input("请输入选项 (1/2/3): ").strip()

        if choice == "1":
            # 查看所有课程实例
            query = """
                SELECT instance_id, course_id, teacher_id, start_date, end_date, created_at, updated_at, exam_id 
                FROM CourseInstance
            """
            cursor.execute(query)
            instances = cursor.fetchall()
            if instances:
                print("所有课程实例信息如下：")
                for instance in instances:
                    print(f"实例ID: {instance.instance_id}, 课程ID: {instance.course_id}, 教师ID: {instance.teacher_id}, "
                          f"开始日期: {instance.start_date}, 结束日期: {instance.end_date}, 创建时间: {instance.created_at}, "
                          f"更新时间: {instance.updated_at}, 考试ID: {instance.exam_id}")
            else:
                print("没有找到任何课程实例。")

        elif choice == "2":
            # 根据课程ID查询对应的所有课程实例
            course_id = int(input("请输入课程ID: "))
            query = """
                SELECT instance_id, course_id, teacher_id, start_date, end_date, created_at, updated_at, exam_id 
                FROM CourseInstance 
                WHERE course_id = ?
            """
            cursor.execute(query, (course_id,))
            instances = cursor.fetchall()
            if instances:
                print(f"课程ID {course_id} 的课程实例信息如下：")
                for instance in instances:
                    print(f"实例ID: {instance.instance_id}, 教师ID: {instance.teacher_id}, "
                          f"开始日期: {instance.start_date}, 结束日期: {instance.end_date}, "
                          f"创建时间: {instance.created_at}, 更新时间: {instance.updated_at}, 考试ID: {instance.exam_id}")
            else:
                print(f"未找到课程ID {course_id} 的任何课程实例。")

        elif choice == "3":
            # 根据课程实例ID查询详细信息
            instance_id = int(input("请输入课程实例ID: "))
            query = """
                SELECT instance_id, course_id, teacher_id, start_date, end_date, created_at, updated_at, exam_id 
                FROM CourseInstance 
                WHERE instance_id = ?
            """
            cursor.execute(query, (instance_id,))
            instance = cursor.fetchone()
            if instance:
                print(f"课程实例ID: {instance.instance_id}, 课程ID: {instance.course_id}, 教师ID: {instance.teacher_id}, "
                      f"开始日期: {instance.start_date}, 结束日期: {instance.end_date}, 创建时间: {instance.created_at}, "
                      f"更新时间: {instance.updated_at}, 考试ID: {instance.exam_id}")
            else:
                print(f"未找到课程实例ID {instance_id} 的任何信息。")
        else:
            print("无效的选项，请重新选择。")

    except ValueError:
        print("输入错误：课程ID或课程实例ID必须是整数。")
    except pyodbc.Error as e:
        print(f"查询课程实例信息失败：{e}")

#删除课程实例，提供按课程实例 ID 或按课程 ID 删除的功能
def delete_course_instance(cursor):
    try:
        print("\n请选择删除类型：")
        print("1. 按课程实例ID删除")
        print("2. 按课程ID删除该课程的所有实例")
        choice = input("请输入选项 (1/2): ").strip()

        if choice == "1":
            # 按课程实例ID删除
            instance_id = int(input("请输入要删除的课程实例ID: "))

            # 检查课程实例是否存在
            check_query = "SELECT instance_id FROM CourseInstance WHERE instance_id = ?"
            cursor.execute(check_query, (instance_id,))
            if not cursor.fetchone():
                print(f"错误：课程实例ID {instance_id} 不存在。")
                return

            # 删除关联的班级课程实例记录
            delete_related_query = "DELETE FROM ClassCourseInstance WHERE instance_id = ?"
            cursor.execute(delete_related_query, (instance_id,))

            # 删除课程实例
            delete_query = "DELETE FROM CourseInstance WHERE instance_id = ?"
            cursor.execute(delete_query, (instance_id,))
            cursor.connection.commit()

            if cursor.rowcount > 0:
                print(f"课程实例ID {instance_id} 删除成功。")
            else:
                print(f"课程实例ID {instance_id} 删除失败。")

        elif choice == "2":
            # 按课程ID删除所有实例
            course_id = int(input("请输入要删除的课程ID: "))

            # 检查是否有课程实例属于该课程
            check_query = "SELECT instance_id FROM CourseInstance WHERE course_id = ?"
            cursor.execute(check_query, (course_id,))
            instances = cursor.fetchall()
            if not instances:
                print(f"错误：课程ID {course_id} 不存在或没有关联的课程实例。")
                return

            # 删除所有关联的班级课程实例记录
            delete_related_query = "DELETE FROM ClassCourseInstance WHERE instance_id IN (SELECT instance_id FROM CourseInstance WHERE course_id = ?)"
            cursor.execute(delete_related_query, (course_id,))

            # 删除课程ID对应的所有实例
            delete_query = "DELETE FROM CourseInstance WHERE course_id = ?"
            cursor.execute(delete_query, (course_id,))
            cursor.connection.commit()

            if cursor.rowcount > 0:
                print(f"课程ID {course_id} 的所有课程实例删除成功。")
            else:
                print(f"课程ID {course_id} 的课程实例删除失败。")
        else:
            print("无效的选项，请重新选择。")

    except ValueError:
        print("输入错误：课程实例ID或课程ID必须是整数。")
    except pyodbc.Error as e:
        print(f"删除课程实例失败：{e}")


#修改课程实例
def update_course_instance(cursor):
    try:
        # 输入要更新的课程实例ID
        instance_id = int(input("请输入要更新的课程实例ID: "))

        # 检查课程实例是否存在
        check_query = "SELECT * FROM CourseInstance WHERE instance_id = ?"
        cursor.execute(check_query, (instance_id,))
        course_instance = cursor.fetchone()
        if not course_instance:
            print(f"错误：课程实例ID {instance_id} 不存在。")
            return

        # 显示当前课程实例信息
        print(f"当前课程实例信息: 课程ID: {course_instance.course_id}, 教师ID: {course_instance.teacher_id}, "
              f"开始日期: {course_instance.start_date}, 结束日期: {course_instance.end_date}, "
              f"考试ID: {course_instance.exam_id}")

        # 输入新信息，直接回车保持原值
        new_course_id = input(f"请输入新的课程ID（当前值: {course_instance.course_id}, 按回车保持不变）: ").strip()
        new_teacher_id = input(f"请输入新的教师ID（当前值: {course_instance.teacher_id}, 按回车保持不变）: ").strip()
        new_start_date = input(f"请输入新的开始日期 (格式: YYYY-MM-DD, 当前值: {course_instance.start_date}, 按回车保持不变): ").strip()
        new_end_date = input(f"请输入新的结束日期 (格式: YYYY-MM-DD, 当前值: {course_instance.end_date}, 按回车保持不变): ").strip()
        new_exam_id_input = input(f"请输入新的考试ID（当前值: {course_instance.exam_id}, 按回车保持不变）: ").strip()

        # 处理输入值，如果为空则保持原值
        new_course_id = int(new_course_id) if new_course_id else course_instance.course_id
        new_teacher_id = int(new_teacher_id) if new_teacher_id else course_instance.teacher_id
        new_start_date = new_start_date if new_start_date else course_instance.start_date
        new_end_date = new_end_date if new_end_date else course_instance.end_date
        new_exam_id = int(new_exam_id_input) if new_exam_id_input else course_instance.exam_id

        # 检查新日期的有效性
        if new_start_date > new_end_date:
            print("错误：结束日期必须晚于开始日期。")
            return

        # 更新信息
        update_query = """
            UPDATE CourseInstance
            SET course_id = ?, teacher_id = ?, start_date = ?, end_date = ?, updated_at = ?, exam_id = ?
            WHERE instance_id = ?
        """
        updated_at = datetime.datetime.now()
        cursor.execute(update_query, (new_course_id, new_teacher_id, new_start_date, new_end_date, updated_at, new_exam_id, instance_id))
        cursor.connection.commit()

        if cursor.rowcount > 0:
            print(f"课程实例ID {instance_id} 更新成功。")
        else:
            print(f"课程实例ID {instance_id} 更新失败。")

    except ValueError:
        print("输入错误：课程ID、教师ID或考试ID必须是整数，日期格式应正确。")
    except pyodbc.Error as e:
        print(f"课程实例更新失败：{e}")
#测试函数，主函数
def main():
    connection = connect_to_database()
    if not connection:
        print("连接数据库失败。")
        return

    cursor = connection.cursor()

    while True:
        print("\n--- Course Instance Management ---")
        print("1. 开课")
        print("2. 查看已开课程")
        print("3. 更新课程实例")
        print("4. 删除课程实例")
        print("5. 修改课程实例")
        print("6. 退出")

        choice = input("请选择一个操作 (1-6): ")

        if choice == "1":
            create_course_instance(cursor)
        elif choice == "2":
            view_course_instances(cursor)
        elif choice == "3":
            update_course_instance(cursor)
        elif choice == "4":
            delete_course_instance(cursor)
        elif choice == "5":
            update_course_instance(cursor)
        elif choice == "6":
            print("退出程序。")
            break
        else:
            print("无效选项，请重新选择。")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
