from connect_database import connect_to_database

def validate_bank_id(bank_id):
    """验证题库 ID 是否存在"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            query = "SELECT bank_id FROM QuestionBank WHERE bank_id = ?"
            cursor.execute(query, (bank_id,))
            result = cursor.fetchone()
            return result is not None
        else:
            print("无法连接到数据库。")
            return False
    except Exception as e:
        print("验证题库 ID 出错:", e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_question_inputs():
    """获取题目基本信息"""
    knowledge_point = input("请输入知识点: ")
    question_text = input("请输入题目内容: ")
    question_type = input("请输入题目类型 (单选/多选/判断/填空): ").strip()
    option_a = option_b = option_c = option_d = correct_answer = None

    if question_type == "单选":
        option_a = input("请输入选项A: ")
        option_b = input("请输入选项B: ")
        option_c = input("请输入选项C: ")
        option_d = input("请输入选项D: ")
        correct_answer = input("请输入正确答案 (A/B/C/D): ").strip().upper()
        if correct_answer not in {"A", "B", "C", "D"}:
            print("错误：单选题正确答案必须为 A/B/C/D 中的一个。")
            return None
    elif question_type == "多选":
        option_a = input("请输入选项A: ")
        option_b = input("请输入选项B: ")
        option_c = input("请输入选项C: ")
        option_d = input("请输入选项D: ")
        correct_answer = input("请输入正确答案 (A/B/C/D 中的多个字符): ").strip().upper()
        if not set(correct_answer).issubset({"A", "B", "C", "D"}):
            print("错误：多选题正确答案必须为 A/B/C/D 中的一个或多个字符。")
            return None
    elif question_type == "判断":
        option_a = "正确"
        option_b = "错误"
        correct_answer = input("请输入正确答案 (A/正确 或 B/错误): ").strip().upper()
        if correct_answer not in {"A", "B"}:
            print("错误：判断题正确答案必须为 A 或 B。")
            return None
    elif question_type == "填空":
        correct_answer = input("请输入正确答案: ")
    else:
        print("错误：题目类型无效，请输入 单选/多选/判断/填空 中的一种。")
        return None

    return knowledge_point, question_type, question_text, option_a, option_b, option_c, option_d, correct_answer

def add_question(bank_id):
    """添加题目"""
    if not validate_bank_id(bank_id):
        print(f"题库 ID {bank_id} 不存在，无法添加题目。")
        return

    question_data = get_question_inputs()
    if not question_data:
        return

    knowledge_point, question_type, question_text, option_a, option_b, option_c, option_d, correct_answer = question_data
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            query = """INSERT INTO Question (bank_id, knowledge_point, question_type, question_text, 
                       option_a, option_b, option_c, option_d, correct_answer)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, (bank_id, knowledge_point, question_type, question_text,
                                   option_a, option_b, option_c, option_d, correct_answer))
            connection.commit()
            print("题目添加成功。")
        else:
            print("无法连接到数据库，添加题目失败。")
    except Exception as e:
        print("添加题目出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

def delete_question(question_id, bank_id):
    """删除题目"""
    if not validate_bank_id(bank_id):
        print(f"题库 ID {bank_id} 不存在，无法删除题目。")
        return

    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            query = "DELETE FROM Question WHERE question_id = ? AND bank_id = ?"
            cursor.execute(query, (question_id, bank_id))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"题目 ID {question_id} 删除成功。")
            else:
                print(f"题目 ID {question_id} 不属于题库 ID {bank_id}。")
        else:
            print("无法连接到数据库，删除题目失败。")
    except Exception as e:
        print("删除题目出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

def update_question(question_id, bank_id):
    """更新题目"""
    # 检查题库是否存在
    if not validate_bank_id(bank_id):
        print(f"题库 ID {bank_id} 不存在，无法修改题目。")
        return

    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # 检查题目是否属于该题库
            query = "SELECT * FROM Question WHERE question_id = ? AND bank_id = ?"
            cursor.execute(query, (question_id, bank_id))
            row = cursor.fetchone()
            if not row:
                print(f"题目 ID {question_id} 不属于题库 ID {bank_id} 或不存在。")
                return

            print(f"当前题目信息：知识点: {row[2]}, 类型: {row[3]}, 内容: {row[4]}")
            print("请输入新的题目信息（按回车跳过不修改的字段）")

            # 获取新的题目信息
            knowledge_point = input(f"知识点 [{row[2]}]: ").strip() or row[2]
            question_type = input(f"题目类型 [{row[3]}]: ").strip() or row[3]
            question_text = input(f"题目内容 [{row[4]}]: ").strip() or row[4]

            option_a = option_b = option_c = option_d = correct_answer = None

            if question_type == "单选":
                option_a = input(f"选项A [{row[5]}]: ").strip() or row[5]
                option_b = input(f"选项B [{row[6]}]: ").strip() or row[6]
                option_c = input(f"选项C [{row[7]}]: ").strip() or row[7]
                option_d = input(f"选项D [{row[8]}]: ").strip() or row[8]
                correct_answer = input(f"正确答案 [{row[9]}]: ").strip().upper() or row[9]
                if correct_answer not in {"A", "B", "C", "D"}:
                    print("错误：单选题正确答案必须为 A/B/C/D 中的一个。")
                    return
            elif question_type == "多选":
                option_a = input(f"选项A [{row[5]}]: ").strip() or row[5]
                option_b = input(f"选项B [{row[6]}]: ").strip() or row[6]
                option_c = input(f"选项C [{row[7]}]: ").strip() or row[7]
                option_d = input(f"选项D [{row[8]}]: ").strip() or row[8]
                correct_answer = input(f"正确答案 [{row[9]}]: ").strip().upper() or row[9]
                if not set(correct_answer).issubset({"A", "B", "C", "D"}):
                    print("错误：多选题正确答案必须为 A/B/C/D 中的一个或多个字符。")
                    return
            elif question_type == "判断":
                option_a = "正确"
                option_b = "错误"
                correct_answer = input(f"正确答案 [{row[9]}] (A/正确 或 B/错误): ").strip().upper() or row[9]
                if correct_answer not in {"A", "B"}:
                    print("错误：判断题正确答案必须为 A 或 B。")
                    return
            elif question_type == "填空":
                correct_answer = input(f"正确答案 [{row[9]}]: ").strip() or row[9]
            else:
                print("错误：题目类型无效，请输入 单选/多选/判断/填空 中的一种。")
                return

            # 更新题目信息
            update_query = """UPDATE Question
                              SET knowledge_point = ?, question_type = ?, question_text = ?, 
                                  option_a = ?, option_b = ?, option_c = ?, option_d = ?, correct_answer = ?
                              WHERE question_id = ? AND bank_id = ?"""
            cursor.execute(update_query, (knowledge_point, question_type, question_text,
                                          option_a, option_b, option_c, option_d, correct_answer,
                                          question_id, bank_id))
            connection.commit()
            print(f"题目 ID {question_id} 信息更新成功。")
        else:
            print("无法连接到数据库，更新题目信息失败。")
    except Exception as e:
        print("修改题目出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

def view_questions(bank_id):
    """查看题目及其统计信息"""
    if not validate_bank_id(bank_id):
        print(f"题库 ID {bank_id} 不存在，无法查看题目。")
        return

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

                    # 输出题目及其统计信息
                    print(f"题目ID: {question_id}, 知识点: {knowledge_point}, 类型: {question_type}, 内容: {question_text}")
                    print(f"  被组卷次数: {paper_count} 次")

            else:
                print(f"题库 ID {bank_id} 中没有题目。")
        else:
            print("无法连接到数据库，无法查看题目。")
    except Exception as e:
        print("查看题目出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def question_management():
    """题目管理主程序"""
    while True:
        print("\n题目管理系统")
        print("1. 添加题目")
        print("2. 删除题目")
        print("3. 修改题目信息")
        print("4. 查看题目")
        print("5. 返回上级菜单")
        choice = input("请输入选项 (1/2/3/4/5): ")

        if choice == "1":
            bank_id = int(input("请输入题库ID: "))
            add_question(bank_id)
        elif choice == "2":
            bank_id = int(input("请输入题库ID: "))
            question_id = int(input("请输入题目ID: "))

            delete_question(question_id, bank_id)
        elif choice == "3":
            bank_id = int(input("请输入题库ID: "))
            question_id = int(input("请输入题目ID: "))
            update_question(question_id, bank_id)
        elif choice == "4":
            bank_id = int(input("请输入题库ID: "))
            view_questions(bank_id)
        elif choice == "5":
            break
        else:
            print("无效选项，请重新输入。")

if __name__ == "__main__":
    question_management()
