# xmltreenode

Abstraction over Python ElementTree. Makes parsing and handling XML files
a bit easier.


## XMLTreeNode

Main functionality lies on XMLTreeNode. It forms useful Python object,
which can be used to build the XML document tree.

Supports multiple search and handling operations, which are missing
from ElementTree implementation.


## CustomXMLParser

Parser to read and parse XML files. Outputs XMLTreeNode structure.


## Installation

Traditional python module install:

    python setup.py install


### Unit tests

Target is to provide full and useful unit test coverage to ensure
nothing breaks while making modifications to code.

To run unit test suite, just do:

    make test


Code coverage test run:

    make coverage


## Examples

See examples folder.


## License

MIT
