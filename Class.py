from connect_database import connect_to_database
import pyodbc
import csv
import os
#班级管理模块

# 创建班级
def create_class(cursor):
    while True:
        try:
            class_id = int(input("请输入班级ID: "))
            class_name = input("请输入班级名: ")

            query = "INSERT INTO Class (class_id, class_name) VALUES (?, ?)"
            cursor.execute(query, (class_id, class_name))
            cursor.connection.commit()
            success_message = "班级创建成功."
            print(success_message)
            break  # 成功后退出循环
        except pyodbc.IntegrityError:
            error_message = "班级创建失败：该班级ID已存在，请重新输入或输入'q'退出。"
            print(error_message)
        except ValueError:
            error_message = "输入错误：班级ID必须是整数，请重新输入或输入'q'退出。"
            print(error_message)
        except pyodbc.Error as e:
            error_message = f"班级创建失败：{e}"
            print(error_message)

        # 用户选择重新输入或退出
        retry_message = "是否继续尝试？(y/n): "
        retry = input(retry_message).strip().lower()
        if retry != 'y':
            exit_message = "已退出班级创建。"
            print(exit_message)
            break

#查看每个班级对应的学生的信息
def view_class_students(cursor):
    try:
        # 输入班级ID
        class_id = int(input("请输入要查看的班级ID: "))

        # 检查班级是否存在
        check_class_query = "SELECT class_name FROM Class WHERE class_id = ?"
        cursor.execute(check_class_query, (class_id,))
        class_info = cursor.fetchone()
        if not class_info:
            print("错误：指定的班级ID不存在。")
            return

        # 显示班级信息
        print(f"班级ID: {class_id}, 班级名称: {class_info.class_name}")

        # 查询班级的学生信息
        query = "SELECT student_id, student_name FROM Student WHERE class_id = ?"
        cursor.execute(query, (class_id,))
        students = cursor.fetchall()

        if students:
            print("班级中的学生信息如下：")
            for student in students:
                print(f"学生ID: {student.student_id}, 学生姓名: {student.student_name}")
        else:
            print("该班级中没有学生。")
    except ValueError:
        print("输入错误：班级ID必须是整数，请重新输入。")
    except pyodbc.Error as e:
        print(f"查询班级学生信息失败：{e}")


# 查看班级1.查看所有班级 2.根据班级ID查询 3.根据班级名称查询
def view_classes(cursor):
    # 提示用户选择查询类型
    print("\n请选择查询类型：")
    print("1. 查看所有班级")
    print("2. 根据班级ID查询")
    print("3. 根据班级名查询")
    choice = input("请输入选项 (1/2/3): ").strip()

    if choice == "1":
        # 查询所有班级
        query = "SELECT * FROM Class"
        try:
            cursor.execute(query)
            classes = cursor.fetchall()
            if classes:
                for class_ in classes:
                    class_info = f"Class ID: {class_.class_id}, Class Name: {class_.class_name}"
                    print(class_info)
            else:
                no_data_message = "没有找到任何班级信息。"
                print(no_data_message)
        except pyodbc.Error as e:
            error_message = f"无法查看班级信息：{e}"
            print(error_message)

    elif choice == "2":
        # 根据班级ID查询
        try:
            class_id = int(input("请输入班级ID: "))
            query = "SELECT * FROM Class WHERE class_id = ?"
            cursor.execute(query, (class_id,))
            result = cursor.fetchone()
            if result:
                class_info = f"Class ID: {result.class_id}, Class Name: {result.class_name}"
                print(class_info)
            else:
                not_found_message = "未找到指定ID的班级。"
                print(not_found_message)
        except ValueError:
            error_message = "输入错误：班级ID必须是整数。"
            print(error_message)
        except pyodbc.Error as e:
            error_message = f"查询失败：{e}"
            print(error_message)

    elif choice == "3":
        # 根据班级名查询
        class_name = input("请输入班级名: ").strip()
        query = "SELECT * FROM Class WHERE class_name = ?"
        try:
            cursor.execute(query, (class_name,))
            result = cursor.fetchall()
            if result:
                for class_ in result:
                    class_info = f"Class ID: {class_.class_id}, Class Name: {class_.class_name}"
                    print(class_info)
            else:
                not_found_message = "未找到指定名称的班级。"
                print(not_found_message)
        except pyodbc.Error as e:
            error_message = f"查询失败：{e}"
            print(error_message)

    else:
        invalid_choice_message = "无效的选项，请重新选择。"
        print(invalid_choice_message)
