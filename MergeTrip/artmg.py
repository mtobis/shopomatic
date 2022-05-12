import argparse

verbose = True

def Print(*args):
    if verbose:
        print(*args)
        
def merge_csv(filenames,columnlist):
    allheaders = set()
    results = []
    for fnam in filenames:
        reader = csv.reader(open(fnam))
        items = list(reader)
        headers = items[0]
        allheaders.update(headers)
        for item in items[1:]:
            results.append(dict(zip(headers,item)))
    allheads = list(allheaders)
    
    with open('artists.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile,fieldnames=allheads)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    import csv
    from os.path import exists

    paramGet = argparse.ArgumentParser()
    paramGet.add_argument("-d","--datalist",help="path to list of csvfiles")
    paramGet.add_argument("-c","--columnlist",help="path to list of output columns")

    args = paramGet.parse_args()
    if args.datalist:
        if exists(args.datalist):
            Print("found")
            with open(args.datalist) as f:
                flist = f.read().splitlines()
        else:
            raise FileNotFoundError
    else:
        flist = ["artist2.csv","artist1.csv"]
        
    if args.columnlist:
        if exists(args.columnlist):
            Print("found 2")
            with open(args.columnlist) as f:
                clist = f.read().splitlines()
        else:
            raise FileNotFoundError
    else:
        clist = None
        
    Print(flist)
    merge_csv(flist,clist)
