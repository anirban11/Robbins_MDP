import os

def generate_prism_file(n: int, n_intervals: int):
    ''' this function generates the prism file cotaining the mdp 
        that computes the optimal expected rank based on interval strategies
        n            = number of draws
        n_intervals  = number of (equi-length) intervals that we break [0,1] in
        outfile_name = name of the output file
    '''
    probability = 1/n_intervals
    with open(f'./Robbin-expected-{n_intervals}I-{n}draws.txt', 'w') as outfile:
        outfile.write('mdp \n\n')
        outfile.write('module P1 \n\n')
        
        # program counter
        outfile.write('pc: [0..2] init 0; \n')

        # one counter per interval
        for each in range(1, n_intervals+1):
            outfile.write(f'c{each}: [0..{n}] init 0; \n')
        
        # number of draws
        outfile.write(f'\nn: [1..{n}] init 1; \n')

        # last number picked from the interval
        outfile.write(f'\nlast: [1..{n_intervals}] init 1; \n')

        # for each program counter 
        for pc in [1,2]:

            # a number is picked uniformly at random from one of the intervals
            if pc == 1:
                s = f'[] (pc = 0 & n < {n}'
            else:
                s = f'[] (pc = 0 & n = {n}'
            # now create the string &(ci < n) & SUM(c_i) < n 
            for each in range(1, n_intervals+1):
                s += f' & c{each} < {n}'
            s += ' & c1'
            for each in range(2, n_intervals+1):
                s += f' + c{each}'
            s += f' < {n})'
            outfile.write(s + '\n')
            s = "" # emptying out s

            # add the transitions
            for each in range(1, n_intervals + 1):
                if each == 1:
                    s += '    -> '
                else: 
                    s += '     + '
                # increase the counter
                s += f"{probability}: (c{each}' = c{each} + 1)"
                # set the last to be current interval
                s += f" & (last' = {each}) & (pc' = {pc}) \n"
            outfile.write(s+";")
        
        # encode player's choices
        outfile.write(f"[cont] pc = 1 & n < {n} -> (pc' = 0) & (n' = n + 1); \n")
        outfile.write("[stop] pc = 1 -> (pc' = 2); \n")

        outfile.write("\nendmodule\n")

        outfile.write('\nrewards "rank"\n')

        # write the reward for each interval
        for each in range(1, n_intervals + 1):
            s = f'    pc = 2 & last = {each} & c{each} >= 1: '
            s += '('
            for i in range(1, each):
                s += f"c{i}"
                # if not(i == each): # if not the last value
                s += "+"
            s += f'(1+c{each})/2)'
            
            s += f" + ({n} - n) * (2*{each}-1)/(2*{n_intervals});"
            outfile.write(s + '\n')

        outfile.write("endrewards")
        
generate_prism_file(6, 10)

# now execute the file (uncomment the following line)
# os.sytem("prism ")
