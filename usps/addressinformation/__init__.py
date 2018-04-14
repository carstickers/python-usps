from usps.addressinformation.base import USPSXMLError, Address, DomesticRate, Track, CarrierPickupAvailability,\
    CarrierPickupSchedule, CarrierPickupCancel,CarrierPickupChange, IntlRateV2, MailService, ServiceDelivery
USPS_CONNECTION_HTTP = 'http://production.shippingapis.com/ShippingAPI.dll'
USPS_CONNECTION = 'https://secure.shippingapis.com/ShippingAPI.dll'
USPS_CONNECTION_TEST = 'https://secure.shippingapis.com/ShippingAPITest.dll'
USPS_CONNECTION_TEST_SECURE = USPS_CONNECTION_TEST
