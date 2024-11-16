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


def view_questions(bank_id):
    """查看题库中题目详细信息"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            # 获取题库中所有题目
            query = "SELECT * FROM Question WHERE bank_id = ?"
            cursor.execute(query, (bank_id,))
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    question_id = row[0]
                    knowledge_point = row[2]
                    question_type = row[3]
                    question_text = row[4]

                    # 查询该题目被组卷的次数
                    query_paper = "SELECT COUNT(*) FROM ExamPaperQuestion WHERE question_id = ?"
                    cursor.execute(query_paper, (question_id,))
                    paper_count = cursor.fetchone()[0]

                    # 查询该题目被考试的次数
                    query_exam = """
                        SELECT COUNT(*) 
                        FROM ExamResult 
                        WHERE question_id = ?
                    """
                    cursor.execute(query_exam, (question_id,))
                    exam_count = cursor.fetchone()[0]

                    # 查询该题目的正确率
                    query_correct_rate = """
                        SELECT 
                            CAST(SUM(CASE WHEN score >= 1 THEN 1 ELSE 0 END) AS FLOAT) / 
                            CAST(COUNT(*) AS FLOAT) * 100
                        FROM ExamResult
                        WHERE question_id = ?
                    """
                    cursor.execute(query_correct_rate, (question_id,))
                    correct_rate = cursor.fetchone()[0]

                    # 处理 None 值
                    correct_rate = correct_rate if correct_rate is not None else 0.0

                    # 输出题目及其统计信息
                    print(
                        f"题目ID: {question_id}, 知识点: {knowledge_point}, 类型: {question_type}, 内容: {question_text}")
                    print(f"  被组卷次数: {paper_count} 次")
                    print(f"  被考试次数: {exam_count} 次")
                    print(f"  正确率: {correct_rate:.2f}%")
            else:
                print(f"题库 ID {bank_id} 中没有题目。")
        else:
            print("无法连接到数据库，无法查看题目。")
    except Exception as e:
        print("Error:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def view_question_banks():
    """查看题库及其详细信息"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            # 获取所有题库
            query = "SELECT * FROM QuestionBank"
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                print(f"当前共有 {len(rows)} 个题库：")
                for row in rows:
                    print(f"题库 ID: {row[0]}, 课程 ID: {row[1]}, 题库名称: {row[2]}")

                # 选择题库查看详细信息
                bank_id = input("请输入需要查看的题库 ID（输入 'q' 返回主菜单）: ")
                if bank_id.lower() == 'q':
                    return
                if bank_id.isdigit():
                    bank_id = int(bank_id)
                    view_questions(bank_id)
                else:
                    print("无效输入，返回主菜单。")
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
        print("\n题库管理系统")
        print("1. 添加题库")
        print("2. 删除题库")
        print("3. 修改题库信息")
        print("4. 查看题库及题目")
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
