import random
import numpy as np
from collections import defaultdict


def get_ur(df):
    """
    Method of getting user-rating pairs
    Parameters
    ----------
    df : pd.DataFrame, rating dataframe

    Returns
    -------
    ur : dict, dictionary stored user-items interactions
    """
    ur = defaultdict(set)
    for _, row in df.iterrows():
        ur[int(row['user'])].add(int(row['item']))

    return ur


def build_candidates_set(test_ur, train_ur, item_pool, candidates_num=1000):
    """
    method of building candidate items for ranking
    Parameters
    ----------
    test_ur : dict, ground_truth that represents the relationship of user and item in the test set
    train_ur : dict, this represents the relationship of user and item in the train set
    item_pool : the set of all items
    candidates_num : int, the number of candidates
    Returns
    -------
    test_ucands : dict, dictionary storing candidates for each user in test set
    """
    # random.seed(1)
    test_ucands = defaultdict(list)
    for k, v in test_ur.items():
        sample_num = candidates_num - len(v) if len(v) < candidates_num else 0
        sub_item_pool = item_pool - v - train_ur[k] # remove GT & interacted
        sample_num = min(len(sub_item_pool), sample_num)
        if sample_num == 0:
            samples = random.sample(v, candidates_num)
            test_ucands[k] = list(set(samples))
        else:
            samples = random.sample(sub_item_pool, sample_num)
            test_ucands[k] = list(v | set(samples))
    
    return test_ucands


def precision_at_k(r, k):
    """
    Precision calculation method
    Parameters
    ----------
    r : List, list of the rank items
    k : int, top-K number

    Returns
    -------
    pre : float, precision value
    """
    assert k >= 1
    r = np.asarray(r)[:k] != 0
    if r.size != k:
        raise ValueError('Relevance score length < k')
    # return np.mean(r)
    pre = sum(r) / len(r)

    return pre


def recall_at_k(rs, test_ur, k):
    """
    Recall calculation method
    Parameters
    ----------
    rs : Dict, {user : rank items} for test set
    test_ur : Dict, {user : items} for test set ground truth
    k : int, top-K number

    Returns
    -------
    rec : float recall value
    """
    assert k >= 1
    res = []
    for user in test_ur.keys():
        r = np.asarray(rs[user])[:k] != 0
        if r.size != k:
            raise ValueError('Relevance score length < k')
        if len(test_ur[user]) == 0:
            raise KeyError(f'Invalid User Index: {user}')
        res.append(sum(r) / len(test_ur[user]))
    rec = np.mean(res)

    return rec


def mrr_at_k(rs, k):
    """
    Mean Reciprocal Rank calculation method
    Parameters
    ----------
    rs : Dict, {user : rank items} for test set
    k : int, topK number

    Returns
    -------
    mrr : float, MRR value
    """
    assert k >= 1
    res = 0
    for r in rs.values():
        r = np.asarray(r)[:k] != 0 
        for index, item in enumerate(r):
            if item == 1:
                res += 1 / (index + 1)
    mrr = res / len(rs)

    return mrr


def ap(r):
    """
    Average precision calculation method
    Parameters
    ----------
    r : List, Relevance scores (list or numpy) in rank order (first element is the first item)

    Returns
    -------
    a_p : float, Average precision value
    """
    r = np.asarray(r) != 0
    out = [precision_at_k(r, k + 1) for k in range(r.size) if r[k]]
    if not out:
        return 0.
    a_p = np.sum(out) / len(r)

    return a_p


def map_at_k(rs):
    """
    Mean Average Precision calculation method
    Parameters
    ----------
    rs : Dict, {user : rank items} for test set

    Returns
    -------
    m_a_p : float, MAP value
    """
    m_a_p = np.mean([ap(r) for r in rs])
    return m_a_p


def dcg_at_k(r, k):
    """
    Discounted Cumulative Gain calculation method
    Parameters
    ----------
    r : List, Relevance scores (list or numpy) in rank order
                (first element is the first item)
    k : int, top-K number

    Returns
    -------
    dcg : float, DCG value
    """
    assert k >= 1
    r = np.asfarray(r)[:k] != 0
    if r.size:
        dcg = np.sum(np.subtract(np.power(2, r), 1) / np.log2(np.arange(2, r.size + 2)))
        return dcg
    return 0.


def ndcg_at_k(r, k):
    """
    Normalized Discounted Cumulative Gain calculation method
    Parameters
    ----------
    r : List, Relevance scores (list or numpy) in rank order
            (first element is the first item)
    k : int, top-K number

    Returns
    -------
    ndcg : float, NDCG value
    """
    assert k >= 1
    idcg = dcg_at_k(sorted(r, reverse=True), k)
    if not idcg:
        return 0.
    ndcg = dcg_at_k(r, k) / idcg

    return ndcg


def hr_at_k(rs, test_ur):
    """
    Hit Ratio calculation method
    Parameters
    ----------
    rs : Dict, {user : rank items} for test set
    test_ur : (Deprecated) Dict, {user : items} for test set ground truth

    Returns
    -------
    hr : float, HR value
    """
    # another way for calculating hit rate
    # numer, denom = 0., 0.
    # for user in test_ur.keys():
    #     numer += np.sum(rs[user])
    #     denom += len(test_ur[user])

    # return numer / denom
    uhr = 0
    for r in rs.values():
        if np.sum(r) != 0:
            uhr += 1
    hr = uhr / len(rs)

    return hr

def get_feature(feature_list):
    if 'gender' in feature_list:
        feature_num = 0
    elif 'age' in feature_list:
        feature_num = 1
    elif 'gender' in feature_list and 'age' in feature_list:
        feature_num = 2
    elif 'gender' not in feature_list and 'age' not in feature_list:
        feature_num = 3
    
    return feature_num

def get_user_info(df, feature_num):
    user_info = dict()
    for _, row in df.iterrows():
        if feature_num == 0:
            user_info[int(row['user'])] = [int(row['gender'])]
        elif feature_num == 1:
            user_info[int(row['user'])] = [int(row['age'])]
        elif feature_num == 2:
            user_info[int(row['user'])] = [int(row['gender']), int(row['age'])]
    return user_info

