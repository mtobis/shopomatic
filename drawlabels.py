import csv, argparse


separator = """<div>
        <pdf:nextpage /> 
    </div>"""

template = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta charset="UTF-8">
<style type=text/css>

    @page {
            size: letter portrait;
            @frame content_frame {
                left: 50pt;
                width: 300pt;
                top: 50pt;
                height: 692pt;
                -pdf-frame-border: 1;    /* for debugging the layout */
            }
        }


    @font-face {
      font-family: Lato,"Lato";
      src: url(Lato2OFL/Lato-Regular.ttf);
    }


    /* Regular */
    @font-face {
       font-family: Lato;
       src: url(Lato2OFL/Lato-Regular.ttf);
       font-weight: regular;
    }

    /* Bold */
    @font-face {
       font-family: Lato;
       src: url(Lato2OFL/Lato-Bold.ttf);
       font-weight: bold;
    }

    /* Italic */
    @font-face {
       font-family: Lato;
       src: url(Lato2OFL/Lato-Italic.ttf);
       font-style: italic;
    }

    /* Bold and italic */
    @font-face {
       font-family: Lato;
       src: url(Lato2OFL/Lato-BoldItalic.ttf);
       font-weight: bold;
       font-style: italic;
    }

    p {
      text-align: center;
    color: red;
    }
</style>
</head>
<body>
    %CONTENT
</body>
</html>
"""


def onelabel(info=None):
    """
    separator = '''<div>
        <pdf:nextpage /> 
    </div>'''
    """


    block = """<div style="border: 2px solid black; text-align: center; overflow: hidden; width: 400px; clear=both; padding: 30px; {color} {bordermod} ">
    <span style="font-size:14pt; font-family:Lato; font-weight:400; line-height:1.2;"><br/>{title}<br/>
    <span style="font-size:20pt; font-family:Lato; font-weight:800; {altcolor} line-height:1.5;"><br><b>{artist}</b><br/><br/></span>
    <span style="font-size:10pt; font-family:Lato; font-weight:400; font-style:regular; line-height:1.8;">{info}<br/><br/></span>
    <span style="font-size:12pt; font-family:Lato; font-weight:400; font-style:regular; line-height:1.8;">{price}</span>
    </div>
    """

    b1dict = info or {

        "title": "Frilly Tulip",
        "artist": "michael tobis",
        "info": 'alcohol ink on tracing paper, 8.5" x 11 "',
        "price": '$1'
        }
    assert isinstance(b1dict,dict)

    b1dict["color"] = ""
    b1dict["altcolor"] = ' color: blue; '
    b1dict["bordermod"] = ""
    
    #import pdb;pdb.set_trace()
    #import pdb;pdb.set_trace()
    b1 = block.format(**b1dict)

    """
    b2dict = b1dict.copy()
    b2dict["bordermod"] = ' border-top: 0; '

    b2 = block.format(**b2dict)

    b3dict = b1dict.copy()
    b3dict["bordermod"] = ' border-bottom: 0; '
    b3dict["color"] = ' color: white; '
    b3dict["altcolor"] =  ' color: white; '
    
    b3 = block.format(**b3dict)
    """
    
    #content = b1 + "<p>&nbsp;</p>" + b3 + b2 + separator 
    content = b1
    
    return content

    """
    html = template.replace("%CONTENT",content)
    return html
    
 
    outfnam = "test.html"

    outf = open(outfnam,"w")

    content = b1 + "<p>&nbsp;</p>" + b3 + b2 + separator +"<p>next page</p>"

    outtext = template.replace("%CONTENT",content)

    outf.write(outtext)
    outf.close()
    return True
    """
    
if __name__ == "__main__":
    contents = ""

    paramGet = argparse.ArgumentParser()
    paramGet.add_argument("datafnam")
    
    args = paramGet.parse_args()

    themnam = args.datafnam

    with open(themnam, newline='') as f:
        reader = csv.reader(f)
        showproducts = list(reader)
        prodkeys = showproducts[0]
        count = 0

        for work in showproducts[1:]:
            count += 1
            workdict = dict(zip(prodkeys,work))
            body = workdict["Body (HTML)"].split("</p>")
            print(body[0])
            if body:
                if "~" in body[0]:
                    artist = body[0].split('~')[0].strip()
                    title = body[0].split('~')[1].strip()
                else:
                    title = body[0].strip()
                    prefix= workdict['Variant SKU'].split("-")[0]
                    artist = workdict['Title'].split('~')[0].strip()
                try:
                    dims = body[2].strip()
                except:
                    import pdb;pdb.set_trace()
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
                if (count % 3):
                    contents += "<p>&nbsp;</p>"
                else:
                    contents += separator

    html = template.replace("%CONTENT",contents)
    
    outfnam = "labels.html"
    outf = open(outfnam,"w")
    outf.write(html)
    outf.close()

