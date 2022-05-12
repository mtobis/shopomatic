verbose = True

def Print(*args):
    if verbose:
        print(*args)

def compheads(files):
    
    assert len(files) > 1
            
    results = []
    allheaders = set()
    
    for nextfile in files:
        assert len(nextfile) > 1
        #headers = nextfile[0].split(",")
        headers = nextfile[0]
        allheaders.update(headers)

        for item in nextfile[1:]:
            #line = item.split(",")
            #line = item
            results.append(dict(zip(headers,item)))

    # return allheaders
    return allheaders,results

def dropartists(filenames):
    files = []
    for fnam in filenames:
        reader = csv.reader(open(fnam))
        files.append(list(reader))
    allheadset,results = compheads(files)
    allheads = list(allheadset)
    Print(allheads)

    with open('artists.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile,fieldnames=allheads)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    import csv

    dropartists(["artist2.csv","artist1.csv"])

    """
    filenames = ["artist2.csv","artist1.csv"]
    files = []
    for fnam in filenames:
        reader = csv.reader(open(fnam))
        files.append(list(reader))
        #files.append(open(fnam).readlines())
    allheadset,results = compheads(files)
    allheads = list(allheadset)
    Print(allheads)

    with open('artists.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile,fieldnames=allheads)
        writer.writeheader()
        for result in results:
            Print(result)
            writer.writerow(result)
    
    #combined = [",".join(allheads)]
    #Print(combined)
    """
