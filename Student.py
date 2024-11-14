from connect_database import connect_to_database
import pyodbc
import csv

#创建学生
def create_student(cursor):
    while True:
        try:
            student_id = int(input("请输入学生ID: "))
            student_name = input("请输入学生姓名: ")
            class_id_input = input("请输入班级ID（如果没有，请留空并按回车）: ").strip()

            # 如果班级ID为空，则设置为 None
            class_id = int(class_id_input) if class_id_input else None

            query = "INSERT INTO Student (student_id, student_name, class_id) VALUES (?, ?, ?)"
            cursor.execute(query, (student_id, student_name, class_id))
            cursor.connection.commit()
            success_message = "学生创建成功."
            print(success_message)
            break  # 成功后退出循环
        except pyodbc.IntegrityError:  # 重复键值错误
            error_message = "学生创建失败：该学生ID已存在，请重新输入。"
            print(error_message)
        except ValueError:  # 输入非整数ID
            error_message = "输入错误：学生ID必须是整数，班级ID如果有也必须是整数，请重新输入。"
            print(error_message)
        except pyodbc.Error as e:  # 其他数据库错误
            error_message = f"学生创建失败：{e}"
            print(error_message)

        # 用户选择重新输入或退出
        retry_message = "是否继续尝试？(y/n): "
        retry = input(retry_message).strip().lower()
        if retry != 'y':
            exit_message = "已退出学生创建。"
            print(exit_message)
            break
#批量导入学生数据
def bulk_import_students(cursor):
    # 用户输入文件名
    print("文件格式为student_id,student_name,class_id(可以为空)")
    filename = input("请输入要导入的CSV文件名（包括路径）: ").strip()

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # 跳过标题行

            for row in csv_reader:
                try:
                    student_id = int(float(row[0]))  # 确保 student_id 是整数
                    student_name = row[1]
                    # 将 class_id 转为整数并处理空值
                    class_id = int(float(row[2])) if row[2] else None

                    query = "INSERT INTO Student (student_id, student_name, class_id) VALUES (?, ?, ?)"
                    cursor.execute(query, (student_id, student_name, class_id))

                except ValueError:
                    print(f"数据错误：学生ID和班级ID必须是整数，跳过该行。行内容: {row}")
                except pyodbc.IntegrityError:
                    print(f"数据错误：学生ID {student_id} 已存在，跳过该行。")
                except pyodbc.Error as e:
                    print(f"插入失败：{e}，行内容: {row}")

        cursor.connection.commit()
        print("批量导入学员信息成功。")
    except FileNotFoundError:
        print("文件未找到，请检查文件路径和文件名。")
    except Exception as e:
        print(f"文件处理错误：{e}")


#查看学生
def view_students(cursor):
    # 提示用户选择查询类型
    print("\n请选择查询类型：")
    print("1. 查看所有学生")
    print("2. 根据学生ID查询")
    print("3. 根据学生姓名查询")
    choice = input("请输入选项 (1/2/3): ").strip()

    if choice == "1":
        # 查询所有学生
        query = "SELECT * FROM Student"
        try:
            cursor.execute(query)
            students = cursor.fetchall()
            if students:
                for student in students:
                    student_info = f"Student ID: {student.student_id}, Name: {student.student_name}, Class ID: {student.class_id}"
                    print(student_info)
            else:
                no_data_message = "没有找到任何学生信息。"
                print(no_data_message)
        except pyodbc.Error as e:
            error_message = f"无法查看学生信息：{e}"
            print(error_message)

    elif choice == "2":
        # 根据学生ID查询
        try:
            student_id = int(input("请输入学生ID: "))
            query = "SELECT * FROM Student WHERE student_id = ?"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            if result:
                student_info = f"Student ID: {result.student_id}, Name: {result.student_name}, Class ID: {result.class_id}"
                print(student_info)
            else:
                not_found_message = "未找到指定ID的学生。"
                print(not_found_message)
        except ValueError:
            error_message = "输入错误：学生ID必须是整数。"
            print(error_message)
        except pyodbc.Error as e:
            error_message = f"查询失败：{e}"
            print(error_message)

    elif choice == "3":
        # 根据学生姓名查询
        student_name = input("请输入学生姓名: ").strip()
        query = "SELECT * FROM Student WHERE student_name = ?"
        try:
            cursor.execute(query, (student_name,))
            results = cursor.fetchall()
            if results:
                for student in results:
                    student_info = f"Student ID: {student.student_id}, Name: {student.student_name}, Class ID: {student.class_id}"
                    print(student_info)
            else:
                not_found_message = "未找到指定姓名的学生。"
                print(not_found_message)
        except pyodbc.Error as e:
            error_message = f"查询失败：{e}"
            print(error_message)

    else:
        invalid_choice_message = "无效的选项，请重新选择。"
        print(invalid_choice_message)

