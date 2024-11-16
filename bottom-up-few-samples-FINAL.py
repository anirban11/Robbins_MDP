import time
from multiprocessing import Pool, cpu_count
 
def compute_all_histories(l,k):
    setofhistories=dict()   # setofhisotires[i] is a dictionary of the form {h_str:h, h'_str:h'}
    h0={}   # initial history
    
    setofhistories[0]={str(sorted(h0.items())):h0}  
    for i in range(1,k+1):
        setofhistories[i]={}
        for h_str, h_dict in setofhistories[i-1].items():
            for j in range(l+1):
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
    h_str, h_dict, d, n, k, l = args

    summa=0
    maxi = max(h_dict)
    for m in range(l+1):
        x=sum(v for j, v in h_dict.items() if j < m)
        if m < maxi:
            exp_rank = x+1+h_dict.get(m,0)/2
        elif m == maxi:
            if m<l:
                exp_rank = 1 + x + h_dict[m]/2 + (n-k-1)/(2*(d-m))
            else:
                exp_rank = (d-l)*(1 + x + h_dict[m]/2 + (n-k-1)/2)
        else:
            if m<l:
                exp_rank=1+k+(n-k-1)*(m-maxi)/(d-maxi) + (n-k-1)/(2*(d-maxi))
            else:
                exp_rank = (d-l)*(1+k+(n-k-1)*(l-maxi)/(d-maxi) + (n-k-1)*(d-l)/(2*(d-maxi)))
        summa+=exp_rank        

    return (h_str, summa / d)


def compute_value_last_round_second_case(args):
    # not all token are placed yet
    h_str, h_dict, d, l = args

    summa = 0
    for m in range(l+1):
        x=sum(v for j, v in h_dict.items() if j < m)
        if m<l:
            exp_rank = x+1+h_dict.get(m,0)/2
        else:
            exp_rank = (d-l)*(x+1+h_dict.get(m,0)/2)
            
        summa+=exp_rank
    return (h_str, summa / d)

def compute_value_first_case(args):
    # all tokens are already placed
    h_str, h_dict, d, n, k, r, Value, l = args
    summa = 0
    maxi = max(h_dict)

    # if n-r>=k:
    for m in range(l+1):
        tag = 0
        x = sum(v for j, v in h_dict.items() if j < m)
        if m < maxi:
            tag = 1
            exp_rank = x + 1 + h_dict.get(m, 0) / 2
            h_prime = dict_update(h_dict.copy(),m,k)
        elif m == maxi:
            if m<l:
                exp_rank = 1 + x + h_dict[m]/2 + (n-r-k-1)/(2*(d-m))
            else:
                exp_rank = (d-l)*(1+ x+ h_dict[m]/2 + (n-r-k-1)/2)
        else:
            if m<l:
                exp_rank = 1 + k + (n-r-k-1)*(m-maxi)/(d-maxi) + (n-r-k-1)/(2*(d-maxi))
            else:
                exp_rank = (d-l)*(1+ k+ (n-r-k-1)*(l-maxi)/(d-maxi) + (n-r-k-1)*(d-l)/(2*(d-maxi)))
        if m<l:
            exp_rank = exp_rank + ((r-1) * ((m+1/2) / d))
        else:
            exp_rank = exp_rank + ((d-l)*(r-1)*(d+l)/(2*d))
        
        valuestop = exp_rank
        if tag == 0:
            if m<l:
                valuenostop = Value.get(h_str, float('inf'))
            else:
                valuenostop = (d-l)*Value.get(h_str, float('inf'))
        else:
            if m<l:
                valuenostop = Value.get((str(sorted(h_prime.items()))), float('inf'))
            else:
                valuenostop = (d-l)*Value.get((str(sorted(h_prime.items()))), float('inf'))
        
        value = min(valuestop, valuenostop)
        summa += value

    return (h_str, summa / d)

def compute_value_second_case(args):
    # not all token are placed yet
    h_str, h_dict, d, k, r, Value, l = args
    summa = 0

    for m in range(l+1):
        x=sum(v for j, v in h_dict.items() if j < m)
        h_prime = dict_update(h_dict.copy(),m,k)

        if m<l:
            exp_rank = x+1+h_dict.get(m,0)/2 + ((r-1)*((m+1/2)/d))
        else:
            exp_rank = (d-l)*(x+1+h_dict.get(m,0)/2) + ((d-l)*(r-1)*(d+l)/(2*d))
            
        valuestop=exp_rank       
        if m<l:
            valuenostop = Value.get((str(sorted(h_prime.items()))), float('inf'))
        else:
            valuenostop = (d-l)*Value.get((str(sorted(h_prime.items()))), float('inf'))


        value=min(valuestop,valuenostop)
        summa+=value

    return (h_str, summa / d)

def compute_exp_rank(n,d,k,l):  
    if n==1:
        return 1  

    setofhistories = compute_all_histories(l,k)
    # print(f'time to compute histories:{time.time()-start}')
    Value = {}

    with Pool(cpu_count()) as pool:
        if n-1 >= k:
            args = [(h_str, h_dict, d, n, k, l) for h_str, h_dict in setofhistories[k].items()]
            results = pool.map(compute_value_last_round_first_case, args)
        else:
            args = [(h_str, h_dict, d, l) for h_str, h_dict in setofhistories[n-1].items()]
            results = pool.map(compute_value_last_round_second_case, args)
        for res in results:
            Value[res[0]] = res[1]
        # print(f'done for last level; time for computing last level is {time.time()-start}')

        # print(f'number of cores: {cpu_count()}')
        for r in range(2, n+1):
            if n-r >= k:
                case = 1
                args = [(h_str, h_dict, d, n, k, r, Value, l) for h_str, h_dict in setofhistories[k].items()]
                results = pool.map(compute_value_first_case, args)
            else:
                case = 2
                args = [(h_str, h_dict, d, k, r, Value, l) for h_str, h_dict in setofhistories[n-r].items()]
                results = pool.map(compute_value_second_case, args)
            for res in results:
                Value[res[0]] = res[1]
            # print(f'deleting previous level...')
            print(f'done for level {r}; this level fell into case {case}; time for computing this level is {time.time()-start}')
    return Value['[]']

if __name__ == "__main__":
    for n in [100000]:
        for d in [1000]:
            for k in [2]:
                for l in [50]:
                    print(f'computing for n={n}, d={d}, k={k}, l={l}')
                    start = time.time()
                    result=compute_exp_rank(n,d,k,l)
                    print("f_bottom_up({},{},{},{})={}".format(n,d,k,l,result), f'time = {time.time() - start}')
        print('')



# if valuestop<valuenostop: 
#     print('stop') 
# else:
#     print('nostop')
