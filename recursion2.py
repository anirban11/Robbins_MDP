import time

def expected_rank_if_stop(k, m, x):
    '''k is the remaining drwas
    m is the interval that the current value is in
    x is the current vector storing the values in each interval so far'''

    ''' returns the expected rank of the future elements'''

    if (k,m,tuple(x)) in dict_stop:
        return dict_stop[k,m,tuple(x)]
    p2_prime = (1 + x[-1]) / 2 + k * (2 * m + 1) / (2 * d)

    if m>0:
        p2_prime += sum(x[j] for j in range(m))
    dict_stop[k, m, tuple(x)] = p2_prime
    return p2_prime

def expected_rank_if_continue(k, x):
    assert k>0
    if (k, tuple(x)) in dict_cont:
        return dict_cont[k, tuple(x)]
    p1_prime = 0
    for l in range(d):
        x_prime = x[:l] + [x[l]+1] + x[l+1:]
        p1_prime+=f(k-1, l, x_prime)
    dict_cont[k, tuple(x)] = p1_prime/d
    return p1_prime/d

    # for i in range(1, k+1): #remaining = k-i, seen = n-k+i
        


def f(k, m, x): 
    '''k is the remaining drwas
    m is the interval that the current value is in
    x is the current vector storing the values in each interval so far'''

    p2_prime = expected_rank_if_stop(k, m, x[:m+1])

    if k==0:
        return p2_prime
    
    if k>0: 
        p1_prime = expected_rank_if_continue(k, x)
        return min(p1_prime, p2_prime)



def f_n_d(n, d):
    assert d>0
    x=[0,] * d
    ans = 0
    for m in range(d):
        x_prime = x[:m] + [x[m]+1] + x[m+1:]

        ans+=f(n-1, m, x_prime)
        print(f'done for m={m}; time = {time.time - start_time}')
    return ans/d


# Example usage:
n = 6
for d in [100]:
    print(f'computing for n={n}, d={d}')
    dict_stop = {}
    dict_cont = {}
    start_time = time.time()
    result = f_n_d(n, d)
    end_time = time.time()
    print("f({}, {}) = {}".format(n, d, result), end_time-start_time)
