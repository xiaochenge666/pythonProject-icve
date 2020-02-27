# created by XiaoChenGe 禁止商业用途 如有问题联系QQ:1430986978
import numpy as np
import tensorflow as tf
from PIL import Image
from com.tools.parameter.parm import Model_PATH
from com.tools.verificationcode.tensorflowTools.gray import getverify

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SAVE_PATH = Model_PATH
CHAR_SET = number
CHAR_SET_LEN = len(CHAR_SET)
IMAGE_HEIGHT = 41
IMAGE_WIDTH = 161
model_Name = 'model'


# 灰度化
def convert2gray(img):
    if len(img.shape) > 2:
        gray = np.mean(img, -1)
        return gray
    else:
        return img


# text到one-hot编码
def text2vec(text):
    vector = np.zeros([MAX_CAPTCHA, CHAR_SET_LEN])
    for i, c in enumerate(text):
        idx = CHAR_SET.index(c)
        vector[i][idx] = 1.0
    return vector


# one——hot到txtx
def vec2text(vec):
    text = []
    for i, c in enumerate(vec):
        text.append(CHAR_SET[c])
    return "".join(text)


# 获得一batch
def get_next_batch(image, batch_size=1):
    image = np.array(image)
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    for i in range(batch_size):
        # image = tf.reshape(convert2gray(image), (IMAGE_HEIGHT, IMAGE_WIDTH, 1))
        image = tf.reshape(convert2gray(image), (IMAGE_HEIGHT, IMAGE_WIDTH, 1))
        batch_x[i, :] = image
    return batch_x


def predict(img):
    global model_Name
    model = tf.keras.models.load_model(SAVE_PATH + model_Name)
    batch = get_next_batch(img)
    # 预测值（传入参数）
    prediction_value = model.predict(batch)
    prediction_value = vec2text(np.argmax(prediction_value, axis=2)[0])
    print('预测值：', prediction_value)
    return prediction_value


def getResultByName(name, path):
    getverify(name, path)
    img = Image.open(path + name + ".png")
    return predict(img)


if __name__ == "__main__":
    getResultByName("0200", 'img/')
