#!/usr/bin/python3
'''
implementing Gustavo Niemeyer's geohash from Wikipedia article

geohash.org website isn't fully functional, and anyway I may need to base
a better addressing scheme on this method.
'''
import logging

logging.basicConfig(level=logging.DEBUG if __debug__ else logging.WARN)

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
    (42.60498046875, -5.60302734375)
    '''
    binary = ''
    for character in geohash:
        binary += bin(ALPHABET.index(character))[2:].rjust(5, '0')
    logging.debug('binary: %s', binary)
    # binary string is longitude bits alternating with latitude
    latitude, longitude = [-90, 90], [-180, 180]
    mean = lambda range: (range[0] + range[1]) / 2
    for index in range(0, len(binary), 2):
        # first do longitude
        digit = int(binary[index])
        middle = mean(longitude)
        longitude = ([longitude[0], middle], [middle, longitude[1]])[digit]
        logging.debug('digit: %s, longitude: %s', digit, longitude)
        # now latitude
        try:
            digit = int(binary[index + 1])
            middle = mean(latitude)
            latitude = ([latitude[0], middle], [middle, latitude[1]])[digit]
            logging.debug('digit: %s, latitude: %s', digit, latitude)
        except IndexError:  # odd number of binary digits
            pass
    return mean(latitude), mean(longitude)
