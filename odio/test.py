def countSeed(key):
    tot = 0
    for i in key:
        tot += ord(i)
    return tot    

key = 'anakayam'

print(countSeed(key))