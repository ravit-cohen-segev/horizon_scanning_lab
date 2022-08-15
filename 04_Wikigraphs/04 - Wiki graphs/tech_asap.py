import collections
import multiprocessing
import networkit as nk
import pickle
import itertools
import pandas as pd
import time
from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support
import networkx as nx
print(multiprocessing.cpu_count())
def apsp(dst,G,idmap):
    src = 'Technology'
    try:
        max_len = len(nx.shortest_path(nxG, source=src, target=dst))
        paths = nk.reachability.AllSimplePaths(G, idmap[src], idmap[dst], cutoff=max_len - 1)
        paths.run()
        a = paths.getAllSimplePaths()
        sub_lst=[]
        for path in a:
            sub_lst.append(path[-2])
        a_counter = collections.Counter(sub_lst)
        most_common = a_counter.most_common()
        paths = []
        for path in a:
            # print(rev_idmap[path[-2]])
            if path[-2] == most_common[-1][0]:
                paths = paths + path
        return {"tech": dst, "set": list(set(paths)),"shortest":max_len}

    except Exception as e:
        a={}
        print(dst,e)




if __name__ == '__main__':
    freeze_support()
    nxG = 0
    with open('./New_Graph.pickle', 'rb') as handle:
        nxG = pickle.load(handle)
    G = nk.nxadapter.nx2nk(nxG)





    url = './ET_05012022.csv'
    df = pd.read_csv(url,
                     # Set first column as rownames in data frame
                     index_col=0,
                     )

    lst = list(df.index)
    start=8
    end=400
    lst=lst[:]

    idmap = dict((id, u) for (id, u) in zip(nxG.nodes(), range(nxG.number_of_nodes())))


    print("starting")
    start1 = time.time()





    pool = multiprocessing.Pool(processes=24)
    tech_lst=pool.map(partial(apsp, G=G,idmap=idmap), lst)
    print(tech_lst)

    with open(f'tech_lst-{start}-{end}.pickle', 'wb') as handle:
        pickle.dump(tech_lst, handle, protocol=pickle.HIGHEST_PROTOCOL)

    end1 = time.time()
    print(end1 - start1)