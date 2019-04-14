# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from .items import DataFangItem, DataDynamicJson, DataPicJson, DataCommentJson, DataHouseapartment, ImageItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum
import sys
from scrapy.settings import Settings
import happybase
import functools


class DataFangPipeline(object):
    def open_spider(self, spider):
        self.f = open("详情.json", "w")

    def process_item(self, item, spider):
        if isinstance(item, DataFangItem):
            json_str = "".join(json.dumps(dict(item), ensure_ascii=False)) + "\n"
            self.f.write(json_str)
        return item

    def close_spider(self, spider):
        self.f.close()


class DynamicJsonPipeline(object):
    def open_spider(self, spider):
        self.f = open("动态.json", "a")

    def process_item(self, item, spider):
        if "dynamicJson" in item.keys():
            item["dynamicJson"] = json.dumps(item["dynamicJson"], ensure_ascii=False)
            json_str = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.f.write(json_str)
        return item

    def close_spider(self, spider):
        self.f.close()


class CommentJsonPipeline(object):
    def open_spider(self, spider):
        self.f = open("评论.json", "w")

    def process_item(self, item, spider):
        if "commentJson" in item.keys():
            item["commentJson"] = json.dumps(item["commentJson"], ensure_ascii=False)
            # if isinstance(item, Data_commentJson):
            json_str = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.f.write(json_str)
        return item

    def close_spider(self, spider):
        self.f.close()


class HouseapartmentPipeline(object):
    def open_spider(self, spider):
        self.f = open("户型.json", "a")

    def process_item(self, item, spider):
        if "houseapartment" in item.keys():
            item["houseapartment"] = json.dumps(item["houseapartment"], ensure_ascii=False)
            json_str = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.f.write(json_str)
        return item

    def close_spider(self, spider):
        self.f.close()


class PicJsonPipeline(object):
    def open_spider(self, spider):
        self.f = open("相册.json", "a")

    def process_item(self, item, spider):
        # if isinstance(item, DataPicJson):
        #     item["picJson"] = json.dumps(item["picJson"], ensure_ascii=False)
        #     json_str = "".join(json.dumps(dict(item), ensure_ascii=False)) + "\n"
        #     self.f.write(json_str)
        # return item
        data_item = []
        if "picJson" in item.keys():
            data = item["picJson"]
            for i in data:
                if isinstance(i, dict):
                    for k, v in i.items():
                        print("cccc", v)
            # print("jjjj",data["picUrl"])
            # for v in data.items():
            #     print("ccc",v)
            item["picJson"] = json.dumps(item["picJson"], ensure_ascii=False)
            json_str = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.f.write(json_str)
        return item


class PictureDownload(ImagesPipeline):
    """
    继承于图片下载管道ImagesPipeline
    """

    def __init__(self, pool, table_name, download_func=None, settings=None):
        self.pool = pool
        self.table_name = table_name
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        resolve = functools.partial(self._key_for_pipe,
                                    base_class_name="ImagesPipeline",
                                    settings=settings)
        self.expires = settings.getint(
            resolve("IMAGES_EXPIRES"), self.EXPIRES
        )

        if not hasattr(self, "IMAGES_RESULT_FIELD"):
            self.IMAGES_RESULT_FIELD = self.DEFAULT_IMAGES_RESULT_FIELD
        if not hasattr(self, "IMAGES_URLS_FIELD"):
            self.IMAGES_URLS_FIELD = self.DEFAULT_IMAGES_URLS_FIELD

        self.images_urls_field = settings.get(
            resolve('IMAGES_URLS_FIELD'),
            self.IMAGES_URLS_FIELD
        )
        self.images_result_field = settings.get(
            resolve('IMAGES_RESULT_FIELD'),
            self.IMAGES_RESULT_FIELD
        )
        self.min_width = settings.getint(
            resolve('IMAGES_MIN_WIDTH'), self.MIN_WIDTH
        )
        self.min_height = settings.getint(
            resolve('IMAGES_MIN_HEIGHT'), self.MIN_HEIGHT
        )
        self.thumbs = settings.get(
            resolve('IMAGES_THUMBS'), self.THUMBS
        )

    @classmethod
    def from_settings(cls, settings):
        try:
            pool = happybase.ConnectionPool(size=5, protocol='compact', transport='framed',
                                            host=settings["HBASE_HOSTS"],
                                            autoconnect=False)

        except Exception as e:
            sys.exit(1)

        return cls(pool, settings['HBASE_TABLE2'])

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def image_downloaded(self, response, request, info):
        print("*\n" * 5, "正在下载图片")
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            time = self._get_time()
            try:
                with self.pool.connection() as connection:
                    table = connection.table(self.table_name)
                    table.put(path, {"cf:content": buf.getvalue(), "cf:size": "880X600"})
                    connection.close()
                    print("successfully storing image into hbase,{time},{id}".format(type=type, time=time, id=path))

            except Exception as e:
                print("Caught Hbase exception of image storing:{e}".format(e=str(e)))
                print("failed storing image into hbase,{time},{id}".format(type=type, time=time, id=path))
        return checksum

    def file_path(self, request, response=None, info=None):
        super(PictureDownload, self).file_path(request, response, info)
        image_guid = request.url
        return request.url
