背景

现在自动化框架暂无清晰的API文档，给今后的代码编写、查阅及维护造成一定的困扰，为了实现将所有测试用例脚本中的注释导出、查阅，查阅网上多数人使用的工具，决定采用sphinx实现自动产生参考文档、索引等。

sphinx的优点：

- 支持多种输出格式：html、Latex、ePub等；
- 丰富的扩展
- 结构化文档
- 自动索引
- 支持语法高亮

## 环境

- 安装Python

- sphinx

  ```shell
  pip install sphinx
  ```

## 实例

#### 目录结构

下面举例展示sphinx相关的目录，初始时需手动创建doc目录，而src目录是框架中需要导出用例的目录。

- sphinx

  - doc

  - src

    - scripts1
  
      - test1.py
    - test11.py
  
    - scripts2
    
      - test2.py
    - test22.py
    
      
    

#### 建立API文档

1. 进入/doc目录下，输入 sphinx-quickstart，会出现一些选项，根据需要填写即可

   ```
   D:\>cd D:\keeplearning\myLearning\Tools_Skills\sphinx\doc
   
   D:\keeplearning\myLearning\Tools_Skills\sphinx\doc>sphinx-quickstart
   Welcome to the Sphinx 2.2.1 quickstart utility.
   
   Please enter values for the following settings (just press Enter to
   accept a default value, if one is given in brackets).
   
   Selected root path: .
   
   You have two options for placing the build directory for Sphinx output.
   Either, you use a directory "_build" within the root path, or you separate
   "source" and "build" directories within the root path.
   > Separate source and build directories (y/n) [n]: y
   
   The project name will occur in several places in the built documentation.
   > Project name: KeepCoding
   > Author name(s): zyp
   > Project release []: 1.0
   
   If the documents are to be written in a language other than English,
   you can select a language here by its language code. Sphinx will then
   translate text that it generates into that language.
   
   For a list of supported codes, see
   https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
   > Project language [en]: zn_CN
   
   Creating file .\source\conf.py.
   Creating file .\source\index.rst.
   Creating file .\Makefile.
   Creating file .\make.bat.
   
   Finished: An initial directory structure has been created.
   
   You should now populate your master file .\source\index.rst and create other documentation
   source files. Use the Makefile to build the docs, like so:
      make builder
   where "builder" is one of the supported builders, e.g. html, latex or linkcheck.
   ```

   

2. 然后出现以下目录结构：

   sphinx

   - doc

     - build
     - source
       - _static
       - _templates
       - conf.py
       - index.rst
     - make.bat
     - Makefile

   - src

     - scripts1

       - test1.py
       - test11.py

     - scripts2

       - test2.py
       - test22.py

       

3. 部分分解说明

   - **Makefile**：可以将它看作是一个包含指令的文件，在使用 `make` 命令时，使用这些指令来构建文档输出。
   - **_build**：这是触发特定输出后用来存放所生成的文件的目录。
   - **_static**：所有不属于源代码（如图像）一部分的文件均存放于此处，稍后会在构建目录中将它们链接在一起。
   - **conf.py**：这是一个 Python 文件，用于存放 Sphinx 的配置值，包括在终端执行 `sphinx-quickstart` 时选中的那些值。
   - **index.rst**：文档项目的 root 目录。如果将文档划分为其他文件，该目录会连接这些文件。

   

4. conf.py文件中可以修改配置：

   配置confi.py：

   ```python
   import os
   import sys
   sys.path.insert(0, os.path.abspath('../../src'))  # 指向src(需要导出用例的目录)
   ```

   为sphinx添加扩展：

   ```python
   extensions = ['sphinx.ext.autodoc',
       'sphinx.ext.doctest',
       'sphinx.ext.intersphinx',
       'sphinx.ext.todo',
       'sphinx.ext.coverage',
       'sphinx.ext.mathjax',
       'sphinx.ext.napoleon'
   ]
   ```

   更换sphinx的主题：

   ```python
   # html_theme = 'alabaster' 默认主题
   import sphinx_rtd_theme    # 需要先pip install sphinx_rtd_theme
   html_theme = 'sphinx_rtd_theme'
   html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
   ```

5. 生成html文件

   不建议把src所有文件一次性生成，不要使用如下操作，否则会产生重复内容：

   ```shell
   sphinx-apidoc -o ./source ../src/ # 这是将src目录下的所有py脚本注释导出，包括src中所有子目录中的脚本
   ```

   需要导出哪个目录的脚本注释，就单独导出。

   正确操作：命令行切换到doc目录下，依次执行：

   ```
   sphinx-apidoc -o [生成rst的位置] [项目代码的位置] -f(强制重新覆盖写，否则会检测，如果有同名文件存在，会跳过不更新)
   ```

   ```shell
   sphinx-apidoc -o ./source ../src/scripts1/  # 这是将src/scriptes1/目录下的所有py脚本注释导出，包含子目录中的py脚本
   sphinx-apidoc -o ./source ../src/scripts2/
   ```

   再执行：

   ```shell
   make clean  # 删除build目录下的文件（第一次build为空文件夹）
   make html	# 在build目录下生成 doctrees、html 目录
   ```

   确认最后输出中含有 `build succeesed`，

   再去build/html目录中检查是否生成了对应的html等其他文件。

   

6. 谷歌浏览器打开build/html/index.html，查看API文档

