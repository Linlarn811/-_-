from connect_database import connect_to_database

def add_question_bank(course_id, bank_name):
    try:
        connection = connect_to_database()

        if connection:
            cursor = connection.cursor()
            query = """INSERT INTO QuestionBank (course_id, bank_name)
                       VALUES (?, ?)"""
            cursor.execute(query, (course_id, bank_name))
            connection.commit()
            print("题库添加成功。")
        else:
            print("无法连接到数据库，添加题库失败。")

    except Exception as e:
        print("Error:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()
def delete_question_bank(bank_id):
    try:
        connection = connect_to_database()

        if connection:
            cursor = connection.cursor()
            query = "DELETE FROM QuestionBank WHERE bank_id = ?"
            cursor.execute(query, (bank_id,))
            connection.commit()
            print(f"题库 ID {bank_id} 删除成功。")
        else:
            print("无法连接到数据库，删除题库失败。")

    except Exception as e:
        print("Error:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()
def update_question_bank(bank_id, bank_name):
    try:
        connection = connect_to_database()

        if connection:
            cursor = connection.cursor()
            query = """UPDATE QuestionBank
                       SET bank_name = ?
                       WHERE bank_id = ?"""
            cursor.execute(query, (bank_name, bank_id))
            connection.commit()
            print(f"题库 ID {bank_id} 信息更新成功。")
        else:
            print("无法连接到数据库，更新题库信息失败。")

    except Exception as e:
        print("Error:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()
def view_question_banks():
    try:
        connection = connect_to_database()

        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM QuestionBank"
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"题库 ID: {row[0]}, 课程 ID: {row[1]}, 题库名称: {row[2]}")
            else:
                print("没有题库记录。")
        else:
            print("无法连接到数据库，无法查看题库。")

    except Exception as e:
        print("Error:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()
def main():
    while True:
        print("题库管理系统")
        print("1. 添加题库")
        print("2. 删除题库")
        print("3. 修改题库信息")
        print("4. 查看题库")
        print("5. 退出")
        choice = input("请输入选项 (1/2/3/4/5): ")

        if choice == "1":
            course_id = int(input("请输入课程ID: "))
            bank_name = input("请输入题库名称: ")
            add_question_bank(course_id, bank_name)
        elif choice == "2":
            bank_id = int(input("请输入题库ID: "))
            delete_question_bank(bank_id)
        elif choice == "3":
            bank_id = int(input("请输入题库ID: "))
            bank_name = input("请输入新的题库名称: ")
            update_question_bank(bank_id, bank_name)
        elif choice == "4":
            view_question_banks()
        elif choice == "5":
            break
        else:
            print("无效选项，请重新输入。")

if __name__ == "__main__":
    main()
