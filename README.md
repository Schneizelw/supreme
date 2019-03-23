# supreme
我的大学毕业设计


1. 在/root/supreme下面(Dockfile所在的路径)
build生成image镜像
-> docker build -t imagename:tag .
再次检查是否生成
-> docker images
打开容器运行
-> docker run -d -p 6800:6800 imagename:tag
检查是否运行成功或失败
-> docker ps 

2. 将该image打上tag push到docker hub
打tag
-> docker tag imagename:tag dockerusername/imagename:tag
push到远端
-> docker push dockerusername/imagename:tag

3. 到slave端的服务器将该docker拉下来运行
docker run -d -p 6800:6800 dockerusername/imagenaem:tag

4. 进入scrapyd项目(lianjia)路径下/root/supreme/lianjia
执行deploy.sh脚本,将项目add到服务器
-> bash deploy.sh deploy
执行start，开启spider任务
-> bash deploy.sh start
如果需要取消
-> bash deploy.sh cancel

5. 进入docker查看日志
获得docker container id
-> docker ps 
进入container
-> docker exec -it containerId /bin/bash
进入logs查看日志即可监察任务

