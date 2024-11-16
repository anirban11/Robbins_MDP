import math
import numpy as np
import seaborn as sns 
from collections import Counter #count
from scipy.stats import rankdata #to compute rank of a list


def reject_stop_k_th_best_prob(applicants,r,k, p):
    #sort first r-1
    first_r_1_sorted = sorted(applicants[:r-1])
    #find best among first r-1
    best_so_far = first_r_1_sorted[0]
    #find k-th best among first r-1
    k_th_best_so_far = first_r_1_sorted[k-1]
    # print(k_th_best_so_far)

    #select an applicant that is better than k_th_best_so_far with probability p
    for i, applicant in enumerate(applicants[r-1:], start=r-1):
        if applicant <= best_so_far:
            break
        elif applicant <= k_th_best_so_far:
            #update p = how close to the best value
            p = (k_th_best_so_far-applicant)/(k_th_best_so_far-best_so_far)

            if np.random.random()<=p:
                break
    return i  # selected_applicant = i

# ------------------ modify the probability of choosing an element ------------------

def reject_stop_modified(applicants,r,k, p):

    first_r_1_sorted = sorted(applicants[:r-1])

    k_th_best_so_far = first_r_1_sorted[k-1]

    for i, applicant in enumerate(applicants[r-1:], start=r-1):
        if applicant <= k_th_best_so_far:
            if applicant <= first_r_1_sorted[0]:
                return i
            p = 1
            for j in range(k-1):
                j_th_best_so_far = first_r_1_sorted[j]
                #update p
                p *= (applicant - j_th_best_so_far)/(k_th_best_so_far-j_th_best_so_far)
                if applicant <= first_r_1_sorted[j+1]:
                    if np.random.random()<=p:
                        return i
                    break
                # if applicant > first_r_1_sorted[j+1]:
                #     continue
                # break
                # print(p)
    return i  # selected_applicant = i

#-------- define function for simulation---------------
def simulate_secreatary_problem(N,n,strat,r, k, p, K):
    Results = []
    my_probability_counter = 0 #to count how many times the K-th best is chosen
    my_expectation_counter = 0
    for i in range(N):
        applicants = np.random.random(size=n)
        result = strat(applicants, r, k, p) #returns the index of the chosen candidate

        Rank_vector = rankdata(applicants, method='min') #returns the ranks, indexed from 1 to n

        my_expectation_counter += Rank_vector[result] #adds the rank
        if Rank_vector[result] <= K:
            my_probability_counter += 1 #how many times the best is chosen
        Results.append(result)
    prob_K_th_best = my_probability_counter/N #probability of choosing the K-th best
    expected_rank = my_expectation_counter/N #expected rank
    # print(f'The strategy is to choose the best value that is less than {k}-th best among first r-1 with probability {p}')
    # print(f'The probability of choosing the {K}-th best candidate is {prob_K_th_best}')
    # print(f'The expected rank of the chosen candidate is {expected_rank}')
    return Results, prob_K_th_best, expected_rank


#------------ simulation function for robbin's problem with memoryless strategy---------------
def simulate_robbin_memoryless_strat_probabilistic(N,n,c, p):
    # Results = []
    # my_probability_counter = 0
    my_expectation_counter = 0
    for i in range(N):
        applicants = np.random.random(size=n)
        Rank_vector = rankdata(applicants, method='min') #returns the ranks, indexed from 1 to n
        for k, applicant in enumerate(applicants, start = 0):
            if applicant <= c/(n-k+c):
                if np.random.random()<=p:
                    break
        my_expectation_counter += Rank_vector[k] #adds the rank
        # Results.append(k)
    expected_rank = my_expectation_counter/N #expected rank
    return expected_rank




N, n = 10000, 1000
e = math.exp(1)
my_strat = reject_stop_k_th_best_prob
my_strat_2 = reject_stop_modified


opt_r_reject_stop = int(n//e) #optimal r value for reject_stop

Results, prob_K_th_best, expected_rank = simulate_secreatary_problem(N, n,my_strat, opt_r_reject_stop,  k=5, p = 1, K =1) 
print(expected_rank)
Results, prob_K_th_best, expected_rank = simulate_secreatary_problem(N, n,my_strat_2, opt_r_reject_stop,  k=5, p = 1, K =1) 
print(expected_rank)
# Results, prob_K_th_best, expected_rank = simulate_secreatary_problem(N, n, my_strat, opt_r_reject_stop,  k=11, p=1, K = 5) 



# Counted = Counter(Results) #which index has been picked how many times
# print(Counted)

# fig = sns.histplot(data = Results, bins= 100).get_figure()
# fig.savefig("output.png")


# ----------- array for reject_stop with different k and p values ----------
# my_array = np.zeros((20, 10))
# p = 0
# for k in range(5,15):
#     for i in range(10):
#         p += 1/10
#         Results, prob_K_th_best, expected_rank = simulate_secreatary_problem(N, n, my_strat, opt_r_reject_stop, k, p, K = 5)
#         my_array[k-1][i] = expected_rank
#         # print(p)
#     p = 0
#     print(my_array[k-1])


#----------------- run robbin's problem with optimal strategy ----------
# print(simulate_robbin_memoryless_strat_probabilistic(N,n,c=2, p=1))


#------------------ Archive ---------------------


# # fig = sns.lineplot(Results).get_figure() #line


# def reject_stop(applicants,r):
#     #find best applicant among first r-1
#     best_applicant_so_far = min(applicants[:r-1])
#     # print(best_applicant_so_far)

#     #select first subsequent applicant that is better than applicant best_applicant_so_far
#     for i, applicant in enumerate(applicants[r-1:], start=r-1):
#         if applicant <= best_applicant_so_far:
#             break
#     # selected_applicant = i
#     return i



#------------------ TODO ------------------
# implement the strategy for robbin's problem with probability p of chosing 
# if I dont have the stopping rule, can ML help me come up with the maximum probability?
# change max to min -- Done
# second best with prob p -- Done
# f(r,p,k) = prob of selecting top k candidates with p selection probability, for all k -- Done
# g(r,p) = expected rank of selected candidate -- Done