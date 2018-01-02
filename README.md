# SpiderMan
Spiderman is the god

### Introduction

**2017~2018 软件课程设计--知乎爬虫**

* 简易的分布式爬虫(使用multiprocessing和queue实现)

* Selenium获取网页，解决网页动态加载问题

* PyTorch情感分析模型

### Architecture

#### **Distributed Version**

![](./arch/overall_arch.png)

##### Master

* URL Pool
* URL Filter (Based on BloomFilter and Regex, to remove duplicates or illegal urls)

##### Worker

![](./arch/worker.png)

* Request with URLs from Master Node (Based on selenium and phantomjs webdriver)
* Parse the html content (questions, answers, topics, people) 
* Save the parsed content to local storage.

#### Thread Manager

![](./arch/Thread.png)

* 使用Queue和threading封装线程池。

--- 

### Runing Process

![](./arch/process.png)

----

### Usage

````python

# run distributed version
# start master 
python master.py
# start worker
python main.py

# run single version
python master.py

````

### Licence

This project is under the **MIT** licence
