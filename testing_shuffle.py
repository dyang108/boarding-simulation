def test():
    """Stupid test function"""
    random.shuffle(range(2000))


def test_2():
    random.sample(range(2000), k=2000)

if __name__ == '__main__':
    import timeit
    import random
    print(timeit.timeit("test()", setup="from __main__ import test", number=1000))
    print(timeit.timeit("test_2()", setup="from __main__ import test_2", number = 1000))
