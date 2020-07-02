import numpy as np
# import os
A = np.zeros((24974, 4), dtype=int)
dict = {} #按照时间划分的车辆字典
dict_VehicleDataByID = {} #按照车辆ID划分的车辆字典
arealistBytime={}
arealist = [[], [], [], []]
RSU = {}
validDict = {}

alpha = 0.3 #指数平滑的参数
bata = 0.1 #恶意车辆发送虚假GPS的概率
MaliciousVehicleID = np.random.randint(14, 99, 4).tolist()
AllRandData = {}

def initSystem():
    read_data('vehicles.txt')  # 读取所有数据保存在A中
    Init_RSU(4)  # 设置A个RSU的地址
    dealMatrixSortByID(A)  # 按照车辆ID组成的字典
    dealMatrixSortByTime(A)  # 按时间分配车辆所在的位置

def GenerateRandomData():
    randRowData = []
    for randNumItem in MaliciousVehicleID:
        randRowData = []
        randTime = np.random.randint(125, 180, int((180 - 125) * bata))
        for randTimeItem in randTime:
            randLon = np.random.randint(0, 1500)
            randlat = np.random.randint(0, 1500)

            randRowData.append([randNumItem,randTimeItem,randLon,randlat])

        AllRandData[randNumItem] = randRowData


def dealMatrixSortByID(A):
    # 这里用字典保存
    for i in range(100):
        # if i == 13:
        #     break
        b = A[A[:, 0] == i]
        dict_VehicleDataByID[i] = b

    # a = range(300)
    # # 这里用字典保存
    # for i in a:
    #     b = A[A[:, 1] == i]
    #     dict[i] = b

def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        id = 0
        for line in lines:
            list = line.strip('\n').split(',')
            # print(list)
            A[id][:] = list[:]
            # A.append(list)
            id += 1
    # print(A)
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
    distance = calculateDistance(reportLocation[0],reportLocation[1],preloaction[0],preloaction[1])
    if(distance>10):
        return 0
    return 1

def replaceMaliciousData():
    for i in range(len(AllRandData)):
        matrix_temp = np.array(AllRandData[MaliciousVehicleID[i]])
        # print(matrix_temp)
        timeList = matrix_temp[:, 1]
        for j in range(len(timeList)):
            # 到底变化谁，那个是按照时间变化的。变化A也不对啊。
            # 直接对dict进行变化？j
            # 这个时间的第i个车辆
            # print("修改前")
            # print(dict[timeList[j]][MaliciousVehicleID[i] - 1])
            # # 将数据进行修改
            # print("修改后")
            # print(AllRandData[MaliciousVehicleID[i]][j])
            dict[timeList[j]][MaliciousVehicleID[i] - 1] = AllRandData[MaliciousVehicleID[i]][j]



