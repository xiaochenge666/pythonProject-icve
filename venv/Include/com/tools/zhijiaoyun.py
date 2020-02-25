import json
import time
from selenium import webdriver
import random
import requests

import os
from Include.com.tools.gray import *
class zhihui():
    header = {
        'Origin': 'https://mooc.icve.com.cn',
        'Referer': 'https://mooc.icve.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(self.header)

    # 获取验证码并将其保存到本地文件
    def getVerificationCode(self, user, path='img/'):
        url = 'https://zjy2.icve.com.cn/common/VerifyCode/index?t=0.7494683560082718'
        url1 = "https://zjy2.icve.com.cn/"
        self.session.get(url1)
        response = self.session.get(url)
        response.encoding = "ISO-8859-1"
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        havaPath = os.path.exists(path)
        if not havaPath:
            os.makedirs(path)

        with open(path + str(user) + ".png", 'wb')as jpg:
            jpg.write(response.content)
        t1 = getResultByName(str(user), path)

        return t1






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
        Json = json.loads(req.text)
        if Json['code'] == 1:
            print("登陆成功！")
            dict = {'code': 1, 'userId': Json['userId'], 'userName': Json['userName'],
                    'displayName': Json['displayName']}
            print("欢迎"+dict['displayName']+'使用网课挂机包')
            return 1
        elif Json['code'] == -2:
            print("密码错误！")
            return -2
        elif Json['code'] == -1:
            print(Json['msg'])
            return -1
        elif Json['code'] == -16:
            print(Json['msg'])
            return -16
        else:
            print('未知错误',Json)
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
    def getLearnningCourseList(self, c='好', q='无', cr='无', w='无', isCommect=True):
        # 说明：此方法负责获取courseOpenId，openClassId，courseName返回一个内置字典的数组
        # 创建列表
        Coures = {}
        # 获取课程科目
        url = 'https://zjy2.icve.com.cn/student/learning/getLearnningCourseList'
        req = self.session.post(url)
        info = json.loads(req.text)
        courseList = info['courseList']
        print("您当前账号中的所有课程：")
        for i in courseList:
            courseList = {'courseName': i['courseName'], 'courseOpenId': i['courseOpenId'], 'openClassId': i['openClassId'],
                    'process': i['process'], 'totalScore': i['totalScore'], 'assistTeacherName': i['assistTeacherName'],
                    'isComment': isCommect, 'c': c, 'q': q, 'cr': cr, 'w': w}
            print(i['courseName'])
            Coures[i['courseName']] = courseList
        return Coures

    def getProcessList(self, courseOpId, openClassId):
        modulidlist = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/study/process/getProcessList'
        date1 = {'courseOpenId': courseOpId, 'openClassId': openClassId}
        req = self.session.post(url, date1)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)
        moduleList = info['progress']['moduleList']
        for i in moduleList:
            list1 = {'moduleId': i['id'], 'name': i['name'], 'percent': i['percent']}
            modulidlist.append(list1)
        return modulidlist

    def getTopicByModuleId(self, courseOpId, moduleId):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/study/process/getTopicByModuleId'
        date1 = {}
        date1['courseOpenId'] = courseOpId
        date1['moduleId'] = moduleId
        req = self.session.post(url, date1)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)
        topicList = info['topicList']
        for i in topicList:
            # print(i)
            list1 = {'topicId': i['id'], 'name': i['name']}
            list.append(list1)
        return list

    def getCellByTopicId(self, courseOpId, openClassId, topicId):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/study/process/getCellByTopicId'
        date1 = {}
        date1['courseOpenId'] = courseOpId
        date1['openClassId'] = openClassId
        date1['topicId'] = topicId
        req = self.session.post(url, date1)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)

        cellList = info['cellList']
        for i in cellList:
            if i['categoryName'] == '子节点':
                # print('-----------字节点----------------')
                # print(i['childNodeList'])
                for i1 in i['childNodeList']:  # 遍历子节点中的课件
                    list1 = {}
                    list1['Id'] = i1['Id']  # cellk课件id
                    list1['cellName'] = i1['cellName']  # 课件名
                    list1['categoryName'] = i1['categoryName']  # 课件类型
                    list1['stuCellFourPercent'] = i1['stuCellFourPercent']  # 课件百分比
                    list.append(list1)
            else:
                # print("------------非子节点--------------")
                list2 = {}
                list2['Id'] = i['Id']
                list2['cellName'] = i['cellName']
                list2['categoryName'] = i['categoryName']
                list2['stuCellFourPercent'] = i['stuCellPercent']
                list.append(list2)
                # print('list:',list)
        return list

    # 切换成当前课件
    def continueStudy(self, courseOpenId, openClassId, cellId, cellName, moduleId):
        url = 'https://zjy2.icve.com.cn/common/Directory/changeStuStudyProcessCellData'
        date1 = {}
        date1['courseOpenId'] = courseOpenId
        date1['openClassId'] = openClassId
        date1['moduleId'] = moduleId
        date1['cellId'] = cellId
        date1['cellName'] = cellName
        req = self.session.post(url, date1)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)

    # 查看课件methed
    def viewDirectory(self, courseOpenId, openClassId, cellId, flag, moduleId):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/common/Directory/viewDirectory'
        date1 = {}
        date1['courseOpenId'] = courseOpenId
        date1['openClassId'] = openClassId
        date1['cellId'] = cellId
        date1['flag'] = flag
        date1['moduleId'] = moduleId

        req = self.session.post(url, date1)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)
        list1 = {}
        if info['code'] == 1:
            list1['audioVideoLong'] = info['audioVideoLong']  # 这是课件的时间
            list1['cellName'] = info['cellName']  # 课件名
            list1['cellLogId'] = info['cellLogId']  # logid
            list1['cellPercent'] = info['cellPercent']  # 当前课件完成百分比
            list1['guIdToken'] = info['guIdToken']  #
            list1['isNeedUpdate'] = info['isNeedUpdate']  # 是否需要更新
            list1['categoryName'] = info['categoryName']  # 课件类型
            list.append(list1)
            # print('=====',list)
            return list  # 返回一个数组
        elif info['code'] == -100:
            currCourseOpenId = info['currCourseOpenId']
            currOpenClassId = info['currOpenClassId']
            currModuleId = info['currModuleId']
            curCellId = info['curCellId']
            currCellName = info['currCellName']
            lastPercent = info['lastPercent']
            # print(currCellName)
            self.continueStudy(currCourseOpenId, currOpenClassId, curCellId, currCellName, currModuleId)
            return self.viewDirectory(currCourseOpenId, currOpenClassId, curCellId, flag, currModuleId)
        else:
            print('未知错误错误码：',info)
            os.system('pause')
            #exit()

    # 上传进度的方法
    def stuProcessCellLog(self, courseOpenId, openClassId, cellId, cellLogId, token, studyNewlyTime):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/common/Directory/stuProcessCellLog'
        date1 = {'picNum': random.randint(4000, 9999), 'studyNewlyPicNum': random.randint(4000, 9999),
                 'studyNewlyTime': studyNewlyTime, 'courseOpenId': courseOpenId, 'openClassId': openClassId,
                 'cellId': cellId, 'cellLogId': cellLogId, 'token': token}

        req = self.session.post(url, date1)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)
        print(info)  # 服务器返回提交是否成功代码
        return info['code']

    # 上传评论的方法
    def addCellActivity(self, courseOpenId, openClassId, cellId, content, activityType):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/common/Directory/addCellActivity'
        if activityType != 1:
            star = 0
        else:
            star = random.randint(4, 5)

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
        date1 = {}
        date1['userId'] = userId
        date1['userName'] = userName
        date1['userDisplayName'] = userDisplayName
        req = self.session.post(url, date1)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.text)
        # print(info)

    # 开始刷课
    # 基本思路
    # 进入目录--》选择课件--》上传进度（若失败则停留11s,在重新上传）--》判断进度是否为100%--》进入下一个课件--》循环
    # 刷评论
    def doFlashComment(self, cName):
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
                time.sleep(random.randint(0, 1))
                # print("-----------------------换Topic,获取cellID-----------------------------")
                c = self.getCellByTopicId(cName['courseOpenId'], cName['openClassId'], i2['topicId'])
                for i3 in c:  # 遍历所有的topicid
                    time.sleep(random.randint(0, 1))
                    # print('-----------------进入viewDirectory模式-----------------------------')
                    v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's',
                                           i1['moduleId'])
                    for i4 in v:  # 遍历所有的课程目录
                        time.sleep(random.randint(0, 1))
                        self.addCellActivity(cName['courseOpenId'], cName['openClassId'], i3['Id'], '', 1)
                        time.sleep(random.randint(0, 1))
                        self.addCellActivity(cName['courseOpenId'], cName['openClassId'], i3['Id'], '', 2)
                        time.sleep(random.randint(0, 1))
                        self.addCellActivity(cName['courseOpenId'], cName['openClassId'], i3['Id'], '', 3)
                        time.sleep(random.randint(0, 1))
                        self.addCellActivity(cName['courseOpenId'], cName['openClassId'], i3['Id'], '', 4)

    def doFlashBody(self, cName):
        isComment = cName['isComment']
        c = cName['c']  # 评论问答纠错笔记
        q = cName['q']
        cr = cName['cr']
        w = cName['w']
        # print('=============换课啦,得courseOpenId，openClassId====================')
        p = self.getProcessList(cName['courseOpenId'], cName['openClassId'])  # 获取进度
        for i1 in p:  # 遍历所有的课程名（courseopenid）
            if i1['percent'] != 100:
                # pint('-------------------换模块啦，得Topic-----------------------------')
                m = self.getTopicByModuleId(cName['courseOpenId'], i1['moduleId'])
                # print(m)
                for i2 in m:  # 遍历所有的ModuleId
                    time.sleep(random.randint(1, 2))
                    # print("-----------------------换Topic,获取cellID-----------------------------")
                    c = self.getCellByTopicId(cName['courseOpenId'], cName['openClassId'], i2['topicId'])
                    for i3 in c:  # 遍历所有的topicid
                        time.sleep(random.randint(1, 2))
                        # print('-----------------进入viewDirectory模式-----------------------------')
                        v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's',
                                               i1['moduleId'])
                        # print(v)
                        for i4 in v:  # 遍历所有的课程目录
                            if i4['cellPercent'] == 100:  # 如果进度100%则跳过
                                pass
                            else:  # 如果进度未满，则上传进度（10s一次）
                                time.sleep(11)
                                res = self.stuProcessCellLog(cName['courseOpenId'], cName['openClassId'], i3['Id'],
                                                             i4['cellLogId'], i4['guIdToken'], i4['audioVideoLong'])
                                print(res)
                                v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's',
                                                       i1['moduleId'])
                                num = v[0]['cellPercent']  # 获取进度
                                print("刷完之后：", num)
                                # 如果需要更新
                                if v[0]['isNeedUpdate'] == 1:
                                    try:
                                        time.sleep(1)
                                        self.update(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's',
                                                    i1['moduleId'], i4['categoryName'], self.name, self.pwo)
                                    except:
                                        print(v)
                                guIdToken = v[0]['guIdToken']

                                if num != 100:  # 如果单个课件没有刷满
                                    while True:  # 循环
                                        time.sleep(11)
                                        code = self.stuProcessCellLog(cName['courseOpenId'], cName['openClassId'],
                                                                      i3['Id'], i4['cellLogId'], guIdToken,
                                                                      i4['audioVideoLong'])  # 提交一次
                                        flash = self.viewDirectory(cName['courseOpenId'], cName['openClassId'],
                                                                   i3['Id'], 's', i1['moduleId'])  # 查看一下情况
                                        if flash[0]['isNeedUpdate'] == 1:
                                            self.update(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's',
                                                        i1['moduleId'], i4['categoryName'], self.name, self.pwo)  # 更新资源
                                        num = flash[0]['cellPercent']  # 课程进度
                                        if num == 100:
                                            print('该课件已完成！')
                                            break
                                        print('循环:', num)
                                        guIdToken = flash[0]['guIdToken']
            else:
                print('该小节已完成！')
                pass
        if isComment:
            pass
            # self.doFlashComment(cName)


if __name__ == '__main__':
    pass
