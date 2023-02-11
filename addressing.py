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
        'Calle GPSWB031630 2406771N'
        (24.067714, -110.316302, 'N', 'Calle', 0)
        '''
        intermediate = Decoders.format_0(address, streetword)
        return intermediate
