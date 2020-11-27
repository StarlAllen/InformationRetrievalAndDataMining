# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 09:21:40 2020

@author: 流转~星云
"""

import math
import numpy as np

#input qrels.txt
#output qrels_dict
def generate_tweetid_gain(file_name):
    qrels_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in qrels_dict:
                qrels_dict[ele[0]] = {}
            # here we want the gain of doc_id in qrels_dict > 0,
            # so it's sorted values can be IDCG groundtruth
            if int(ele[3]) > 0:
                qrels_dict[ele[0]][ele[2]] = int(ele[3])
    return qrels_dict
#input result.txt
#output test_dict
def read_tweetid_test(file_name):
    # input file format
    # query_id doc_id
    # query_id doc_id
    # query_id doc_id
    # ...
    test_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in test_dict:
                test_dict[ele[0]] = []
            test_dict[ele[0]].append(ele[1])
    return test_dict

#Precission @K
def MAP_eval(qrels_dict, test_dict, k = 100):
    AP_result = []
    for query in qrels_dict:
        #算出每个相关docid在测试结果中的位置 
        test_result = test_dict[query]
        true_list =qrels_dict[query].keys()
        #true_list = set(qrels_dict[query].keys())
        #print(len(true_list))
        #length_use = min(k, len(test_result), len(true_list))
        length_use = min(k, len(test_result))
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        P_result = []
        i = 0
        j = 0
        #P@K  AvgPrec
        for doc_id in test_result[0: length_use]:
            i += 1
            if doc_id in true_list:
                j += 1
                P_result.append(j / i)
                #print(i_retrieval_true / i)
            #else:
            #    P_result.append(0)
        if P_result:
            AP = np.sum(P_result) / (len(P_result))
            #AP = np.mean(P_result)
            #print('query:', query, ',AP:', AP)
            AP_result.append(AP)
        else:
            #print('query:', query, ' not found a true value')
            AP_result.append(0)
    return np.mean(AP_result)

#考虑第一个相关文档的名次位置即可
def MRR_eval(qrels_dict, test_dict, k = 100):
    RR_result = []
    for query in qrels_dict:
        test_result = test_dict[query]
        true_list = set(qrels_dict[query].keys())
        #print(len(true_list))
        #length_use = min(k, len(test_result), len(true_list))
        length_use = min(k, len(test_result))
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        P_result = []
        i = 0
        i_retrieval_true = 0
        
        for doc_id in test_result[0: length_use]:
            i += 1
            if doc_id in true_list:
                i_retrieval_true = 1
                P_result.append(i_retrieval_true / i)
                #第一个相关文档出现即退出
                break
                #print(i_retrieval_true / i)
        if P_result:
            RR = np.sum(P_result)/1.0
            #print('query:', query, ',RR:', RR)
            RR_result.append(RR)
        else:
            #print('query:', query, ' not found a true value')
            RR_result.append(0)
    return np.mean(RR_result)

'''
Normalized Discounted cumulative gain 
归一化折损累计增益
NDCG基于两个假设：
高度相关的文档比边缘相关的文档更加有用
文档的排名越低，对用户越无用
'''

def NDCG_eval(qrels_dict, test_dict, k = 100):
    NDCG_result = []
    for query in qrels_dict:
        test_result = test_dict[query]  #test idset        
        
        #true related
        true_list = list(qrels_dict[query].values())
        true_list = sorted(true_list[0:k], reverse=True)        
        #true_list = true_list[0:k]
        #print(true_list[1:5])
        
        i = 1       
        rel1 = qrels_dict[query].get(test_result[0], 0)
        #DCG = (pow(2, rel1)-1)        
        DCG = rel1
        IDCG = true_list[0]
        #IDCG = test_dict[query].get(true_list[0],0)
        #IDCG =  pow(2, true_list[0])-1
        
        # maybe k is bigger than arr length
        length_use = min(k, len(test_result), len(true_list))
        
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        
        for doc_id in test_result[1: length_use]:            
            rel = qrels_dict[query].get(doc_id, 0) #rel：在某位置上的相关度 0 1 2
            DCG += rel/math.log(i+1,2)
            IDCG += true_list[i]/math.log(i+1,2)
            #DCG += (pow(2, rel) - 1) / math.log(i+1, 2)  #对测试结果的排名做一个惩罚
            #IDCG += (pow(2, true_list[i]) - 1) / math.log(i+1, 2)
            i += 1
        #标准化
        NDCG = DCG / IDCG
        #print('query', query, ', NDCG: ', NDCG)
        NDCG_result.append(NDCG)
    return np.mean(NDCG_result)

def evaluation():
    k = 100
    # query relevance file
    file_qrels_path = 'F:\\Dataset\\qrels.txt'
    # qrels_dict = {query_id:{doc_id:gain, doc_id:gain, ...}, ...}
    qrels_dict = generate_tweetid_gain(file_qrels_path)
    # ur result, format is in function read_tweetid_test, or u can write by ur own
    file_test_path = 'F:\\Dataset\\result.txt'
    #file_test_path ='F:Dataset\\my_result_PLN_BM25.txt'
    # test_dict = {query_id:[doc_id, doc_id, ...], ...}
    test_dict = read_tweetid_test(file_test_path)
    MAP = MAP_eval(qrels_dict, test_dict, k)
    print('MAP', ' = ', MAP, sep='')
    MRR = MRR_eval(qrels_dict, test_dict, k)
    print('MRR', ' = ', MRR, sep='')
    NDCG = NDCG_eval(qrels_dict, test_dict, k)
    print('NDCG', ' = ', NDCG, sep='')
if __name__ == '__main__':
    evaluation()

