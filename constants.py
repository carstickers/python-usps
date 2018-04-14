"""CONTAINER VARIABLe

"""

FIRST_CLASS_MAIL_TYPE = [ "LETTER", "FLAT", "PACKAGE SERVICE RETAIL", "POSTCARD","PACKAGE SERVICE"  ]
CONTAINER = [
    "VARIABLE",
    "FLAT RATE ENVELOPE",
    "PADDED FLAT RATE ENVELOPE",
    "LEGAL FLAT RATE ENVELOPE",
    "SM FLAT RATE ENVELOPE",
    "WINDOW FLAT RATE ENVELOPE",
    "GIFT CARD FLAT RATE ENVELOPE",
    "SM FLAT RATE BOX",
    "MD FLAT RATE BOX",
    "LG FLAT RATE BOX",
    "REGIONALRATEBOXA",
    "REGIONALRATEBOXB",
    "RECTANGULAR",
    "NONRECTANGULAR",
    "CUBIC PARCELS",
    "CUBIC SOFT PACK"]

"""
Special Service Name

ServiceID

Insurance

100

Insurance – Priority Mail Express

101

Return Receipt

102

Collect on Delivery

103

Certificate of Mailing (Form 3665)

104

Certified Mail

105

USPS Tracking

106

Return Receipt for Merchandise

107

Signature Confirmation

108

Registered Mail

109

Return Receipt Electronic

110

Registered mail COD collection Charge

112

Return Receipt – Priority Mail Express

118

Adult Signature Required

119

Adult Signature Restricted Delivery

120

Insurance – Priority Mail

125

USPS Tracking Electronic

155

Signature Confirmation Electronic

156

Certificate of Mailing (Form 3817)

160

Priority Mail Express 1030 AM Delivery

161

Certified Mail Restricted Delivery

170

Certified Mail Adult Signature Required

171

Certified Mail Adult Signature Restricted Delivery

172

Signature Confirm. Restrict. Delivery

173

Signature Confirmation Electronic Restricted Delivery

174

Collect on Delivery Restricted Delivery

175

Registered Mail Restricted Delivery

176

Insurance Restricted Delivery

177

Insurance Restrict.  Delivery – Priority Mail

179

Insurance Restrict. Delivery – Priority Mail Express

178

Insurance Restrict. Delivery (Bulk Only)

180

Special Handling - Fragile

190"""
SPECIAL_SERVICE = [101, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 112, 118, 119, 120, 125, 155, 156, 160, 161,
                   170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 190]

CARRIER_PICKUP_SCHEDULE_REQUEST_SERVICE_TYPE = ["PriorityMailExpress",
                                                "PriorityMail",
                                                "FirstClass",
                                                "ParcelSelect",
                                                "Returns",
                                                "International",
                                                "OtherPackages"]
