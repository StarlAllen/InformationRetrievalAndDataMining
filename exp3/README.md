<font face="宋体" size="4" color="black"> 
内容 
</font>

# IR_Evaluation

information retrieval evaluation on  tweets(based on MAP,MRR and NDCG)

#### 学号：201800130119

#### 姓名： 刘欣

## 一、实验步骤：

### 1、qrel提取

首先根据qrels.txt读取得到qrels,并以字典形式保存。

同理，对测试结果集同样返回query的rels

### 2、MAP_eval：（Mean Average Precision）

##伪代码

AP_result = []

for query in qrels_dict：

    #calculate related doc_id
    
    P_result = []#Define a list to storage scores
    
    idx1=0  #记录遍历表test_result的索引
    
    idx2=0  #记录对应前idx2个的检索结果在topK中出现次数
    
    for doc_id in test_result：
    
        idx1 += 1
        
        if doc_id in true_list:
            
            idx2 += 1
            
            P_result.append(idx2/idx1)
    
    #mean of P
    
    AP = mean(P_result)
    
    AP_result.append(AP)

return  mean(AP_result)

### 3.MRR_eval:(Mean Reciprocal Rank)

just consider first relevant doc

score =  1/k   where k is the relevant doc's position

### 4.NDCG:(Normalized Discounted Cumulative Gain)

计算流程与MAP相似，具体的值计算公式如下：

**计算公式**

$$
DCG_n = rel_1 + \Sigma_{i=2}^{n}\frac{rel_i}{\log_2i}
$$

$$
NDCG_n = \frac{DCG_n}{IDCG_n}
$$

**！！注意该算法的第一项计算方式是不一样的，需要单独拿出来算 **

## 实验过程中存在问题及解决办法：

### MAP中，求每个query平均值考虑了在真实集中不存在的元素

实际上，我们求的是平均精确度，在计算平均值的时候，只需要考虑相关的即可，不相关文档（评分为0）不算在内

### NDCG的计算方法
现在有两种方法，第一种：书上的直接rel计算，并且第一项要单独计算（否则第一项分母为零的情况）
第二种：采用pow(2,rel)-1/math.log(i+1,2)的方法，直接可以从第一项开始算起。
要理解两者之间的不同，并且只能采用其中一种来计算。






