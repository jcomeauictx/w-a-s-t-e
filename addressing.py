#!/usr/bin/python3
'''
Implementation of ideas in the addressing RFC
'''

def format_0(latitude, longitude, direction, streetword, position):
    '''
    first two args are latitude and longitude
    third arg is the general direction of the street: 'N' for N-S, 'E' for E-W
    4th arg is the word for 'street'
    final arg is the position of the word for 'street' in the address.

    >>> format_0(24.067714, -110.316302, 'N', 'Calle', 0)
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
