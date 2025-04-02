import phonenumbers
from django.core.exceptions import ValidationError
import pycountry

def validate_phone_number(phone_number, country_code):
    """Validate phone number using phonenumbers package based on country ISO code."""
    if not country_code:
        raise ValidationError({"country": "Country selection is required."})

    try:
        # Ensure the country exists
        if not pycountry.countries.get(alpha_2=country_code.upper()):
            raise ValidationError({"country": "Invalid country code."})

        # Parse and validate the phone number
        parsed_number = phonenumbers.parse(phone_number, country_code.upper())

        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError({"phone_number": "Invalid phone number format for the selected country."})

    except phonenumbers.NumberParseException:
        raise ValidationError({"phone_number": "Invalid phone number format."})

    return phone_number