#更新班级信息
def update_class(cursor):
    while True:
        try:
            # 获取要更新的班级ID
            class_id = int(input("请输入要更新的班级ID: "))

            # 检查班级是否存在
            check_class_query = "SELECT * FROM Class WHERE class_id = ?"
            cursor.execute(check_class_query, (class_id,))
            current_class = cursor.fetchone()
            if not current_class:
                print("错误：指定的班级ID不存在。")
                return

            # 显示当前班级信息
            print(f"当前班级信息 -> 班级ID: {current_class.class_id}, 班级名称: {current_class.class_name}")

            # 获取新的班级名称
            new_class_name = input("请输入新的班级名称（直接回车保持不变）: ").strip() or current_class.class_name

            # 构建并执行更新查询（仅更新班级名称，不更新班级ID）
            update_query = "UPDATE Class SET class_name = ? WHERE class_id = ?"
            cursor.execute(update_query, (new_class_name, class_id))
            cursor.connection.commit()

            if cursor.rowcount > 0:
                print("班级更新成功。")
            else:
                print("未找到指定班级ID，未更新任何记录。")
            break

        except ValueError:
            print("输入错误：班级ID必须是整数，请重新输入。")
        except pyodbc.Error as e:
            print(f"班级更新失败：{e}")

        # 选择是否重新尝试
        retry_message = "是否继续尝试？(y/n): "
        retry = input(retry_message).strip().lower()
        if retry != 'y':
            print("已退出班级更新。")
            break

#删除班级
def delete_class(cursor):
    while True:
        try:
            class_id = int(input("请输入要删除的班级ID: "))

            # 首先将关联的学生记录的 class_id 置为 NULL
            update_students_query = "UPDATE Student SET class_id = NULL WHERE class_id = ?"
            cursor.execute(update_students_query, (class_id,))

            # 然后删除班级记录
            delete_class_query = "DELETE FROM Class WHERE class_id = ?"
            cursor.execute(delete_class_query, (class_id,))
            cursor.connection.commit()

            if cursor.rowcount > 0:
                success_message = "班级及其关联的学生记录更新成功，班级已删除。"
                print(success_message)
            else:
                not_found_message = "未找到指定班级ID，未删除任何记录。"
                print(not_found_message)
            break

        except ValueError:  # 输入非整数ID
            error_message = "输入错误：班级ID必须是整数，请重新输入。"
            print(error_message)
        except pyodbc.Error as e:  # 其他数据库错误
            error_message = f"班级删除失败：{e}"
            print(error_message)

        # 用户选择重新输入或退出
        retry_message = "是否继续尝试？(y/n): "
        retry = input(retry_message).strip().lower()
        if retry != 'y':
            exit_message = "已退出班级删除。"
            print(exit_message)
            break


#踢出学员 将指定学员的 class_id 字段设置为 NULL，从而移出指定班级。
def remove_student_from_class(cursor):
    try:
        student_id = int(input("请输入要移出班级的学员ID: "))
        query = "UPDATE Student SET class_id = NULL WHERE student_id = ?"
        cursor.execute(query, (student_id,))
        cursor.connection.commit()

        if cursor.rowcount > 0:
            success_message = "学员已成功移出班级。"
            print(success_message)
        else:
            not_found_message = "未找到指定学员ID，未移除任何记录。"
            print(not_found_message)
    except ValueError:
        error_message = "输入错误：学员ID必须是整数，请重新输入。"
        print(error_message)
    except pyodbc.Error as e:
        error_message = f"操作失败：{e}"
        print(error_message)
#转班
#将指定学员的 class_id 更新为新班级ID，从而实现学员转班功能
def transfer_student_to_class(cursor):
    try:
        student_id = int(input("请输入要转班的学员ID: "))
        new_class_id = int(input("请输入新的班级ID: "))

        # 检查新班级ID是否存在
        check_class_query = "SELECT 1 FROM Class WHERE class_id = ?"
        cursor.execute(check_class_query, (new_class_id,))
        if not cursor.fetchone():
            print("错误：指定的班级ID不存在。")
            return

        # 转班操作
        query = "UPDATE Student SET class_id = ? WHERE student_id = ?"
        cursor.execute(query, (new_class_id, student_id))
        cursor.connection.commit()

        if cursor.rowcount > 0:
            success_message = "学员已成功转班。"
            print(success_message)
        else:
            not_found_message = "未找到指定学员ID，未转班。"
            print(not_found_message)
    except ValueError:
        error_message = "输入错误：学员ID和班级ID必须是整数，请重新输入。"
        print(error_message)
    except pyodbc.Error as e:
        error_message = f"转班失败：{e}"
        print(error_message)

