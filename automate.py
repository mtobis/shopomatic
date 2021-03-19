import csv, sys, argparse, datetime

    
def getprods(datafnam,verbose=True):
    allprods = []
    with open(datafnam, newline='') as f:
        reader = csv.reader(f)
        newproducts = list(reader)
        prodkeys = newproducts[0]
        for work in newproducts[1:]:
            workdict = dict(zip(prodkeys,work))
            allprods.append(workdict)
        """
        if verbose:
            for workdict in allprods:
                for k in workdict.keys():
                    print (k,"-::-",workdict[k])
        """
        return allprods

def gettpl(tplfnam,verbose=True):
    with open(tplfnam, newline='') as f:
        reader = csv.reader(f)
        templates = list(reader)
        templatekeys = templates[0]
        templatedata = templates[1]
        template = dict(zip(templatekeys,templatedata))
        """
        if verbose:
            for k,v in template.items():
                print(k,"-:-",v)
        """
        return template,templatekeys

def populate(template,artwork,sku,verbose=True):
    result = template.copy()
    #import pdb;pdb.set_trace()
    artistraw = artwork.get("Artist's Name") or artwork["Artist's Name "]
    artistlist = artistraw.lower().split() 
    titleraw  = artwork["Title of work"]
    titlelist = titleraw.lower().split()
    handlelist = artistlist + titlelist

    dimensions = [artwork["Width of work in inches"],
                      artwork["Height of work in inches"],
                      artwork["Depth of work in inches "],
                 ]
    result["Handle"] = "-".join(handlelist)
    result["Title"] = " ".join(artistlist) + " ~ " + " ".join(titlelist)
    linedict = {"title": titleraw,
                "media": artwork["Medium of work"],
                "dimensions": '" x '.join(dimensions) + '"',
                "colour": artwork.get("Extended description or other text to display to add interest (optional but recommended)") or
                          artwork["Extended description or other text to display to add interest (optional but recommended) 10 to 50 words is ideal, 100 word maximum."]
               }
    result["Body (HTML)"] = template["Body (HTML)"].format(**linedict)
    result["Variant Price"] = "%8.2f"%float(artwork["List price (Canadian dollars)"])
    result["Variant SKU"] = sku

    if verbose:
        print(titleraw)

    return result

def checksku(sku):
    year = str(datetime.datetime.now().year)[-2:]
    try:
        ivalue = int(sku)
    except ValueError:
        raise argparse.ArgumentTypeError("\n\nY%s-%s is not a valid sku. Use a 1 to 4 digit number\n\n." %(year,sku))
    if ivalue < 1 or ivalue > 9999:
        raise argparse.ArgumentTypeError("\n\nY%s-%s is not a valid sku. Use a 1 to 4 digit number.\n\n" % (year,sku))
    return ivalue
                
if __name__ == "__main__":
    tplfnam = "prodtpl.csv"
    #datafnam = "justin.csv" # don't hardwire! FIXME!!!!!!!!!!!!!
    #produpnam = "products.csv"
    verbose = False

    year = str(datetime.datetime.now().year)[-2:]
    
    paramGet = argparse.ArgumentParser()
    paramGet.add_argument("sku",type=checksku)
    paramGet.add_argument("datafnam")
    paramGet.add_argument("-d","--data",help="csv file to process")
    paramGet.add_argument("-v","--verbose",help="increase verbosity",action="store_true")

    datafnam = args.datafnam
    assert (".csv" in datafnam)
    produpnam = datfnam.replace(".csv","_up.csv")
    
    args = paramGet.parse_args()
    if args.data:
        datafnam = args.data
    if args.verbose:
        verbose = True
    if verbose:
        print(datafnam)
    sku = int(args.sku)
    """
    if verbose:
        skustr = "%04d"%args.sku
        print(f"Y{year}-{skustr}")
    """
    
    newprods = getprods(datafnam,verbose)
    
    template,templatekeys = gettpl(tplfnam,verbose)

    results = []

    for newprod in newprods:
        """
        skustr = "%03d"%sku
        skustr = f"Y{year}-{skustr}"
        """
        skustr = f"Y{year}-{sku:04d}"

        if verbose:
            print(skustr)
        results.append(populate(template,newprod,skustr,verbose))
        sku += 1
        try:
            assert (sku < 10000)
        except AssertionError:
            print ("\n\nMaximum SKU exceeded\n\n")
            raise
    """
    if verbose:
        for result in results:
            for k,v in result.items():
                print(k,": ",v)
            print("**")
    """
        
    # csv writer

    print(produpnam)
    with open(produpnam, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=templatekeys)

        writer.writeheader()
        for result in results:
            writer.writerow(result)
        csvfile.close()

    print("products successfully processed: %d"%len(results) )
    
