from com.version_auto_auth.tools.zhijiaoyun import *
def init():
    z = zhihui()
    username = input("请输入用户名：")
    password = input("请输入密码：")
    z.login_final(username, password)
    CourseList = z.getLearnningCourseList()
    for i in range(3):
        print("tips:为了保证不出错直接复制上边的课程名！")
    courseName = input("请输入课程名：")
    z.doFlashBody(CourseList[str(courseName)])
    print("完成刷课")