7. 修改界面展示

   1. **如果需要修改主页的展示效果，可以改变rst文件中的一些格式，或者增加rst文件**
   2.  生成的导航中会多出一些节点， 如： Submodules  Subpackages， 如何不生成这些节点?  直接运行changeFormat.py文件（这里参考自：https://blog.csdn.net/ypfeime/article/details/92319685）

   

## 文档更新

- 情况1：修改了rst文件，或者在src目录下的某个子文件夹中添加或修改了 xxx.py 等一个或多个文件，比如src/scripts1/中增加或修改了py文件：
  1. 直接切换到doc目录下，执行`make html`

- 情况2：在src目录中添加了newadd 文件夹，且里面含有py脚本：
  1. 切换到doc目录下，先执行`sphinx-apidoc -o ./source ../src/newadd/ `
  2. 再执行`make html`



## sphinx语法

sphinx采用 reStructuredText (reST) 的概念和语法 。

1. 章节标题： 在双上划线符号之间（或为下划线）, 并且符号的长度不能小于文本的长度: 

   ```
   Welcome to UTest API documentation!
   =======================================
   
   ```

   通常没有专门的符号表示标题的等级，但是对于Python 文档，可以这样认为:

   - `#` 及上划线表示部分
   - `*` 及上划线表示章节
   - `=`, 小章节
   - `-`, 子章节
   - `^`, 子章节的子章节
   - `"`, 段落

   

2. 内联标记 (与markdown语法一致)

   - 星号: `*text*`   斜体： *example演示*
   - 双星号: `**text**`  加粗 ：**example演示**
   - 反引号: \`\`\`code\`\`\`   代码样式： ```example演示```

    **注**：星号及反引号在文本中容易与内联标记符号混淆，可使用反斜杠符号转义. 

   标记的一些限制：

   - 不能相互嵌套
   - 内容前后不能由空白: 这样写``* text*`` 是错误的
   - 如果内容需要特殊字符分隔. 使用反斜杠转义，如: `thisis\ *one*\ word`

   

3. 列表

    列表标记仅在段落的开头，列表可以嵌套，但是需跟父列表使用**空行分隔** 

   ```
        * Item Foo
   
           * childitem foo1
           * childitem foo2
   
        * Item Bar
   
           1. childitem bar1
           2. childitem bar2
           
            #. Item 1
        #. Item2
        
           * childitem foo1
           * childitem foo2
   
        1. item3
        2. item4
   
           1. childitem1
           2. chidlitem2
   
   ```

   

4. 跳转到某一标签

   方式一：

    标签直接放在章节标题前面

   在 demo1.rst 中设置标签：

   ```
   .. _demo1.py-label:
   
   demo1 module
   ============
   
   ```

    在其他文件中可以通过 :ref:\`demo1.py-label\` 来跳转

   ```
   :ref:`demo1.py-label`.
   
   ```

   

   方式二：

    标签不放在章节开头，但是需要给出明确的链接

   在demo3.rst中设置标签，此时标签可以不放在章节开头：

   ```
   demo3 module
   ============
   .. _demo3.py-label:
   
   ```

    在其他文件中可以通过 :ref:\`name <demo3.py-label>\`. 来跳转，这里name可以任意命名

   ```
   :ref:`name <demo3.py-label>`.
   
   ```

   ​	

5. 显性标记

   显性标记不展示在html中，有点像注释的感觉。主要是用在那些需做特殊处理的reST结构中，如尾注，突出段落，评论，通用指令。显式标记以 `..` 开始，后跟空白符，段落的缩进一样。（在显示标记与正常的段落间需有空行）

   ```
   .. sphinx_demo documentation master file, created by
      sphinx-quickstart on Fri Nov  1 11:10:41 2019.
   
   .. toctree::
      :maxdepth: 4
      :caption: Contents:
   
   ```

   

6. 某个测试框架使用模板：

   ```python
   def test_123():
       """
       [用例描述]：
           版本测试用例简述（通俗易懂）
       [测试策略]：
           * 跳过条件；
           * 设备间策略差异等.
       [测试数据]：
           1. 示例1:遍历测试所有支持的编码格式
           2. 示例2:不同采集制式下，遍历不同ucode模式
       [前置条件]：
           1. module-setup_module:
           2. class-setup_class:
           3. function-setup_function:
       [测试步骤]：
           1. 示例1：
               1. 设置（修改）。。。。，检查。。。；
               2. 设置。。。。，检查。。。；
               3. 设置。。。。，检查。。。；
           2. 示例2：
               1. 设置。。。。；
               2. 设置。。。。；
               3. 检查的违章包括：
                   * 压线、 11
                   * 压双黄线、 9
                   * 压单黄线、10
                   * 逆行、2
       [后置条件]：
           1. function-setup_function:
           2. class-setup_class:
           3. module-setup_module:
       """
       pass
   
   ```

   注意点：

   1. 注释中的换行一律使用Enter，然后使用Tab缩进；
   2. 在[用例描述]：[测试策略]：这样的标题后面不要写文字，Enter换行后写； 如果没有需要添加的内容，换行后写“无”字；
   3. 对于选择用序号1.2.3还是* ， 如果有明确的先后步骤请使用1.2.3. ， 没有先后顺序或步骤根据自己审美选择用1.2.3或* ；
   4. 使用1.2.3.时需要英文输入法, 同时注意标记符号与 内容之间需要有空格；
   5. 如果有其他更好的写法欢迎补充，最终看在html中展示的结果为准，同时最好能兼顾脚本中注释的美观。