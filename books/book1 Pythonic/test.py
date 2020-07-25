import os

filelist = []


def listFileName(dirname, filesuffix):
    '''
    找出dirname目录下所有以filesuffix结尾的文件名
    :param dirname: 文件路径
    :param filesuffix: 文件名后缀
    :return: 以filesuffix结尾的文件名构成的列表
    '''
    os.chdir(dirname)
    for file in os.listdir('.'):
        childfile = os.path.join(dirname, file)
        if childfile.endswith(filesuffix):
            filelist.append(childfile)
        if os.path.isdir(childfile):
            listFileName(childfile, filesuffix)
    return filelist


print(listFileName(r'D:\keeplearning', 'md'))

