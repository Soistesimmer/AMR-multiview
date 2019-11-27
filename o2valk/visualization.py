import matplotlib.pyplot as plt
import re
import time

import numpy as np


def read_bleu_file(filename):
    with open(filename, 'r')as file:
        x, y = [], []
        for line in file.readlines():
            if line.startswith('BLEU'):
                bleu=re.findall(r'BLEU\s=\s(\d+\.\d+)?,',line)[0]
                y.append(float(bleu))
            else:
                x.append(int(line[:-2]))
    return np.array(x),np.array(y)

def bleu_plot_figure(x, y, m):
    plt.axis([0, 25, 8, 35.])
    plt.xlabel('Epoch')
    plt.ylabel('BLEU Score')

    plt.plot(x/1e4,y,'C1-',label=m)

    plt.legend(loc='best')
    plt.show()

def read_log_file(filename, count):
    with open(filename, 'r')as file:
        time_record=[]
        for line in file.readlines():
            line_split=line.split()
            if len(line_split)>4 and line_split[4]=='train':
                time_record.append((' '.join(line.split()[:2]))[1:-4])
            elif len(time_record)>0 and time_record[-1]!='<sep>':
                time_record.append('<sep>')
    time_record=time_record[:count]
    total_time=0
    last_time=0
    for time_tmp in time_record:
        if time_tmp=='<sep>':
            last_time=0
            continue
        this_time = time.mktime(time.strptime(time_tmp, "%Y-%m-%d %H:%M:%S"))
        if last_time < 1e-6:
            pass
        else:
            total_time+=this_time-last_time
        last_time=this_time
    return int(total_time/count)

def speed_analysis(time_list, x_labels):
    print(time_list)
    plt.xlabel('model')
    plt.ylabel('second')
    plt.ylim([0,200])
    plt.bar(x_labels, time_list,width=0.5)
    plt.show()

if __name__ == '__main__':
    # filename='E:/PyCharmProjects/work-code-20190910/o2valk/result/bleu_result_c.txt'
    # x, y = read_bleu_file(filename)
    # bleu_plot_figure(x, y, 'combine')
    total=150
    filename='result/all_webnlg.log'
    all_time=read_log_file(filename,total)
    filename='result/reconstructor_webnlg.log'
    reconstructor_time=read_log_file(filename,total)
    filename='result/biaffine_webnlg.log'
    biaffine_time=read_log_file(filename,total)
    filename='result/baseline_webnlg.log'
    baseline_time=read_log_file(filename,total)
    speed_analysis([baseline_time,biaffine_time,reconstructor_time,all_time],['baseline','+biaffine classifier','+reconstructor','+all'])

