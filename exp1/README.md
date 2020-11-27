# InvertedIndex-BooleanRetrieval
# by 刘欣 201800130119
exp on tweets dataset about Inverted index and boolean retireval model

Inverted index process:

对于每一项词条，提取id,name,tweet等信息，调用TextBlob库函数做单词的还原处理等。

接下来定义倒排字典，遍历词条的单词项，判断是否在字典中，如果在字典中就将该词项所在id加入到该词项字典中，如果不在字典中，将该次添加到字典中并加入对应id。


Boolean retrieval model:
(and or not)
and: 两个集合求交集
or:  两个集合求并集
not: 两个集合求差集

查询组合：
A and B and C:
先处理前两项，然后处理第三项。
优化做法：先合并较短两项，再与最后一项合并。

A or B and C
先处理A or B 再处理and  C




