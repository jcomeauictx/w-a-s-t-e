- Feature Name: A permissionless, unique, physical addressing scheme
- Start Date: 2023-02-07
- RFC PR: [w-a-s-t-e/rfcs](https://github.com/w-a-s-t-e/rfcs/addressing_rfc.md)
- GitHub Issue: [w-a-s-t-e/issues#1](https://github.com/w-a-s-t-e/issues/1)

# Summary
[summary]: #summary

An address for anywhere on a particular planet, that any denizen of that
location can generate without permission and with a very high likelihood of
uniqueness.

# Motivation
[motivation]: #motivation

Why are we doing this? What use cases does it support? What is the expected outcome?

In developing countries, even in relatively advanced areas like La Paz, BCS, Mexico, governments can be glacially slow in assigning street names and numbers.

This situation can make useless delivery addresses such as that of my workshop until a few months ago, when the street was given the name Castro Beltr&aacuten:

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
and number: if the street runs roughly north and south, the N or S component
would be the street name, and the E or W component would be the street number.
Vice versa for an east-west street. Either can be used if the street runs at
a 45-degree angle from a compass point, or the street runs in all directions.

Using the same example as above, the improved address would be:

    John Comeau
    Calle 24.067714NGPS 110.316302W (W instead of O for "oeste" for clarity)
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
would be to borrow the hexadecimal digits A through F: my house number above
would then change from 110.316302W to B0316202W.

Shortening the numbers is more difficult. The 4th decimal place represents 11.1
meters at the equator, which is far too large a grain for shanty towns or
tent cities, and chopping the 6th decimal place isn't much of an improvement.
One possibility would be to use a fixed, known, coordinate set for the city
center, and have the street address be an offset from that. Yet another
possibility would be to use one of the various (Geohash)[https://en.wikipedia.org/wiki/Geohash] formats, splitting it into two parts to represent street name
and number. Such improvements will be explored if they should turn out to
be necessary.

# Reference-level explanation
[reference-level-explanation]: #reference-level-explanation

This is the technical portion of the RFC. Explain the design in sufficient detail that:

- Its interaction with other features is clear.
- It is reasonably clear how the feature would be implemented.
- Corner cases are dissected by example.

The section should return to the examples given in the previous section, 
and explain more fully how the detailed proposal makes those examples work.

# Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

# Rationale and alternatives
[rationale-and-alternatives]: #rationale-and-alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not choosing them?
- What is the impact of not doing this?

# Prior art
[prior-art]: #prior-art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other ML compilers or languages and discuss the experience their community has had?
- For community proposals: Is this done by some other community and what were their experiences with it?
- For other teams: What lessons can we learn from what other communities have done here?
- Papers: Are there any published papers or great posts that discuss this? 
  If you have some relevant papers to refer to, this can serve as a more detailed theoretical background.

If there is no prior art, that is fine - your ideas are interesting to us whether they are 
  brand new or if it is an adaptation from other languages.

Note that while precedent set by other languages is some motivation, it does not on its own motivate an RFC.
Please also take into consideration that TVM intentionally diverges from other compilers.

# Unresolved questions
[unresolved-questions]: #unresolved-questions

- What parts of the design do you expect to resolve through the RFC process before this gets merged?
- What parts of the design do you expect to resolve through the implementation of this feature before stabilization?
- What related issues do you consider out of scope for this RFC that could be addressed in the future 
  independently of the solution that comes out of this RFC?

# Future possibilities
[future-possibilities]: #future-possibilities

Think about what the natural extension and evolution of your proposal would
be and how it would affect the language and project as a whole in a holistic
way. Try to use this section as a tool to more fully consider all possible
interactions with the project and language in your proposal.
Also consider how this all fits into the roadmap for the project
and of the relevant sub-team.

This is also a good place to "dump ideas", if they are out of scope for the
RFC you are writing but otherwise related.

If you have tried and cannot think of any future possibilities,
you may simply state that you cannot think of anything.

Note that having something written down in the future-possibilities section
is not a reason to accept the current or a future RFC; such notes should be
in the section on motivation or rationale in this or subsequent RFCs.
The section merely provides additional information.
