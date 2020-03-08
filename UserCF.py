#coding:utf-8

import math
"""
计算用户相似性需要计算两两用户的相似性O(n^2),但是商品数量是大量的，且每个用户兴趣商品也不一样，那么可能存在大量的用户
商品空间交集为空，于是可先有用户交集的商品库，即建立商品-用户倒排表（类似搜索的倒排索引），然后填充用户相似矩阵的分子部分
"""
def UserSimilarity(train):
    inverse_dict = {}
    N = {}
    # create inverse table
    for u, iterms in train.items():
        N[u] = len(iterms)
        for item in iterms.keys():
            if item not in inverse_dict:
                inverse_dict[item] = set()
            else:
                inverse_dict[item].add(u)
    c = {}
    for item, us in inverse_dict.items():
        # foreach the interaction item
        for u in us:
            for v in us:
                if u == v:
                    continue
                else:
                    c[u][v] += 1
    w = {}
    for u, related_users in c.items():
        for v, cuv in related_users.items():
            w[u][v] = c[u][v]/math.sqrt(N[u]*N[v])
    return w

# reduce the weight of hot item
def UserSimilarity1(train):
    inverse_dict = {}
    N = {}
    # create inverse table
    for u, iterms in train.items():
        N[u] = len(iterms)
        for item in iterms.keys():
            if item not in inverse_dict:
                inverse_dict[item] = set()
            else:
                inverse_dict[item].add(u)
    c = {}
    for item, us in inverse_dict.items():
        # foreach the interaction item
        for u in us:
            for v in us:
                if u == v:
                    continue
                else:
                    c[u][v] += 1/math.sqrt(1+len(us))
    w = {}
    for u, related_users in c.items():
        for v, cuv in related_users.items():
            w[u][v] = c[u][v]/math.sqrt(N[u]*N[v])
    return w

def Recommend(user, train, w):
    rank = {}
    old_item = train[user]
    for v,w_uv in sorted(w[user].items,reverse=True)[:3]:
        for item in v:
            if item in old_item:
                continue
            else:
                rank[item] += w_uv
    return rank

