#!/usr/bin/python3
'''
Implementation of ideas in the addressing RFC
'''

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
        street, number = intermediate[0][4:], intermediate[1][:-1]
        if float(street) >= 100:
            street = 'ABCDEF'[(int(float(street)) // 10) - 10] + street[2:]
        street = street.replace('.', '')[:-1]  # get rid of decimal point
        street = intermediate[0][0:4] + street
        # and final digit
        if float(number) >= 100:
            number = 'ABCDEF'[(int(float(street)) // 10) - 10] + number[2:]
        number = number.replace('.', '')[:-1]  # get rid of decimal point
        number += intermediate[1][-1]
        # and final digit
        final = [street, number]
        final.insert(position, streetword)
        return ' '.join(final)

class Decoders():
    '''
    decoding the various formats back into raw GPS coordinates

    >>> Decoders.format_0('Calle GPSW110.316302 24.067714N', 'Calle')
    (24.067714, -110.316302, 'N', 'Calle', 0)
    '''
    @staticmethod
    def format_0(address, streetword):
        '''
        reconstruct and return args for encode.format0(...)
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
