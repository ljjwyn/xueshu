# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class filterPipeline(object):
    """
    只有中文论文
    """

    def process_item(self, item, spider):
        name = item['title']
        for c in name:
            if not ('\u4e00' <= c <= '\u9fa5'):
                print("____________________erro")
                raise DropItem("English title found:%s" % item)
                print("English Find")
        return item


class DuplicatesPipeline(object):
    """
    论文标题去重
    """

    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        name = item['title']
        if name in self.book_set:
            raise DropItem("Duplicate title found:%s" % item)

        self.book_set.add(name)
        return item


class XueshuPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item