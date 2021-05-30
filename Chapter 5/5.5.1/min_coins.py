import math
fd = open("dataset_317330_10.txt", "r")
inputs = fd.readlines()
n = inputs[0]
f = inputs[1]
    
def convert_list(text_arr):
    coins = []
    for text in text_arr:
        coins.append(int(text))
    return coins
    
def get_min_coins(coins, k):
    min_coins = dict()
    min_coins[0] = 0
    for amount in range(1, k + 1):
        min_coins[amount] = math.inf
        for index in range(0, len(coins)):
            if amount >= coins[index]:
                if min_coins[amount - coins[index]] + 1 < min_coins[amount]:
                    min_coins[amount] = min_coins[amount - coins[index]] + 1
    print(min_coins[k])

    
coins = convert_list(f.strip('\n').split(','))
get_min_coins(coins, int(n.strip('\n')))