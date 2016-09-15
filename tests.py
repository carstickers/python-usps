import unittest

from usps.addressinformation import *

USERID = None

class TestAddressInformationAPI(unittest.TestCase):

    def test_validate_address(self):
        address_validation = Address(url=USPS_CONNECTION_TEST, user_id=USERID)
        response = address_validation.validate(address2='6406 Ivy Lane', city='Greenbelt', state='MD')

        self.assertEqual(response['Address2'], '6406 IVY LN')
        self.assertEqual(response['City'], 'GREENBELT')
        self.assertEqual(response['State'], 'MD')
        self.assertEqual(response['Zip5'], '20770')
        self.assertEqual(response['Zip4'], '1441')


if __name__ == '__main__':
    #please append your USPS USERID to test against the wire
    import sys
    USERID = sys.argv.pop()
    unittest.main()
