from bson import ObjectId
from datetime import datetime, date

from flask.json import JSONEncoder as BaseJSONEncoder


class JSONEncoder(BaseJSONEncoder):
    """Класс кодирования JSON, который приводит:
    - `ObjectId` к `str`
    - `datetime и date` к `ISO` формату
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)
