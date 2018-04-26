import unittest
from xml.etree import ElementTree as ET
from xml.dom import minidom
from usps.addressinformation import *
USERID = None
import xmltodict
import json
from constants import CARRIER_PICKUP_SCHEDULE_REQUEST_SERVICE_TYPE

USERID = ""
USPS_CONNECTION_TEST = 'https://secure.shippingapis.com/ShippingAPITest.dll'
USPS_CONNECTION_HTTP = 'http://production.shippingapis.com/ShippingAPI.dll'
class TestAddressInformationAPI(unittest.TestCase):

    def test_validate_address(self):
        address_validation = Address(user_id=USERID, url=USPS_CONNECTION_TEST)
        response = address_validation.validate(address2='760 Charcot Ave', city='San Jose', state='CA')
        print(response)
        # print(minidom.parseString(ET.tostring(response_xml)).toprettyxml(indent="    "))

    def test_package_makexml(self):
        """
        test rate
        Returns:

        """
        rate = DomesticRate(user_id=USERID, url=USPS_CONNECTION_TEST)

        package_dict_one = {
            'Service': 'FIRST CLASS',
            'FirstClassMailType': 'LETTER',
            'ZipOrigination': 44106,
            'ZipDestination': 20770,
            'Pounds': 0,
            'Ounces': float(3.12345678),
            'Container': '',
            'Size': 'REGULAR',
            'Machinable': True
        }

        package_dict_two = {
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
        }
        xml = rate.make_xml(package_dicts=[package_dict_one, package_dict_two])
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))

    def test_make_rate_request(self):
        """
        test rate xml construction and api call
        Returns:

        """
        rate = DomesticRate(user_id=USERID, url=USPS_CONNECTION_TEST)

        package_dict_one = {
            'Service': 'FIRST CLASS',
            'FirstClassMailType': 'LETTER',
            'ZipOrigination': 44106,
            'ZipDestination': 20770,
            'Pounds': 0,
            'Ounces': float(3.12345678),
            'Container': 'VARIABLE',
            'Size': 'REGULAR',
            'Machinable': True
        }

        package_dict_two = {
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
        }

        xml = rate.make_xml(package_dicts=[package_dict_one, package_dict_two])
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))
        response_xml = rate.submit_xml(xml)
        print(minidom.parseString(ET.tostring(response_xml)).toprettyxml(indent="    "))
        return_dict = xmltodict.parse(ET.tostring(response_xml))
        print(json.loads(json.dumps(return_dict)))


    def test_intelRate(self):

        package_dict_two = {
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
        }

        intl = IntlRateV2(user_id=USERID, )
        xml = intl.make_xml(package_dicts=[package_dict_two])
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))
        response_xml = intl.submit_xml(xml)
        print(intl.to_json(response_xml))

    def test_tracker(self):
        """
        test tracker
        Returns:

        """
        tracker = Track(user_id="766POSTG6978",url=USPS_CONNECTION_TEST)
        tracker_ids = ['9405536897846333893331']
        xml = tracker.make_xml(tracker_ids=tracker_ids)
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))
        response_xml = tracker.submit_xml(xml)
        print(minidom.parseString(ET.tostring(response_xml)).toprettyxml(indent="    "))

    def test_carrier_pickup_availability(self):
        """
        test carrier pickup availability
        Returns:

        """
        avail = CarrierPickupAvailability(user_id='766POSTG6978',url=USPS_CONNECTION_TEST)
        request_dict = {
            "FirmName": "PostGround Corp",
            "SuiteOrApt": "Suite777",
            "Address2": "760 Charcot Ave",
            "Urbanization": "",
            "City": "San Jose",
            "State": "CA",
            "ZIP5": "95131",
            "ZIP4": "2223"
        }
        xml = avail.make_xml(
            pickup_availability_dict=request_dict
        )
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))
        response_xml = avail.submit_xml(xml)
        print(avail.to_json(response_xml))

    def test_carrier_pickup_schedule(self):
        """

        No test api
        Returns:

        """
        schedule = CarrierPickupSchedule(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict = {
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
        }
        xml = schedule.make_xml(pickup_schedule_dict=request_dict)
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))
        response_xml = schedule.submit_xml(xml)
        print(schedule.to_json(response_xml))

    def test_carrier_pickup_cancel(self):
        """
        No test api
        Returns:

        """
        pickup_cancel = CarrierPickupCancel(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict = {
            "FirmName": "PostGround Corp",
            "SuiteOrApt": "Suite777",
            "Address2": "760 Charcot Ave",
            "Urbanization": "",
            "City": "San Jose",
            "State": "CA",
            "ZIP5": "95131",
            "ZIP4": "2223",
            "ConfirmationNumber": "XXXXXX"
        }
        xml = pickup_cancel.make_xml(pickup_cancel_dict=request_dict)
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))

    def test_carrier_pickup_change(self):
        """

        No test api
        Returns:

        """
        schedule = CarrierPickupChange(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict = {
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
            "ConfirmationNumber" :"xxxx"

        }
        xml = schedule.make_xml(pickup_schedule_change_dict=request_dict)
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))


    def test_mail_service(self):
        SERVICE_NAME = ['PriorityMail', 'StandardB', 'FirstClassMail', 'ExpressMailCommitment']
        mail_service = MailService(user_id=USERID, url=USPS_CONNECTION_TEST)
        request_dict ={
            "OriginZip": "95131",
            "DestinationZip": "21114"
        }
        for service_name in SERVICE_NAME:
            xml = mail_service.make_xml(mail_service_dict=request_dict,service_name=service_name)
            print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))

    def test_sdcgetlocation(self):
        sdcgl = ServiceDelivery(user_id=USERID, url=USPS_CONNECTION_HTTP)
        request_dict = {
            "MailClass": "0",
            "OriginZIP": "70601",
            "DestinationZIP": "98101",
            "AcceptDate": "30-April-2018",
            "AcceptTime": "0900",
            "NonEMDetail": "True",
        }
        xml = sdcgl.make_xml(sdc_get_location_dict=request_dict)
        print(minidom.parseString(ET.tostring(xml)).toprettyxml(indent="    "))
        response_xml = sdcgl.submit_xml(xml)
        print(sdcgl.to_json(response_xml))


if __name__ == '__main__':
    #please append your USPS USERID to test against the wire
    import sys
    unittest.main()
