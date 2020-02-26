# created by XiaoChenGe 禁止商业用途 如有问题联系QQ:1430986978
from PIL import Image
import numpy

#二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
def convert(img):

    #二值化图像
    #:param img:需要二值化的图像
    #:return:二值化后的图像
    ##由RGB转为灰度
    img_grey = img.convert('L')
    ##二值化阈值，若大于threshold置为1，小于为0
    threshold = 200
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    ##把table矩阵转为图片
    out_img = img_grey.point(table, '1')
    return out_img
def print_mat_img(img):
    ##这里用到了numpy包，需要引入
    ##把图片转为矩阵，传给mat_img,类型为int8
    mat_img = np.asarray(img, np.int8)
    ##两层遍历每一点
    for h in range(img.height):
        for w in range(img.width):
            print(mat_img[h][w], end='')
        print('')
def flood_fill(img, x, y):
    '''
    降噪
    :param img:
    :param x: 当前x坐标
    :param y: 当前y坐标
    :return:
    '''
    cur_pixel = img.getpixel((x, y))
    width = img.width
    height = img.height

    # 若当前点为白色，则不统计邻域值
    if cur_pixel == 1:
        return 0

    if y == 0:
        if x == 0:
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))
            + img.getpixel((x + 1, y + 1))
            return 4 - sum
        else:
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum
def remove_noise_point(img, start, end):
    '''
    去杂点
    :param img:要去除噪点的图片
    :param start:噪点评分下限
    :param end:噪点评分上限
    :return:去除噪点后的Img
    '''
    ##新建noise_point_list来储存噪点
    noise_point_list = []
    ##两层for遍历每个像素，再调用之前写好的flood_fill寻找噪点
    for w in range(img.width):
        for h in range(img.height):
            around_num = flood_fill(img, w, h)
            ##若当前像素的噪点评分在start和end之间，则判断为噪点
            if(start < around_num < end) and img.getpixel((w, h)) == 0:
                pos = (w, h)
                noise_point_list.append(pos)

    ##把噪点置为背景色
    for pos in noise_point_list:
        img.putpixel((pos[0], pos[1]), 1)
    return img
def add_line_by_x(x_list, img):
    mat_img = np.asarray(img, np.int8)
    for x in x_list:
        for h in range(img.height):
            mat_img[h, x] = 0
        image = Image.fromarray(np.uint8(mat_img))
    return image
def add_line_by_y(y_list, img):
    mat_img = np.asarray(img, np.int8)
    for y in y_list:
        for w in range(img.width):
            mat_img[y, w] = 0
        image = Image.fromarray(np.uint8(mat_img))
    return image
# def getverify1(name):
#     #打开图片
#     im = Image.open(name)
#     #转化到灰度图片
#     imgry = im.convert('L')
#     #保存图像
#     imgry.save('g'+name)
#     #二值化，采用法制分割法,threshold为分割点
#     out = imgry.point(table,'1')
#     out.save('b'+name)
#     out=remove_noise_point(out,1,5)
#     out.save('f'+name)
def getverify(name,path=''):
    #打开图片
    name=path+name+'.png'
    im = Image.open(name)
    #转化到灰度图片
    imgry = im.convert('L')
    #保存图像
    imgry.save(name)
    #二值化，采用法制分割法,threshold为分割点
    out = imgry.point(table,'1')
    out.save(name)
    out=remove_noise_point(out,1,5)
    # print('xxxx')
    out.save(name)

