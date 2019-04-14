# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class DataFangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    subarea = scrapy.Field()        # 一级区域
    area = scrapy.Field()           # 当前城市
    housecoord = scrapy.Field()     # 楼盘坐标
    housename = scrapy.Field()      # housename
    housename2 = scrapy.Field()     # 别名
    houseproperty = scrapy.Field()  # 楼盘标签
    _id = scrapy.Field()            # 楼盘url
    source = scrapy.Field()         # 来源
    allstatus = scrapy.Field()      # 采集状态
    houseprice = scrapy.Field()     # 均价
    houseatr = scrapy.Field()       # 物业类别
    housetype = scrapy.Field()      # 建筑类别
    years = scrapy.Field()          # 产权年限
    decoration = scrapy.Field()     # 装修状况
    developer = scrapy.Field()      # 开发商
    houseaddress = scrapy.Field()       # 楼盘地址
    salestatus = scrapy.Field()         # 销售状态
    startSaleString = scrapy.Field()        # 开盘时间
    endSaleString = scrapy.Field()          # 交房时间
    saleaddress = scrapy.Field()        # 售楼地址
    landarea = scrapy.Field()           # 占地面积
    housearea = scrapy.Field()          # 建筑面积
    plotratio = scrapy.Field()          # 容积率
    greenrate = scrapy.Field()          # 绿化率
    carsite = scrapy.Field()            # 停车位
    housecount = scrapy.Field()         # 楼栋总数
    allcount = scrapy.Field()           # 总户数
    managecompany = scrapy.Field()      # 物业公司
    managefee = scrapy.Field()          # 物业费
    floorCondition = scrapy.Field()     # 楼层状况
    fetch_time = scrapy.Field()         # 采集时间
    insoect = scrapy.Field()            # 采集状态



    startsaletime = scrapy.Field()         # 楼盘评论
    endsaletime = scrapy.Field()         # 楼盘评论

class DataDynamicJson(scrapy.Item):

    dynamicJson = scrapy.Field()        # 楼盘动态
    soutse = scrapy.Field()        # 楼盘动态
    title = scrapy.Field()        # 楼盘动态
    content = scrapy.Field()        # 楼盘动态
    publishDate = scrapy.Field()        # 楼盘动态
    _id = scrapy.Field()        # 楼盘动态

class DataDynamicJson1(scrapy.Item):
    dynamicJson = scrapy.Field()
    _id = scrapy.Field()




class DataCommentJson(scrapy.Item):
    commentJson = scrapy.Field()    # 楼盘评论
    sourceUrl = scrapy.Field()    # 楼盘评论
    source = scrapy.Field()    # 楼盘评论
    content = scrapy.Field()    # 楼盘评论
    createDate = scrapy.Field()    # 楼盘评论
    userNick = scrapy.Field()    # 楼盘评论
    _id = scrapy.Field()    # 楼盘评论


class DataHouseapartment(scrapy.Item):
    houseapartment = scrapy.Field()     # 户型json
    houseUrl = scrapy.Field()     # 户型json
    name = scrapy.Field()     # 户型json
    salesStatus = scrapy.Field()     # 户型json
    roomNum = scrapy.Field()     # 户型json
    hallNum = scrapy.Field()     # 户型json
    toiletNum = scrapy.Field()     # 户型json
    constructSpace = scrapy.Field()     # 户型json
    price = scrapy.Field()     # 户型json
    propertyType = scrapy.Field()     # 户型json
    remark = scrapy.Field()     # 户型json
    imgs = scrapy.Field()     # 户型json
    totalPrices = scrapy.Field()     # 户型json
    _id = scrapy.Field()     # 户型json


class DataPicJson(scrapy.Item):
    picJson = scrapy.Field()
    picUrl = scrapy.Field()
    _id = scrapy.Field()
    type = scrapy.Field()

class Image(scrapy.Item):
    _id = scrapy.Field()    # url
    content = scrapy.Field()    # img
    fileSaveFlag = scrapy.Field()   # 是否下载成功
    file_source = scrapy.Field()    # 来源

class ImageItem(scrapy.Item):
     _id = scrapy.Field()
     images = scrapy.Field()
     image_paths = scrapy.Field()
