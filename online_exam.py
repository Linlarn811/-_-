import pyodbc
from datetime import datetime, timedelta
from connect_database import connect_to_database


# 发布考试
def publish_exam(instance_id, paper_id, exam_name, start_time, duration):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            # 检查课程实例ID是否有效
            query = "SELECT instance_id FROM CourseInstance WHERE instance_id = ?"
            cursor.execute(query, (instance_id,))
            existing_instance_id = cursor.fetchone()

            if existing_instance_id:
                # 课程实例ID有效，计算考试的结束时间
                end_time = start_time + timedelta(minutes=duration)

                # 插入考试记录
                query = """INSERT INTO Exam (instance_id, paper_id, exam_name, exam_date, duration) 
                           VALUES (?, ?, ?, ?, ?)"""
                cursor.execute(query, (instance_id, paper_id, exam_name, start_time, duration))
                connection.commit()  # 确保提交事务
                print("考试发布成功！")
            else:
                print(f"课程实例ID {instance_id} 不存在，请检查！")
    except Exception as e:
        print("发布考试出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

def view_exam_status():
    connection = connect_to_database()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        # 查询所有考试信息及对应的课程和课程实例信息
        query = """SELECT e.exam_id, e.exam_name, e.exam_date, e.duration, e.passing_score, e.paper_id, 
                          ci.course_id, ci.instance_id, c.course_name
                   FROM Exam e
                   JOIN CourseInstance ci ON e.instance_id = ci.instance_id
                   JOIN Course c ON ci.course_id = c.course_id"""
        cursor.execute(query)
        exams = cursor.fetchall()

        if exams:
            print("----- 当前考试列表 -----")
            for exam in exams:
                exam_id, exam_name, exam_date, duration, passing_score, paper_id, instance_id, course_id, course_name = exam
                print(
                    f"考试ID: {exam_id}, 考试名称: {exam_name}, 考试时间: {exam_date}, "
                    f"考试时长: {duration}分钟, 及格分数: {passing_score}, 试卷ID: {paper_id}, "
                    f"课程ID: {instance_id}, 课程名称: {course_name}, 课程实例ID: {course_id}")
        else:
            print("当前没有发布的考试。")
    except pyodbc.Error as e:
        print("查询考试状态时出错:", e)
    finally:
        cursor.close()
        connection.close()


def student_answer(exam_id, student_id, answers):
    connection = connect_to_database()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        # 查询试卷ID
        query = """SELECT e.paper_id
                   FROM Exam e
                   WHERE e.exam_id = ?"""
        cursor.execute(query, (exam_id,))
        paper_id = cursor.fetchone()

        if paper_id:
            paper_id = paper_id[0]

            # 查询与试卷ID对应的所有题目的 question_id 和 question_score
            query = """SELECT epq.question_id, epq.question_score
                       FROM ExamPaperQuestion epq
                       WHERE epq.paper_id = ?"""
            cursor.execute(query, (paper_id,))
            question_data = cursor.fetchall()

            if question_data:
                print("----- 试卷题目 -----")
                for idx, (question_id, question_score) in enumerate(question_data, 1):
                    print(f"正在查询题目 {idx}, question_id: {question_id}")

                    # 查询每道题的详细内容
                    query = """SELECT q.question_text, q.option_a, q.option_b, q.option_c, q.option_d, q.correct_answer
                               FROM Question q
                               WHERE q.question_id = ?"""
                    cursor.execute(query, (question_id,))
                    question = cursor.fetchone()

                    if question:
                        question_text, option_a, option_b, option_c, option_d, correct_answer = question
                        print(f"题目 {idx}: {question_text}")

                        # 判断题目类型并处理显示选项
                        if option_a or option_b or option_c or option_d:  # 单选或多选
                            print(f"A: {option_a}")
                            print(f"B: {option_b}")
                            print(f"C: {option_c}")
                            print(f"D: {option_d}")
                        elif option_a == "正确" and option_b == "错误":  # 判断题
                            print("A: 正确")
                            print("B: 错误")
                        else:  # 填空题无需选项
                            print("此题为填空题。")

                        # 学生回答问题
                        while True:
                            if option_a or option_b or option_c or option_d:  # 单选/多选
                                answer = input(f"请输入第 {idx} 题的答案（A/B/C/D）：")
                                if answer.strip().upper() in ['A', 'B', 'C', 'D']:
                                    answers[question_id] = answer.upper()
                                    # 比较学生答案与正确答案并计算分数
                                    score = 0  # 默认分数为 0
                                    if correct_answer and correct_answer.upper() == answers[question_id].upper():
                                        score = question_score  # 答对得分
                                    break
                                else:
                                    print("无效的答案，请输入 A、B、C 或 D。")
                            elif option_a == "正确" and option_b == "错误":  # 判断题
                                answer = input(f"请输入第 {idx} 题的答案（A/正确 或 B/错误）：")
                                if answer.strip().upper() in ['A', 'B']:
                                    answers[question_id] = answer.upper()
                                    # 比较学生答案与正确答案并计算分数
                                    score = 0  # 默认分数为 0
                                    if correct_answer and correct_answer.upper() == answers[question_id].upper():
                                        score = question_score  # 答对得分
                                    break
                                else:
                                    print("无效的答案，请输入 A/正确 或 B/错误。")
                            else:  # 填空题
                                answer = input(f"请输入第 {idx} 题的答案：")
                                answers[question_id] = answer.strip()
                                break


                        # 插入答题结果
                        cursor.execute("""
                            INSERT INTO ExamResult (exam_id, student_id, question_id, student_answer, score, exam_date)
                            VALUES (?, ?, ?, ?, ?, GETDATE())
                        """, (exam_id, student_id, question_id, answers[question_id], score))
                        print(f"已保存题目 {idx} 的答题结果。")
            else:
                print("未找到试卷中的题目。")
        else:
            print("未找到对应的试卷ID。")

        connection.commit()
        print(f"学生 {student_id} 的所有答题结果已提交。")
    except pyodbc.Error as e:
        print("答题结果提交时出错:", e)
    finally:
        cursor.close()
        connection.close()



# 主程序入口
def main():
    print("----- 在线考试模块 -----")
    print("1. 发布在线考试")
    print("2. 查看考试状态")
    print("3. 学生答题")
    print("4. 退出")

    while True:
        choice = input("请选择操作（1-4）：")

        if choice == '1':
            course_instance_id = input("课程实例ID：")
            exam_paper_id = input("试卷ID：")
            exam_name = input("考试名称：")
            start_time = input("开始时间（格式：YYYY-MM-DD HH:MM:SS）：")
            duration = int(input("考试时长（分钟）："))

            try:
                # 转换时间格式
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

                # 调用发布考试函数
                publish_exam(course_instance_id, exam_paper_id, exam_name, start_time, duration)

            except ValueError:
                print("时间格式不正确，请重新输入。")

        elif choice == '2':
            # 查看考试状态
            view_exam_status()

        elif choice == '3':
            # 学生答题
            try:
                exam_id = int(input("请输入考试ID："))
                student_id = int(input("请输入学生ID："))

                # 假设题目答案是字典，键为题目ID，值为学生的答案
                answers = {}
                student_answer(exam_id, student_id, answers)
            except ValueError:
                print("无效的输入，请确保考试ID和学生ID为数字。")

        elif choice == '4':
            print("退出")
            break
        else:
            print("无效的选择，请重新输入。")


if __name__ == "__main__":
    main()
