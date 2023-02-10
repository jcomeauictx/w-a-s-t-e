- Feature Name: A permissionless, unique, physical addressing scheme
- Start Date: 2023-02-07
- RFC PR: [w-a-s-t-e/rfcs](https://github.com/jcomeauictx/w-a-s-t-e/rfcs/addressing.md)
- GitHub Issue: [w-a-s-t-e/issues#1](https://github.com/jcomeauictx/w-a-s-t-e/issues/1)

# Summary
[summary]: #summary

An address for anywhere on a particular planet, that any denizen of that
location can generate without permission and with a very high likelihood of
uniqueness.

# Motivation
[motivation]: #motivation

In developing countries, even in relatively advanced areas like La Paz, BCS, Mexico, governments can be glacially slow in assigning street names and numbers.

This situation can make useless delivery addresses such as that of my workshop until a few months ago, when the street was given the name Castro Beltrán:

    John Comeau
    Calle S/N S/N (sin nombre, "without name", sin numero "without number")
    Colonia Los Cardones
    La Paz, BCS 23089

This makes it difficult for delivery services to find one's house or business,
necessitating GPS coordinates to be sent, typically, in Mexico, by use of
a WhatsApp "ping" (or "pin" as it's spelled in Spanish).

A universal, permissionless, widely recognized scheme for generation unique
addresses would reduce the need for such ad-hoc solutions.

# Guide-level explanation
[guide-level-explanation]: #guide-level-explanation

The simplest solution would use unadorned GPS coordinates as the street name
and number: if the street runs roughly north and south, the longitude component
would be the street name, and the latitude component would be the street number.
Vice versa for an east-west street. Either can be used if the street runs close
to a 45-degree angle from a compass point, or the street runs in all directions.

Precede the "street name" with "GPS" and the direction ('N', 'S', 'E', 'W').
Use the English direction abbreviations, but use local language for "street",
"avenue", or "road".

Suffix the direction to the "street number".

Using the same example as above, the improved address would be:

    John Comeau
    Calle GPSW110.316302 24.067714N
    Colonia Los Cardones
    La Paz, BCS 23089

This may work fine in many cases, and no further refinements need be considered;
a delivery person could likely decipher this even without being aware of this
protocol.

However, there are, in all likelihood, addressing restrictions built into
various websites and databases, which will reject the above based on decimal
points, or length of numbers, or a mix of letters and numbers. For these cases,
some variations on this general scheme may be of use.

Getting rid of the decimal point will require fixed-length coordinates, which
is conceptually simple enough. However, degrees east and west can exceed 100,
so the tens digit will have to encode for that possibilty. The easiest way
would be to borrow the hexadecimal digits A through F: my street name above
would then change from W110.316302 to WB031630.

Shortening the numbers is more difficult. The 4th decimal place represents 11.1
meters at the equator, which is far too large a grain for shanty towns or
tent cities. Chopping the 6th decimal place isn't much of an improvement,
but should arguably be done: Calle GPSWB031630 2406771N.

One possibility would be to use a fixed, known, coordinate set for the city
center, and have the street address be an offset from that. Yet another
possibility would be to use one of the various [Geohash](https://en.wikipedia.org/wiki/Geohash) formats, splitting it into two parts to represent street name
and number. Such improvements will be explored if they should turn out to
be necessary.

# Reference-level explanation
[reference-level-explanation]: #reference-level-explanation

Python code for the simplest form:

```python
#!/usr/bin/python3
'''
Implementation of ideas in the addressing RFC
'''

```python
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
```

# Drawbacks
[drawbacks]: #drawbacks

No known drawbacks. Even in developed countries where street names and numbers
are always assigned before construction, this method could be voluntarily used
as an alternative.

# Rationale and alternatives
[rationale-and-alternatives]: #rationale-and-alternatives

Impact of not doing this is simply to leave ad-hoc solutions as the only
alternatives.

# Prior art
[prior-art]: #prior-art

[Geohash](https://en.wikipedia.org/wiki/Geohash) could be used as is.

# Unresolved questions
[unresolved-questions]: #unresolved-questions

All of this is unresolved at this time (2023-02-10).

# Future possibilities
[future-possibilities]: #future-possibilities

Nothing considered at the moment (2023-02-10).
