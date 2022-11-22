import os
import unittest
import random
from datetime import datetime, timedelta
from xml.dom import minidom
from xml.etree import ElementTree

import xmltodict

from constants import CARRIER_PICKUP_SCHEDULE_REQUEST_SERVICE_TYPE
from usps.addressinformation import *

USERID = os.environ.get('USERID')  # A user id must be defined in the environment variables to run the test
USPS_CONNECTION_TEST = 'https://secure.shippingapis.com/ShippingAPITest.dll'
USPS_CONNECTION_HTTP = 'http://production.shippingapis.com/ShippingAPI.dll'


# USPS cares about the order of the arbitrary order that the data submitted, but normal users shouldn't.
# Let's shuffle the data to ensure that it can be inputted in any order.
def randomize_dict(obj):
    # Python 3.7+ maintains ordering in dicts
    randomized = {}
    keys = list(obj.keys())
    random.shuffle(keys)
    for key in keys:
        if isinstance(obj[key], dict):
            randomized[key] = randomize_dict(obj[key])
        else:
            randomized[key] = obj[key]

    return randomized


def print_xml(xml):
    print(minidom.parseString(ElementTree.tostring(xml)).toprettyxml(indent="    "))

class TestAddressInformationAPI(unittest.TestCase):

    def test_validate_address(self):
        self.assertIsNotNone(USERID)
        address_validation = Address(user_id=USERID, url=USPS_CONNECTION_TEST)
        response = address_validation.validate(address2='760 Charcot Ave', city='San Jose', state='CA')

    def test_domestic_rate_make_xml(self):
        """
        test rate
        Returns:

        """
        self.assertIsNotNone(USERID)
        rate = DomesticRate(user_id=USERID, url=USPS_CONNECTION_TEST)

        package_dict_one = randomize_dict({
            'Service': 'FIRST CLASS',
            'FirstClassMailType': 'LETTER',
            'ZipOrigination': 44106,
            'ZipDestination': 20770,
            'Pounds': 0,
            'Ounces': float(3.12345678),
            'Container': '',
            'Size': 'REGULAR',
            'Machinable': True
        })
        package_dict_two = randomize_dict({
            'Service': 'PRIORITY',
            'ZipOrigination': 44106,
            'ZipDestination': 20770,
            'Pounds': 1,
            'Ounces': 8,
            'Container': 'NONRECTANGULAR',
            'Size': 'LARGE',
            'Width': 15,
            'Length': 30,
            'Height': 15,
            'Girth': 55,
            'Value': 1000,
            'SpecialServices': [
                {
                    'SpecialService': 1
                },
                {
                    'SpecialService': 2
                }]
        })

        xml = rate.make_xml(package_dicts=[package_dict_one, package_dict_two])

    def test_domestic_rate_submit(self):
        """
        test rate xml construction and api call
        Returns:

        """
        rate = DomesticRate(user_id=USERID, url=USPS_CONNECTION_TEST)

        package_dict_one = randomize_dict({
            'Service': 'FIRST CLASS',
            'FirstClassMailType': 'LETTER',
            'ZipOrigination': 44106,
            'ZipDestination': 20770,
            'Pounds': 0,
            'Ounces': 3.12345678,
            'Container': 'VARIABLE',
            'Machinable': True
        })

        package_dict_two = randomize_dict({
            'Service': 'PRIORITY',
            'ZipOrigination': 44106,
            'ZipDestination': 20770,
            'Pounds': 1,
            'Ounces': 8,
            'Container': 'NONRECTANGULAR',
            'Width': 15,
            'Length': 30,
            'Height': 15,
            'Girth': 55,
            'Value': 1000,
            'SpecialServices': [
                {
                    'SpecialService': 108
                },
                {
                    'SpecialService': 100
                }],
            'Content':
                {
                    'ContentType': 'LIVES',
                    'ContentDescription': 'Other'
                }
        })

        xml = rate.make_xml(package_dicts=[package_dict_one, package_dict_two])
        response_xml = rate.submit_xml(xml)
        return_dict = xmltodict.parse(ElementTree.tostring(response_xml))

        self.assertTrue('RateV4Response' in return_dict and 'Package' in return_dict.get('RateV4Response'))
        self.assertTrue(len(return_dict['RateV4Response']['Package']) == 2)

    def test_intel_rate_v2_submit(self):
        package_dict_two = randomize_dict({
            'Pounds': 1,
            'Ounces': 8,
            'MailType': 'Package',
            'GXG': {
                'POBoxFlag': 'Y',
                'GiftFlag': 'Y'
            },
            'ValueOfContents': 200,
            'Country': 'Australia',
            'Container': 'RECTANGULAR',
            'Size': 'LARGE',
            'Width': 15,
            'Length': 30,
            'Height': 15,
            'Girth': 55,
            'OriginZip': 18701,
            'CommercialFlag': 'N',
            'ExtraServices': [
                {
                    'ExtraService': 106
                }
            ],
            'Content':
                {
                    'ContentType': 'Documents',
                    'ContentDescription': 'Other'
                }
        })

        self.assertIsNotNone(USERID)

        intl = IntlRateV2(user_id=USERID, )
        xml = intl.make_xml(package_dicts=[package_dict_two])
        response_xml = intl.submit_xml(xml)

    def test_tracker_submit(self):
        tracker = Track(user_id="766POSTG6978", url=USPS_CONNECTION_TEST)
        tracker_ids = ['9405536897846333893331']
        xml = tracker.make_xml(tracker_ids=tracker_ids)

        # USPS doesn't seem to offer sandbox or testing tracking numbers so lets just check against a
        # valid not found response
        with self.assertRaises(USPSXMLError) as context:
            tracker.submit_xml(xml)

        self.assertTrue(
            'A status update is not yet available on your Priority Mail' in context.exception.info.get('Description'))

    def test_carrier_pickup_availability_submit(self):
        self.assertIsNotNone(USERID)
        avail = CarrierPickupAvailability(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict = randomize_dict({
            "FirmName": "PostGround Corp",
            "SuiteOrApt": "Suite777",
            "Address2": "760 Charcot Ave",
            "Urbanization": "",
            "City": "San Jose",
            "State": "CA",
            "ZIP5": "95131",
            "ZIP4": "2223"
        })
        xml = avail.make_xml(
            pickup_availability_dict=request_dict
        )
        response_xml = avail.submit_xml(xml)

    def test_carrier_pickup_schedule_submit(self):
        self.assertIsNotNone(USERID)
        schedule = CarrierPickupSchedule(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict = randomize_dict({
            "FirstName": "Luyi",
            "LastName": "Doe",
            "FirmName": "PostGround Corp",
            "SuiteOrApt": "",
            "Address2": "760 Charcot Ave",
            "Urbanization": "",
            "City": "San Jose",
            "State": "CA",
            "ZIP5": "95131",
            "ZIP4": "2223",
            "Phone": "555-555-1234",
            "Extension": "",
            "Package": [
                {
                    "ServiceType": CARRIER_PICKUP_SCHEDULE_REQUEST_SERVICE_TYPE[0],
                    "Count": 2
                },
                {
                    "ServiceType": CARRIER_PICKUP_SCHEDULE_REQUEST_SERVICE_TYPE[1],
                    "Count": 2
                }
            ],
            "EstimatedWeight": "14",
            "PackageLocation": "Front Door",
            "SpecialInstructions": "Behind the screen door"
        })
        xml = schedule.make_xml(pickup_schedule_dict=request_dict)
        response_xml = schedule.submit_xml(xml)

    def test_carrier_pickup_cancel_make_xml(self):
        self.assertIsNotNone(USERID)
        pickup_cancel = CarrierPickupCancel(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict = randomize_dict({
            "FirmName": "PostGround Corp",
            "SuiteOrApt": "Suite777",
            "Address2": "760 Charcot Ave",
            "Urbanization": "",
            "City": "San Jose",
            "State": "CA",
            "ZIP5": "95131",
            "ZIP4": "2223",
            "ConfirmationNumber": "XXXXXX"
        })
        xml = pickup_cancel.make_xml(pickup_cancel_dict=request_dict)

    def test_carrier_pickup_change_make_xml(self):
        # https://www.usps.com/business/web-tools-apis/service-delivery-calculator-get-locations-api.htm
        self.assertIsNotNone(USERID)
        schedule = CarrierPickupChange(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict = randomize_dict({
            "FirstName": "Luyi",
            "LastName": "Doe",
            "FirmName": "PostGround Corp",
            "SuiteOrApt": "",
            "Address2": "760 Charcot Ave",
            "Urbanization": "",
            "City": "San Jose",
            "State": "CA",
            "ZIP5": "95131",
            "ZIP4": "2223",
            "Phone": "555-555-1234",
            "Extension": "",
            "Package": [
                {
                    "ServiceType": CARRIER_PICKUP_SCHEDULE_REQUEST_SERVICE_TYPE[0],
                    "Count": 2
                },
                {
                    "ServiceType": CARRIER_PICKUP_SCHEDULE_REQUEST_SERVICE_TYPE[1],
                    "Count": 2
                }
            ],
            "EstimatedWeight": "14",
            "PackageLocation": "Front Door",
            "SpecialInstructions": "Behind the screen door",
            "ConfirmationNumber": "xxxx"

        })
        xml = schedule.make_xml(pickup_schedule_change_dict=request_dict)

    def test_mail_services_make_xml(self):
        self.assertIsNotNone(USERID)
        mail_service = MailService(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict = randomize_dict({
            "OriginZip": "95131",
            "DestinationZip": "21114"
        })
        for service_name in MailService.SERVICE_NAMES:
            xml = mail_service.make_xml(mail_service_dict=request_dict, service_name=service_name)

    def test_sdc_get_location(self):
        self.assertIsNotNone(USERID)
        service_delivery = ServiceDelivery(user_id=USERID, url=USPS_CONNECTION_HTTP)
        request_dict = randomize_dict({
            "MailClass": "0",
            "OriginZIP": "70601",
            "DestinationZIP": "98101",
            "AcceptDate": (datetime.now() + timedelta(days=1)).strftime('%d-%B-%Y'),
            "AcceptTime": "0900",
            "NonEMDetail": "True",
        })
        xml = service_delivery.make_xml(sdc_get_location_dict=request_dict)
        response_xml = service_delivery.submit_xml(xml)


if __name__ == '__main__':
    unittest.main()
