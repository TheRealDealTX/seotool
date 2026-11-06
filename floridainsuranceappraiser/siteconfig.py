"""Business constants for floridainsuranceappraiser.com (shared by build.py and content/)."""
from datetime import date

BIZ = {
    "name": "Florida Insurance Appraiser",
    "phone_display": "+1 (844) 537-1427",
    "phone_short": "(844) 537-1427",
    "phone_href": "+18445371427",
    "email": "info@floridainsuranceappraiser.com",
    "origin": "https://floridainsuranceappraiser.com",
    "state": "FL",
    "state_long": "Florida",
}
TODAY = date.today().isoformat()
PHONE = BIZ["phone_display"]
PHONE_LINK = f'<a href="tel:{BIZ["phone_href"]}">{BIZ["phone_display"]}</a>'
