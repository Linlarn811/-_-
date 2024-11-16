# 胡雅兰
import pyodbc
from connect_database import connect_to_database


# 生成证书
def generate_certificate(student_id):
    connection = connect_to_database()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        # 查询学生的所有考试成绩
        query = """
            SELECT e.exam_id, er.score
            FROM ExamResult er
            JOIN Exam e ON er.exam_id = e.exam_id
            WHERE er.student_id = ?
        """
        cursor.execute(query, (student_id,))
        exam_results = cursor.fetchall()

        if not exam_results:
            print(f"学生 {student_id} 没有考试成绩。")
            return

        # 计算总成绩
        total_score = sum([score for _, score in exam_results])
        print(f"学生 {student_id} 的总成绩为: {total_score} 分")

        # 根据总成绩生成证书
        certificate_type = "毕业证书" if total_score >= 60 else "结业证书"

        # 更新学生进度记录，保存证书
        query = """
            UPDATE StudentProgress
            SET certificate = ?, total_credits = ?
            WHERE student_id = ?
        """
        cursor.execute(query, (certificate_type, total_score, student_id))
        connection.commit()

        print(f"生成的证书类型为: {certificate_type}")
    except pyodbc.Error as e:
        print("生成证书时出错:", e)
    finally:
        cursor.close()
        connection.close()


# 导出学员学习情况
def export_student_progress():
    connection = connect_to_database()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        # 查询所有学生的学习记录（课程、考试、证书）
        query = """
            SELECT s.student_id, s.student_name, sp.total_credits, sp.certificate, e.exam_name, er.score
            FROM Student s
            JOIN StudentProgress sp ON s.student_id = sp.student_id
            LEFT JOIN ExamResult er ON s.student_id = er.student_id
            LEFT JOIN Exam e ON er.exam_id = e.exam_id
        """
        cursor.execute(query)
        student_records = cursor.fetchall()

        if not student_records:
            print("没有学生学习记录。")
            return

        # 输出所有学生的学习情况
        print("----- 学员学习情况 -----")
        for record in student_records:
            student_id, student_name, total_credits, certificate, exam_name, score = record
            print(f"学生ID: {student_id}, 学生姓名: {student_name}, 总学分: {total_credits}, "
                  f"证书: {certificate}, 考试: {exam_name}, 得分: {score}")
    except pyodbc.Error as e:
        print("导出学习情况时出错:", e)
    finally:
        cursor.close()
        connection.close()


# 更新学生学习进度和证书
def update_student_progress(student_id, total_credits, certificate):
    connection = connect_to_database()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        # 更新学生的学习进度和证书
        query = """
            UPDATE StudentProgress
            SET total_credits = ?, certificate = ?
            WHERE student_id = ?
        """
        cursor.execute(query, (total_credits, certificate, student_id))
        connection.commit()
        print(f"学生 {student_id} 的学习进度已更新，证书为: {certificate}")
    except pyodbc.Error as e:
        print("更新学习进度时出错:", e)
    finally:
        cursor.close()
        connection.close()


# 主程序
def main():
    print("----- 存档管理模块 -----")
    print("1. 生成学生证书")
    print("2. 导出学员学习情况")
    print("3. 存档管理")
    print("4. 退出")

    while True:
        choice = input("请选择操作（1-4）：")

        if choice == '1':
            student_id = int(input("请输入学生ID："))
            generate_certificate(student_id)

        elif choice == '2':
            export_student_progress()

        elif choice == '3':
            student_id = int(input("请输入学生ID："))
            total_credits = int(input("请输入总学分："))
            certificate = input("请输入证书类型：")
            update_student_progress(student_id, total_credits, certificate)

        elif choice == '4':
            print("退出")
            break
        else:
            print("无效的选择，请重新输入。")

if __name__ == "__main__":
    main()
