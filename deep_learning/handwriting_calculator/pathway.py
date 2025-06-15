import os

def pathway(dir, basename): # helper functions to deal with path settings; don't call this "abspath"...; interesting name convention yes but it works
    return os.path.abspath(
        os.path.join(
            dir,
            basename
        )
    )

if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname) # now the working directory is set to the file path
    
    print(
        pathway(os.getcwd(), "TEST BASENAME")
    )