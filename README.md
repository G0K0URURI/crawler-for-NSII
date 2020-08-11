# crawler-for-NSII

这是一个用于从NSII上爬取标本信息的程序。

该程序主要有两个功能：爬取某一物种的所有标本信息；从标本信息中筛选出采集地信息精度为县级或以上的标本，利用高德地图进行地名规范化、查找经纬度，最后保留省市县三级行政规划、经纬度和行政区划代码。其中高德地图API见https://lbs.amap.com/api/webservice/guide/api/georegeo
