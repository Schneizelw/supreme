# supreme

## 简介

&ensp;&ensp;&ensp;&ensp;本文使用Python3.6基于Scrapy框架去实现分布式大规模爬取链家的租房和新房楼盘数据。对于封装的Ajax请求使用Splash渲染页面并且配置Nginx实现多机器负载均衡，使用Redis存取url缓存以及去重实现分布式，使用Mongodb存取数据。项目部署通过Docker对接Scrapyd实现分布式部署。最后后端使用Django搭建服务器，前端使用JavaScript开发的Echarts实现数据可视化。本系统致力于突破单机爬虫能力。



### scrapy框架
&ensp;&ensp;&ensp;&ensp;Scrapy是一款由python开发的用于抓取网站和提取结构化数据的应用程序框架。处理应有与爬虫外还广泛用于各种数据挖掘，信息处理，自动化测试，程序监控等等。主要有七个部分组成：
- Engine:框架的核心，主要控制数据流在其他本分之间的流动。
- Scheduler:主要负责处理Request，处理engine的请求，包括存储request和返回request。
- Downloader:接受engine的请求触发请求页面获取数据，将数据返回给engine。
- Downloader Middlewares:处于Engine和Downloader之间的钩子框架，用加工engine给downloader发送的的request，以及处理downloader返回给engine的response。
- Spider：代码的主要逻辑和解析规则，主要负责解析engine返回的response，生成item，返回给engine。
- Spider Middlewares:处于Engine和Spider之间的钩子框架，用于加工engine给spider发送的response，以及处理spider发送给engine的item。
- Item Pipeline: 处理engine传回的item数据，主要是清洗，整理过滤数据，以及数据入库。

![](https://github.com/Schneizelw/supreme/blob/master/imgs/scrapy.png)

- 数据流过程：
&ensp;&ensp;&ensp;&ensp;Engine首先打开一个网站，获取初始url将此url发送给scheduler，然后scheduler调度url发送给engine。Engine获取url发送给downloader，期间经过downloader middlerwares的处理，downloder请求url获取response返回给engine，期间经过downloader middlerwares处理。Engine将该response发送给spider解析，期间经过spider middlerwares的处理，spider解析网页，如果结果是item则发送给engine，期间经过spider middler wares处理，如果是新的request直接发送给request。Engine将spider返回的iem交给item pipelines处理，item pipeline将该item清洗过滤存入到数据库中。如果是新的request则发送给scheduler。

### docker部署scrapyd

1. 在/root/supreme下面(Dockfile所在的路径)
- build生成image镜像
> docker build -t imagename:tag .
- 再次检查是否生成
> docker images
- 打开容器运行
> docker run -d -p 6800:6800 imagename:tag
-检查是否运行成功或失败
> docker ps 

2. 将该image打上tag push到docker hub
- 打tag
> docker tag imagename:tag dockerusername/imagename:tag
- push到远端
> docker push dockerusername/imagename:tag

3. 到slave端的服务器将该docker拉下来运行
> docker run -d -p 6800:6800 dockerusername/imagenaem:tag

### deploy部署spider

4. 进入scrapyd项目(lianjia)路径下/root/supreme/lianjia
- 执行deploy.sh脚本,将项目add到服务器
> bash deploy.sh deploy
- 执行start，开启spider任务
> bash deploy.sh start
- 如果需要取消
> bash deploy.sh cancel

5. 进入docker查看日志
- 获得docker container id
> docker ps 
- 进入container 进入/code/logs查看日志即可监察任务
> docker exec -it containerId /bin/bash

