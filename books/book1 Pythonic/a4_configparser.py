import configparser
conf = configparser.ConfigParser()
conf.read('example.conf')
print(conf.getboolean('section1','option1'))  # False
print(conf.get('section2','in_default'))    # 'an option value in default'


# Python中字符串格式化：
example_str = '%(protocol)s://%(server)s:%(port)s/' % {'protocol':'http','server':'example.com','port':1080,}
print(example_str)

# ConfigParser中类似用法
print(conf.get('db1','conn_str'))
print(conf.get('db2','conn_str'))
# mysql://zyp:ppp@localhost:3306/example
# mysql://root:www@192.168.0.110:3306/example
