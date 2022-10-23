def printlog(*args, sep=' ', end='\n'):
    print(*args, sep=sep, end=end)
    with open("userscripts/printlog.txt", "a") as f:
        f.write(sep.join(map(repr, args)) + end)