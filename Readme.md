1: 能够分布式

(1): start_urls

(2): queue-requests

(3): queue-dupefilter

Above save in the same PC's redis

2: 各个机器能够计算负载，是个机器根据自己的负载智能的执行爬虫

1: 机器负载严重，如何控制爬虫量或爬虫速度

3：对各节点的监控及对各个任务的在每个节点的监控

(1): 执行执行情况， 负载如何

参考: scrapy官方的监控

4：数据的展示， 与数据库对接, 数据下载功能

(1)：分别存储于于mysql，mongodb的方案

(2): 页面下载更，批量下载， 如果数据量太大(500M)怎么下载

5: 健全的日志功能

6: 调度系统(celery)：
改变任务的定时时间


#############################

6: 可视化用selenium来获取整个动态加载的网页
(1):  页面部分是动态加载的，像京东
(2):  整个页面使动态加载
(3):  加载内容为json



国内同行：
http://www.zaoshu.io/
http://www.hicrawler.com/

国外:
https://www.import.io/


######################################
基于redis+bloomfilter过滤的python package install:

(1): Install Hiredis:

###### On Mac:
brew install hiredis

###### With Ubuntu:
apt-get install libhiredis-dev

###### From source:
git clone https://github.com/redis/hiredis
cd hiredis && make && sudo make install

Note that `libhiredis.so.0.13` file, Default location is `/usr/local/lib/libhiredis.so.0.13`, 
but you ` import pyreBloom` code yield error: 'ImportError: libhiredis.so.0.13: cannot open shared object file: No such file or directory'

Methods: cp /usr/local/lib/libhiredis.so.0.13 /usr/local/lib64/

(2): 可以在虚拟环境或系统环境：
git@github.com:seomoz/pyreBloom.git
cd pyreBloom
pip install -r requirements.txt
python setup.py install

######
Relate dProject:

(1): apollo

(2): elastic_jobs
