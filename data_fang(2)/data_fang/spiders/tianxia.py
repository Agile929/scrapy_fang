# -*- coding: utf-8 -*-
import scrapy, json

from lxml import etree
from ..items import DataFangItem, DataDynamicJson, DataDynamicJson1, DataCommentJson, DataPicJson, \
    DataHouseapartment, ImageItem
import re, io
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep


class TianxiaSpider(scrapy.Spider):
    name = "tianxia"
    allowed_domains = ["fang.com"]
    city_link_list = io.open(r"/home/kevin/Desktop/data_fang/data_fang/spiders/城市url", "r", encoding="gbk")
    # city_link_list = city_link_list.readline()
    for link in city_link_list:
        start_urls = link.replace("\n", "")
        start_urls = [start_urls]
        print("999", start_urls)

    def __init__(self):
        super(TianxiaSpider, self).__init__()

        # self.all_comment_dict = {}

        # self.dynamicJson = ""
        self.dynamicJson = []

    def parse(self, response):
        # 解析每个城市
        print("0312", response.url)
        new_house = response.xpath(
            "//div[@class='newnav20141104nr']//div/a[contains(text(),'新房')]/@href").extract()[0]  # 获取新房url
        # new_house = "".join(new_house)
        new_house = re.sub(r"\?\w+\=\w+", "", new_house)  # 去掉？后面的字符
        print("url", new_house)
        yield scrapy.Request(new_house, callback=self.parse_all_house)

    def parse_all_house(self, response):
        # 解析所有房源
        url = response.url
        url = ''.join(url)

        # all_house = response.xpath("//*[@class='clearfix']/div/a/@href ").extract_first()  # 获取当前页面所有的房源url
        all_house = response.xpath("//*[@class='clearfix']/div/a/@href ").extract()  # 获取当前页面所有的房源url
        for one_house in all_house:
            house = u"https:" + one_house
            # house = u"https:" + all_house
            house = re.sub(r"\?\w+=\w+_\w+", "", house)  # 去掉？后面的字符
            # print("房源", house)
            yield scrapy.Request(house, callback=self.home_page)

        The_next_page = response.xpath(
            '//li[@class="floatr rankWrap"]/div/a[contains(text(),">")]/@href').extract_first()  # 获取下一页
        if The_next_page != None:
            The_next_page = url + The_next_page
            yield scrapy.Request(The_next_page, callback=self.parse_all_house)

    # def parse_all_house(self, response):
    #     # 解析所有房源
    #     url = response.url
    #     url = ''.join(url)
    #
    #     # all_house = response.xpath("//*[@class='clearfix']/div/a/@href ").extract_first()  # 获取当前页面所有的房源url
    #     all_house = response.xpath("//*[@class='clearfix']/div/a/@href ").extract()  # 获取当前页面所有的房源url
    #     for one_house in all_house:
    #         house = u"https:" + one_house
    #         # house = u"https:" + all_house
    #         house = re.sub(r"\?\w+=\w+_\w+", "", house)  # 去掉？后面的字符
    #         # print("房源", house)
    #         # house = "https://123833.fang.com/"
    #         yield scrapy.Request(house, callback=self.home_page)
    #
    #     pages = response.xpath(
    #         '//div[@class="page"]/ul/li/a/@href').extract()  # 获取下一页
    #     # pages = url + pages
    #     for the_next_page in pages:
    #         if the_next_page != 'javascript:void(0)':
    #             the_next_page = url + the_next_page
    #             print("下一页", the_next_page)
    #             yield scrapy.Request(the_next_page, callback=self.parse_all_house)
    #
    #
    #     # the_next_page = response.xpath(
    #     #     '//li[@class="floatr rankWrap"]/div/a[contains(text(),">")]/@href').extract_first()  # 获取下一页
    #     # # print("909090", the_next_page)
    #     # # the_next_page = url + the_next_page
    #     # if the_next_page is not None:
    #     #     the_next_page = url + the_next_page
    #     #     # print("下一页", the_next_page)
    #     #     yield scrapy.Request(the_next_page, callback=self.parse_all_house)

    def home_page(self, response):
        # 解析首页获取详情页
        item = DataFangItem()
        item['_id'] = response.url
        # print("_id", item['_id'])
        item['subarea'] = response.xpath('//div[@class="br_left"]//ul[@class="tf f12"]//li[3]/a/text()').extract()
        item['subarea'] = "".join(item['subarea'])  # 字符串切片，去掉后面2个字
        item['subarea'] = item['subarea'][:-2]
        item['area'] = response.xpath('//div[@class="s2"]/div/a/text()').extract()  # 当前城市
        item['area'] = "".join(item['area']).replace(",", "")
        print("区域", item['subarea'])
        print("城市", item['area'])

        positioning = response.xpath("//div[@class='mapbox_dt']/iframe/@src").extract_first()  # 获取楼盘定位地址
        print(positioning)
        positioning = u"https:" + positioning

        particulars = response.xpath("//*[@class='navleft tf']//a[contains(text(),'详情')]/@href|"
                                     "//*[@class='navleft tf']//a[contains(text(),'详细')]/@href").extract()  # 楼盘详情
        particulars = "".join(particulars)
        particulars = u"https:" + particulars
        print("楼盘详情", particulars)
        # yield scrapy.Request(positioning, meta={"item": item, "xiangqing": particulars}, callback=self.positioning)

        # try:
        #     dynamic = response.xpath("//*[@class='navleft tf']//a[contains(text(),'动态')]/@href").extract()  # 楼盘动态
        #     dynamic = "".join(dynamic)
        #     dynamic = u"https:" + dynamic
        #     print("楼盘动态", dynamic)
        #     yield scrapy.Request(dynamic, callback=self.parse_dynamic)
        # except Exception as e:
        #     pass

        # try:
        #     comments = response.xpath(
        #         "//*[@class='navleft tf']//a[contains(text(),'点评')]/@href").extract_first()  # 楼盘点评
        #     comments = "".join(comments)
        #     comments = u"https:" + comments
        #     print("楼盘评论", comments)
        #     yield scrapy.Request(comments, callback=self.parse_comments)
        # except Exception as e:
        #     pass

        # try:
        #     houseapartment = response.xpath(
        #         "//*[@class='navleft tf']//a[contains(text(),'户型')]/@href").extract_first()  # 楼盘户型
        #     print("户型", houseapartment)
        #     # houseapartment = "".join(houseapartment)
        #     houseapartment = u"https:" + houseapartment
        #     yield scrapy.Request(houseapartment, callback=self.parse_houseapartment)
        # except Exception as e:
        #     pass

        try:
            houseImage = response.xpath(
                "//*[@class='navleft tf']//a[contains(text(),'相册')]/@href").extract_first()  # 楼盘相册
            if not houseImage:
                yield {"_id": item['_id'], "houseImage": json.dumps([])}
            houseImage = u"https:" + houseImage
            yield scrapy.Request(houseImage, meta={"_id": response.url}, callback=self.parse_image_base)
        except Exception as e:
            pass

    # def parse_picJson(self, response):
    #     # item = Data_picJson()
    #     a = response.url
    #     print("123", a)
    #     # url = re.sub(r"\w+\/\d+.htm","",a)
    #     # item["_id"] = url
    #     all_data = response.xpath('//dl[@class="dl"]//dd//span[contains(text(),"效果图")]/../em/text()|'
    #                               '//dl[@class="dl"]//dd//span[contains(text(),"实景图")]/../em/text()|'
    #                               '//dl[@class="dl"]//dd//span[contains(text(),"交通图")]/../em/text()|'
    #                               '//dl[@class="dl"]//dd//span[contains(text(),"样板间")]/../em/text()').extract()
    #     print(all_data)
    #     for i in range(1, len(all_data)):
    #         # data = re.search(r"(\d+)", i).group(1)
    #         all_data[i] = all_data[i] // 6 + 1 if all_data[i] % 6 else all_data[i] // 6
    #         # print("数据", data)
    #
    #     all_photo_url = response.xpath('//dl[@class="dl"]//dd//span[contains(text(),"效果图")]/../@href|'
    #                                    '//dl[@class="dl"]//dd//span[contains(text(),"实景图")]/../@href|'
    #                                    '//dl[@class="dl"]//dd//span[contains(text(),"交通图")]/../@href|'
    #                                    '//dl[@class="dl"]//dd//span[contains(text(),"样板间")]/../@href').extract()
    #     for i in range(len(all_photo_url)):
    #         photo_url = u"https:" + all_photo_url[i]
    #         # print("8989", photo_url)
    #
    #         yield scrapy.Request(photo_url, meta={"data": all_data[i]}, callback=self.parse_photo)
    #     # all_data = response.xpath('//dl[@class="dl"]//dd//span[contains(text(),"效果图")]/..|'
    #     #                           '//dl[@class="dl"]//dd//span[contains(text(),"实景图")]/..|'
    #     #                           '//dl[@class="dl"]//dd//span[contains(text(),"交通图")]/..|'
    #     #                           '//dl[@class="dl"]//dd//span[contains(text(),"样板间")]/..').extract()
    #     # for i in all_data:
    #     #     data = re.search(r"(\d+)",i).group(1)
    #     #     print("数据",data)

    def parse_image_base(self, response):
        """
        使用正则的方法匹配url,并且直接使用ajax请求
        :return:
        """
        html = response.text
        _id = response.meta["_id"]
        building_name = re.search(r"//(\w+)\.", response.url).group(1)
        building_number = re.search(r"(\d+)\.htm", response.url).group(1)
        module_dict = {}
        image_list = []
        re_effect_image = re.compile(r"\<a\W.*?\<span\>效果图\<\/span\>.*?\<\/a\>")
        re_realsight_image = re.compile(r"\<a\W.*?\<span\>实景图\<\/span\>.*?\<\/a\>")
        re_traffic_image = re.compile(r"\<a\W.*?\<span\>交通图\<\/span\>.*?\<\/a\>")
        re_prototype_room = re.compile(r"\<a\W.*?\<span\>样板间\<\/span\>.*?\<\/a\>")

        effect_image = re_effect_image.findall(html)
        realsight_image = re_realsight_image.findall(html)
        traffic_image = re_traffic_image.findall(html)
        prototype_room = re_prototype_room.findall(html)

        pattern_url = re.compile(r"//.*?htm")
        pattern_num = re.compile(r"<em>(\d+)<\/em>")

        # use interface to get data directly
        effect_number, realsight_number, traffic_number, prototype_number = (0, 0, 0, 0)
        if effect_image:
            try:
                effect_image_url = "http:" + pattern_url.findall(effect_image[0])[0]
                effect_number = int(pattern_num.search(effect_image[0]).group(1))
                module_dict.update({"xiaoguotu": [effect_number, effect_image_url, 904]})
            except Exception as e:
                print(str(e))
                effect_number = 0
        if realsight_image:
            try:
                realsight_image_url = "http:" + pattern_url.findall(realsight_image[0])[0]
                realsight_number = int(pattern_num.search(realsight_image[0]).group(1))
                module_dict.update({"shijingtu": [realsight_number, realsight_image_url, 903]})
            except Exception as e:
                print(str(e))
                realsight_number = 0
        if traffic_image:
            try:
                traffic_image_url = "http:" + pattern_url.findall(traffic_image[0])[0]
                traffic_number = int(pattern_num.search(traffic_image[0]).group(1))
                module_dict.update({"jiaotongtu": [traffic_number, traffic_image_url, 901]})
            except Exception as e:
                print(str(e))
                traffic_number = 0
        if prototype_room:
            try:
                prototype_room_url = "http:" + pattern_url.findall(prototype_room[0])[0]
                prototype_number = int(pattern_num.search(prototype_room[0]).group(1))
                module_dict.update({"yangbanjian": [prototype_number, prototype_room_url, 905]})
            except Exception as e:
                print(str(e))
                prototype_number = 0

        # 判断如果各种图全部没有，则直接返回
        if effect_number + realsight_number + traffic_number + prototype_number == 0:
            print("一张图片都没有")
            yield {"_id": _id, "picJson": json.dumps("", ensure_ascii=False)}
        # print(module_dict)
        else:
            full_image_interface_list = []
            for key, value in module_dict.items():
                base_url = "http://" + building_name + ".fang.com/house/ajaxrequest/photolist_get.php?newcode=" + building_number + "&type=" + str(
                    value[2]) + "&room=&nextpage="

                page_number = value[0] // 6 + 2 if value[0] % 6 else value[0] // 6 + 1

                [full_image_interface_list.append([base_url + str(i), key]) for i in range(1, page_number)]
            first_url = full_image_interface_list.pop()
            meta = {"_id": _id, "request_list": full_image_interface_list, "type": first_url[1], "json_data": []},
            yield scrapy.Request(first_url[0], meta={"item": meta}, callback=self.parse_images)

    def parse_images(self, response):
        """

        :param total_number: total number of images of effect
        :param style_number: total number of images of effect
        :return:
        """
        # image url can be get through combination of string
        # longyuandaguanlh.fang.com/house/ajaxrequest/photolist_get.php?newcode=2811122272&type=904&nextpage=6&room=
        # print(type(response.meta["item"]), response.meta["item"])
        item = dict(response.meta["item"][0])
        TuUrl = ImageItem()
        data_list = item["json_data"]
        image_type = item["type"]
        _id = item["_id"]
        full_image_interface_list = item["request_list"]
        # aaa = response.url
        # print("aaa", aaa)

        if full_image_interface_list:
            data = json.loads(response.body)
            # print("相册借口", data)
            [data_list.append({"picUrl": "http:" + re.sub(r"\d+x\d+\.", "880x600.", i["url_s"]), "type": image_type})
             for i in data]

            first_url = full_image_interface_list.pop()
            meta = {"_id": _id, "request_list": full_image_interface_list, "type": first_url[1],
                    "json_data": data_list},
            yield scrapy.Request(first_url[0], meta={"item": meta}, callback=self.parse_images)
        else:
            # print(data_list)
            yield {"_id": _id, "picJson": json.dumps(data_list)}

        data = json.loads(response.text)
        for images in data:
            TuUrl["_id"] = ["http:" + re.sub(r"\d+x\d+\.", "880x600.", images["url_s"])]
            print("tttttt", TuUrl["_id"])
            yield TuUrl

    # def parse_photo(self, response):
    #     page = response.meta["data"]
    #     # print("989898",parameter)
    #     # item = Data_picJson()
    #     start_url = response.url
    #     url = re.sub(r"\w+\/\w+_\d+_\d+.htm", "", start_url)
    #     _id = url
    #     building_name = re.search(r"//(\w+)\.", start_url).group(1)
    #     building_number = re.search(r"(\d+)\.htm", start_url).group(1)
    #     style_number = re.search(r"_(\d+)_", start_url).group(1)
    #     print("参数", style_number)
    #     if style_number == "901":
    #         item = "jiaotongtu"
    #     elif style_number == "903":
    #         item = "shijingtu"
    #     elif style_number == "904":
    #         item = "xiaoguotu"
    #     elif style_number == "905":
    #         item = "yangbanjian"
    #
    #     # print("++++", item["type"])
    #     parameter = 1
    #     while True:
    #         base_url = "https://" + building_name + ".fang.com/house/ajaxrequest/photolist_get.php?newcode=" + building_number + "&type=" + style_number + "&nextpage=" + str(
    #             parameter) + "&room="
    #         yield scrapy.Request(base_url, meta={"item": item, "_id": _id}, callback=self.photo_interface)
    #         parameter += 1
    #         if parameter > page:
    #             break
    #     # yield scrapy.Request(base_url,meta={"item": item},callback=self.photo_interface)

    # def photo_interface(self, response):
    #     # data = respose.xpath('//*[@id="json"]/ul/li[2]/div/span[2]/text()').extract()[0]
    #     # if data == '"没有数据"':
    #     item = Data_picJson()
    #     type = response.meta["item"]
    #     _id = response.meta["_id"]
    #     print(item)
    #     print(_id)
    #     all_comment_dict = {"_id": _id}
    #     picJson = []
    #     url = response.url
    #     print("5555", url)
    #     datas = json.loads(response.text)
    #     print("132", datas)
    #     for data in datas:
    #         item["type"] = type
    #         # item = Data_picJson()
    #         item["picUrl"] = data["url"]
    #         print("1321", item["picUrl"])
    #         # print(item)
    #         # yield item
    #         picJson.append(dict(item))
    #
    #     picJson = json.dumps(picJson, ensure_ascii=False)
    #     all_comment_dict.update({"picJson": picJson})
    #     print('2323', all_comment_dict)
    #     yield all_comment_dict

    def parse_houseapartment(self, response):
        # 解析户型页面 通过拼接 接口获取数据
        data_url = response.url
        building_name = re.sub(r"\w+\/\w+_\d+_\d+.htm", "", data_url)
        building_number = re.search(r"(\d+)\.htm", data_url).group(1)

        jiekou_url = building_name + "house/ajaxrequest/householdlist_get.php?newcode=" + building_number + "&room=all"
        print("借口", jiekou_url)
        yield scrapy.Request(jiekou_url, meta={"house_url": building_name}, callback=self.house_interface)

    def house_interface(self, response):
        # 户型接口
        item = DataHouseapartment()
        house_url = response.meta["house_url"]
        all_comment_dict = {"_id": house_url}
        houseapartment = []
        datas = json.loads(response.text)
        for data in datas:
            # item["houseUrl"]
            images = []
            imag = "http:" + re.sub("220x150", "748x600", data["houseimageurl"])
            images.append({"picUrl": imag})
            item["imgs"] = images  # 户型名称
            # item["_id"] = house_url  # 户型url
            item["name"] = data["housetitle"]  # 户型名称
            item["houseUrl"] = house_url + "photo/d_house_" + data["picID"] + ".htm"
            item["salesStatus"] = data["status"]  # 在售状态
            item["roomNum"] = data["room"]  # 户型(房)
            item["hallNum"] = data["hall"]  # 户型(厅)
            item["toiletNum"] = data["toilet"]  # 户型(卫)
            item["constructSpace"] = data["buildingarea"]
            # item["price"] = data["toilet"]
            # item["propertyType"] = data["toilet"]
            # item["remark"] = data["toilet"]
            print(item)
            try:
                if "-" in data["reference_price"]:
                    lower_price, high_price = data["reference_price"].split("-")
                    print("123", lower_price)
                    print("321", high_price)
                    data["reference_price"] = str((float(lower_price) + float(high_price)) / 2)
            except Exception as e:
                print(str(e))
            try:
                item["price"] = int(float(data["reference_price"]) / float(data["buildingarea"]) * 10000) if \
                    data["reference_price"] != "待定" and data["buildingarea"] != "待定" \
                    and data["reference_price"] and data["buildingarea"] \
                    and float(data["reference_price"]) and \
                    float(data["buildingarea"]) else None  # 参考均价
            except Exception as e:
                # print(apartment_url)
                print(str(e))
            if not data["reference_price"]:
                item["totalPrices"] = ""
            elif data["reference_price"] == "待定":
                item["totalPrices"] = data["reference_price"]
            else:
                item["totalPrices"] = data["reference_price"] + "万元/套"
            # data_dict["houseapartment"].append(item)
            # print("9999", item)
            #
            # data_dict["houseapartment"] = json.dumps(data_dict["houseapartment"], ensure_ascii=False)
            # return data_dict
            houseapartment.append(dict(item))

        # print("接口接口", type(commentJson), commentJson)
        houseapartment = json.dumps(houseapartment, ensure_ascii=False)
        all_comment_dict.update({"houseapartment": houseapartment})
        print("户型借口", all_comment_dict)
        yield all_comment_dict

    def parse_comments(self, response):
        # 解析评论
        # item = DataCommentJson()
        url = response.url
        house = re.sub(r"dianping/", "", url)
        # all_comment_dict = {"_id": re.sub(r"dianping\/", "", url)}
        # commentJson = []
        # all_comment = response.xpath("//div[@id='dpContentList']/div[contains(@id,'detail')]")
        # for i in all_comment:
        #     item["sourceUrl"] = url  # 当前页面的ｕｒｌ
        #     # item["_id"] = re.sub(r"dianping\/", "", item["sourceUrl"])
        #     item["source"] = "房天下"
        #     # item["userNick"] = i.xpath('./div[@class="comm_list_nr fl"]/div[@class="comm_list_header"]/text()').extract_first()     # 用户名
        #     item["userNick"] = i.xpath('./div[2]/div[1]//text()').extract()  # 用户名
        #     item["userNick"] = ''.join(item["userNick"])
        #     # try:
        #     item["userNick"] = item["userNick"].replace(" ", "")
        #     item["userNick"] = item["userNick"].replace("\n", "")
        #     item["userNick"] = item["userNick"].replace("\t", "")
        #     item["userNick"] = item["userNick"].replace(",", "")
        #     # except Exception as e:
        #     #     pass
        #     print("234", item["userNick"])
        #     try:
        #         item["content"] = i.xpath('.//a//p/text()').extract_first()  # 评论内容
        #     except Exception as e:
        #         item["content"] = None
        #     item["createDate"] = i.xpath(".//em/span/text()").extract_first()  # 评论时间
        #
        #     commentJson.append(dict(item))
        #
        # # print("8888888", type(commentJson), commentJson)
        # # commentJson = json.dumps(commentJson, ensure_ascii=False)
        # all_comment_dict.update({"commentJson": commentJson})
        # # print("2222", all_comment_dict)
        # print("2222" * 10)
        # yield all_comment_dict
        particulars = response.xpath("//*[@class='navleft tf']//a[contains(text(),'详情')]/@href|"
                                     "//*[@class='navleft tf']//a[contains(text(),'详细')]/@href").extract_first()
        particulars = u"https:" + particulars
        parameter = re.search(r"/(\d+)/", particulars).group(1)
        parameter = str(parameter)
        # print("4654546", parameter)
        port_url = house + "house/ajaxrequest/dianpingList_201501.php"
        # 借口url
        data = "1"
        yield scrapy.FormRequest(port_url,
                                 formdata={"dianpingNewcode": parameter, "ifjiajing": "0",
                                           "page": data, "pageesize": "60", "starnum": "6", "shtag": "-1"},
                                 callback=self.comment_port)
        # data += str(1)
        # while True:
        #     page = response.xpath('//div[@class="more10"]//a[contains(text(),"再显示20条")]').extract_first()
        #     if page != None:
        #         port_url = house + "house/ajaxrequest/dianpingList_201501.php"
        #         # 借口url
        #         data = "2"
        #         yield scrapy.FormRequest(port_url,
        #                                  formdata={"dianpingNewcode": parameter, "ifjiajing": "0",
        #                                            "page": data, "pageesize": "20", "starnum": "6", "shtag": "-1"},
        #                                  callback=self.comment_port)
        #         data += str(1)
        #     else:
        #         # yield all_comment_dict
        #         break

    def comment_port(self, response):
        # item = response.meta["data"]
        item = DataCommentJson()
        url = response.url
        url = re.sub(r"house\/\w+\/\w+_\d+.php", "", url)
        # print('54545', item)
        all_comment_dict = {}
        commentJson = []
        datas = json.loads(response.text)["list"]
        print("989898", datas)
        for data in datas:
            # print("data", type(data), data)
            # print("datass", type(datas), datas)
            item["_id"] = url
            item["source"] = "房天下"
            item["userNick"] = data["username"]
            item["content"] = data["content"]
            item["sourceUrl"] = url + "dianping/"
            item["createDate"] = data["create_time"]
            print("打印", item)
            commentJson.append(dict(item))

        # print("接口接口", type(commentJson), commentJson)
        # commentJson = json.dumps(commentJson, ensure_ascii=False)
        all_comment_dict.update({"commentJson": commentJson})
        # print("户型借口", all_comment_dict)
        yield all_comment_dict

    def parse_dynamic(self, response):
        # item = DataDynamicJson()
        # all_comment_dict = {}
        # dynamicJson = []
        # url = response.url
        # url = re.sub(r"house\/\d+\/\w+\.htm", "", url)
        # item["_id"] = url
        # print("aaaaaa", url)
        # yield item
        # dynamicJson.append(dict(item))
        # dynamicJson = json.dumps(dynamicJson, ensure_ascii=False)
        # all_comment_dict.update({"dynamicJson": dynamicJson})
        # # print("2222", all_comment_dict)
        # yield all_comment_dict

        # dynamic = response.xpath("//*[@class='navleft tf']//a[contains(text(),'首页')]/@href").extract()  # 楼盘首页
        # dynamic = "".join(dynamic)
        # _id = u"https:" + dynamic

        dynamic_url = response.xpath(
            '//div[@id="gushi_all"]//a[contains(text(),"详情")]/@href').extract_first()  # 获取动态里详情链接
        if dynamic_url != None:
            dynamic_url = u"https:" + dynamic_url
            # print("item111", url)
            # dynamic_url_all = response.xpath(
            #     '//div[@id="gushi_all"]//p[@class="c6_f14"]//a[contains(text(),"详情")]/@href').extract()  # 获取动态里详情链接
            #
            # for url in dynamic_url_all:
            #     dynamic_url = u"https:" + url

            yield scrapy.Request(dynamic_url, callback=self.dynamic_particulars)
        # the_next_page = response.xpath('//div[@id="gushi_all"]//li[@class="clearfix dbib"]//a[contains(text(),"下一页")]/@href').extract_first()   # 下一页
        # print("0033",the_next_page)
        # if the_next_page != None:
        #     the_next_page = _id + the_next_page
        #     yield scrapy.Request(the_next_page,callback=self.parse_dynamic)

    def dynamic_particulars(self, response):
        item = DataDynamicJson()
        dynamic = response.xpath("//*[@class='navleft tf']//a[contains(text(),'首页')]/@href").extract()  # 楼盘首页
        dynamic = "".join(dynamic)
        _id = u"https:" + dynamic
        # all_comment_dict = {"_id": _id}
        # dynamicJson = ""
        url = response.url
        url = re.sub(r"\d+_\d+\.htm", "", url)
        # url1 = re.sub(r"house\/", "", url)
        print("url", url)
        dynamic_content = response.xpath("//div[@class='atc-wrapper']")
        for i in dynamic_content:
            item["soutse"] = "房天下"
            item["title"] = i.xpath("./h1/text()").extract_first()
            print(item["title"])
            item["publishDate"] = i.xpath("./h2/text()[3]").extract_first()
            print("时间1111", type(item["publishDate"]), item["publishDate"])
            item['publishDate'] = re.search(r"\d+.*", item["publishDate"], re.S).group()  # 时间
            # item["publishDate"] = item["publishDate"].replace(" ", "")
            item["publishDate"] = item["publishDate"].replace("\n", "")
            item["publishDate"] = item["publishDate"].replace("\t", "")
            item["publishDate"] = item["publishDate"].replace("\r", "")
            # time = "".join(time)
            # data["publishDate"] =re.search(r"/d+.*",time,re.S).group()
            print("时间", item["publishDate"])
            item["content"] = i.xpath(
                ".//p[@style='text-indent:2em;']//text()|//div[@class='leftboxcom']//text()").extract()
            item["content"] = "".join(item["content"])
            item["content"] = item["content"].replace(" ", "")
            item["content"] = item["content"].replace("\n", "")
            item["content"] = item["content"].replace("\t", "")
            item["content"] = item["content"].replace("\r", "")
            print("内容", item["content"])
            # try:
            self.dynamicJson.append(dict(item))
            # except Exception as e:
            # self.dynamicJson += str(dict(item))
        # dynamicJson = json.dumps(dynamicJson, ensure_ascii=False)
        # all_comment_dict.update({"dynamicJson": dynamicJson})
        # # self.all_comment_dict = self.all_comment_dict.split()
        # # yield scrapy.Request(url, meta={"dynamicJson": dict(item), "_id": _id}, callback=self.all_comment_dict_dynamic)
        # yield all_comment_dict

        the_next_page1 = response.xpath('//div[@class="fy-wrapper"]/a[@class="syp"]/@href').extract_first()
        the_next_page = url + the_next_page1
        print("拼接url", the_next_page)
        if the_next_page1 != "javascript:void(0);":
            # print("上一篇" * 10)
            yield scrapy.Request(the_next_page, callback=self.dynamic_particulars)
        else:
            all_comment_dict = {"_id": _id}
            # print("返回数据" * 10)
            # self.dynamicJson = json.dumps(self.dynamicJson, ensure_ascii=False)
            # self.dynamicJson = ("{}".format(self.dynamicJson))
            all_comment_dict.update({"dynamicJson": self.dynamicJson})
            yield all_comment_dict
            self.dynamicJson.clear()
            all_comment_dict.clear()
            # del (self.dynamicJson)
            # print(type(self.all_comment_dict), self.all_comment_dict)
            # neme = "self.dynamicJson" + str()
            # locals()["self.dynamicJson"] + str()

    # def sub_dynamic_particulars(self,response):
    #     item = DataDynamicJson()
    #     url = response.url
    #     url = re.sub(r"\d+_\d+\.htm", "", url)
    #     # url1 = re.sub(r"house\/", "", url)
    #     print("url", url)
    #
    #     dynamic_content = response.xpath("//div[@class='atc-wrapper']")
    #     for i in dynamic_content:
    #         # item["_id"] = id
    #
    #         item["soutse"] = "房天下"
    #         item["title"] = i.xpath("./h1/text()").extract_first()
    #         # print(item["title"])
    #         # if not item["title"]:
    #         #     pass
    #         # item["_id"] = url1
    #         item["publishDate"] = i.xpath("./h2/text()[3]").extract_first()
    #         item["publishDate"] = item["publishDate"].replace(" ", "")
    #         item["publishDate"] = item["publishDate"].replace("\n", "")
    #         item["publishDate"] = item["publishDate"].replace("\t", "")
    #         item["publishDate"] = item["publishDate"].replace("\r", "")
    #         # time = "".join(time)
    #         # data["publishDate"] =re.search(r"/d+.*",time,re.S).group()
    #         # print("时间", item["publishDate"])
    #         item["content"] = i.xpath(
    #             ".//p[@style='text-indent:2em;']//text()|//div[@class='leftboxcom']//text()").extract()
    #         item["content"] = "".join(item["content"])
    #         item["content"] = item["content"].replace(" ", "")
    #         item["content"] = item["content"].replace("\n", "")
    #         item["content"] = item["content"].replace("\t", "")
    #         item["content"] = item["content"].replace("\r", "")
    #         # print("内容", item["content"])
    #
    #         # print(item)
    #         # yield item
    #         # print("2222222",type(self.dynamicJson),self.dynamicJson)
    #         self.dynamicJson.append(dict(item))
    #
    #         # print(self.dynamicJson)
    #
    #     the_next_page1 = response.xpath('//div[@class="fy-wrapper"]/a[@class="syp"]/@href').extract_first()
    #     the_next_page = url + the_next_page1
    #     print("拼接url", the_next_page)
    #     if the_next_page1 != "javascript:void(0);":
    #         # print("上一篇" * 10)
    #         yield scrapy.Request(the_next_page, callback=self.sub_dynamic_particulars)
    #     else:
    #         # break
    #         # print("返回数据" * 10)
    #         self.all_comment_dict["_id"] = _id
    #         # self.dynamicJson = json.dumps(self.dynamicJson, ensure_ascii=False)
    #         self.all_comment_dict.update({"dynamicJson": self.dynamicJson})
    #         # print(type(self.all_comment_dict), self.all_comment_dict)
    #         # self.all_comment_dict = self.all_comment_dict.split()
    #         yield self.all_comment_dict

    def positioning(self, response):
        item = response.meta["item"]
        particulars = response.meta["xiangqing"]
        ditu = response.body.decode("utf8")
        # print("定位123", ditu)
        # re_search = re.search(r'"mapx":"(.*?)","mapy":"(.*?)"', ditu, re.DOTALL)
        re_search = re.search(r'"mapx":"(\d+\.\d+)","mapy":"(\d+\.\d+)"', ditu, re.DOTALL)
        housecoord = re_search.group(2) + "," + re_search.group(1)
        # print("123", housecoord)
        item["housecoord"] = housecoord
        print("定位", item["housecoord"])
        yield scrapy.Request(particulars, meta={"item": item}, callback=self.parse_particulars)

    def parse_particulars(self, response):
        # 解析详情页
        # url = response.meta["url"]
        a = response.url
        print("123321", a)
        # new_house = response.meta('new_house')
        pattern = re.compile(r'\W+', re.S)
        html = response.body.decode("gb18030")
        # encoding = "gb18030"
        soup = BeautifulSoup(html, "html.parser")
        # print("源码",soup)
        html = etree.HTML(html)
        item = response.meta['item']
        # url = response.url
        # url = re.sub(r"/house/\d+/\w+.htm","",url)
        # print("url123",url)
        item['housename'] = response.xpath('//*[@id="daohang"]//h1/a/text()').extract()  # 楼盘名称
        item['housename'] = "".join(item['housename'])
        try:
            housename2 = response.xpath('//*[@id="daohang"]//div/span/text()').extract()  # 楼盘别名
            housename2 = "".join(housename2)
            item['housename2'] = housename2[3:]  # 字符串切片去掉前面三个字符
            if not item['housename2']:
                item['housename2'] = ""
            print("别名", item['housename2'])
        except Exception as e:
            item['housename2'] = None
            print("别名111", item['housename2'])
        houseproperty = response.xpath('//div[@class="lpicon tf"]//text()').extract()  # 楼盘标签
        print("楼盘标签", houseproperty)
        houseproperty = [pattern.sub('', i) for i in houseproperty]
        print(houseproperty)
        re_houseproperty = []
        [re_houseproperty.append(i)
         for i in houseproperty if i]
        houseproperty = ",".join(re_houseproperty)  # 空格替换逗号
        houseproperty = "".join(houseproperty)
        print(houseproperty)
        item["houseproperty"] = houseproperty
        sleep(0.5)
        basic_information = response.xpath("//div[@class='main-left']")
        # print("123", basic_information)
        for i in basic_information:
            # 基本信息
            # item['_id'] = url  # 楼盘url
            item['source'] = "房天下"  # 来源
            item['allstatus'] = "1"  # 采集状态
            price = i.xpath('./div[1]//em/text()').extract()  # 均价

            print("价格111", price)
            price = ''.join(price)
            try:
                price = price.replace("\n", "")
                price = price.replace("\t", "")
                price = price.replace(" ", "")
            except Exception as e:
                pass
            print("价格", price)
            try:
                item['houseprice'] = re.search(r"\d+.*", price, re.S).group()  # 取出数字及后面的字
            except Exception as e:
                item['houseprice'] = "待定"
            book_list = soup.find(attrs={"class": "main-left"})
            # print("0909", book_list)
            book_list_name = book_list.find_all("li")
            data_dict = {}
            for i in book_list_name:
                key = i.find(attrs={"class": "list-left"})
                try:
                    key = key.text
                except Exception as e:
                    pass
                value = i.find(attrs={"class": ["list-right", "list-right-text", "list-right-floor"]})  # 获取两个class名
                # value = i.find_all("div[2]")
                print("89898", value)
                # value = i.find(attrs={"class": "list-right-text"})
                # value = i.find("div")
                try:
                    value = value.text
                    print("value", value)
                except Exception as e:
                    pass
                try:
                    key = key.replace(" ", "")
                    key = key.replace("\n", "")
                    key = key.replace("\t", "")
                except Exception as e:
                    pass
                try:
                    value = value.replace(" ", "")
                    value = value.replace("\n", "")
                    value = value.replace("\t", "")
                except Exception as e:
                    pass
                data_dict.update({key: value})
                print("9888", data_dict)
            # 基本信息
            if "物业类别：" in data_dict.keys():
                item['houseatr'] = data_dict["物业类别："]
            if "建筑类别：" in data_dict.keys():
                item['housetype'] = data_dict["建筑类别："]
            elif "写字楼级别：" in data_dict.keys():
                item['housetype'] = data_dict["写字楼级别："]
            if "产权年限：" in data_dict.keys():
                item['years'] = data_dict["产权年限："]
                item['years'] = item['years'].replace(",", "")
            if "装修状况：" in data_dict.keys():
                item['decoration'] = data_dict["装修状况："]
            if "开发商：" in data_dict.keys():
                item['developer'] = data_dict["开发商："]
            if "楼盘地址：" in data_dict.keys():
                item['houseaddress'] = data_dict["楼盘地址："]
            # 销售信息
            if "销售状态：" in data_dict.keys():
                item['salestatus'] = data_dict["销售状态："]
            if "开盘时间：" in data_dict.keys():
                item['startSaleString'] = data_dict["开盘时间："]
            if "交房时间：" in data_dict.keys():
                item['endSaleString'] = data_dict["交房时间："]
            if "售楼地址：" in data_dict.keys():
                item['saleaddress'] = data_dict["售楼地址："]
            # 小区规划
            if "占地面积：" in data_dict.keys():
                landarea = data_dict["占地面积："]
                data_re = re.findall(r"\d+", landarea, re.S)  # 取出数字
                item['landarea'] = ("".join(data_re))  # 列表转字符串
                # print("占地面积", data['landarea'])
            if "建筑面积：" in data_dict.keys():
                housearea = data_dict["建筑面积："]
                data_re = re.findall(r"[\d\.]+", housearea, re.S)  # 取出数字
                item['housearea'] = ("".join(data_re))  # 列表转字符串
                print("建筑面积", item['landarea'])
            if "容积率：" in data_dict.keys():
                item['plotratio'] = data_dict["容积率："]
                item['plotratio'] = ''.join(item['plotratio'].split())
            if "绿化率：" in data_dict.keys():
                item['greenrate'] = re.sub(r'\%', '', data_dict["绿化率："])  # 去掉%
                if item['greenrate'] == "暂无资料":
                    item['greenrate'] = None
            if "停车位：" in data_dict.keys():
                item['carsite'] = data_dict["停车位："]
                try:
                    item['carsite'] = item['carsite'].replace("\r", "")
                    item['carsite'] = item['carsite'].replace("\n", "")
                    item['carsite'] = item['carsite'].replace("\t", "")
                    item['carsite'] = item['carsite'].replace(" ", "")
                except Exception as e:
                    pass
            elif "停车位配置：" in data_dict.keys():
                item['carsite'] = data_dict["停车位配置："]
                try:
                    item['carsite'] = item['carsite'].replace("\r", "")
                    item['carsite'] = item['carsite'].replace("\n", "")
                    item['carsite'] = item['carsite'].replace("\t", "")
                    item['carsite'] = item['carsite'].replace(" ", "")
                except Exception as e:
                    pass
            print("停车位", item['carsite'])
            if "楼栋总数：" in data_dict.keys():
                housecount = data_dict["楼栋总数："]
                data_re = re.findall(r"\d+", housecount, re.S)  # 取出数字
                item['housecount'] = ("".join(data_re))  # 列表转字符串
                # print("楼栋总数", data['housecount'])
            elif "楼栋情况：" in data_dict.keys():
                item['housecount'] = data_dict["楼栋情况："]
            print("10" * 10)

            if "总户数：" in data_dict.keys():
                allcount = data_dict["总户数："]
                data_re = re.findall(r"\d+", allcount, re.S)  # 取出数字
                item['allcount'] = ("".join(data_re))  # 列表转字符串
                # print("总户数", data['allcount'])
            if "物业公司：" in data_dict.keys():
                item['managecompany'] = data_dict["物业公司："]
            if "物业费：" in data_dict.keys():
                item['managefee'] = data_dict["物业费："]
                item['managefee'] = "".join(item['managefee'].split())  # 去掉\xa0字符
            if "楼层状况：" in data_dict.keys():
                item['floorCondition'] = data_dict["楼层状况："]

            item['fetch_time'] = str(datetime.now())  # 获取当前时间

            # data["insoect"] = 1
            pattern = re.compile(r'(\d{4}).*?(\d{1,2}).*?(\d{1,2})')
            pattern_without_day = re.compile(r'(\d{4}).*?(\d{1,2})')

            if item['startSaleString']:
                re_serch = pattern.search(item["startSaleString"])
                if re_serch:
                    start_year, start_month, start_day = re_serch.group(1), re_serch.group(2), re_serch.group(3)
                    start_month, start_day = start_month.rjust(2, '0'), start_day.rjust(2, '0')
                    item["startsaletime"] = start_year + "-" + start_month + "-" + start_day + " 00:00:00"
                else:
                    try:
                        re_serch = pattern_without_day.search(item["startSaleString"])
                        start_year, start_month = re_serch.group(1), re_serch.group(2)
                        start_month = start_month.rjust(2, '0')
                        item["startsaletime"] = start_year + "-" + start_month + "-01 00:00:00"
                    except:
                        pass
            if item["endSaleString"]:
                re_serch = pattern.search(item["endSaleString"])
                if re_serch:
                    start_year, start_month, start_day = re_serch.group(1), re_serch.group(2), re_serch.group(3)
                    start_month, start_day = start_month.rjust(2, '0'), start_day.rjust(2, '0')
                    item["endsaletime"] = start_year + "-" + start_month + "-" + start_day + " 00:00:00"
                else:
                    try:
                        re_serch = pattern_without_day.search(item["endSaleString"])
                        start_year, start_month = re_serch.group(1), re_serch.group(2)
                        start_month = start_month.rjust(2, '0')
                        item["endsaletime"] = start_year + "-" + start_month + "-" + "-01 00:00:00"
                    except:
                        pass

            for key, value in item.items():
                # key = "".join(key)
                # value = "".join(value)
                print("key", key)
                print("value", value)
                if value and value.endswith(","):
                    # print("endwith:','", value)
                    item[key] = value[:-1]
                if value and type(value) == str and '[' in value:  # 去掉[]内的内容
                    item[key] = re.sub(r'[^\w]?\[.*?\]', '', value)
                    # print("[ ]",data[key])
            # print("222", item)
            yield item

        # The_next_page = response.xpath('//li[@class="floatr rankWrap"]/div/a[contains(text(),">")]/@href').extract_first()  # 获取下一页
        # # if not  The_next_page == None:
        # print("909090",The_next_page)
        #
        # The_next_page = url + The_next_page
        # if The_next_page != None :
        #     print("下一页"*10)
        #     yield scrapy.Request(The_next_page, callback=self.home_page)

    # def re_sub_time(self, item):
    #     pattern = re.compile(r'(\d{4}).*?(\d{1,2}).*?(\d{1,2})')
    #     pattern_without_day = re.compile(r'(\d{4}).*?(\d{1,2})')
    #
    #     if item['startSaleString']:
    #         re_serch = pattern.search(item["startSaleString"])
    #         if re_serch:
    #             start_year, start_month, start_day = re_serch.group(1), re_serch.group(2), re_serch.group(3)
    #             start_month, start_day = start_month.rjust(2, '0'), start_day.rjust(2, '0')
    #             item["startsaletime"] = start_year + "-" + start_month + "-" + start_day + " 00:00:00"
    #         else:
    #             try:
    #                 re_serch = pattern_without_day.search(item["startSaleString"])
    #                 start_year, start_month = re_serch.group(1), re_serch.group(2)
    #                 start_month = start_month.rjust(2, '0')
    #                 item["startsaletime"] = start_year + "-" + start_month + "-01 00:00:00"
    #             except:
    #                 pass
    #     if item["endSaleString"]:
    #         re_serch = pattern.search(item["endSaleString"])
    #         if re_serch:
    #             start_year, start_month, start_day = re_serch.group(1), re_serch.group(2), re_serch.group(3)
    #             start_month, start_day = start_month.rjust(2, '0'), start_day.rjust(2, '0')
    #             item["endsaletime"] = start_year + "-" + start_month + "-" + start_day + " 00:00:00"
    #         else:
    #             try:
    #                 re_serch = pattern_without_day.search(item["endSaleString"])
    #                 start_year, start_month = re_serch.group(1), re_serch.group(2)
    #                 start_month = start_month.rjust(2, '0')
    #                 item["endsaletime"] = start_year + "-" + start_month + "-" + "-01 00:00:00"
    #             except:
    #                 pass
    #
    #
    #
    #
    #
