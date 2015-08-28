# 我的工作环境配置
--------------------------
文本和代码工具：**Sublime Text 3**
版本控制工具：**Git和GitHub**
程序设计语言：**Python 3**
文本格式化语言：**Markdown**
多平台笔记工具：**印象笔记（Evernote）**
数据库工具：**MongoDB**
统计开发平台：**R和Stata**
--------------------------
## Sublime Text 3
### 安装插件管理器（Package  Control）

The simplest method of installation is through the Sublime Text console. The console is accessed via the **ctrl+`** shortcut or the **View > Show Console** menu. Once open, paste the appropriate Python code for your version of Sublime Text into the console.

*import urllib.request,os,hashlib; h = 'eb2297e1a458f27d836c04bb0cbaf282' + 'd0e7a3098092775ccb37ca9d6b2e4b7d'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)*

参见[相关网址](https://packagecontrol.io/installation#st3)

## Git和GitHub
### 安装Git

从[Git主站](http://git-scm.com/)下载并安装。

安装完成后，可以在开始菜单里找到**Git->Git Bash**，打开Git Bash，进行最后一步设置，即在命令行输入：
```
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
```

### 建立版本库（repository）

版本库可以理解为一个目录，这个目录里面的所有文件都可以被Git管理起来，每个文件的修改、删除，Git都能跟踪，以便任何时刻都可以追踪历史，或者在将来某个时刻可以“还原”。

1. 建立一个目录
2. 通过`git init`命令把这个目录变成Git可以管理的仓库

瞬间Git就把仓库建好了，而且告诉你是一个空的仓库（empty Git repository），细心的读者可以发现当前目录下多了一个.git的目录，这个目录是Git来跟踪管理版本库的，没事千万不要手动修改这个目录里面的文件，不然改乱了，就把Git仓库给破坏了。

### 远程仓库

请自行注册GitHub账号。由于你的本地Git仓库和GitHub仓库之间的传输是通过SSH加密的，所以，需要一点设置：

第1步：创建**SSH Key**。在用户主目录下，看看有没有.ssh目录，如果有，再看看这个目录下有没有id_rsa和id_rsa.pub这两个文件，如果已经有了，可直接跳到下一步。如果没有，打开Shell（Windows下打开Git Bash），创建SSH Key：
```
$ ssh-keygen -t rsa -C "youremail@example.com"
```

如果一切顺利的话，可以在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。

第2步：登陆GitHub，打开“Account settings”，“SSH Keys”页面：
然后，点“Add SSH Key”，填上任意Title，在Key文本框里粘贴id_rsa.pub文件的内容：
![alt text](C:/Room/Warehouse/GitWork/images/001/p01.png)
点“Add Key”，你就应该看到已经添加的Key：
![alt text](C:/Room/Warehouse/GitWork/images/001/p02.png)

为什么GitHub需要SSH Key呢？因为GitHub需要识别出你推送的提交确实是你推送的，而不是别人冒充的，而Git支持SSH协议，所以，GitHub只要知道了你的公钥，就可以确认只有你自己才能推送。

当然，GitHub允许你添加多个Key。假定你有若干电脑，你一会儿在公司提交，一会儿在家里提交，只要把每台电脑的Key都添加到GitHub，就可以在每台电脑上往GitHub推送了。

现在的情景是，你已经在本地创建了一个Git仓库后，又想在GitHub创建一个Git仓库，并且让这两个仓库进行远程同步，这样，GitHub上的仓库既可以作为备份，又可以让其他人通过该仓库来协作，真是一举多得。

首先，登陆GitHub，然后，在右上角找到“Create a new repo”按钮，创建一个新的仓库：
![alt text](C:/Room/Warehouse/GitWork/images/001/p03.png)
在Repository name填入learngit，其他保持默认设置，点击“Create repository”按钮，就成功地创建了一个新的Git仓库
![alt text](C:/Room/Warehouse/GitWork/images/001/p04.png)

根据提示，push an existing repository from the command line
```
git remote add origin https://github.com/plutoese/pluto.git
git push -u origin master
```

### GUI工具 —— SourceTree




