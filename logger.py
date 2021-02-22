VERBOSE = False

def verbose(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)