import random

tokens_list = open('tokens.txt',"r").read().splitlines()
proxies_list = open('proxies.txt',"r").read().splitlines()

new = []

for i in tokens_list:
    new_data = None
    if i.count("|") == 2:
        new_data = i + "|" + random.choice(proxies_list)
    else:
        new_data = i
    new.append( new_data + "\n" )

open("tokens_with_proxies.txt","w").writelines(new)
