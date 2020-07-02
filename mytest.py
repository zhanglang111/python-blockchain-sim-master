# import numpy as np
# import matplotlib.pyplot as plt
# fig,ax=plt.subplots()
# #这才是正太分布，设计初始的信誉值，
# a = np.random.normal(80,5,size=100) # 最小值,最大值,数量
#
# print(max(a))
# print(min(a))
#
# #假定有5俩车是恶意车辆。
# print(a)
# #将数据导入到txt文件中
# #统计有哪些是恶意车辆，
import numpy as np
import random

A = np.zeros((25235, 4), dtype=int)
dict = {}
arealistBytime={}
arealist = [[], [], [], []]
RSU = {}
validDict = {}
alpha = 0.3
#将位置改为相差10米都不算进去
#需要写一个，保存矩阵，看矩阵是否相同，找出不相同的点，然后用算法进行判断车辆的位置是否在合理的区间，而且这个区间要满足全部。
#是上一秒和下一秒的关系所以就只用的三维矩阵，4来存储就行了


def initSystem():
    read_data('vehicles.txt')  # 读取所有数据保存在A中
    Init_RSU(4)  # 设置A个RSU的地址
    dealMatrixSortByTime(A)  # 按时间分配车辆所在的位置

def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        id = 0
        for line in lines:
            list = line.split(',')
            A[id][:] = list[:]
            id += 1
#处理这个数据，将时间相同的数据拿出来，
# def get125to180sec():
#     for i in range(125,180):
#
#         validDict[i] =
def Init_RSU(s):
    index = 1
    for i in range(s):
        item = RSU.setdefault(i, {})
        item.setdefault('covRadius', 375)  # random.randint(500,700))
        item.setdefault('vehicles', {})
        if i == 0:
            item.setdefault('location', [375, 375])
        elif i == 1:
            item.setdefault('location', [1225, 375])
        elif i == 2:
            item.setdefault('location', [375, 1225])
        else:
            item.setdefault('location', [1225, 1225])
        index = index + 1
def dealMatrixSortByTime(A):
    a = range(300)
    #这里用字典保存
    for i in a:
        b = A[A[:,1]==i]
        dict[i] = b
def numCountinSec():
    listinSec = []
    for i in range(300):
        listinSec.append(dict[i].shape[0])
    return listinSec

def zone(sec):
    #这个dist就是没有分区的啊
    VehicleInSec = dict[sec]
    #这里应该是车辆的个数。再分区,#处理完之后需要释放这个list
    a = range(dict[sec].shape[0])
    for i in a:
        l = VehicleInSec[i,:].tolist()
        if (l[2]<=750)&(l[3]<=750):
            arealist[0].append(l)
            continue
        elif (l[2]<=1500)&(l[3]<=750):
            arealist[1].append(l)
            continue
        elif (l[2]<=750)&(l[3]<=1500):
            arealist[2].append(l)
            continue
        else:
            arealist[3].append(l)
            continue

##计算邻居
def AllNears():
    #得出4个矩阵
    subList = []
    for i in range(4):
        matrix = getNears(arealist[i],i)
        subList.append(matrix)
    return subList

# def judgeIsError(i,j):


def getNears(l,areaIndex):
    areaVehicleNums = len(l)
    if(areaVehicleNums<=1):
        return
    else:
        areaNearNet = np.zeros((areaVehicleNums,areaVehicleNums))
        for i in range(areaVehicleNums):
            for j in range(i+1,areaVehicleNums):
                if areaNearNet[i][j] == 1:
                    continue
                else:
                    lm = arealist[areaIndex][i]
                    ln = arealist[areaIndex][j]
                    if calculateDistance(lm[2],lm[3],ln[2],ln[3])<=100:
                        areaNearNet[i][j] = 1  #i,j互为邻居
                        areaNearNet[j][i] = 1  # i,j互为邻居
        return areaNearNet
def calculateDistance(lon1,lat1,lon2,lat2):
    distance = np.sqrt(np.square(lon2-lon1)+np.square(lat2-lat1))
    return distance

def predictLocationByHistoryLocation(list):
    prelocation = []
    prelocation.append(list[2][0]+alpha*(list[1][0]-list[0][0])+(1-alpha)*(list[2][0]-list[1][0]))
    prelocation.append(list[2][1] + alpha*(list[1][1] - list[0][1]) + (1-alpha)* (list[2][1] - list[1][1]))
    return prelocation

def judgeIsValidLocation(reportLocation,preloaction):
    #计算距离
    distance = calculateDistance(reportLocation[0],reportlocation[1],preloaction[0],preloaction[1])
    if(distance>10):
        return 0
    return 1
