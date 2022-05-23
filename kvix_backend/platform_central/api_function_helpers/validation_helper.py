import re
import datetime
from datetime import date 

def email_mobile_validator(email=None,mobile=None):
    if email :
        email_validator_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        email_valid = re.match(email_validator_regex,email)
        return email_valid

    if mobile :
        mobile_validator_regex = '^[0-9]{10}$'
        mobile_valid = re.match(mobile_validator_regex,mobile)
        return mobile_valid



# class splcharFilter(Filter):
#     def __iter__(self):
#         for token in Filter.__iter__(self):
#             strip_field = ''
#             for character in token['data']:
#                 if (character.isalnum()) | (character == " "):
#                     strip_field +=character
#             token['data'] = strip_field            
#         yield token

def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))