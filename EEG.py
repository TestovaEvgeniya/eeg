import numpy as np
import csv
import pylab
import math

eeg=[]
rangee=[]
percent=0.2
delta=0.7
iterator=0
artifacts=[]
artifacts_time=[]
answers=[1.16,1.71, 1.63, 2.58, 3.45, 5.625, 6.57, 7.11]
ao=[0,0,0,0,0,0,0,0]

artif=[]
artif_time=[]
with open('data.csv', 'rt', encoding='utf-8') as csvfile:
    eegreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in eegreader:
        eeg_row=[]
        for element in row:
            if len(element.split(' '))>1:
                eeg_row.append(float(element.split(' ')[len(element.split(' '))-1]))
        eeg.append(eeg_row)
        rangee.append([np.mean(eeg_row)-(max(eeg_row)-min(eeg_row))*percent, np.mean(eeg_row)+(max(eeg_row)-min(eeg_row))*percent])

eeg= np.array(eeg)

for row in eeg:
    artifacts.append([])
    artifacts_time.append([])
    time_iterator=0
    for element in row:
        if element < rangee[iterator][0] or  element >rangee[iterator][1]:
            artifacts[iterator].append(element)
            artifacts_time[iterator].append(time_iterator*1./121)
        time_iterator+=1
    iterator+=1
    
zeros=[]   
iterator=0   
for row in artifacts:
    artif.append([])
    zeros.append([])
    artif_time.append([])
    time_iterator=0
    for i in range(0, len(row)-2):
        if (row[i]>rangee[iterator][0] and row[i+1]<rangee[iterator][1]) or (row[i]<rangee[iterator][0] and row[i+1]>rangee[iterator][1]):
            if math.fabs(artifacts_time[iterator][i]-artifacts_time[iterator][i+1])<delta:
                artif_time[iterator].append((artifacts_time[iterator][i]+artifacts_time[iterator][i+1])/2)
                zeros[iterator].append(0)
            
    iterator+=1

time=[t*1./121 for t in range(len(eeg[0]))]
n_channels=np.shape(eeg)[0]

pylab.figure()
pylab.rcParams["figure.figsize"] = (60,60)


for ch in range(n_channels):
    pylab.subplot(n_channels,1,ch+1)
    pylab.plot(time,eeg[ch])
    pylab.axhline(y=rangee[ch][0], color='yellow')
    pylab.axhline(y=rangee[ch][1], color='yellow')
    pylab.scatter(artifacts_time[ch], artifacts[ch], color='green') 
    #pylab.scatter(artif_time[ch], zeros[ch], color='red')
    #pylab.scatter(answers, ao, color='black')
    for i in range(len(artif_time[ch])):
        pylab.axvline(x=artif_time[ch][i], color='red') 
    for i in range(len(answers)):
        pylab.axvline(x=answers[i], color='black')
pylab.show()


print(artif_time)






