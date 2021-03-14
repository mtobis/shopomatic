import csv, sys, argparse

    
def getprods(datafnam,verbose=True):
    allprods = []
    with open(datafnam, newline='') as f:
        reader = csv.reader(f)
        newproducts = list(reader)
        prodkeys = newproducts[0]
        for work in newproducts[1:]:
            workdict = dict(zip(prodkeys,work))
            allprods.append(workdict)
        if verbose:
            for workdict in allprods:
                for k in workdict.keys():
                    print (k,"-::-",workdict[k])
        return allprods

def gettpl(tplfnam,verbose=True):
    with open(tplfnam, newline='') as f:
        reader = csv.reader(f)
        templates = list(reader)
        templatekeys = templates[0]
        templatedata = templates[1]
        template = dict(zip(templatekeys,templatedata))
        if verbose:
            for k,v in template.items():
                print(k,"-:-",v)
        return template

def populate(template,artwork,verbose=True,skubase=10):
    result = template
    artistraw = artwork["Artist's Name"]
    artistlist = artistraw.lower().split() 
    titleraw  = artwork["Title of work"]
    titlelist = titleraw.lower().split()
    handlelist = artistlist + titlelist
    result["Handle"] = "-".join(handlelist)
    result["Title"] = " ".join(artistlist) + " ~ " + " ".join(titlelist)
    if verbose:
        for k,v in result.items():
            print(k,":-:",v)
    return result

                
if __name__ == "__main__":
    tplfnam = "prodtpl.csv"
    datafnam = "palmerup.csv"
    verbose = False

    paramGet = argparse.ArgumentParser()
    paramGet.add_argument("-d","--data",help="csv file to process")
    paramGet.add_argument("-v","--verbose",help="increase verbosity",action="store_true")
    args = paramGet.parse_args()
    if args.data:
        datafnam = args.data
    if args.verbose:
        verbose = True
    if verbose:
        print(datafnam)

    newprods = getprods(datafnam,verbose)
    #print(len(newprods))
    if verbose:
        for k,v in newprods[0].items():
            print(k,":: ",v)
        print("*************")
    
    template = gettpl(tplfnam,verbose)
    #print( len(template.keys()) )
    if verbose:
        for k,v in template.items():
            print(k,":: ",v)

    result = []
    for newprod in newprods:
        result.append(populate(template,newprod,verbose))
    print("items successfully processed: %d"%len(result) )

    # csv writer


""" 
    prefixfnam = "prefixlist.csv"
    prefixlist = open(prefixfnam).readlines()
    prefixlist = [item.strip().split(',') for item in prefixlist]
    prefixes = {item[0]:item[1] for item in prefixlist}

###

            body = workdict["Body (HTML)"].split("</p>")
            print(body[0])
            #if "elena" in body[0]:
            #import pdb; pdb.set_trace()
            if body:
                if "~" in body[0]:
                    artist = body[0].split('~')[0].strip()
                    title = body[0].split('~')[1].strip()
                else:
                    print (body[0])
                    title = body[0].strip()
                    prefix= workdict['Variant SKU'].split("-")[0]
                try:
                    artist=prefixes[prefix].lower()
                except:
                    import pdb;pdb.set_trace()
                
                try:
                    dims = body[2].strip()
                except:
                    import pdp;pdb.set_trace()
                    dims = ""
                info = body[1].strip()
                info = info + '<br/>' + dims
                info = info.replace("<br>","")
                title = title.split("strong")[1][1:]
                print("!",title)
                title = title.replace("<b>","").replace("</b>","")
                title = title.replace("<em>",'<i>').replace("</em>","</i>")[:-2]
                title = "<i>"+title+"</i>"
                outdict = {
                "title": title.replace("<p>",""),
                "artist": artist.replace("<p>",""),
                "info": info.replace("<p>",""),
                "price": "$"+workdict["Variant Price"].split(".")[0]
                }
                contents += onelabel(outdict)

    html = template.replace("%CONTENT",contents)
    
    outfnam = "labels.html"
    outf = open(outfnam,"w")
    outf.write(html)
    outf.close()
"""
