import json
import datetime

'''
json在序列化datetime时会抛出TypeError异常，
因为json模块本身不支持datetime的序列化，
需要对json本身的JSONEncoder进行拓展。
'''
class DataTimeEncoder(json.JSONEncoder):  # JSONEncoder进行扩展
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return obj.JSONEncoder.default(self, obj)

d = datetime.datetime.now()
print(json.dumps(d, cls= DataTimeEncoder))  # 使用cls指定编码器的名称



