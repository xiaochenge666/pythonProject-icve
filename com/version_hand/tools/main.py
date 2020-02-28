from com.version_hand.tools.zhijiaoyun import *


def init():
    print("\t\t\t\t\t\t小陈鸽网课挂机宝")
    while (True):
        print("==============================================================================================\n")
        z = zhihui()
        username = input("请输入用户名：\n")
        password = input("请输入密码：\n")
        try:
            z.getVerificationCode(username)
            code = input("输入验证码:\n")
            z.login(username, password, code)
            print('\n请手动关闭验证码窗口在继续....')
            os.system("pause")
            z.getLearnningCourseList()
            for i in range(3):
                print("\t\t\t\ttips:为了保证不出错直接复制上边的课程名！")
            courseName = input("请输入课程名：\n")
            print('\n开始挂机中,请勿关闭此窗口.....')
            z.doFlashCourse(courseName)
            print("刷课完毕,按任意键退出.....\n")
            os.system("pause")
            exit()
        except:
            print("异常，请重试！")
            print("=============================================================================================\n\n")
            os.system("pause")
