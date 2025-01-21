import math

def memoryless(n,c):

    # pk = c/(n-k+c)
    # qk = 1-pk
    p_values = dict()
    q_values = dict()
    for k in range(1,n+1):
        p_values[k] = c/(n-k+c)
        q_values[k] = 1-(c/(n-k+c))

    def f1(k):
        x1 = ((n-k)*(p_values[k]**2)) + sum((((p_values[k] - p_values[j])**2)/q_values[j]) for j in range(1, k))
        x2 = math.prod(q_values[j] for j in range(1,k))
        return x1*x2

    result = 1 + (sum(f1(k) for k in range(1,n+1)))/2

    return result

for n in range(100,101):
    for c in [1.9469]:
        print("f({},{}) = {}".format(n, c, memoryless(n,c)))