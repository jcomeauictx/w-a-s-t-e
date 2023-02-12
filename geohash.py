#!/usr/bin/python3
'''
implementing Gustavo Niemeyer's geohash from Wikipedia article

geohash.org website isn't fully functional, and anyway I may need to base
a better addressing scheme on this method.
'''

ALPHABET = '0123456789bcdefghjkmnpqrstuvwxyz'

def encode(latitude, longitude):
    '''
    encode latitude and longitude into Geohash format

    see //en.wikipedia.org/wiki/Geohash, //geohash.org/
    '''

def decode(geohash):
    '''
    decode geohash into latitude and longitude

    >>> decode('ezs42')  # from wikipedia example
    '0110111111110000010000010'
    '''
    binary = ''
    for character in geohash:
        binary += bin(ALPHABET.index(character))[2:].rjust(5, '0')
    return binary
