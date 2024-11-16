import pyodbc
from connect_database import connect_to_database


# 创建课程
def create_course(cursor, course_name, description, organization, category, course_type, credits, cost, total_duration):
    # 课程类型的有效值
    valid_course_types = ["混合", "面授", "录播", "直播"]

    # 验证课程类型是否有效
    if course_type not in valid_course_types:
        print("无效的课程类型！请确保课程类型是 '混合', '面授', '录播' 或 '直播' 中的一个有效值。")
        return

    # 验证学分（假设学分应为正整数）
    if credits <= 0:
        print("学分应为正整数。")
        return

    # 验证课程费用（假设费用应为非负数）
    if cost < 0:
        print("课程费用应为非负数。")
        return

    # 验证课程总时长（假设时长应为正整数）
    if total_duration <= 0:
        print("课程总时长应为正整数。")
        return

    query = """
    INSERT INTO Course (course_name, description, organization, category, course_type, credits, cost, total_duration)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(query,
                       (course_name, description, organization, category, course_type, credits, cost, total_duration))
        cursor.connection.commit()
        print(f"课程 '{course_name}' 创建成功。")
    except Exception as e:
        print(f"创建课程时发生错误: {e}")


# 更新课程信息
def update_course(cursor, course_id, description, organization, category, course_type):
    # 课程类型的有效值
    valid_course_types = ["混合", "面授", "录播", "直播"]

    # 验证课程类型是否有效
    if course_type not in valid_course_types:
        print("无效的课程类型！请确保课程类型是 '混合', '面授', '录播' 或 '直播' 中的一个有效值。")
        return

    query = """
    UPDATE Course 
    SET description = ?, organization = ?, category = ?, course_type = ? 
    WHERE course_id = ?
    """
    try:
        cursor.execute(query, (description, organization, category, course_type, course_id))
        cursor.connection.commit()
        print(f"课程 ID {course_id} 更新成功。")
    except Exception as e:
        print(f"更新课程时发生错误: {e}")


# 删除课程
def delete_course(cursor, course_id):
    try:
        # 删除相关联的试卷和题库数据

        cursor.execute("DELETE FROM QuestionBank WHERE course_id = ?", (course_id,))

        # 删除课程
        cursor.execute("DELETE FROM Course WHERE course_id = ?", (course_id,))
        cursor.connection.commit()
        print(f"课程 ID {course_id} 及其关联数据删除成功。")
    except Exception as e:
        print(f"删除课程时发生错误: {e}")


# 查看所有课程
def show_all_courses(cursor):
    query = "SELECT * FROM Course"
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        print("\n--- 所有课程 ---")
        for row in rows:
            print(
                f"课程ID: {row.course_id}, 课程名称: {row.course_name}, 描述: {row.description}, 机构: {row.organization}, 类别: {row.category}, 类型: {row.course_type}, 学分: {row.credits}, 费用: {row.cost}, 时长: {row.total_duration}")
    else:
        print("没有找到课程信息。")


# 主程序
def main():
    connection = connect_to_database()
    if not connection:
        print("连接数据库失败.")
        return

    cursor = connection.cursor()

    while True:
        print("\n--- 课程管理系统 ---")
        print("1. 创建课程")
        print("2. 删除课程")
        print("3. 更新课程信息")
        print("4. 查看所有课程")
        print("5. 退出程序")

        choice = input("请选择一个操作 (1-5): ")

        if choice == "1":
            course_name = input("请输入课程名称: ")
            description = input("请输入课程描述: ")
            organization = input("请输入课程所在机构: ")
            category = input("请输入课程类别: ")
            course_type = input("请输入课程类型（混合/面授/录播/直播）: ")
            credits = int(input("请输入课程学分: "))
            cost = float(input("请输入课程费用: "))
            total_duration = int(input("请输入课程总时长（分钟）: "))
            create_course(cursor, course_name, description, organization, category, course_type, credits, cost,
                          total_duration)
        elif choice == "2":
            course_id = int(input("请输入要删除的课程ID: "))
            delete_course(cursor, course_id)
        elif choice == "3":
            course_id = int(input("请输入要更新的课程ID: "))
            description = input("请输入新的课程描述: ")
            organization = input("请输入新的课程所在机构: ")
            category = input("请输入新的课程类别: ")
            course_type = input("请输入新的课程类型（混合/面授/录播/直播）: ")
            update_course(cursor, course_id, description, organization, category, course_type)
        elif choice == "4":
            show_all_courses(cursor)
        elif choice == "5":
            print("退出程序。")
            break
        else:
            print("无效的选项，请重新选择。")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()