import csv, sys, argparse, datetime
import pdb
from pdb import set_trace as ST
verbose = False

def titlecase(rawtitle):

    """
    usage: print( titlecase("  the test IS a  wee  test string ") )
    """
    
    exceptions = ["and", "or", "the", "a", "of", "in"]

    lcwords = rawtitle.lower().strip().split()
    title = [lcwords[0].capitalize()] + \
             [word if word in exceptions else word.capitalize() for word in lcwords[1:]]

    #return " ".join(title)
    return title

def cleanartists(infnam="allartists.csv"):
    bynick = {}
    bymail = {}
    with open("allartists.csv") as a1:
        reader = csv.reader(a1)
        artists = list(reader)
    
    artkeys = artists[0]
    if verbose:
        for artkey in artkeys:
            print("_"+artkey+"_")
    for artist in artists[1:]:
        artistdict = dict(zip(artkeys,artist))
        nickname = artistdict["Nickname"].strip().lower()
        if nickname:
            bynick[nickname] = artistdict
        email = artistdict["Contact email"]
        bymail[email] = artistdict
    return(bynick,bymail)
    
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

def populate(template,artwork,sku,bynick,bymail,verbose=True):
    print(sku)
    result = template.copy()
    #import pdb;pdb.set_trace()
    artisthandle = artwork["Please enter your gallery nickname"].lower()

    if "@" in artisthandle:
        artistraw = bymail[artisthandle]["What name do you sign your works with?"]
    else:
        artistraw = bynick[artisthandle]["What name do you sign your works with?"]
    
    #artistraw = artwork.get("Artist's Name") or artwork["Artist's Name "]


    
    artistlist = artistraw.lower().split() 
    titleraw  = artwork["Title of Work"].replace('"','')
    titlelist = titlecase(titleraw)
    handlelist = artistlist + titlelist

    dimensions = [artwork['Width of "___" in inches'],
                      artwork['Height of "___" in Inches']
                 ]

    if artwork["Hangs"] == "Wall hanging":
        media = artwork['Medium of "___"'] + " on " + artwork['Substrate of "___"'].replace("stretched ","")
    else:
        media = artwork['What materials is "___" made of?']
        
    result["Handle"] = "-".join(handlelist)
    result["Title"] = " ".join(artistlist) + " ~ " + " ".join(titlelist)
    linedict = {"title": titleraw,
                "media": media,
                "dimensions": '" x '.join(dimensions) + '"',
                "colour": artwork["Colour Text"]}
    linedict["media"] = linedict["media"].lower()
    """
    if isframed:
        linedict["dimensions"] += "; framed: " +  '" x '.join(framedims) + '"'
    """
    result["Body (HTML)"] = template["Body (HTML)"].format(**linedict)
    result["Variant Price"] = "%8.2f"%float(artwork['Your recommended list price for "___"'])
    result["Variant SKU"] = sku

    if verbose:
        print(titleraw)

    return result

"""    
def populate_orig(template,artwork,sku,verbose=True):
    print(sku)
    result = template.copy()
    #import pdb;pdb.set_trace()
    artistraw = artwork.get("Artist's Name") or artwork["Artist's Name "]
    artistlist = artistraw.lower().split() 
    titleraw  = artwork["Title of work"]
    titlelist = titleraw.split()
    handlelist = artistlist + titlelist

    dimensions = [artwork.get("Width of work in inches") or artwork["Width of work in inches (not including frame)"],
                      artwork["Height of work in inches"],
                      artwork["Depth of work in inches "],
                 ]


    ###isframed = not artwork["Materials of the frame (if unframed leave blank)"].isspace()
    ###framedims = [artwork["Width of framed piece in inches (if unframed leave blank)"],
    ###                  artwork["Width of framed piece in inches (if unframed leave blank)"],
    ###                  artwork["Width of framed piece in inches (if unframed leave blank)"],
    ###             ]
    
    result["Handle"] = "-".join(handlelist)
    result["Title"] = " ".join(artistlist) + " ~ " + " ".join(titlelist)
    linedict = {"title": titleraw,
                "media": artwork.get('Medium of work (describe the pigment and the surface, as "oil on canvas" or "acrylic on cradleboard" etc.)') or \
                artwork["Medium of work"],
                "dimensions": '" x '.join(dimensions) + '"',
                "colour": artwork.get("Extended description or other text to display to add interest (optional but recommended)") or
                          artwork.get("Extended description or other text to display to add interest (optional but recommended) 10 to 50 words is ideal, 100 word maximum.") or
                          artwork["Extended description"]}
    linedict["media"] = linedict["media"].lower()
    
    ###if isframed:
    ###    linedict["dimensions"] += "; framed: " +  '" x '.join(framedims) + '"'
    
    result["Body (HTML)"] = template["Body (HTML)"].format(**linedict)
    result["Variant Price"] = "%8.2f"%float(artwork["List price (Canadian dollars)"])
    result["Variant SKU"] = sku

    if verbose:
        print(titleraw)

    return result
"""
        
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
    datadir = "Data/"
    #datafnam = "justin.csv" # don't hardwire! FIXME!!!!!!!!!!!!!
    #produpnam = "products.csv"
    verbose = False

    bynick,bymail = cleanartists() 
    
    year = str(datetime.datetime.now().year)[-2:]
    
    paramGet = argparse.ArgumentParser()
    paramGet.add_argument("sku",type=checksku)
    paramGet.add_argument("datafnam")
    paramGet.add_argument("-d","--data",help="csv file to process")
    paramGet.add_argument("-v","--verbose",help="increase verbosity",action="store_true")


    
    args = paramGet.parse_args()

    datafnam = args.datafnam
    assert (".csv" in datafnam)

    
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

    qualdatafnam = datadir + datafnam
    produpnam = qualdatafnam.replace(".csv","_up.csv")
    
    newprods = getprods(qualdatafnam,verbose)
    
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
        results.append(populate(template,newprod,skustr,bynick,bymail,verbose))
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
    