#加入学员
def add_student_to_class(cursor):
    try:
        student_id = int(input("请输入要加入班级的学员ID: "))
        class_id = int(input("请输入班级ID: "))

        # 检查班级ID是否存在
        check_class_query = "SELECT 1 FROM Class WHERE class_id = ?"
        cursor.execute(check_class_query, (class_id,))
        if not cursor.fetchone():
            print("错误：指定的班级ID不存在。")
            return

        # 加入学员操作
        query = "UPDATE Student SET class_id = ? WHERE student_id = ?"
        cursor.execute(query, (class_id, student_id))
        cursor.connection.commit()

        if cursor.rowcount > 0:
            success_message = "学员已成功加入班级。"
            print(success_message)
        else:
            not_found_message = "未找到指定学员ID，未加入任何班级。"
            print(not_found_message)
    except ValueError:
        error_message = "输入错误：学员ID和班级ID必须是整数，请重新输入。"
        print(error_message)
    except pyodbc.Error as e:
        error_message = f"加入班级失败：{e}"
        print(error_message)

#批量加入学生
#指定加入班级，读取学生信息文件，批量加入
#信息文件格式全为学生ID
def bulk_update_students_class(cursor):
    try:
        # 用户输入班级ID
        class_id = int(input("请输入要加入学生的班级ID: "))

        # 检查班级是否存在
        check_class_query = "SELECT class_name FROM Class WHERE class_id = ?"
        cursor.execute(check_class_query, (class_id,))
        class_info = cursor.fetchone()
        if not class_info:
            print("错误：指定的班级ID不存在。")
            return
        print(f"班级ID: {class_id}, 班级名称: {class_info.class_name}")

        # 固定目录路径，用户只需输入文件名
        base_directory = r"D:\pythonProject\在线教学系统\data"
        filename = input("请输入包含学生信息的文件名（无需路径）: ").strip()
        full_path = os.path.join(base_directory, filename)  # 拼接完整路径

        # 读取并批量更新学生的班级信息
        with open(full_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # 跳过标题行

            for row in csv_reader:
                try:
                    student_id = int(row[0].strip())  # 解析 student_id 为整数

                    # 更新现有学生的班级信息
                    query = "UPDATE Student SET class_id = ? WHERE student_id = ?"
                    cursor.execute(query, (class_id, student_id))

                    # 检查更新结果
                    if cursor.rowcount == 0:
                        print(f"警告：未找到学生ID {student_id}，未更新该记录。")

                except ValueError:
                    print(f"数据错误：学生ID必须是整数，跳过该行。行内容: {row}")
                except pyodbc.Error as e:
                    print(f"更新失败：{e}，行内容: {row}")

        cursor.connection.commit()
        print("批量更新学生班级信息成功。")

    except FileNotFoundError:
        print("文件未找到，请检查文件名并确保文件存在于指定目录。")
    except ValueError:
        print("输入错误：班级ID必须是整数。")
    except Exception as e:
        print(f"批量更新学生班级信息时发生错误：{e}")


#主函数，调试用



# 调用的模块函数在这里定义的前提下
# 添加到主函数中的功能选项

def main():
    connection = connect_to_database()
    if not connection:
        print("连接数据库失败.")
        return

    cursor = connection.cursor()

    while True:
        print("\n--- 班级与学员管理系统 ---")
        print("1. 创建班级")
        print("2. 查看班级")
        print("3. 更新班级")
        print("4. 删除班级")
        print("5. 踢出学员")
        print("6. 转班")
        print("7. 加入学员")
        print("8. 查看班级中的学生信息")
        print("9. 批量加入学生到班级")
        print("10. 退出程序")

        choice = input("请选择一个操作 (1-10): ")

        if choice == "1":
            create_class(cursor)
        elif choice == "2":
            view_classes(cursor)
        elif choice == "3":
            update_class(cursor)
        elif choice == "4":
            delete_class(cursor)
        elif choice == "5":
            remove_student_from_class(cursor)
        elif choice == "6":
            transfer_student_to_class(cursor)
        elif choice == "7":
            add_student_to_class(cursor)
        elif choice == "8":
            view_class_students(cursor)
        elif choice == "9":
            bulk_update_students_class(cursor)
        elif choice == "10":
            print("退出程序。")
            break
        else:
            print("无效的选项，请重新选择。")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()



