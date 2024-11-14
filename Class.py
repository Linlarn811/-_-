from connect_database import connect_to_database
import pyodbc
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
            check_class_query = "SELECT 1 FROM Class WHERE class_id = ?"
            cursor.execute(check_class_query, (class_id,))
            if not cursor.fetchone():
                print("错误：指定的班级ID不存在。")
                return

            # 提供更新班级ID的选项
            update_id_input = input("是否更新班级ID？(y/n): ").strip().lower()
            new_class_id = None
            if update_id_input == 'y':
                new_class_id = int(input("请输入新的班级ID: "))
                # 检查新班级ID是否已存在
                cursor.execute(check_class_query, (new_class_id,))
                if cursor.fetchone():
                    print("错误：新班级ID已存在，请选择其他ID。")
                    continue

            # 更新班级名称
            new_class_name = input("请输入新的班级名称: ")

            # 构建并执行更新查询
            if new_class_id:
                update_query = "UPDATE Class SET class_id = ?, class_name = ? WHERE class_id = ?"
                cursor.execute(update_query, (new_class_id, new_class_name, class_id))
            else:
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
        except pyodbc.IntegrityError:
            print("更新失败：新班级ID已存在，无法更新。")
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

            query = "DELETE FROM Class WHERE class_id = ?"
            cursor.execute(query, (class_id,))
            cursor.connection.commit()

            if cursor.rowcount > 0:
                success_message = "班级删除成功."
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
        print("8. 退出程序")

        choice = input("请选择一个操作 (1-8): ")

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
            print("退出程序。")
            break
        else:
            print("无效的选项，请重新选择。")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()

