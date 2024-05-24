import utilities
import datetime

data = {"user_id": 123}
expires = datetime.timedelta(hours=2)
token = utilities.create_token(data, expires)
print(token)