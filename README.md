**自动化轨道桥预防性维修策略优化研究-SOA算法**

使用方法：

需要python3环境

1.安装相关依赖：

```shell
pip install -r requirement.txt
```

2.运行SOA:

第一个模型：

```shell
python run_model1.py
```



第二个模型:

```shell
python run_model2.py
```

3.相关配置

SOA算法主体部分在SOA.py文件中

SOA部分配置可在config.py中进行修改，config.py中各变量含义：

n：搜索空间维数

pop_size：种群规模

generation_num：最大迭代次数

x_max：各维度最大值

x_min：各维度最小值

mu_max：最大隶属度值

mu_min：最小隶属度值

