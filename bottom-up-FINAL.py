import time
from multiprocessing import Pool, cpu_count
    
    
def compute_all_histories(d,k):
    setofhistories=dict()    # setofhisotires[i] is a dictionary of the form {h_str:h, h'_str:h'}
    h0={}   # initial history
    
    setofhistories[0]={str(sorted(h0.items())):h0}  
    for i in range(1,k+1):
        setofhistories[i]={}
        for h_str, h_dict in setofhistories[i-1].items():
            for j in range(d):
                h_copy = dict_update(h_dict.copy(),j,k)
                if str(sorted(h_copy.items())) not in setofhistories[i].keys(): # not explored yet
                    setofhistories[i][str(sorted(h_copy.items()))] = h_copy
    return setofhistories



def dict_update(h:dict, m: int, k:int):
    h[m] = h.get(m, 0) + 1
    if sum(h.values()) > k:
        maxi = max(h)
        if h[maxi] == 1:
            h.pop(maxi)
        else:
            h[maxi] -= 1
    return h



def compute_value_last_round_first_case(args):
    # all tokens are already placed
    h_str, h_dict, d, n, k = args

    summa=0
    maxi = max(h_dict)
    for m in range(d):
        x=sum(v for j, v in h_dict.items() if j < m)
        if m < maxi:
            exp_rank = x+1+h_dict.get(m,0)/2
        elif m == maxi:
            exp_rank = 1+x+h_dict[m]/2 + (n-k-1)/(2*(d-m))
        else:
            exp_rank=1+k+(n-k-1)*(m-maxi)/(d-maxi) + (n-k-1)/(2*(d-maxi))
        summa+=exp_rank        

    return (h_str, summa / d)


def compute_value_last_round_second_case(args):
    # not all token are placed yet
    h_str, h_dict, d = args

    summa = 0
    for m in range(d):

        x=sum(v for j, v in h_dict.items() if j < m)
        exp_rank = x+1+h_dict.get(m,0)/2
            
        summa+=exp_rank
    return (h_str, summa / d)

def compute_value_first_case(args):
    # all tokens are already placed
    h_str, h_dict, d, n, k, r, Value = args
    summa = 0
    maxi = max(h_dict)

    for m in range(d):
        tag = 0
        x = sum(v for j, v in h_dict.items() if j < m)
        if m < maxi:
            tag = 1
            exp_rank = x + 1 + h_dict.get(m, 0) / 2
            h_prime = dict_update(h_dict.copy(),m,k)

        elif m == maxi:
            exp_rank = 1 + x + h_dict[m]/2 + (n-r-k-1)/(2*(d-m))
        else:
            exp_rank = 1 + k + (n-r-k-1)*(m-maxi)/(d-maxi) + (n-r-k-1)/(2*(d-maxi))
        exp_rank += (r-1) * ((m+1/2) / d)
        
        valuestop = exp_rank
        if tag == 0:
            valuenostop = Value.get(h_str, float('inf'))
        else:
            valuenostop = Value.get((str(sorted(h_prime.items()))), float('inf'))
        
        value = min(valuestop, valuenostop)
        summa += value

    return (h_str, summa / d)

def compute_value_second_case(args):
    # not all token are placed yet
    h_str, h_dict, d, k, r, Value = args
    summa = 0
    

    for m in range(d):
        x=sum(v for j, v in h_dict.items() if j < m)
        h_prime = dict_update(h_dict.copy(),m,k)

        exp_rank = x+1+h_dict.get(m,0)/2 + (r-1)*((m+1/2)/d)
            
        valuestop=exp_rank       
        valuenostop=Value.get((str(sorted(h_prime.items()))), float('inf'))

        value=min(valuestop,valuenostop)
        summa+=value

    return (h_str, summa / d)

def compute_exp_rank(n,d,k):  
    if n==1:
        return 1  

    setofhistories = compute_all_histories(d,k)

    print(f'time to compute histories:{time.time()-start}')
    Value = {}

    with Pool(cpu_count()) as pool:
        if n-1 >= k:
            args = [(h_str, h_dict, d, n, k) for h_str, h_dict in setofhistories[k].items()]
            results = pool.map(compute_value_last_round_first_case, args)
        else:
            args = [(h_str, h_dict, d) for h_str, h_dict in setofhistories[n-1].items()]
            results = pool.map(compute_value_last_round_second_case, args)
        for res in results:
            Value[res[0]] = res[1]
        print(f'done for last level; time for computing last level is {time.time()-start}')
        
        # print(f'number of cores: {cpu_count()}')
        for r in range(2, n+1):
            if n-r >= k:
                case = 1
                args = [(h_str, h_dict, d, n, k, r, Value) for h_str, h_dict in setofhistories[k].items()]
                results = pool.map(compute_value_first_case, args)
            else:
                case = 2
                args = [(h_str, h_dict, d, k, r, Value) for h_str, h_dict in setofhistories[n-r].items()]
                results = pool.map(compute_value_second_case, args)
            for res in results:
                Value[res[0]] = res[1]
            # print(f'deleting previous level...')
            keys_to_delete = [key for key in Value.keys() if key[1] == r-1]
            for key in keys_to_delete:
                del Value[key]
            print(f'done for level {r}; this level fell into case {case}; time for computing this level is {time.time()-start}')
    return Value['[]']

if __name__ == "__main__":
    for n in [5]:
        for d in [1000]:
            for k in [3]:
                print(f'computing for n={n}, d={d}, k={k}')
                start = time.time()
                result=compute_exp_rank(n,d,k)
                print("f_bottom_up({},{},{})={}".format(n,d,k,result), f'time = {time.time() - start}')



# if valuestop<valuenostop: 
#     print('stop') 
# else:
#     print('nostop')
