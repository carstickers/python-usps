Python USPS
===========

This is a fork of the python-usps library https://github.com/cuker/python-usps.  A lot of the library
was removed and refactored to be more simple as the only practical application of the USPS library thus
far has been address validation.


Installation
------------

    pip install python-usps2

This package is a fork of the original python-usps by Jason Kraus, so I have named the package differently
on Pypi to account for this.

Usage
-----

    from usps.addressinformation import *


    address_validation = Address(user_id='YOUR_USER_ID')
    response = address_validation.validate(address1='500 E. third st', city='Loveland', state='CO')

If an address is invalid (Doesn't exist) will raise USPSXMLError


Note

python-usps is not at all endorsed by the USPS in any way.