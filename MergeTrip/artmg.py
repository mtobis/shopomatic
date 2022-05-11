verbose = True

def Print(*args):
    if verbose:
        print(*args)


def compheads(files):
    # assumes no commas in headers; else need to use csv library
    
    assert len(files) > 1
    firstfile = files[0]
    firstheaders = firstfile[0].split(",")
    # print(firstheaders)
    allheaders = firstheaders
    count = 1
    for nextfile in files[1:]:
        headers = nextfile[0].split(",")
        for item in allheaders:
            if item not in headers:
                Print(count,"missing header item",item)
        for item in headers:
            if not item in allheaders:
                Print(count,"adding header item",item)
                allheaders.append(item)
    return allheaders

if __name__ == "__main__":
    filenames = ["artist2.csv","artist1.csv"]
    files = []
    for fnam in filenames:
        files.append(open(fnam).readlines())
    compheads(files)
