# coding=UTF-8

import bisect
import random
from array import array
from collections import namedtuple, deque, UserDict

# Container sequences
# list, tuple, and collections.deque can hold items of different types.

# Flat sequences
# str, bytes, bytearray, memoryview, and array.array hold items of one type.

# To initialize tuples, arrays, and other types of sequences, you could also start from a
# listcomp, but a genexp saves memory because it yields items one by one using the iterator
# protocol instead of building a whole list just to feed another constructor.

# Tuples as Records
# The collections.namedtuple function is a factory that produces subclasses of tuple
# enhanced with field names and a class name
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
print(tokyo)
# City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139.691667))
print(tokyo.population)
print(City._fields)
LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)
print(delhi._asdict())
#OrderedDict([('name', 'Delhi NCR'), ('country', 'IN'), ('population', 21.935), ('coordinates', LatLong(lat=28.613889, long=77.208889))])
for key, value in delhi._asdict().items():
    print(key + ':', value)

# The bisect module offers two main functions—bisect and insort—that use the binary
# search algorithm to quickly find and insert items in any sorted sequence.
SIZE = 7
random.seed(1729)
my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_list,new_item)
    print(new_item,'->', my_list)

# Arrays
# If the list will only contain numbers, an array.array is more efficient than a list
# it supports all mutable sequence operations (including .pop, .insert, and .extend), and
# additional methods for fast loading and saving such as .frombytes and .tofile.
floats = array('d', (random.random() for i in range(10*7)))
print(floats)
# A quick experiment show that it takes about 0.1s for array.fromfile to load 10 million
# double-precision floats from a binary file created with array.tofile.

# The class collections.deque is a thread-safe double-ended queue designed for fast
# inserting and removing from both ends.
dq = deque(range(10), maxlen=10)
print(dq)
dq.appendleft(-1)
print(dq)
# deque([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8], maxlen=10)
dq.extend([11, 22, 33])
print(dq)
# deque([2, 3, 4, 5, 6, 7, 8, 11, 22, 33], maxlen=10)

# Every Pythonista knows that d.get(k, default) is an alternative to
# d[k] whenever a default value is more convenient than handling KeyError.
# to show one case where dict.get is not the best way to handle a missing key.

# Variations of dict
# collections.OrderedDict Maintains keys in insertion order
# It’s almost always easier to create a new mapping type by extending UserDict rather than dict.
class StrKeyDict(UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

        def __contains__(self, key):
            return str(key) in self.data

        def __setitem__(self, key, item):
            self.data[str(key)] = item

















