# connect nickname to artist data

import csv

def getartists(fnam="artists.csv"):
    with open(fnam) as f:
        reader = csv.reader(f)
        artistdata = list(reader)
        artistkeys = artistdata[0]
        artists = artistdata[1:]
        return(artistkeys,artists)



if __name__ == "__main__":
    artistkeys,artists = getartists()
    for artist in artists:
        artistdict = dict(zip(artistkeys,artist))
        print(artistdict)
        input("?")
