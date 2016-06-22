# coding=utf-8
import numpy as np
def loadDataSet():
	dataMat = []
	labelMat = []
	fr = open('testset.txt')
	for line in fr.readlines():
		lineArr = line.strip().split()
		dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
		labelMat.append(int(lineArr[2]))
	return dataMat, labelMat
def gradAscent(dataMatIn, classLabels):
	dataMatrix = np.mat(dataMatIn)
	xs = dataMatrix[:,1:]
	labelMat = np.mat(classLabels).transpose()
	m, n = np.shape(xs)
	alpha = 0.01
	maxCycles = 1000
	weights=np.ones((n,1))
	bias = 1.0
	for k in range(maxCycles):
		f = np.array(labelMat) * (np.array(xs * weights)+bias)
		choices = f <= 0
		if not choices.max():
			break
		errorclassxs = xs[choices[:,0],:]
		errorclasslabel = labelMat[choices[:,0],:]
		weights = weights + alpha*(errorclassxs.T*errorclasslabel)
		bias = bias + alpha*sum(errorclasslabel)[0,0]
	l = weights.reshape(1,len(weights))[0].tolist()[0]
	l.insert(0,bias)

	return np.array(l).reshape(len(l),1)
		
		
def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat, labelMat = loadDataSet()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2] 
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()
