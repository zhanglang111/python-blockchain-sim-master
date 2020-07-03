import numpy as np
from BlockChain import *
from enum import Enum

import threading
import math

#初始化区块链
testBlock = Blockchain()
testBlock.create_genesis_block()

#全局的基于时间的车辆位置HASH和车辆关系HASH
dict_timeVehicleLocation_HASH = {}
dict_timeVehicleLink_HASH = {}

#车辆信誉值的参数，正态分布
mu = 80  # 期望为1
sigma = 4  # 标准差为3
num = 100  # 个数为10000

NearDistance = 100

A = np.zeros((24974, 4), dtype=int)
VehicleInsec = []

class myThread (threading.Thread):
    def __init__(self, threadID, name, lon,lat):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.lon = lon
        self.lat = lat
    def run(self):
        print("开始线程：" + self.name)
        tran_system(self.name, self.lon, self.lat,125,181)
        print("退出线程：" + self.name)

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
#数据上链
def UploadDataToBlockChain(toUpDta):
    json_str = json.dumps(toUpDta.__dict__)
    # print(json_str)
    testBlock.add_new_transaction(json_str)
    testBlock.mine()
    #想得到最后一个区块的hash,先试试
    return testBlock.chain[-1].hash



#这里面是主要的处理逻辑
def tran_system(name,lon,lat,timeStart,timeEnd):

    #这是车辆的位置信息与邻接矩阵，并没有合成车辆的轨迹信息
    #车辆的轨迹信息是需要使用区块链的方式继续宁获取的

    #不会造成死锁，因为是下一次再使用。

    for timesec in range(timeStart,timeEnd):
        LocationHashItem =  dict_timeVehicleLocation_HASH.setdefault(timesec,{})
        LinkHashItem = dict_timeVehicleLink_HASH.setdefault(timesec,{})
        VehicleInSecTime = A[A[:, 1] == timesec]
        VehiclesInArea = []
        for VehicleIndex in range(VehicleInSecTime.shape[0]):
            l = VehicleInSecTime[VehicleIndex, :].tolist()
            if (l[2] <= lon) & (l[3] <= lat):
                VehiclesInArea.append(l)
        #根据车辆的位置建立邻接矩阵

        NearsLinkInArea = getNearlink_Matrix(VehiclesInArea)
        #
        # print(type(VehiclesInArea))
        # print(type(VehiclesInArea))
        ##将邻接矩阵转为列表形式进行上传到区块链。
        list_NearsLinkInArea =  MatrixToList(NearsLinkInArea)
        # print(type(list_NearsLinkInArea))

        #车辆位置的上链以及邻接矩阵的上链
        if((lon == 750)&(lat == 750)):
            VehiclesInAreaToUpdate = Arealist(timesec,0,VehiclesInArea)
            time_Area_locationHash = UploadDataToBlockChain(VehiclesInAreaToUpdate)
            LocationHashItem.setdefault(0, time_Area_locationHash)

            NearsLinkInAreaToUpdate = NearsMarix(timesec, 0, list_NearsLinkInArea)
            time_Area_linkHash = UploadDataToBlockChain(NearsLinkInAreaToUpdate)
            LinkHashItem.setdefault(0, time_Area_linkHash)
        elif ((lon == 1500) & (lat == 750)):
            VehiclesInAreaToUpdate = Arealist(timesec, 1, VehiclesInArea)
            time_Area_locationHash = UploadDataToBlockChain(VehiclesInAreaToUpdate)
            LocationHashItem.setdefault(0, time_Area_locationHash)

            NearsLinkInAreaToUpdate = NearsMarix(timesec, 1, list_NearsLinkInArea)
            time_Area_linkHash = UploadDataToBlockChain(NearsLinkInAreaToUpdate)
            LinkHashItem.setdefault(0, time_Area_linkHash)
        elif ((lon == 750) & (lat == 1500)):
            VehiclesInAreaToUpdate = Arealist(timesec, 2, VehiclesInArea)
            time_Area_locationHash = UploadDataToBlockChain(VehiclesInAreaToUpdate)
            LocationHashItem.setdefault(0, time_Area_locationHash)

            NearsLinkInAreaToUpdate = NearsMarix(timesec, 2, list_NearsLinkInArea)
            time_Area_linkHash = UploadDataToBlockChain(NearsLinkInAreaToUpdate)
            LinkHashItem.setdefault(0, time_Area_linkHash)
        else:
            VehiclesInAreaToUpdate = Arealist(timesec, 3, VehiclesInArea)
            time_Area_locationHash = UploadDataToBlockChain(VehiclesInAreaToUpdate)
            LocationHashItem.setdefault(0, time_Area_locationHash)

            NearsLinkInAreaToUpdate = NearsMarix(timesec, 3, list_NearsLinkInArea)
            time_Area_linkHash = UploadDataToBlockChain(NearsLinkInAreaToUpdate)
            LinkHashItem.setdefault(0, time_Area_linkHash)



def getNearlink_Matrix(VehiclesInArea):
    areaVehicleNums = len(VehiclesInArea)
    areaNearNet = np.zeros((areaVehicleNums, areaVehicleNums))
    # 计算邻接矩阵
    if (areaVehicleNums <= 1):
        return
    for i in range(areaVehicleNums):
        for j in range(i + 1, areaVehicleNums):
            if areaNearNet[i][j] == 1:
                continue
            else:
                # 如果没有计算过则计算两车之间的距离
                lm = VehiclesInArea[i]
                ln = VehiclesInArea[j]
                if calculateDistance(lm[2], lm[3], ln[2], ln[3]) <= NearDistance:
                    areaNearNet[i][j] = 1  # i,j互为邻居
                    areaNearNet[j][i] = 1  # i,j互为邻居
    return areaNearNet
def calculateDistance(lon1,lat1,lon2,lat2):
    distance = np.sqrt(np.square(lon2-lon1)+np.square(lat2-lat1))
    return distance

def MatrixToList(NearsLinkInArea):
    list_NearsLinkInArea = []
    for i in range(NearsLinkInArea.shape[0]):
        list_NearsLinkInArea.append(NearsLinkInArea[i, :].tolist())
    return list_NearsLinkInArea


if __name__ == '__main__':

    #首先先加载数据
    read_data('vehicles.txt')

    ArealistLocation = [[750,750],[1500,750],[750,1500],[1500,1500]]


    thread0 = myThread(0, "Area_0", ArealistLocation[0][0], ArealistLocation[0][1])


    thread0.start()


    # initSystem()
    # # initSecondSubAreaSunlocationAndlink()
    #
    #
    # for secondIndex in range(125, 181):
    #     #弄成分布式只需要找到车辆的位置
    #     mySecondItem = dict_VehicleTimeAndArea.setdefault(secondIndex, {})
    #     #这里可能需要初始化一个
    #     myAreaList = initZone(secondIndex)  # 每一秒的位置区域划分
    #     nearLinkList = AllNears()  # 四个区域的邻接表
    #     for AreaIndex in range(4):
    #         myAreaItem = mySecondItem.setdefault(AreaIndex, {})
    #         myAreaItem.setdefault("matrix_location", myAreaList[AreaIndex])
    #         myAreaItem.setdefault("matrix_nearlink", nearLinkList[AreaIndex])
    #     print("1")
    #
    # print("dasda")
    # print(dict_VehicleTimeAndArea)