#更新学生
def update_student(cursor):
    while True:
        try:
            student_id = int(input("请输入要更新的学生ID: "))

            # 查询当前学生的详细信息
            query = "SELECT student_name, class_id FROM Student WHERE student_id = ?"
            cursor.execute(query, (student_id,))
            student = cursor.fetchone()

            if not student:
                not_found_message = "未找到指定学生ID，无法更新信息。"
                print(not_found_message)
                break

            # 获取当前的学生姓名和班级ID
            current_name = student.student_name
            current_class_id = student.class_id

            # 输入新的学生姓名
            new_name = input(f"请输入新的学生姓名（当前值：{current_name}，如果不修改，请直接按回车）: ").strip()
            if not new_name:  # 如果用户没有输入新名字，保持原值
                new_name = current_name

            # 输入新的班级ID
            new_class_id_input = input(f"请输入新的班级ID（当前值：{current_class_id}，如果不修改，请直接按回车）: ").strip()

            # 如果班级ID为空，则保持原值
            if not new_class_id_input:
                new_class_id = current_class_id
            else:
                try:
                    new_class_id = int(new_class_id_input)

                    # 检查班级ID是否有效
                    query = "SELECT class_id FROM Class WHERE class_id = ?"
                    cursor.execute(query, (new_class_id,))
                    if cursor.fetchone() is None:
                        error_message = f"班级ID {new_class_id} 不存在，请输入有效的班级ID。"
                        print(error_message)
                        continue
                except ValueError:
                    error_message = "班级ID必须是整数，请重新输入。"
                    print(error_message)
                    continue

            # 构建 SQL 更新语句
            if new_class_id is not None:
                query = "UPDATE Student SET student_name = ?, class_id = ? WHERE student_id = ?"
                cursor.execute(query, (new_name, new_class_id, student_id))
            else:
                query = "UPDATE Student SET student_name = ?, class_id = NULL WHERE student_id = ?"
                cursor.execute(query, (new_name, student_id))

            cursor.connection.commit()

            if cursor.rowcount > 0:
                success_message = "学生信息更新成功."
                print(success_message)
            else:
                not_found_message = "未找到指定学生ID，未更新任何记录。"
                print(not_found_message)
            break

        except ValueError:  # 输入非整数ID或班级ID
            error_message = "输入错误：学生ID和班级ID必须是整数，请重新输入。"
            print(error_message)
        except pyodbc.Error as e:  # 其他数据库错误
            error_message = f"学生信息更新失败：{e}"
            print(error_message)

        # 用户选择重新输入或退出
        retry_message = "是否继续尝试？(y/n): "
        retry = input(retry_message).strip().lower()
        if retry != 'y':
            exit_message = "已退出学生信息更新。"
            print(exit_message)
            break


#删除学生
def delete_student(cursor):
    while True:
        try:
            student_id = int(input("请输入要删除的学生ID: "))

            query = "DELETE FROM Student WHERE student_id = ?"
            cursor.execute(query, (student_id,))
            cursor.connection.commit()

            if cursor.rowcount > 0:
                success_message = "学生删除成功."
                print(success_message)
            else:
                not_found_message = "未找到指定学生ID，未删除任何记录。"
                print(not_found_message)
            break
        except ValueError:  # 输入非整数ID
            error_message = "输入错误：学生ID必须是整数，请重新输入。"
            print(error_message)
        except pyodbc.Error as e:  # 其他数据库错误
            error_message = f"学生删除失败：{e}"
            print(error_message)

        # 用户选择重新输入或退出
        retry_message = "是否继续尝试？(y/n): "
        retry = input(retry_message).strip().lower()
        if retry != 'y':
            exit_message = "已退出学生删除。"
            print(exit_message)
            break
#调用函数，调试用
def main():
    connection = connect_to_database()
    if not connection:
        print("连接数据库失败.")
        return

    cursor = connection.cursor()

    while True:
        print("\n--- Student Management System ---")
        print("1. Create a new student")
        print("2. View all students or search by ID/name")
        print("3. Update student information")
        print("4. Delete a student")
        print("5. Exit")
        print("6.批量导入数据")
        choice = input("Select an option: ")

        if choice == "1":
            create_student(cursor)
        elif choice == "2":
            view_students(cursor)
        elif choice == "3":
            update_student(cursor)
        elif choice == "4":
            delete_student(cursor)
        elif choice=="6":
            bulk_import_students(cursor)
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please select again.")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
