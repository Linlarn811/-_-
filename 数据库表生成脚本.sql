USE [在线教学系统]
GO
/****** Object:  Table [dbo].[Class]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Class](
	[class_id] [int] NOT NULL,
	[class_name] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[class_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ClassCourseInstance]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ClassCourseInstance](
	[class_id] [int] NOT NULL,
	[instance_id] [int] NOT NULL,
	[enrollment_date] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[class_id] ASC,
	[instance_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Course]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Course](
	[course_id] [int] IDENTITY(1,1) NOT NULL,
	[course_name] [nvarchar](255) NOT NULL,
	[description] [nvarchar](max) NULL,
	[organization] [nvarchar](255) NULL,
	[category] [nvarchar](100) NULL,
	[course_type] [nvarchar](20) NULL,
	[credits] [int] NULL,
	[cost] [decimal](10, 2) NULL,
	[total_duration] [int] NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[course_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CourseChapter]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CourseChapter](
	[chapter_id] [int] IDENTITY(1,1) NOT NULL,
	[course_id] [int] NOT NULL,
	[chapter_title] [nvarchar](255) NOT NULL,
	[description] [nvarchar](max) NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[chapter_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CourseInstance]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CourseInstance](
	[instance_id] [int] IDENTITY(1,1) NOT NULL,
	[course_id] [int] NOT NULL,
	[teacher_id] [int] NULL,
	[start_date] [date] NOT NULL,
	[end_date] [date] NOT NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
	[exam_id] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[instance_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [UQ_exam_id] UNIQUE NONCLUSTERED 
(
	[exam_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CourseMaterial]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CourseMaterial](
	[material_id] [int] IDENTITY(1,1) NOT NULL,
	[chapter_id] [int] NOT NULL,
	[material_name] [nvarchar](255) NOT NULL,
	[description] [nvarchar](max) NULL,
	[upload_date] [datetime] NULL,
	[uploader_id] [int] NULL,
	[is_visible] [bit] NULL,
	[file_path] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[material_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CourseTag]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CourseTag](
	[course_id] [int] NOT NULL,
	[tag_id] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[course_id] ASC,
	[tag_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Exam]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Exam](
	[exam_id] [int] IDENTITY(1,1) NOT NULL,
	[instance_id] [int] NOT NULL,
	[paper_id] [int] NOT NULL,
	[exam_name] [nvarchar](255) NOT NULL,
	[exam_date] [datetime] NOT NULL,
	[duration] [int] NOT NULL,
	[passing_score] [int] NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[exam_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[instance_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ExamPaper]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ExamPaper](
	[paper_id] [int] IDENTITY(1,1) NOT NULL,
	[course_id] [int] NOT NULL,
	[paper_name] [nvarchar](255) NOT NULL,
	[total_score] [int] NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[paper_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ExamPaperQuestion]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ExamPaperQuestion](
	[paper_id] [int] NOT NULL,
	[question_id] [int] NOT NULL,
	[question_score] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[paper_id] ASC,
	[question_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ExamResult]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ExamResult](
	[result_id] [int] IDENTITY(1,1) NOT NULL,
	[exam_id] [int] NOT NULL,
	[student_id] [int] NOT NULL,
	[score] [int] NOT NULL,
	[exam_date] [datetime] NULL,
	[progress_id] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[result_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[exam_id] ASC,
	[student_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Question]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Question](
	[question_id] [int] IDENTITY(1,1) NOT NULL,
	[bank_id] [int] NOT NULL,
	[knowledge_point] [nvarchar](255) NULL,
	[question_type] [nvarchar](20) NULL,
	[question_text] [nvarchar](max) NOT NULL,
	[option_a] [nvarchar](255) NULL,
	[option_b] [nvarchar](255) NULL,
	[option_c] [nvarchar](255) NULL,
	[option_d] [nvarchar](255) NULL,
	[correct_answer] [nvarchar](255) NULL,
	[usage_count] [int] NULL,
	[exam_count] [int] NULL,
	[correct_rate] [decimal](5, 2) NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[question_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[QuestionBank]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[QuestionBank](
	[bank_id] [int] IDENTITY(1,1) NOT NULL,
	[course_id] [int] NOT NULL,
	[bank_name] [nvarchar](255) NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[bank_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Student]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Student](
	[student_id] [int] NOT NULL,
	[student_name] [varchar](255) NOT NULL,
	[class_id] [int] NULL,
 CONSTRAINT [PK_Student] PRIMARY KEY CLUSTERED 
(
	[student_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[StudentProgress]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[StudentProgress](
	[progress_id] [int] IDENTITY(1,1) NOT NULL,
	[student_id] [int] NOT NULL,
	[total_credits] [int] NULL,
	[certificate] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[progress_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[student_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tag]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tag](
	[tag_id] [int] IDENTITY(1,1) NOT NULL,
	[tag_name] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[tag_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[tag_name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Teacher]    Script Date: 2024-11-05 21:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Teacher](
	[teacher_id] [int] IDENTITY(1,1) NOT NULL,
	[teacher_name] [nvarchar](255) NOT NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[teacher_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[ClassCourseInstance] ADD  DEFAULT (getdate()) FOR [enrollment_date]
GO
ALTER TABLE [dbo].[Course] ADD  DEFAULT ((0)) FOR [credits]
GO
ALTER TABLE [dbo].[Course] ADD  DEFAULT ((0.0)) FOR [cost]
GO
ALTER TABLE [dbo].[Course] ADD  DEFAULT ((0)) FOR [total_duration]
GO
ALTER TABLE [dbo].[Course] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Course] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[CourseChapter] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[CourseChapter] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[CourseInstance] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[CourseInstance] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[CourseMaterial] ADD  DEFAULT (getdate()) FOR [upload_date]
GO
ALTER TABLE [dbo].[CourseMaterial] ADD  DEFAULT ((1)) FOR [is_visible]
GO
ALTER TABLE [dbo].[Exam] ADD  DEFAULT ((60)) FOR [passing_score]
GO
ALTER TABLE [dbo].[Exam] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Exam] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[ExamPaper] ADD  DEFAULT ((100)) FOR [total_score]
GO
ALTER TABLE [dbo].[ExamPaper] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[ExamPaper] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[ExamResult] ADD  DEFAULT (getdate()) FOR [exam_date]
GO
ALTER TABLE [dbo].[Question] ADD  DEFAULT ((0)) FOR [usage_count]
GO
ALTER TABLE [dbo].[Question] ADD  DEFAULT ((0)) FOR [exam_count]
GO
ALTER TABLE [dbo].[Question] ADD  DEFAULT ((0.0)) FOR [correct_rate]
GO
ALTER TABLE [dbo].[Question] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Question] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[QuestionBank] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[QuestionBank] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[StudentProgress] ADD  DEFAULT ((0)) FOR [total_credits]
GO
ALTER TABLE [dbo].[Teacher] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Teacher] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[ClassCourseInstance]  WITH CHECK ADD FOREIGN KEY([class_id])
REFERENCES [dbo].[Class] ([class_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[ClassCourseInstance]  WITH CHECK ADD FOREIGN KEY([instance_id])
REFERENCES [dbo].[CourseInstance] ([instance_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[CourseChapter]  WITH CHECK ADD FOREIGN KEY([course_id])
REFERENCES [dbo].[Course] ([course_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[CourseInstance]  WITH CHECK ADD FOREIGN KEY([course_id])
REFERENCES [dbo].[Course] ([course_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[CourseInstance]  WITH CHECK ADD FOREIGN KEY([teacher_id])
REFERENCES [dbo].[Teacher] ([teacher_id])
ON DELETE SET NULL
GO
ALTER TABLE [dbo].[CourseInstance]  WITH CHECK ADD  CONSTRAINT [FK_CourseInstance_Exam] FOREIGN KEY([exam_id])
REFERENCES [dbo].[Exam] ([exam_id])
GO
ALTER TABLE [dbo].[CourseInstance] CHECK CONSTRAINT [FK_CourseInstance_Exam]
GO
ALTER TABLE [dbo].[CourseMaterial]  WITH CHECK ADD FOREIGN KEY([chapter_id])
REFERENCES [dbo].[CourseChapter] ([chapter_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[CourseTag]  WITH CHECK ADD FOREIGN KEY([course_id])
REFERENCES [dbo].[Course] ([course_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[CourseTag]  WITH CHECK ADD FOREIGN KEY([tag_id])
REFERENCES [dbo].[Tag] ([tag_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Exam]  WITH CHECK ADD FOREIGN KEY([instance_id])
REFERENCES [dbo].[CourseInstance] ([instance_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Exam]  WITH CHECK ADD FOREIGN KEY([paper_id])
REFERENCES [dbo].[ExamPaper] ([paper_id])
GO
ALTER TABLE [dbo].[ExamPaper]  WITH CHECK ADD FOREIGN KEY([course_id])
REFERENCES [dbo].[Course] ([course_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[ExamPaperQuestion]  WITH CHECK ADD FOREIGN KEY([paper_id])
REFERENCES [dbo].[ExamPaper] ([paper_id])
GO
ALTER TABLE [dbo].[ExamPaperQuestion]  WITH CHECK ADD FOREIGN KEY([question_id])
REFERENCES [dbo].[Question] ([question_id])
GO
ALTER TABLE [dbo].[ExamResult]  WITH CHECK ADD FOREIGN KEY([exam_id])
REFERENCES [dbo].[Exam] ([exam_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[ExamResult]  WITH CHECK ADD FOREIGN KEY([student_id])
REFERENCES [dbo].[Student] ([student_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[ExamResult]  WITH CHECK ADD  CONSTRAINT [FK_ExamResult_StudentProgress] FOREIGN KEY([progress_id])
REFERENCES [dbo].[StudentProgress] ([progress_id])
GO
ALTER TABLE [dbo].[ExamResult] CHECK CONSTRAINT [FK_ExamResult_StudentProgress]
GO
ALTER TABLE [dbo].[Question]  WITH CHECK ADD FOREIGN KEY([bank_id])
REFERENCES [dbo].[QuestionBank] ([bank_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[QuestionBank]  WITH CHECK ADD FOREIGN KEY([course_id])
REFERENCES [dbo].[Course] ([course_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Student]  WITH CHECK ADD  CONSTRAINT [FK_Class_Student] FOREIGN KEY([class_id])
REFERENCES [dbo].[Class] ([class_id])
GO
ALTER TABLE [dbo].[Student] CHECK CONSTRAINT [FK_Class_Student]
GO
ALTER TABLE [dbo].[StudentProgress]  WITH CHECK ADD FOREIGN KEY([student_id])
REFERENCES [dbo].[Student] ([student_id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Course]  WITH CHECK ADD CHECK  (([course_type]='混合' OR [course_type]='面授' OR [course_type]='录播' OR [course_type]='直播'))
GO
ALTER TABLE [dbo].[Question]  WITH CHECK ADD CHECK  (([question_type]='填空' OR [question_type]='判断' OR [question_type]='多选' OR [question_type]='单选'))
GO
