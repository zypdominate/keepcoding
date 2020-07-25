import os
import re

sphinxPath = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))


def modify_doc_title_dir(source_path):
    """
    rst文件中：有‘========’和‘----------’行的表示其行上一行的文字是标题，‘=’和‘-’要大于等于标题的长度。
    使用sphinx-apidoc -o ./source/rst_files ../../命令
    使用sphinx-apidoc -o ./source ../src/utils/ -f
    将生成rst文件放在./source/rst_files目录下。 生成rst文件后将rst_files/modules.rst文件中的标题去掉，并修改maxdepth字段。
    删除和修改使用sphinx-apidoc -o 命令的生成的rst文件中的标题
    :param abspath_rstfiles_dir: rst文件所在的文件夹的绝对路径
    :return:
    """
    rst_files = [file for file in source_path if file.endswith('rst')]
    print(f'rst_files:{rst_files}')
    del_nodes = ['Submodules', 'Module contents', 'Subpackages']  # 要删除的节点(标题目录的节点)
    del_str = [' module', ' package']  # 要删除的标题中的字符串
    for rst_file in rst_files:
        currentfile = os.path.join(abspath_rstfiles_dir, rst_file)
        print(f'currentfile:{currentfile}')
        with open(currentfile, 'r') as fr:
            file_lines = fr.readlines()
            write_con = []
            flag = 0
            for file_line in file_lines:
                if file_line.strip() in del_nodes:
                    flag = 1
                    continue
                if flag:
                    flag = 0
                    continue
                if re.search(del_str[0], file_line):
                    modify_line = file_line.split('.')[-1].replace(del_str[0], '.py')
                    write_con.append(modify_line)
                    continue
                if re.search(del_str[1], file_line):
                    modify_line = file_line.split('.')[-1].replace(del_str[1], '')
                    write_con.append(modify_line)
                    continue
                write_con.append(file_line)
        with open(os.path.join(abspath_rstfiles_dir, rst_file), 'w') as fw:
            fw.writelines(write_con)


if __name__ == '__main__':

    abspath_rstfiles_dir = os.path.join(sphinxPath, 'sphinx/doc/source')
    print(abspath_rstfiles_dir)
    source_path = os.listdir(abspath_rstfiles_dir)
    modify_doc_title_dir(source_path)
