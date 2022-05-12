verbose = True

def Print(*args):
    if verbose:
        print(*args)

def compheads(files):
    
    assert len(files) > 1
    firstfile = files[0]
    #firstheaders = firstfile[0].split(",")
    firstheaders = firstfile[0]

    #Gather headers = necessary?
    """
    allheaders = firstheaders
    count = 1
    for nextfile in files[1:]:
        #headers = nextfile[0].split(",")
        headers = nextfile[0]
        for item in allheaders:
            if item not in headers:
                Print(count,"missing header item",item)
        for item in headers:
            if not item in allheaders:
                Print(count,"adding header item",item)
                allheaders.append(item)
    """
    
    # Gather results
            
    results = []
    headers = set()
    
    for nextfile in files:
        assert len(nextfile) > 1
        #headers = nextfile[0].split(",")
        headers.update( nextfile[0])

        for item in nextfile[1:]:
            #line = item.split(",")
            line = item
            results.append(dict(zip(headers,line)))

    # return allheaders
    return headers

if __name__ == "__main__":
    import csv
    
    filenames = ["artist2.csv","artist1.csv"]
    files = []
    for fnam in filenames:
        reader = csv.reader(open(fnam))
        files.append(list(reader))
        #files.append(open(fnam).readlines())
    allheads = list(compheads(files))
    Print(allheads)
    #combined = [",".join(allheads)]
    #Print(combined)