if __name__ == '__main__':
    initSystem()

    MaliciousVehicle = 0

    # #通过4块区域补成一大块区域？
    # for i in range(125,180):
    #     print(dict[i].shape)


    #前面3秒直接过
    for i in range(125,127):
        zone(i)
        sublistForeTime = AllNears()  # 四个区域的邻接表
        arealistBytime[i] = arealist  # 四个区域的车辆信息存储
        arealist = [[], [], [], []]



    for i in range(127,181):
        print("###########################################################")
        zone(i)
        sublistForeTime = AllNears() #四个区域的邻接表
        arealistBytime[i] = arealist #四个区域的车辆信息存储
        arealist = [[], [], [], []]
        zone(i+1)  # 划分车辆的区域
        sublistNowTime = AllNears()
        arealistBytime[i+1] = arealist
        arealist = [[], [], [], []]
        #四个区域分别对比
        for j in range(4):
            print("第"+str(i)+"秒第"+str(j)+"区域的车辆个数为"+str(len(sublistForeTime[j])))
            print("第" + str(i+1) + "秒第" + str(j) + "区域的车辆个数为" + str(len(sublistForeTime[j])))
            #这里不一致可以直接跳过，因为RSU已经做过处理。但如果是同时出现怎么办，实验假设一时刻仅有一辆车辆进行恶意数据的发送。
            if len(sublistForeTime[j])!=(len(sublistNowTime[j])):
                #这里怎么去处理

                continue
            judgeresult = (sublistForeTime[j] == sublistNowTime[j]).all()
            if not judgeresult:
                print("两秒之间的邻接矩阵内的数据对应不上，需要审核")
                print("---------------------------------")
            else:
                print("两秒之间邻接矩阵没有发生改变，不需要审核")
                print("---------------------------------")
                continue
            compareNode = (sublistForeTime[j] == sublistNowTime[j])
            resultindex = []
            for k in range(compareNode.shape[0]):
                for l in range(k, compareNode.shape[0]):
                    if not compareNode[k, l]:
                        resultindex.append([k, l])
            matrix_resultindex = np.array(resultindex)
            matrix_sublistForeTime = np.array(sublistForeTime[j])
            maxtrix_sublistNowTime = np.array(sublistNowTime[j])
            for l in range(matrix_resultindex.shape[0]):
                linkWithSusCountForeTime = 0
                linkWithSusCountNowTime = 0
                m = matrix_resultindex[l,1]
                # print(matrix_sublistForeTime[:,j])
                for n in matrix_sublistForeTime[:, m]:
                    if n == 1:
                        linkWithSusCountForeTime = linkWithSusCountForeTime + 1
                print("上一秒多少个与该车辆有联系")
                print(linkWithSusCountForeTime)

                for n in maxtrix_sublistNowTime[:, m]:
                    if n == 1:
                        linkWithSusCountNowTime = linkWithSusCountNowTime + 1
                print("当前与该车辆有联系")
                print(linkWithSusCountNowTime)

                #先把车辆的历史位置找出来
                locationList = []
                testlocationlist = []
                #表示125-127的三秒内，推测128秒是否正常
                # for t in range(i-2,i+1):
                #     testlocationlist.append(arealistBytime[t][j][m])
                # mytetslist = np.array(testlocationlist)
                # print(testlocationlist[])
                testlocationlist = []
                for t in range(i-2,i+1):
                    testlocationlist.append(dict[t][m,:])  # t代表时间，m代表第几个车辆（邻接矩阵的第几列）
                    locationList.append(dict[t][m,2:4]) #t代表时间，m代表第几个车辆（邻接矩阵的第几列）
                prelocation = predictLocationByHistoryLocation(locationList)
                #如果说预测的距离和真实的具体相差超过5米，就算位置出错
                # print("车辆在第")
                print(testlocationlist)
                print(locationList)
                print("预测位置"+str(prelocation))
                reportlocation = dict[t+1][m,2:4]
                print("报告位置"+str(reportlocation))
                isvalid = judgeIsValidLocation(reportlocation,prelocation)
                if not isvalid:
                    MaliciousVehicle = MaliciousVehicle+1
                    print("发现恶意车辆，车辆信息为#####################################%%%%%%%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$$$$$$$$$$#########################################&&&&&&&&&%%%%%%%%%%%%%")
                    print(dict[t+1][m,:])
                else:
                    print("车辆的位置正常，已被排除为恶意车辆")

    print(MaliciousVehicle)









