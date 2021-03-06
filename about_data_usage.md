# 数据说明


## 整体使用说明

1. 原始数据以 json 文件的格式提供，目录位于仓库的 ./data 。

2. json 文件的格式非常简单，以下 cn.json 的开头，作为例子  
   ```
   [
    {
     "date": "20200102",
     "is_open": 1,
     "comment": ""
    },
    {
     "date": "20200103",
     "is_open": 1,
     "comment": ""
    },
    ...
   ]

   ```

3. 数据更新频率。有自动化的脚本会每日/每周来自动推送最新的开放日历到 data 目录。

4. 时效性。当前暂时只维护 cn 的数据，大致维护到当天的后60-90天。


## 特定语言的脚本


如果每次使用都完整地走 http 拉取、文本解析、本地对象等流程，造成了一系列的不必要时间开销。所以，提供了带某些语言的程序接口。

1. 更便捷地调用，不用理会网络交互等细节了。

2. 性能更好。使用了本地文件缓存，内存缓存等，并且自动维护时效性。  
   比如，python 的接口，设置了内存缓存和本地文件缓存有效期为24小时，过了就从网络重新拉取。
