from connect_database import connect_to_database
import pyodbc

# 管理考试信息：创建考试试卷
def create_exam_paper(course_id, paper_name, total_score=100):
    """创建考试试卷并关联课程"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            # 插入新的试卷信息
            query = "INSERT INTO ExamPaper (course_id, paper_name, total_score) VALUES (?, ?, ?)"
            cursor.execute(query, (course_id, paper_name, total_score))
            connection.commit()
            print("考试试卷创建成功！")
    except Exception as e:
        print("创建考试试卷出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()


# 设置试卷题目
def set_exam_paper_question(paper_id, question_id, score):
    """将题目添加到试卷中"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            # 插入试卷题目记录
            query = "INSERT INTO ExamPaperQuestion (paper_id, question_id, question_score) VALUES (?, ?, ?)"
            cursor.execute(query, (paper_id, question_id, score))
            connection.commit()
            print(f"题目 {question_id} 已添加到试卷 {paper_id}，得分 {score}")
    except Exception as e:
        print("添加试卷题目出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()


# 设置试卷题目及分数
def set_exam_paper_questions(paper_id, num_questions, num_questions_bank, total_score, random_choice=False):
    """设置试卷题目及分数"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # 获取当前试卷已存在的题目及总分
            query = "SELECT question_id, question_score FROM ExamPaperQuestion WHERE paper_id = ?"
            cursor.execute(query, (paper_id,))
            existing_questions = {row[0]: row[1] for row in cursor.fetchall()}
            current_score = sum(existing_questions.values())

            if random_choice:
                # 随机从题库选择题目
                query = f"SELECT question_id FROM Question WHERE bank_id = {num_questions_bank} ORDER BY NEWID()"
                cursor.execute(query)
                question_ids = [row[0] for row in cursor.fetchall() if row[0] not in existing_questions]

                for question_id in question_ids[:num_questions]:
                    if current_score >= total_score:
                        print("试卷已满分，无法继续添加题目！")
                        break
                    question_score = float(input(f"请输入题目 {question_id} 的得分（剩余满分：{total_score - current_score}）："))
                    if question_score <= 0 or current_score + question_score > total_score:
                        print("分数输入无效，跳过此题！")
                        continue
                    set_exam_paper_question(paper_id, question_id, question_score)
                    current_score += question_score
            else:
                # 手动选择题目并设置分数
                while current_score < total_score:
                    print(f"当前试卷得分总计: {current_score}/{total_score}")
                    question_id = int(input(f"请输入题目ID（剩余满分: {total_score - current_score}）："))
                    if question_id in existing_questions:
                        print(f"题目 {question_id} 已存在于试卷中，无法重复添加！")
                        continue
                    question_score = float(input("请输入该题分数："))
                    if question_score <= 0 or current_score + question_score > total_score:
                        print(f"分数输入无效！请确保输入的分数为正数，且总分不超过满分 {total_score}。")
                        continue

                    # 添加题目到试卷
                    set_exam_paper_question(paper_id, question_id, question_score)
                    current_score += question_score

                    if current_score < total_score:
                        continue_choice = input("试卷尚未满分，是否继续添加题目？（y/n）：")
                        if continue_choice.lower() != 'y':
                            break
    except Exception as e:
        print("设置试卷题目出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

def view_student_exam_history(student_id):
    """查看学生的考试历史"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # 查询学生的考试记录及试卷总成绩
            query = """SELECT 
                        er.exam_id,  -- 学生参加的考试ID
                        SUM(COALESCE(epq.question_score, 0)) AS total_score,  -- 试卷总得分，使用COALESCE确保NULL值转为0
                        SUM(COALESCE(er.score, 0)) AS student_score  -- 学生得分，使用COALESCE确保NULL值转为0
                    FROM ExamResult er
                    JOIN ExamPaperQuestion epq 
                        ON er.question_id = epq.question_id  -- 连接条件，确认正确连接
                    WHERE er.student_id = ?  -- 根据学生ID过滤
                    GROUP BY er.exam_id  -- 按考试ID分组
            """

            # 执行查询，传递 student_id 作为参数
            cursor.execute(query, (student_id,))

            # 获取查询结果
            results = cursor.fetchall()
            for result in results:
                print(f"考试ID: {result[0]}, 试卷总分: {result[1]}, 学生得分: {result[2]}")

            cursor.close()
            connection.close()
    except pyodbc.Error as e:
        print("数据库操作时出错:", e)


def view_class_average_score(course_id):
    """查看班级考试平均成绩"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # 查询每个学生的总得分
            query = """
                SELECT AVG(student_total_score)  -- 计算班级的平均总得分
                FROM (
                    SELECT er.student_id, SUM(er.score) AS student_total_score  -- 计算每个学生的总得分
                    FROM ExamResult er
                    JOIN ExamPaperQuestion epq ON er.exam_id = epq.exam_id  -- 根据试卷ID连接
                    JOIN ExamPaper ep ON epq.paper_id = ep.paper_id  -- 根据试卷ID连接试卷表
                    WHERE ep.course_id = ?  -- 根据课程ID过滤
                    GROUP BY er.student_id  -- 按学生分组
                ) AS student_scores
            """
            cursor.execute(query, (course_id,))

            # 获取查询结果
            average_score = cursor.fetchone()[0]

            # 输出班级平均成绩
            if average_score is not None:
                print(f"课程 {course_id} 的班级平均成绩为: {average_score:.2f}")
            else:
                print(f"课程 {course_id} 没有学生成绩。")

    except Exception as e:
        print("查看班级平均成绩出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()


# 查看所有历史生成的试卷及对应题目
def view_all_exam_papers():
    """查看所有历史生成的试卷，并查询每个试卷的题目"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            query = "SELECT paper_id, paper_name, course_id, total_score FROM ExamPaper"
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                print("所有历史生成的试卷：")
                for row in rows:
                    paper_id, paper_name, course_id, total_score = row
                    print(f"试卷ID: {paper_id}, 试卷名称: {paper_name}, 课程ID: {course_id}, 总分: {total_score}")

                    query_questions = """SELECT q.question_text, epq.question_score
                                         FROM ExamPaperQuestion epq
                                         JOIN Question q ON epq.question_id = q.question_id
                                         WHERE epq.paper_id = ?"""
                    cursor.execute(query_questions, (paper_id,))
                    question_rows = cursor.fetchall()

                    if question_rows:
                        print("  试卷题目：")
                        for idx, (question_text, question_score) in enumerate(question_rows, 1):
                            print(f"    题目 {idx}: {question_text} (分数: {question_score})")
                    else:
                        print("  此试卷没有设置题目。")
            else:
                print("没有历史生成的试卷记录。")
    except Exception as e:
        print("查看试卷记录出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

# 删除试卷中的某个题目
def delete_question_from_paper(paper_id, question_id):
    """从指定试卷中删除题目"""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            # 检查题目是否存在于试卷中
            check_query = "SELECT * FROM ExamPaperQuestion WHERE paper_id = ? AND question_id = ?"
            cursor.execute(check_query, (paper_id, question_id))
            if not cursor.fetchone():
                print(f"题目 {question_id} 不在试卷 {paper_id} 中！")
                return

            # 删除指定题目
            delete_query = "DELETE FROM ExamPaperQuestion WHERE paper_id = ? AND question_id = ?"
            cursor.execute(delete_query, (paper_id, question_id))
            connection.commit()
            print(f"题目 {question_id} 已从试卷 {paper_id} 中删除！")
    except Exception as e:
        print("删除试卷题目出错:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

# 主程序测试：交互式界面
def main():
    while True:
        print("\n----- 考试管理模块 -----")
        print("1. 创建考试试卷")
        print("2. 设置试卷题目")
        print("3. 查看学生考试历史")
        print("4. 查看班级平均成绩")
        print("5. 查看所有历史生成的试卷")
        print("6. 删除试卷中的某个题目")  # 新增模块
        print("7. 退出")

        choice = input("请选择操作（1-7）：")


        if choice == '1':
            course_id = input("请输入课程ID：")
            paper_name = input("请输入试卷名称：")
            total_score = input("请输入总分（默认为100）：")
            total_score = int(total_score) if total_score else 100
            create_exam_paper(course_id, paper_name, total_score)

        elif choice == '2':
            try:
                paper_id = input("请输入试卷ID：")
                num_questions = int(input("请输入试卷题目数量: "))
                num_questions_bank = int(input("请输入选择的题库ID: "))
                connection = connect_to_database()
                if connection:
                    cursor = connection.cursor()
                    query = "SELECT total_score FROM ExamPaper WHERE paper_id = ?"
                    cursor.execute(query, (paper_id,))
                    result = cursor.fetchone()
                    if not result:
                        print("试卷ID不存在，请检查后重试！")
                        continue
                    total_score = result[0]
                else:
                    print("数据库连接失败，请稍后再试！")
                    continue

                if num_questions <= 0:
                    raise ValueError

                random_choice = input("是否随机组卷（y/n）: ")
                if random_choice.lower() == 'y':
                    set_exam_paper_questions(paper_id, num_questions, num_questions_bank, total_score, random_choice=True)
                else:
                    set_exam_paper_questions(paper_id, num_questions, num_questions_bank, total_score, random_choice=False)
            except ValueError:
                print("输入无效，数量必须是正整数！")
            except Exception as e:
                print("组卷过程中出现错误：", e)

        elif choice == '3':
            student_id = input("请输入学生ID：")
            view_student_exam_history(student_id)

        elif choice == '4':
            course_id = input("请输入课程ID：")
            view_class_average_score(course_id)

        elif choice == '5':
            view_all_exam_papers()


        elif choice == '7':
            print("退出程序！")
            break

        elif choice == '6':  # 新增选项
            paper_id = input("请输入试卷ID：")
            question_id = input("请输入要删除的题目ID：")
            delete_question_from_paper(paper_id, question_id)

        else:
            print("无效选择，请重新输入！")


if __name__ == "__main__":
    main()
