import pandas as pd
# from scipy.fftpack import fft,ifft
import keras
from keras.models import *
from mne.io import read_raw_cnt
import mne
import random
import numpy as np
import h5py
from scipy import signal
import os
from random import sample
from keras.utils.vis_utils import plot_model

def datagenerator(batchsize,train_data,win_train,y_lable, start_time,down_simple, test_list, channel):
    x_train, y_train = list(range(batchsize)), list(range(batchsize))
    for i in range(batchsize):
    
        k = sample(test_list, 1)[0]
        y_data = y_lable[k]-1
        time_start = random.randint(35,int(1000-win_train))
        x1 = int(start_time[k]/down_simple)+time_start
        x2 = int(start_time[k]/down_simple)+time_start+win_train
        x_1 = train_data[:,x1:x2]
        x_2 = np.reshape(x_1,(channel, win_train, 1))
        x_train[i]=x_2         
        y_train[i] = keras.utils.to_categorical(y_data, num_classes=4, dtype='float32')
    x_train = np.reshape(x_train,(batchsize,channel, win_train, 1))
    y_train = np.reshape(y_train,(batchsize,4))
    return x_train, y_train



def get_data(wn1,wn2,input_fname, down_simple=4):
    
    rawEEG = read_raw_cnt(input_fname, eog=(), misc=(), ecg=(), emg=(), data_format='auto', date_format='mm/dd/yy', preload=False, verbose=None)
    tmp = rawEEG.to_data_frame()
    tmp1 = tmp.values
    tmp2 = tmp1[:,-8:]
    train_data = tmp2[::down_simple,]
    
    events_from_annot, _ = mne.events_from_annotations(rawEEG, event_id = 'auto')
    train_label = [events_from_annot[i, 2] for i in range(events_from_annot.shape[0]) if (i%2 == 0)]
    train_start_time = [events_from_annot[i, 0] for i in range(events_from_annot.shape[0]) if (i%2 == 1)]
    
    channel_data_list = []
    for i in range(train_data.shape[1]):
        b, a = signal.butter(6, [wn1,wn2], 'bandpass')
        filtedData = signal.filtfilt(b, a, train_data[:,i])   #data为要过滤的信号
        channel_data_list.append(filtedData)
    channel_data_list = np.array(channel_data_list)
    
    return channel_data_list, train_label, train_start_time


def get_test_list(block_n):
    if block_n == 0:
        test_list = list(range(20))
    if block_n == 1:
        test_list = list(range(20, 40))
    if block_n == 2:
        test_list = list(range(40, 60))
    if block_n == 3:
        test_list = list(range(60, 80))
    if block_n == 4:
        test_list = list(range(80, 100))
    if block_n == 5:
        test_list = list(range(100, 120))
    
    return test_list

if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = "0,1"
    down_simple = 4
    fs = 1000/down_simple
    channel = 8
    batchsize = 1000
    f_down = 7
    f_up = 17
    wn1 = 2*f_down/fs
    wn2 = 2*f_up/fs
    
    total_av_acc_list = []
    t_train_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    for pre_selelct in range(1, 7):
        path=path='E:/better_data/0%d.cnt'%pre_selelct
        test_data, test_label, test_start_time = get_data(wn1, wn2, path, down_simple)
        av_acc_list = []
        for t_train in t_train_list:
            win_train = int(fs*t_train)
            print(t_train, pre_selelct)
            acc_list = []
            for block_n in range(6):
                model_path='D:/dwl/code_ssvep/DL/my_data_code/scnn/tcnn_model_0.1/c_model_0%d_%3.1fs_%d.h5'%(pre_selelct, t_train, block_n)
                model = load_model(model_path)
                print("load successed")
            
                test_list = get_test_list(block_n)
            
                x_true, y_true = datagenerator(batchsize, test_data, win_train, test_label, test_start_time, down_simple, test_list, channel)
                y_pred = model.predict(np.array(x_true))
                
                a, b = 0, 0
                pred, true = [], []
                for i in range (batchsize):
                    y_pred_ = np.argmax(y_pred[i])
                    pred.append(y_pred_)
                    y_true1  = np.argmax(y_true[i])
                    true.append(y_true1)
                    if y_true1 == y_pred_:
                        a += 1
                    else:
                        b+= 1
                acc = a/(a+b)
                # print(acc)
                acc_list.append(acc)
            # print(acc_list)
            mean_acc = np.mean(acc_list)
            print(mean_acc)
            av_acc_list.append(mean_acc)
        total_av_acc_list.append(av_acc_list)

    print(total_av_acc_list)
    
    # # save the results as excel
    # company_name_list = total_av_acc_list
    # df = pd.DataFrame(company_name_list)
    # df.to_excel("D:/dwl/results_0.1/ours/tcnn/tcnn_8channel_ours_.xlsx", index=False)