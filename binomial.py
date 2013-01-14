from math import exp
from payoffs import VanillaCall
from options import VanillaOption

def binomial_tree(s0, N, up, down):
    tree = [[s0]]
    for i in range(1,N):
        new_level = [tree[i-1][0] * up] + [down * e for e in tree[i-1]]
        tree.append(new_level)
    return tree
    

def binomial_price(option, spot, vol, r, N):
    up = exp(vol * (1.0 * option.expiry / N) ** 0.5)
    down = exp(-vol * (1.0 * option.expiry / N) ** 0.5)
    tree = binomial_tree(spot, N, up, down)
    p = (exp(r * option.expiry/N) - down) / (up - down)
    disc = exp(-r * option.expiry/N)
    tree[-1] = [option.payoff(s) for s in tree[-1]]
   
    for i in reversed(range(N-1)):
        for j in range(len(tree[i])):
            tree[i][j] = disc * (p * tree[i+1][j] + (1-p) * tree[i+1][j+1])
            
    return tree[0][0]

if __name__ == '__main__':
    call_130_1 = VanillaOption(VanillaCall(130),1)
    print(binomial_price(call_130_1, 100, 0.4, 0.04, 200))
