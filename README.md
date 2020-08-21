# ipstatistics



ipstatistics是一个基于ipip库的，用于快速筛选ip列表的脚本，可以快速筛选出国家、地区以及排除特殊地区的ip目标。



# Installation

**ipstatistics使用基于ipip基本库，配合完整收费版ipip库可获得完整体验。除收费版以外，可以使用试用版ipip库体验使用。**



- [https://www.ipip.net/product/ip.html#ipv4city](https://www.ipip.net/product/ip.html#ipv4city)



修改配置脚本中的ipdb路径

```
db = ipdb.City(os.path.abspath('./ipipfree.ipdb'))
```



安装基本库

```
python3 -m pip install ipip-ipdb
```



# Usage

![](./help.jpg)

聚合国家统计

![](./country_rank.jpg)

筛选地区统计

![](./province_rank.jpg)

筛选url列表

![](filter.jpg)