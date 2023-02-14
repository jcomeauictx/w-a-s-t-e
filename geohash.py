#!/usr/bin/python3
'''
implementing Gustavo Niemeyer's geohash from Wikipedia article

geohash.org website isn't fully functional, and anyway I may need to base
a better addressing scheme on this method.
'''
import sys
import logging

logging.basicConfig(level=logging.DEBUG if __debug__ else logging.WARN)

ALPHABET = '0123456789bcdefghjkmnpqrstuvwxyz'

def encode(latitude, longitude, max_error=.00001, alphabet=ALPHABET,
           prefer_odd=False):
    '''
    encode latitude and longitude into Geohash format

    I didn't actually see an explanation of this, just figured it out from
    the decode example.

    `prefer_odd` will return an odd-length geohash if allowed by max_error

    >>> encode(42.605, -5.603, .03, prefer_odd=True)
    'ezs42'
    '''
    bits = bit_length(alphabet)  # for padding bitstring
    spread = [[-90, 90], [-180, 180]]
    given = (latitude, longitude)
    bitstring = ''
    error = [sys.maxsize, sys.maxsize]
    while error[1] > max_error:
        # start with longitude. latitude can be truncated.
        for index in (1, 0):
            middle = mean(spread[index])
            error[index] = abs(middle - spread[index][1])
            if given[index] >= middle:
                spread[index] = [middle, spread[index][1]]
                bitstring += '1'
            else:
                spread[index] = [spread[index][0], middle]
                bitstring += '0'
            logging.debug('%s: %s, range: %s: error: %s',
                          ['latitude', 'longitude'][index], given[index],
                          spread[index], error)
    logging.debug('final: error=%s, bitstring=%s', error, bitstring)
    if error[0] > max_error:
        raise ValueError('latitude too imprecise for max_error')
    padding = '0' * (bits - (len(bitstring) % bits))
    logging.debug('padding bitstring with %r', padding)
    bitstring += padding
    logging.debug('bitstring length: %s', len(bitstring))
    geohash = ''
    for index in range(0, len(bitstring), 5):
        geohash += alphabet[int(bitstring[index:index + 5], 2)]
    if prefer_odd and not len(geohash) % 2:
        check = decode(geohash[:-1], return_error=True)
        if check[0] <= max_error:
            geohash = geohash[:-1]
    return geohash

def decode(geohash, return_error=False):
    '''
    decode geohash into latitude and longitude

    see //en.wikipedia.org/wiki/Geohash, //geohash.org/

    >>> decode('ezs42')  # from wikipedia example
    (42.60498046875, -5.60302734375)
    '''
    binary = ''
    for character in geohash:
        binary += bin(ALPHABET.index(character))[2:].rjust(5, '0')
    logging.debug('binary: %s', binary)
    # binary string is longitude bits alternating with latitude
    latitude, longitude = [-90, 90], [-180, 180]
    error = [mean(latitude) + latitude[1], mean(longitude) + longitude[1]]
    for index in range(0, len(binary), 2):
        # first do longitude
        digit = int(binary[index])
        middle = mean(longitude)
        longitude = ([longitude[0], middle], [middle, longitude[1]])[digit]
        error[1] /= 2
        logging.debug('digit: %s, longitude: %s', digit, longitude)
        # now latitude
        try:
            digit = int(binary[index + 1])
            middle = mean(latitude)
            latitude = ([latitude[0], middle], [middle, latitude[1]])[digit]
            error[0] /= 2
            logging.debug('digit: %s, latitude: %s', digit, latitude)
        except IndexError:  # odd number of binary digits
            pass
    logging.debug('max error (lat/lon): %s', error)
    return error if return_error else (mean(latitude), mean(longitude))

def mean(numeric_array, digits=6, final_round=False):
    '''
    calculate arithmetic mean

    see notes on 'final rounding' in Wikipedia article

    >>> mean([42.583, 42.627], 0, True)
    42.6
    '''
    average = sum(numeric_array) / len(numeric_array)
    if final_round:
        # this part assumes an array of length 2!
        truncated = sys.maxsize
        digits -= 1
        while not numeric_array[0] < truncated < numeric_array[1]:
            digits += 1
            truncated = round(average, digits)
        average = truncated
    return average

def bit_length(alphabet):
    '''
    max bit length represented by the alphabet in use
    '''
    return (len(alphabet) - 1).bit_length()  # bits per character
