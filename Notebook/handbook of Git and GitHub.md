# Git和GitHub手册

## 安装Git

从[Git主站](http://git-scm.com/)下载并安装。

安装完成后，可以在开始菜单里找到**Git->Git Bash**，打开Git Bash，进行最后一步设置，即在命令行输入：
```
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
```

## 建立版本库（repository）

版本库可以理解为一个目录，这个目录里面的所有文件都可以被Git管理起来，每个文件的修改、删除，Git都能跟踪，以便任何时刻都可以追踪历史，或者在将来某个时刻可以“还原”。

1. 建立一个目录
2. 通过`git init`命令把这个目录变成Git可以管理的仓库

瞬间Git就把仓库建好了，而且告诉你是一个空的仓库（empty Git repository），细心的读者可以发现当前目录下多了一个.git的目录，这个目录是Git来跟踪管理版本库的，没事千万不要手动修改这个目录里面的文件，不然改乱了，就把Git仓库给破坏了。

该目录我们称为工作区，工作区的隐藏目录.git，就是版本库。Git的版本库里存了很多东西，其中最重要的就是称为stage（或者叫index）的暂存区，还有Git为我们自动创建的第一个分支master，以及指向master的一个指针叫HEAD。
![alt text](C:/Room/Warehouse/GitWork/images/001/Image03.jpg)

我们把文件往Git版本库里添加的时候，是分两步执行的：

1. 用`git add`把文件添加进去，实际上就是把文件修改添加到暂存区；
2. 用`git commit`提交更改，实际上就是把暂存区的所有内容提交到当前分支。

因为我们创建Git版本库时，Git自动为我们创建了唯一一个master分支，所以，现在，git commit就是往master分支上提交更改。你可以简单理解为，需要提交的文件修改通通放到暂存区，然后，一次性提交暂存区的所有修改。

看图说话，如何进行add和commit：
![alt text](C:/Room/Warehouse/GitWork/images/001/Image04.jpg)
![alt text](C:/Room/Warehouse/GitWork/images/001/Image05.jpg)

## 添加文件到文件库

和把大象放到冰箱需要3步相比，把一个文件放到Git仓库只需要两步。例如现在我们编写一个**readme.txt**文件，内容如下：
```
Git is a version control system.
Git is free software.
```

1. 用命令`git add`告诉Git，把文件添加到仓库
```
$ git add readme.txt
```
2. 用命令`git commit`告诉Git，把文件提交到仓库
```
$ git commit -m "wrote a readme file"
```

为什么Git添加文件需要add，commit一共两步呢？因为commit可以一次提交很多文件，所以你可以多次add不同的文件。

## 修改文件

我们已经成功地添加并提交了一个readme.txt文件，现在，是时候继续工作了，于是，我们继续修改readme.txt文件，改成如下内容：
```
Git is a distributed version control system.
Git is free software.
```

现在，运行git status命令查看结果：
```
$ git status
```

虽然Git告诉我们readme.txt被修改了，但如果能看看具体修改了什么内容，自然是很好的。比如你休假两周从国外回来，第一天上班时，已经记不清上次怎么修改的readme.txt，所以，需要用git diff这个命令查看：
```
$ git diff readme.txt
```

知道了对readme.txt作了什么修改后，再把它提交到仓库就放心多了，提交修改和提交新文件是一样的。

## 历史记录

在Git中，我们用`git log`命令查看历史记录
```
$ git log
$ git log --pretty=oneline
```

你看到的一大串类似3628164...882e1e0的是**commit id（版本号）**。

每提交一个新版本，实际上Git就会把它们自动串成一条时间线。如果使用可视化工具查看Git历史，就可以更清楚地看到提交历史的时间线

如果回到了某个版本，再想查看未来的历史记录，用`git log`就不行了，要用`git reflog`

## 时间穿梭机

现在，我们要把当前版本回退到上一个版本，就可以使用`git reset`命令
```
$ git reset --hard HEAD^
```

在Git中，用HEAD表示当前版本，也就是最新的提交3628164...882e1e0（注意我的提交ID和你的肯定不一样），上一个版本就是HEAD^，上上一个版本就是HEAD^^，当然往上100个版本写100个^比较容易数不过来，所以写成HEAD~100。

Git的版本回退速度非常快，因为Git在内部有个指向当前版本的HEAD指针，当你回退版本的时候，Git仅仅是把HEAD从指向append GPL：
![alt text](C:/Room/Warehouse/GitWork/images/001/Image01.jpg)
改为指向add distributed：
![alt text](C:/Room/Warehouse/GitWork/images/001/Image02.jpg)
然后顺便把工作区的文件更新了。

我们也可以回到指定的版本，例如
```
$ git reset --hard 3628164
```

## 撤销修改

Git告诉你，`git checkout -- file`可以丢弃工作区的修改:
```
$ git checkout -- readme.txt
```

命令`git checkout -- readme.txt`意思就是，把readme.txt文件在工作区的修改全部撤销，这里有两种情况：一种是readme.txt自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态；一种是readme.txt已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。
总之，就是让这个文件回到最近一次git commit或git add时的状态。

Git同样告诉我们，用命令`git reset HEAD file`可以把暂存区的修改撤销掉（unstage），重新放回工作区:
```
$ git reset HEAD readme.txt
```

可见，`git reset`命令既可以回退版本，也可以把暂存区的修改回退到工作区。当我们用HEAD时，表示最新的版本。

小结：
场景1：当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时，用命令`git checkout -- file`。

场景2：当你不但改乱了工作区某个文件的内容，还添加到了暂存区时，想丢弃修改，分两步，第一步用命令`git reset HEAD file`，就回到了场景1，第二步按场景1操作。

场景3：已经提交了不合适的修改到版本库时，想要撤销本次提交，参考版本回退一节，不过前提是没有推送到远程库。

## 删除文件

在Git中，删除也是一个修改操作。一般情况下，你通常直接在文件管理器中把没用的文件删了，或者用rm命令删了：
```
$ rm test.txt
```

Git知道你删除了文件，因此，工作区和版本库就不一致了，git status命令会立刻告诉你哪些文件被删除了。

现在你有两个选择，一是确实要从版本库中删除该文件，那就用命令`git rm`删掉，并且`git commit`：
```
$ git rm test.txt
$ git commit -m "remove test.txt"
```

另一种情况是删错了，因为版本库里还有呢，所以可以很轻松地把误删的文件恢复到最新版本：
```
$ git checkout -- test.txt
```

## 远程仓库

请自行注册GitHub账号。由于你的本地Git仓库和GitHub仓库之间的传输是通过SSH加密的，所以，需要一点设置：

第1步：创建**SSH Key**。在用户主目录下，看看有没有.ssh目录，如果有，再看看这个目录下有没有id_rsa和id_rsa.pub这两个文件，如果已经有了，可直接跳到下一步。如果没有，打开Shell（Windows下打开Git Bash），创建SSH Key：
```
$ ssh-keygen -t rsa -C "youremail@example.com"
```

如果一切顺利的话，可以在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。

第2步：登陆**GitHub**，打开“Account settings”，“SSH Keys”页面：
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

设置推送，push an existing repository from the command line
```
git remote add origin https://github.com/plutoese/pluto.git
git push -u origin master
```



















