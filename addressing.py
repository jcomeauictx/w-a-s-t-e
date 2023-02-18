#!/usr/bin/python3 -OO
'''
Implementation of ideas in the addressing RFC
'''
import  sys
import logging
from geohash import encode as geohash_encode, decode as geohash_decode

CONSONANTS = list('bcdfghjklmnprstvwxyz')
CONSONANTS += [
    'bl', 'br', 'ch', 'dr', 'fl', 'fr', 'gl', 'gr', 'll', 'pl', 'pr', 'zh'
]
VOWELS = ['ae', 'ai', 'oa'] + list('aeiou')
ALPHABET = [c + v for c in CONSONANTS for v in VOWELS]
REPLACE = (('llae', 'qua'), ('llai', 'que'), ('lloa', 'qui'), ('groa', 'quo'))
for _ in dict(REPLACE):
    ALPHABET[ALPHABET.index(_)] = dict(REPLACE)[_]
logging.debug('alphabet: %s, length: %s', ALPHABET, len(ALPHABET))

class Encoders():
    '''
    encoding formats for distributed addressing
    '''
    @staticmethod
    def format_0(latitude, longitude, direction, streetword, position):
        '''
        first two args are latitude and longitude
        third arg is the general direction of the street:
            'N' for N-S, 'E' for E-W
        4th arg is the word for 'street'
        final arg is the position of the word for 'street' in the address.

        >>> Encoders.format_0(24.067714, -110.316302, 'N', 'Calle', 0)
        'Calle GPSW110.316302 24.067714N'
        '''
        address = ['GPS']
        if direction == 'N':
            address[0] += 'W' if longitude < 0 else 'E'
            address[0] += str(abs(longitude))
            address.append(str(abs(latitude)))
            address[1] += 'S' if latitude < 0 else 'N'
        else:
            address[0] += 'S' if latitude < 0 else 'N'
            address[0] += str(abs(latitude))
            address.append(str(abs(longitude)))
            address[1] += 'W' if longitude < 0 else 'E'
        address.insert(position, streetword)
        return ' '.join(address)

    @staticmethod
    def format_1(latitude, longitude, direction, streetword, position):
        '''
        See format_0 docstring

        >>> Encoders.format_1(24.067714, -110.316302, 'N', 'Calle', 0)
        'Calle GPSWB031630 2406771N'
        '''
        intermediate = Encoders.format_0(latitude, longitude, direction,
                                         streetword, position).split()
        intermediate.pop(position)
        street = round(float(intermediate[0][4:]), 5)
        number = round(float(intermediate[1][:-1]), 5)
        if street >= 100:
            street = 'ABCDEF'[(int(street) // 10) - 10] + str(street)[2:]
        street = str(street).replace('.', '')  # get rid of decimal point
        street = intermediate[0][0:4] + street.ljust(7, '0')
        if number >= 100:
            number = 'ABCDEF'[(int(street) // 10) - 10] + str(number)[2:]
        number = str(number).replace('.', '')  # get rid of decimal point
        number = number.ljust(7, '0') + intermediate[1][-1]
        final = [street, number]
        final.insert(position, streetword)
        return ' '.join(final)

    @staticmethod
    def format_2(latitude, longitude):
        '''
        encode geohash address

        >>> Encoders.format_2(77.15, -127.86)
        'petaluma'
        '''
        return geohash_encode(latitude, longitude, alphabet=ALPHABET)

class Decoders():
    '''
    decoding the various formats back into raw GPS coordinates
    '''
    @staticmethod
    def format_0(address, streetword):
        '''
        reconstruct and return args for encode.format0(...)

        >>> Decoders.format_0('Calle GPSW110.316302 24.067714N', 'Calle')
        (24.067714, -110.316302, 'N', 'Calle', 0)
        '''
        parts = address.split()
        position = parts.index(streetword)
        parts.pop(position)
        first = parts[0][3:]
        if first.startswith(('E', 'W')):
            direction = 'N'
            easting, first = first[0], first[1:]
            northing, second = parts[1][-1], parts[1][:-1]
            longitude = float(first) * (-1 if easting == 'W' else 1)
            latitude = float(second) * (-1 if northing == 'S' else 1)
        else:
            direction = 'E'
            northing, first = first[0], first[1:]
            easting, second = parts[1][-1], parts[1][:-1]
            longitude = float(second) * (-1 if easting == 'W' else 1)
            latitude = float(first) * (-1 if northing == 'S' else 1)
        return (latitude, longitude, direction, streetword, position)

    @staticmethod
    def format_1(address, streetword):
        '''
        reconstruct and return args for decode.format1(...)

        except that latitude and longitude will only have 5 digit precision

        >>> Decoders.format_1('Calle GPSWB031630 2406771N', 'Calle')
        (24.06771, -110.3163, 'N', 'Calle', 0)
        '''
        parts = address.split()
        position = parts.index(streetword)
        parts.pop(position)
        first = parts[0][3:]
        if first.startswith(('E', 'W')):
            direction = 'N'
            easting, first = first[0], first[1:]
            northing, second = parts[1][-1], parts[1][:-1]
            if first.startswith(tuple('ABCDEF')):
                first = str('ABCDEF'.index(first[0]) + 10) + first[1:]
            if second.startswith(tuple('ABCDEF')):
                second = str('ABCDEF'.index(second[0]) + 10) + second[1:]
            longitude = float(first) * (-1 if easting == 'W' else 1)
            latitude = float(second) * (-1 if northing == 'S' else 1)
        else:
            direction = 'E'
            northing, first = first[0], first[1:]
            easting, second = parts[1][-1], parts[1][:-1]
            if first.startswith(tuple('ABCDEF')):
                first = str('ABCDEF'.index(first[0]) + 10) + first[1:]
            if second.startswith(tuple('ABCDEF')):
                second = str('ABCDEF'.index(second[0]) + 10) + second[1:]
            longitude = float(second) * (-1 if easting == 'W' else 1)
            latitude = float(first) * (-1 if northing == 'S' else 1)
        longitude /= 100000
        latitude /= 100000
        return (latitude, longitude, direction, streetword, position)

    @staticmethod
    def format_2(address, alphabet=ALPHABET):
        '''
        decode geohash address

        # this turns out to be in the north Atlantic off Prince Patrick Island!
        >>> Decoders.format_2('petaluma')
        (77.15, -127.86)
        '''
        address = address.lower()
        try:
            string, number = address.split()
            return (geohash_decode(string, alphabet=alphabet), number)
        except ValueError:
            return geohash_decode(address, alphabet=alphabet)

if __name__ == '__main__':
    ARGS = sys.argv[1:]
    # pylint: disable=no-value-for-parameter
    if ARGS:
        if ARGS[0] == 'encode':
            print(Encoders.format_2(*ARGS[1:]))
        elif ARGS[0] == 'decode':
            print(Decoders.format_2(*ARGS[1:]))
        else:
            logging.error('Must specify "encode" or "decode"')
    else:
        logging.error('Nothing to do')
