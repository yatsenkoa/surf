import numpy as np
from fast_pagerank import pagerank_power
from scipy import sparse
import json
from urllib.parse import urlparse


def generate_index(websites_dict: dict):
    reverse_index = {}
    index = []

    ind = 0
    for item in websites_dict.keys():
        reverse_index[item] = ind
        ind += 1

        index.append(item)

    return index, reverse_index

def generate_relational_matrix(index: dict, websites_dict: dict):
    mat_size = len(index)
    mat = np.zeros((mat_size, mat_size))
    
    for item in websites_dict.keys():
        
        total_links_x = len(websites_dict[item]['out_links'])
        x = index[item]

        for out_link in websites_dict[item]['out_links']:

            try:
                y = index[out_link]
                mat[y][x] = (1 / total_links_x)
            except Exception as e:
                continue
        
    return mat

def pagerank(mat):

    random_prob = 0.8
    mat_size = mat.shape[0]
    
    e = np.ones((mat_size, mat_size))
    r_prev = None
    A = random_prob * mat + (1 - random_prob) * (1 / mat_size) * e
    n_mat = np.ones((mat_size,)) * ((1 - random_prob) / mat_size)
    r = np.ones((mat_size,)) * (1 / mat_size)
    epsilon = 1e-10

    for i in range(5000):

        r_prev = r
        r = random_prob * np.dot(A, r) 
        r_norm = np.linalg.norm(r)
        r = r / r_norm

    return r / sum(r)

def test_pagerank():
    test_mat = np.array([[0.5, 0.5, 0], [0.5, 0, 0], [0, 0.5, 1]])
    
    print(pagerank(test_mat))

def run_pagerank():
    
    META_DICT = "../data/meta.json"
    RANK_DICT = "../data/ranks.json"

    with open(META_DICT, 'r') as meta_file:
        print('loading json...')
        dictionary = json.load(meta_file)
    
    print('making index...')
    ind, ind_rev = generate_index(dictionary)
    
    print('making relational matrix...')
    mat = generate_relational_matrix(ind_rev, dictionary)

    print('running pagerank...')
    ranks = pagerank(mat)
    
    sorted_ranks = list(ranks.argsort())
    sorted_ranks = list(map(lambda a: ind[a].split('/')[0], sorted_ranks))

    with open(RANK_DICT, 'w') as rank_file:
        
        rank_file.write(json.dumps(sorted_ranks))
    
if __name__ == "__main__":
    run_pagerank()
