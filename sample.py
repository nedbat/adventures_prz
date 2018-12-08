def f(n):
    print("Look!: {}".format(n))
    if n > 0:
        f(n-1)

f(4)
