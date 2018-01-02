# coding:utf-8
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential,load_model
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from bs4 import BeautifulSoup
import time
import requests
import numpy as np
from PIL import Image
import shutil
import re

# dimensions of our images.
img_width, img_height = 60, 30

crop_weights = './cropWeights.h5'
class_weights = './classWeights.h5'
_crop_model = './cropModel.h5'
_class_model = './classModel.h5'
nb_train_samples = 100
nb_validation_samples = 10
nb_epoch = 3000
map_list = ['3', '5', '6','7','8','9','A','B','D','E','F','G','H','J','K','M','N','P','R','S','T','U','V','X','Y']
map_array = np.array(map_list)


def crop(im):
    step = 1
    box_list = []
    for i in range(121):
        box_list.append((step*i, 0, 30+step*i, 60))
    if not os.path.exists('./captchaTemp/data'):
        os.mkdir('captchaTemp')
        os.mkdir('./captchaTemp/data')
    count = 0
    for each in box_list:
        region = im.crop(each)
        region.save('captchaTemp/data/' + str(count) + '.png')
        count += 1


def predict(crop_model, class_model):
    date_gen_crop = ImageDataGenerator(rescale=1./255, zca_whitening=True)
    date_gen_class = ImageDataGenerator(rescale=1./255, zca_whitening=True)
    crop_generator = date_gen_crop.flow_from_directory(
        'captchaTemp',
        color_mode='grayscale',
        shuffle=False,
        target_size=(60,30))
    crop_file_names = crop_generator.filenames
    predict_crop = crop_model.predict_generator(crop_generator,121)
    # sorting images
    maping = []
    for imName in crop_file_names:
        maping.append(int(re.sub('\D*','',imName)))
    good_arr = predict_crop[:,1]
    print('predict_crop: {}'.format(good_arr))
    index = np.argsort(good_arr).tolist()
    print(len(index))
    print(len(good_arr))
    final_index = [maping[p] for p in index]
    index = []
    index = final_index
    print('index: {}'.format(index))
    target = index[-5:-1]
    print('target: {}'.format(target))
    index = index[:-4]
    check_and_replace(index, target, 18)
    target.sort()
    if os.path.exists('./tobe_classfied'):
        shutil.rmtree('./tobe_classfied')
    os.mkdir('tobe_classfied')
    os.mkdir('./tobe_classfied/data')
    im_list = []
    for each in target:
        im_list.append(str(each) + '.png')
    print(im_list)
    for each in im_list:
        temp = Image.open('./captchaTemp/data/' + each)
        temp.save('./tobe_classfied/data/' + each)
    class_generator = date_gen_class.flow_from_directory(
        'tobe_classfied',
        color_mode='grayscale',
        shuffle=False,
        target_size=(60,30))
    predict_class = class_model.predict_generator(class_generator,4)
    class_file_names = class_generator.filenames
    sorted_file_names = os.listdir('./tobe_classfied/data')
    sorted_file_names.sort(key=lambda x : int(x[:-4]))
    print('predictLcass: {}'.format(predict_class))
    print('class_file_names:{}'.format(class_file_names))
    print('sorted_file_names:{}'.format(sorted_file_names))
    class_index = []
    temp = [0,0,0,0]
    result = predict_class.argmax(axis = 1)
    result.tolist()
    print('result:{}'.format(result))
    for each in class_file_names:
        class_index.append(sorted_file_names.index(os.path.basename(each)))
    for each in class_index:
        temp[each] = result[class_index.index(each)]
    result = temp
    print('result: {}'.format(result))
    final_class = map_array[result]
    print(final_class)
    final_class.tolist()
    captcha = ''.join(final_class)
    print('captcha:{}'.format(captcha))
    return captcha


def check_and_replace(index,target,distance):
    state = 1
    for i in range(0,len(target)-1):
        for j in range(i+1,len(target)):
            if abs(target[i] - target[j]) < distance:
                print('i: {}, j: {}'.format(str(i),str(j)))
                print('replace {} '.format(str(target[j])))
                target[j] = index.pop()
                print('target:{}'.format(str(target)))
                state *= 0
            else:
                state *=1
    while state == 0:
        state = 1
        for i in range(0,len(target)-1):
            for j in range(i+1,len(target)):
                if abs(target[i] - target[j]) < distance:
                    print('i: {}, j: {}'.format(str(i),str(j)))
                    print('replace {} '.format(str(target[j])))
                    target[j] = index.pop()
                    print('target:{}'.format(str(target)))
                    state *= 0
                else:
                    state *=1


if __name__ == '__main__':
    crop_model = load_model(_crop_model)
    class_model = load_model(_class_model)
    im = Image.open('captcha.jpg')
    crop(im)
    verify = predict(crop_model, class_model)