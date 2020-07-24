"""[summary]
Given an ID type integer, return the corresponding spotify URI
"""
import csv

def getSpotifyURI(ID):
    for row in csv_file:
        #print(row['ID'])
        if(ID == row['ID']):
            URI = row['URI']
            print(URI)
            return URI

file = open('Test\spotifyURICollection.csv', newline='', encoding='utf-8-sig')
csv_file = csv.DictReader(file)

getSpotifyURI('filler')
getSpotifyURI('filler1')
getSpotifyURI('filler2')
    
    