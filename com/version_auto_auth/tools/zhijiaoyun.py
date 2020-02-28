import json
import sys
import time
from selenium import webdriver
import random
import requests
from com.version_auto_auth.tools.verificationcode.tensorflowTools.Tensorflow import getResultByName
import os


class zhihui():
    header = {
        'Origin': 'https://mooc.icve.com.cn',
        'Referer': 'https://mooc.icve.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.119 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(self.header)

    # 获取验证码并将其保存到本地文件
    def getVerificationCode(self, user, path):
        url = 'https://zjy2.icve.com.cn/common/VerifyCode/index?t=0.7494683560082718'
        url1 = "https://zjy2.icve.com.cn/"
        self.session.get(url1)
        response = self.session.get(url)
        response.encoding = "ISO-8859-1"
        with open(path + str(user) + ".png", 'wb')as jpg:
            jpg.write(response.content)
        code = getResultByName(str(user), path)
        return code

    # 使用selenium处理需要更新的资源
    def update(self, courseOpenId, openClassId, cellId, flag, moduleId, type, user, pwt):
        # 创建对象
        # driver = webdriver.Firefox()
        driver = webdriver.PhantomJS(executable_path=r'G:\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        # 登陆
        driver.get('https://zjy2.icve.com.cn/portal/login.html')
        driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[1]/div/input').send_keys(
            user)  # 账号
        driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/input').send_keys(
            pwt)  # 密码
        driver.find_element_by_xpath('//*[@id="btnLogin"]').click()  # 登陆
        time.sleep(1)
        url = 'https://zjy2.icve.com.cn/common/directory/directory.html?courseOpenId=' + str(
            courseOpenId) + '&openClassId=' + str(openClassId) + '&cellId=' + str(cellId) + '&flag=' + str(
            flag) + '&moduleId=' + str(moduleId)
        driver.get(url)  # 目录界面
        time.sleep(1)
        if type == '视频':
            # 如果是视频
            time.sleep(2)
            try:
                driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[1]/div/div/div[7]/div[1]/div").click()
            except:
                print('出错')
            time.sleep(2)
        driver.close()
        return 0

    # 1.登陆函数，使用户登陆平台并保持登陆状态
    def login(self, username, password, code):
        # 登陆账号保持登陆状态
        self.name = username
        self.pwo = password
        list = []
        date = {
            'userName': username,
            'userPwd': password,
            'verifyCode': code
        }
        # 登陆地址
        url = 'https://zjy2.icve.com.cn/common/login/login'
        # 发起请求
        req = self.session.post(url, date)
        print(req)
        Json = json.loads(req.text)
        # print(Json)
        if Json['code'] == 1:
            print("登陆成功！")
            dict = {}
            dict['code'] = 1
            dict['userId'] = Json['userId']
            dict['userName'] = Json['userName']
            dict['displayName'] = Json['displayName']
            return 1
        elif Json['code'] == -2:
            print("密码错误！")
            return -2
        elif Json['code'] == -1:
            print("用户不存在！")
            return -1
        else:
            print('未知错误')
            return 0

    # 封装后的登陆
    def login_final(self, user, pwd, path='tools/verificationcode/img/'):
        for i in range(20):
            code = self.getVerificationCode(user, path)
            state = self.login(user, pwd, code)
            if state == 1:
                print('×33333')
                return 1
                break
            elif state == -2:
                return 0
                break
            elif state == -1:
                return 0
                break

    # 3.获得courseOpenId
    def getLearnningCourseList(self, cname=''):
        # 说明：此方法负责获取courseOpenId，openClassId，courseName返回一个内置字典的数组
        # 创建列表
        coures_list = {}
        # 获取课程科目
        url = 'https://zjy2.icve.com.cn/student/learning/getLearnningCourseList'
        req = self.session.post(url)
        info = json.loads(req.text)
        courseList = info['courseList']
        print("您当前账号中的所有课程：")
        for i in courseList:
            courseList = {'courseName': i['courseName'],
                          'courseOpenId': i['courseOpenId'],
                          'openClassId': i['openClassId'],
                          'process': i['process'], 'totalScore': i['totalScore'],
                          'assistTeacherName': i['assistTeacherName']}
            coures_list[i['courseName']] = courseList
            print(i['courseName'])
        c = {}
        if cname in coures_list:
            c = coures_list[str(cname)]
        return coures_list, c

    def getModuleList(self, coures_list_item):
        module_id_list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/study/process/getProcessList'
        date = {'courseOpenId': coures_list_item['courseOpenId'], 'openClassId': coures_list_item['openClassId']}
        res = self.session.post(url, date)
        res = json.loads(res.text)
        moduleList = res['progress']['moduleList']
        for i in moduleList:
            list_item = {'moduleId': i['id'], 'name': i['name'], 'percent': i['percent'],
                         'courseOpenId': coures_list_item['courseOpenId'],
                         'openClassId': coures_list_item['openClassId']}
            module_id_list.append(list_item)
        return module_id_list

    def getTopicByModuleId(self, module_id_list):
        if module_id_list:
            module_topic_list = []  # 各个模块(module)下的topic_list
            for _ in module_id_list:
                topic_list = []  # 储存topic下的信息
                url = 'https://zjy2.icve.com.cn/study/process/getTopicByModuleId'
                date = {'courseOpenId': _['courseOpenId'], 'moduleId': _['moduleId']}
                res = self.session.post(url, date)
                res = json.loads(res.text)
                topicList = res['topicList']
                for i in topicList:
                    topicList = {'topicId': i['id'], 'name': i['name'],
                                 'courseOpenId': _['courseOpenId'],
                                 'moduleId': _['moduleId'],
                                 'openClassId': _['openClassId']
                                 }
                    topic_list.append(topicList)
                module_topic_list.append(topic_list)
            return module_topic_list

    def getCellByTopicId(self, module_topic_list):
        if module_topic_list:
            module_topic_cell_list = []

            for _ in module_topic_list:  # module
                topic_cell_list = []
                for _1 in _:  # topic
                    cell_list = []
                    url = 'https://zjy2.icve.com.cn/study/process/getCellByTopicId'
                    data = {'courseOpenId': _1['courseOpenId'], 'openClassId': _1['openClassId'],
                            'topicId': _1['topicId']}
                    res = self.session.post(url, data)

                    # 将读到的信息转换成json对象并写入到一个文件中
                    res = json.loads(res.text)
                    cellList = res['cellList']

                    for i in cellList:
                        if i['categoryName'] == '子节点':
                            for i1 in i['childNodeList']:  # 遍历子节点中的课件
                                child_cell = {'Id': i1['Id'],
                                              'cellName': i1['cellName'],
                                              'categoryName': i1['categoryName'],
                                              'stuCellFourPercent': i1['stuCellFourPercent'],
                                              'courseOpenId': _1['courseOpenId'],
                                              'openClassId': _1['openClassId'],
                                              'topicId': _1['topicId'],
                                              'moduleId': _1['moduleId']
                                              }
                                cell_list.append(child_cell)
                        else:
                            cell = {'Id': i['Id'],
                                    'cellName': i['cellName'],
                                    'categoryName': i['categoryName'],
                                    'stuCellFourPercent': i['stuCellPercent'],
                                    'courseOpenId': _1['courseOpenId'],
                                    'openClassId': _1['openClassId'],
                                    'topicId': _1['topicId'],
                                    'moduleId': _1['moduleId']
                                    }
                            cell_list.append(cell)

                    topic_cell_list.append(cell_list)
                module_topic_cell_list.append(topic_cell_list)
            return module_topic_cell_list

    def getAllCellList(self, module_topic_cell_list):
        all_cell_list = []
        for _ in module_topic_cell_list:
            for _1 in _:
                for _2 in _1:
                    all_cell_list.append(_2)
        return all_cell_list

        # 切换成当前课件

    def continueStudy(self, courseOpenId, openClassId, cellId, cellName, moduleId):
        url = 'https://zjy2.icve.com.cn/common/Directory/changeStuStudyProcessCellData'
        date = {'courseOpenId': courseOpenId,
                'openClassId': openClassId,
                'moduleId': moduleId,
                'cellId': cellId,
                'cellName': cellName
                }
        req = self.session.post(url, date)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)

    # 查看课件methed
    def viewDirectory(self, courseOpenId, openClassId, cellId, flag, moduleId):

        url = 'https://zjy2.icve.com.cn/common/Directory/viewDirectory'
        date1 = {'courseOpenId': courseOpenId, 'openClassId': openClassId, 'cellId': cellId, 'flag': flag,
                 'moduleId': moduleId}
        res = self.session.post(url, date1)
        info = json.loads(res.text)

        if info['code'] == 1:
            course_info = {'audioVideoLong': info['audioVideoLong'], 'cellName': info['cellName'],
                           'cellLogId': info['cellLogId'], 'cellPercent': info['cellPercent'],
                           'guIdToken': info['guIdToken'], 'isNeedUpdate': info['isNeedUpdate'],
                           'categoryName': info['categoryName']}
            return course_info  # 返回一个数组
        elif info['code'] == -100:
            currCourseOpenId = info['currCourseOpenId']
            currOpenClassId = info['currOpenClassId']
            currModuleId = info['currModuleId']
            curCellId = info['curCellId']
            currCellName = info['currCellName']
            lastPercent = info['lastPercent']
            self.continueStudy(currCourseOpenId, currOpenClassId, curCellId, currCellName, currModuleId)
            return self.viewDirectory(currCourseOpenId, currOpenClassId, curCellId, flag, currModuleId)
        else:
            print('未知错误错误码：', info)
            os.system('pause')
            exit()

    # 上传进度的方法
    def stuProcessCellLog(self, courseOpenId, openClassId, cellId, cellLogId, token, studyNewlyTime):
        url = 'https://zjy2.icve.com.cn/common/Directory/stuProcessCellLog'
        date = {'picNum': random.randint(4000, 9999),
                'studyNewlyPicNum': random.randint(4000, 9999),
                'studyNewlyTime': studyNewlyTime,
                'courseOpenId': courseOpenId,
                'openClassId': openClassId,
                'cellId': cellId,
                'cellLogId': cellLogId,
                'token': token}

        req = self.session.post(url, date)
        info = json.loads(req.text)
        print('服务器响应：', info)
        return info['code']

    # 上传评论的方法
    def addCellActivity(self, courseOpenId, openClassId, cellId, activityType):
        url = 'https://zjy2.icve.com.cn/common/Directory/addCellActivity'
        if activityType != 1:
            star = 0
        else:
            star = random.randint(4, 5)
        content = ''
        if activityType == 1:
            content = random.choice(['好', '灰常好', 'good', '阔以', '1', '0', 'ok'])
        elif activityType == 2:
            content = random.choice(['无', '没有', 'Nothing', '没得', '2', 'none'])
        elif activityType == 3:
            content = random.choice(['无', '没有', 'anything', '没得', '1', '0'])
        elif activityType == 4:
            content = random.choice(['无', '没有', 'no', '没得', '好', '1', '2'])

        date1 = {
            # 'content':'灰常好',#评论的内容
            'docJson': '',  # 视频进度
            # 'activityType': '1',#评论1，问答：3，笔记：2，纠错4
            'star': star,
            'activityType': activityType,
            'content': content,
            'courseOpenId': courseOpenId,
            'openClassId': openClassId,
            'cellId': cellId
        }
        req = self.session.post(url, date1)
        time.sleep(random.randint(0, 1))
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)
        print(info)

    def zjyUserOnlineTimeRedis(self, userId, userName, userDisplayName):
        list = []  # 储存moduleId 日志
        url = 'https://dm.icve.com.cn/ZjyLogsManage/zjyUserOnlineTimeRedis'
        date1 = {'userId': userId, 'userName': userName, 'userDisplayName': userDisplayName}
        req = self.session.post(url, date1)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)

    # 选课
    def addCourse(self):
        url = 'https://zjy2.icve.com.cn/student/courseCenter/saveClass'
        data = {
            'courseOpenId': 'jdragyrir9flsp3c1zq9q',
            'openClassId': 'ur7sagyrh51fq2dn1zvznq'
        }
        res = self.session.post(url, data)
        res = json.loads(res.text)
        print(res['msg'])

    # 退课
    def quitCourse(self):
        url = 'https://zjy2.icve.com.cn/student/courseCenter/quitOpenClass'
        data = {
            'courseOpenId': 'jdragyrir9flsp3c1zq9q',
            'openClassId': 'ur7sagyrh51fq2dn1zvznq',
            'termId': 'upepap2qvyviahtkhtodyw'
        }
        res = self.session.post(url, data)
        res = json.loads(res.text)
        print(res)

    # 通过课程名获取courseOpenId, openClassId,termList
    def getCOiD(self, cname):
        courseListDic = {}
        url = 'https://zjy2.icve.com.cn/student/learning/getLearnningCourseList'
        res = self.session.post(url)
        res = json.loads(res.text)
        for _ in res['courseList']:
            courseListDic[str(_['courseName'])] = {'courseOpenId': _['courseOpenId'], 'openClassId': _['openClassId']}

        print(courseListDic)
        c = courseListDic[str(cname)]
        return c['courseOpenId'], c['openClassId'], res['termList']

        # 获取指定课名的作业

    # 平时作业
    def getHomeWorkList(self, courseOpenId, openClassId):
        url = 'https://zjy2.icve.com.cn/study/homework/getHomeworkList'
        data = {
            'courseOpenId': courseOpenId,
            'openClassId': openClassId,
            'pageSize': 1000
        }
        res = self.session.post(url, data)
        res = json.loads(res.text)
        openClassType = res['openClassType']
        homework_list = []
        for i in res['list']:
            item = {
                'homeworkTermTimeId': i['homeworkTermTimeId'],
                'homeworkId': i['Id'],
                'courseOpenId': data['courseOpenId'],
                'openClassId': data['openClassId'],
                'openClassType': openClassType
            }
            homework_list.append(item)
        return homework_list

    # 查看细节
    def getDetails(self, homework_list):
        detailsList = []
        print('===============================作业列表=====================================')
        for _ in homework_list:
            url = 'https://security.zjy2.icve.com.cn/study/homework/detail'
            data = {
                'courseOpenId': _['courseOpenId'],
                'openClassId': _['openClassId'],
                'homeworkId': _['homeworkId'],
                'hkTermTimeId': _['homeworkTermTimeId'],
                'openClassType': _['openClassType'],
                'viewType': 1
            }
            res = self.session.post(url, data)
            res = json.loads(res.text)
            detailsList.append(res)
            print('作业名：', res['homework']['Title'])
        # print(detailsList)
        return detailsList

    # 查看历史记录
    def docHomeworkHistory(self, details_list):
        history_list = []
        for _ in details_list:
            if _['homeworkStulist']:
                url = 'https://security.zjy2.icve.com.cn/study/homework/history'
                data = {
                    'courseOpenId': _['courseOpenId'],
                    'homeWorkId': _['homeworkId'],
                    'activityId': _['activityId'],
                    'hkTermTimeId': _['hkTermTimeId'],
                    'studentWorkId': _['homeworkStulist'][0]['Id'],
                    'faceType': _['faceType']
                }
                res = self.session.post(url, data)
                res = json.loads(res.text)
                history_list.append(res)
                # print(res, '\n')
            else:
                data = {'code': -1, 'msg': '该作业未完成'}
                history_list.append(data)
                print('{code: -1 msg: 该作业未完成! }')
        return history_list

    # 答案解析
    def parseAnswer(self, q_list):
        dic_a = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I'}
        dic_b = {'0': 'X', '1': '√'}
        if q_list:
            for q in q_list:
                print("================题目===================")
                Title = q['Title']
                print(Title)

                answerList = q['answerList']
                for _1 in answerList:
                    print(dic_a[str(_1['SortOrder'])], ' ', _1['Content'])

                Answer = q['Answer']
                print('正确答案：')
                if Answer:
                    if q['questionType'] == 1 or q['questionType'] == 2:  # 单选或多选
                        for _a in Answer:
                            print(dic_a[str(_a[0])])
                    elif q['questionType'] == 5 or q['questionType'] == 6:  # 填空题或问答题
                        for i, _a in enumerate(Answer):
                            print('第' + str(i + 1) + '题：', _a)
                    elif q['questionType'] == 3:  # 填空题或问答题
                        for i, _a in enumerate(Answer):
                            print(dic_b[str(_a)])
                    else:
                        for _a in Answer:
                            print(_a)
                    resultAnalysis = q['resultAnalysis']
                    print("解析：" + resultAnalysis)
                else:
                    print('答案未公布！')

    # 获取答案的数据并解析
    def parseHomeworkAnswer(self, history_list):
        for _ in history_list:
            if _['code'] == 1:
                self.parseAnswer(_['questions'])
            else:
                print('未完成')

    # 考试
    def getExameList(self):
        url = 'https://zjy2.icve.com.cn/student/myExam/getMyExamList'
        data = {'unprocessed': 0}
        res = self.session.post(url, data)
        res = json.loads(res.text)
        return res

    def getExamHistory(self, exam_list):
        examlist = []
        if exam_list:
            for _ in exam_list['list']:
                courseOpenId = _['courseOpenId']
                openClassId = _['openClassId']
                exam_list2 = []
                for _1 in _['examList']:
                    if _1['stuOnlineExamId']:
                        url = 'https://security.zjy2.icve.com.cn/study/onlineExam/history'
                        data = {
                            'courseOpenId': courseOpenId,
                            'openClassId': openClassId,
                            'stuOnlineExamId': _1['stuOnlineExamId'],
                            'type': _1['type'],
                            'viewType': 2
                        }
                        res = self.session.post(url, data)
                        res = json.loads(res.text)
                        exam_list2.append(res)
                    else:
                        exam_list2.append([])
                        print('无记录')
                examlist.append(exam_list2)
        return examlist

    def parseExamAnswer(self, examhistory_res):
        if examhistory_res:
            for _ in examhistory_res:
                for _1 in _:
                    print('++++++++++++试卷++++++++++++++++')
                    if _1:
                        self.parseAnswer(_1['questions'])

    def doFlashComment(self, cName):
        # 开始刷课
        # 基本思路
        # 进入目录--》选择课件--》上传进度（若失败则停留11s,在重新上传）--》判断进度是否为100%--》进入下一个课件--》循环
        # 刷评论
        c = cName['c']  # 评论问答纠错笔记
        q = cName['q']
        cr = cName['cr']
        w = cName['w']
        # print('=============换课啦,得courseOpenId，openClassId====================')
        p = self.getProcessList(cName['courseOpenId'], cName['openClassId'])  # 获取进度
        for i1 in p:  # 遍历所有的课程名（courseopenid）
            # pint('-------------------换模块啦，得Topic-----------------------------')
            m = self.getTopicByModuleId(cName['courseOpenId'], i1['moduleId'])
            for i2 in m:  # 遍历所有的ModuleId
                # print("-----------------------换Topic,获取cellID-----------------------------")
                c = self.getCellByTopicId(cName['courseOpenId'], cName['openClassId'], i2['topicId'])
                for i3 in c:  # 遍历所有的topicid
                    # print('-----------------进入viewDirectory模式-----------------------------')
                    v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's',
                                           i1['moduleId'])
                    for i4 in v:  # 遍历所有的课程目录
                        self.addCellActivity(cName['courseOpenId'], cName['openClassId'], i3['Id'], '', 1)
                        self.addCellActivity(cName['courseOpenId'], cName['openClassId'], i3['Id'], '', 2)
                        self.addCellActivity(cName['courseOpenId'], cName['openClassId'], i3['Id'], '', 3)
                        self.addCellActivity(cName['courseOpenId'], cName['openClassId'], i3['Id'], '', 4)

    def viewDir(self, _):
        fls = self.viewDirectory(courseOpenId=_['courseOpenId'], openClassId=_['openClassId'], cellId=_['Id'],
                                 flag='s', moduleId=_['moduleId'])
        self.stuProcessCellLog(courseOpenId=_['courseOpenId'], openClassId=_['openClassId'],
                               cellId=_['Id'], cellLogId=fls['cellLogId'], token=fls['guIdToken'],
                               studyNewlyTime=fls['audioVideoLong'])
        print(fls['cellName'], '进度：', fls['cellPercent'])
        return fls

    def doFlashCourse(self, cname):
        all_list, one = self.getLearnningCourseList(cname)  # p1：所有课程 p2:指定课程名课程信息
        module_topic_cell_list = self.getCellByTopicId(z.getTopicByModuleId(z.getModuleList(
            one)))  # 获取该门课件的所有celld信息；返回数据结构：[moudel[topic[cell[],cell[]..],topic[cell[],cell[]..],...],moudel[]....]
        all_cell_list = self.getAllCellList(module_topic_cell_list)
        for _ in all_cell_list:
            ######################################################################################
            #               'audioVideoLong': info['audioVideoLong'],
            #               'cellName': info['cellName'],             #
            #               'cellLogId': info['cellLogId'],
            #               'cellPercent': info['cellPercent'],   #
            #               'guIdToken': info['guIdToken'],
            #               'isNeedUpdate': info['isNeedUpdate'], #
            #               'categoryName': info['categoryName']                                  #
            ########################################################################################
            fls = self.viewDir(_)  # 刷新一次
            if fls['cellPercent'] < 100:
                while True:
                    time.sleep(random.randint(0, 6))
                    fls = self.viewDir(_)
                    if fls['cellPercent'] >= 100:
                        break
                    if fls['isNeedUpdate']:
                        break


class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


# sys.stdout = Logger("F:\\源代码\\python_pycharm\\pythonProject-icve\\com\\version_auto_auth\\a.txt")  # 这里我将Log输出到D盘
if __name__ == '__main__':
    z = zhihui()
    z.login_final('081218191', 'sui2001.', 'verificationcode/img/')
    z.doFlashCourse('中药综合知识与技能')

    pass
