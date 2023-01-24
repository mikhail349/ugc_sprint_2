from bson import ObjectId
from datetime import datetime, date

from flask.json import JSONEncoder as BaseJSONEncoder


class JSONEncoder(BaseJSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)
