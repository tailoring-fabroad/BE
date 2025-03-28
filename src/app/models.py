from pydantic import BaseModel
import datetime

def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")

def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )

class RWModel(BaseModel):
    model_config = {
        "validate_by_name": True,
        "json_encoders": {datetime.datetime: convert_datetime_to_realworld},
        "alias_generator": convert_field_to_camel_case,
        "from_attributes": True  # Tambahkan ini jika kamu akses dari ORM
    }
