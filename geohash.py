#!/usr/bin/python3
'''
implementing Gustavo Niemeyer's geohash from Wikipedia article

geohash.org website isn't fully functional, and anyway I may need to base
a better addressing scheme on this method.
'''
import sys
import re
import logging

logging.basicConfig(level=logging.DEBUG if __debug__ else logging.WARN)

ALPHABET = '0123456789bcdefghjkmnpqrstuvwxyz'

def encode(latitude, longitude, error_override=None, alphabet=ALPHABET,
           prefer_odd=False):
    '''
    encode latitude and longitude into Geohash format

    I didn't actually see an explanation of this, just figured it out from
    the decode example.

    latitude and longitude can be provided as strings or floats.

    max_error is calculated from number of digits of precision, but if
    `error_override` is provided, it is used for both latitude and longitude.

    `prefer_odd` will return an odd-length geohash if allowed by max_error

    >>> encode(42.605, -5.603, .03, prefer_odd=True)
    'ezs42'
    '''
    spread = [[-90, 90], [-180, 180]]
    given, max_error = normalize(latitude, longitude)
    if error_override is not None:
        max_error = (float(error_override), float(error_override))
    bitstring = ''
    error = [sys.maxsize, sys.maxsize]
    while error[1] > max_error[1]:
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
    if error[0] > max_error[0]:
        raise ValueError('latitude too imprecise for max_error')
    bitstring = pad(bitstring, alphabet)
    logging.debug('bitstring length: %s', len(bitstring))
    geohash = []
    for index in range(0, len(bitstring), 5):
        geohash += [alphabet[int(bitstring[index:index + 5], 2)]]
    if prefer_odd and not len(geohash) % 2:
        # chopping a character will affect error of both lat and lon
        logging.debug('checking error of odd geohash %s', geohash[:-1])
        check = decode(geohash[:-1], return_error=True)
        if check[0] <= max_error[0] and check[1] <= max_error[1]:
            geohash = geohash[:-1]
    return ''.join(geohash)

def decode(geohash, alphabet=ALPHABET, return_error=False):
    '''
    decode geohash into latitude and longitude

    see //en.wikipedia.org/wiki/Geohash, //geohash.org/

    >>> decode('ezs42')  # from wikipedia example
    (42.6, -5.6)
    '''
    bits = bit_length(alphabet)  # for padding bitstring
    binary = ''
    if str(alphabet) == alphabet:  # checking we have a normal alphabet
        split = list  # if so, easy to split geohash into pieces
    else:
        split = re.compile('(?:' + '|'.join(alphabet) + ')').findall
    logging.debug('pre-split geohash: %s', geohash)
    geohash = [piece.lower() for piece in split(geohash)]
    logging.debug('split geohash: %s', geohash)
    for character in geohash:
        binary += bin(alphabet.index(character))[2:].rjust(bits, '0')
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
    if return_error:
        return error
    digits = (significant_digits(error[0]), significant_digits(error[1]))
    latitude = mean(latitude, digits[0], final_round=True)
    longitude = mean(longitude, digits[1], final_round=True)
    return (latitude, longitude)

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

def pad(bitstring, alphabet):
    '''
    make sure bitstring is in exact multiple of the alphabet bit_length

    >>> pad('01010', ALPHABET)
    '01010'
    >>> pad('01', ALPHABET)
    '01000'
    '''
    bits = bit_length(alphabet)  # for padding bitstring
    padding = '0' * ((bits - (len(bitstring) % bits)) % bits)
    logging.debug('padding bitstring with %r', padding)
    return bitstring + padding

def normalize(latitude, longitude):
    '''
    determine max_error for latitude and longitude
    return both as floats in a tuple, same for max_error

    rationale: let's say longitude is provided as 42.605; this should
    have been rounded down from just under 42.6055 or less, or rounded up
    from 42.6045 or more. so the error is plus or minus 0.0005.

    latitude and longitude may have been provided as strings, if from the
    command line or from a foreign script, or as floats. we assume either,
    and convert in all cases.

    >>> normalize(43, -6)
    ((43.0, -6.0), (0.5, 0.5))

    >>> normalize('42.605', '-5.603')
    ((42.605, -5.603), (0.0005, 0.0005))
    '''
    latitude, longitude = str(latitude), str(longitude)
    max_error = (error_calculation(latitude), error_calculation(longitude))
    return (float(latitude), float(longitude)), max_error

def error_calculation(numeric_string):
    '''
    see docstring for `normalize`.
    '''
    dot = numeric_string.rfind('.')
    if dot != -1:
        error = 0.5 * (10 ** -(len(numeric_string) - (dot + 1)))
    else:
        error = 0.5  # no dot in number at all
    return error

def significant_digits(error):
    '''
    calculate significant digits from the maximum error

    only designed to work with errors < 1
    simplistic approach only counts significant the digits with a zero
    in the error.

    >>> significant_digits(.022)
    1
    >>> significant_digits(.01010)
    1
    >>> significant_digits(.1)
    0
    >>> significant_digits(10)
    0
    '''
    digits = 0
    if error * 10 < 1:
        error = str(error)
        match = re.search(r'\.(0+)', error)
        if not match:
            raise ValueError('Strange error value %s' % error)
        else:
            digits = len(match.group(1))
    return digits