if __name__ == '__main__':
    #初始化车辆数据，包括车辆数据的读入，按照时间进行划分为字典，初始化RSU
    initSystem()
    GenerateRandomData()
    replaceMaliciousData()
    print(MaliciousVehicleID)
    MaliciousVehicle = 0

    # 前面3秒直接过
    for i in range(125,127):
        zone(i)
        sublistForeTime = AllNears()  # 四个区域的邻接表
        arealistBytime[i] = arealist  # 四个区域的车辆信息存储
        arealist = [[], [], [], []]


    for times in range(2):
        for i in range(127,181):
            # print("###########################################################")
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
                #这里不一致可以直接跳过，因为RSU已经做过处理。但如果是同时出现怎么办，实验假设一时刻仅有一辆车辆进行恶意数据的发送。
                #说明矩阵维度不一样
                areaStateChange = abs(len(sublistForeTime[j]) - len(sublistNowTime[j]))
                if areaStateChange>0:
                    matrix_inareaFormTime = []
                    matrix_inareaNowTime = []
                    matrix_inareaFormTime = np.array(arealistBytime[i][j])#i代表第i秒，j代表区域
                    matrix_inareaNowTime = np.array(arealistBytime[i+1][j])
                    formState = matrix_inareaFormTime[:, 0].tolist() #
                    #找出多的或者少的那个索引，因为前后两个矩阵的维度不一样，因为第一列代表的是id
                    nowState = matrix_inareaNowTime[:,0].tolist()
                    minlen = min(len(formState),len(nowState))
                    if len(formState) - len(nowState) > 0:
                        SmallStateChange = nowState
                        BiggerStateChange = formState
                    else:
                        SmallStateChange = formState
                        BiggerStateChange = nowState
                    # print(SmallStateChange)
                    # print(BiggerStateChange)
                    # print("现在是"+str(i)+"秒")
                    SusVehicle = []
                    while areaStateChange>0:
                        for k in range(minlen):
                            if SmallStateChange[k] != BiggerStateChange[k]:
                                SusVehicle.append(BiggerStateChange[k])
                                BiggerStateChange.pop(k)
                                areaStateChange = areaStateChange-1
                                if areaStateChange == 0:
                                    break
                    # 这是车辆的id
                    for item in SusVehicle:
                        testlocationlist = []
                        locationList = []
                        if (item > 13):
                            for t in range(i - 2, i + 1):
                                testlocationlist.append(dict[t][item-1, :])  # t代表时间，m代表第几个车辆（邻接矩阵的第几列）
                                locationList.append(dict[t][item-1, 2:4])  # t代表时间，m代表第几个车辆（邻接矩阵的第几列）
                        else:
                            for t in range(i - 2, i + 1):
                                testlocationlist.append(dict[t][item, :])  # t代表时间，m代表第几个车辆（邻接矩阵的第几列）
                                locationList.append(dict[t][item, 2:4])  # t代表时间，m代表第几个车辆（邻接矩阵的第几列）
                        # print(locationList)
                        # print(testlocationlist)
                        prelocation = predictLocationByHistoryLocation(locationList)

                        reportlocation = []
                        if(item>13):
                            reportlocation = dict[t + 1][item-1, 2:4]
                        else:
                            reportlocation = dict[t + 1][item, 2:4]
                        # print("上报的位置为")
                        # print(reportlocation)
                        isvalid = judgeIsValidLocation(reportlocation, prelocation)
                    if not isvalid:
                        MaliciousVehicle = MaliciousVehicle + 1
                        print("发现恶意车辆，车辆信息为#####################################%%%%%%%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$$$$$$$$$$#########################################&&&&&&&&&%%%%%%%%%%%%%")
                        print(dict[t + 1][item-1, :])
                    # else:
                    #     print("车辆的位置正常，已被排除为恶意车辆")
                else:
                    judgeresult = (sublistForeTime[j] == sublistNowTime[j]).all()
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
                        # print("上一秒多少个与该车辆有联系")//这里可能是设计其他的算法在这里面，后面再加吧，区块链的功能还没实现呢。
                        # print(linkWithSusCountForeTime)

                        for n in maxtrix_sublistNowTime[:, m]:
                            if n == 1:
                                linkWithSusCountNowTime = linkWithSusCountNowTime + 1
                        # print("当前与该车辆有联系")
                        # print(linkWithSusCountNowTime)

                        #先把车辆的历史位置找出来
                        locationList = []
                        testlocationlist = []
                        for t in range(i-2,i+1):
                            testlocationlist.append(dict[t][m,:])  # t代表时间，m代表第几个车辆（邻接矩阵的第几列）
                            locationList.append(dict[t][m,2:4]) #t代表时间，m代表第几个车辆（邻接矩阵的第几列）
                        prelocation = predictLocationByHistoryLocation(locationList)
                        # print("车辆在第")
                        # print(testlocationlist)
                        # print(locationList)
                        # print("预测位置"+str(prelocation))
                        reportlocation = dict[t+1][m,2:4]
                        # print("报告位置"+str(reportlocation))
                        isvalid = judgeIsValidLocation(reportlocation,prelocation)
                        if not isvalid:
                            MaliciousVehicle = MaliciousVehicle+1
                            print("发现恶意车辆，车辆信息为#####################################%%%%%%%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$$$$$$$$$$#########################################&&&&&&&&&%%%%%%%%%%%%%")
                            print(dict[t+1][m,:])
                        # else:
                        #     print("车辆的位置正常，已被排除为恶意车辆")

    print(MaliciousVehicle)









