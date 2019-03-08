from datetime import date, datetime
from decimal import Decimal
from collections import namedtuple

class Timestamp(datetime):
    """
    Essentially a bespoke constructor for datetime.datetime 
    object which will accept:
      - unix timestamp (assumped if passed an int)
      - ISO format string (assumed if passed a string)
      - a python datetime.datetime object (returns the object unchanged)
    """

    ### TO DO:
    ###   - Make it work also sending normal datetime args

    def __new__(cls, timestamp):
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        elif isinstance(timestamp, str):
            if len(timestamp) < 10:
                raise ValueError('Expected string matching format YYYY-MM-DD[ HH:MM:SS.ffffff], received:' + timestamp)
            timestamp = timestamp + '0001-01-01 00:00:00.000000'[len(timestamp):]
            return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        elif isinstance(timestamp, datetime):
            return timestamp
        else:
            return datetime(*timestamp)

class Date(date):
    """
    A date class with a bespoke constructor to accept strings and timestamps.
    """

    ### TO DO:
    ###   - Make it work also sending normal date args
    ###   - Truncate timestamp values to date
    
    def __new__(cls, date_input):
        if isinstance(date_input, (int, float)):
            return date.fromtimestamp(date_input)
        elif isinstance(date_input, str):
            return datetime.strptime(date_input, '%Y-%m-%d').date()
        elif isinstance(date_input, date):
            return date_input
        else:
            return date(*date_input)

type_lookup = {
    ### TO DO:
    ###   - handle missing keys
    ###   - string to lower
    ###   - add complex types
    ###   - add restricted string length types
    
    # Hive
    'tinyint': int,
    'smallint': int,
    'int': int,
    'integer': int,
    'bigint': int, 
    'float': float,
    'double': float,
    'double precision': float,
    'decimal': Decimal,
    'numeric': Decimal,
    'timestamp': Timestamp,
    'date': Date,
    #'interval': None,            # Not supported
    'string': str,
    #'varchar': str,              # Truncation not supported
    #'char': str,                 # Truncation and padding not supported
    'boolean': bool,
    'binary': bytearray,
    #'array': tuple,              # No type checking inside
    #'struct': namedtuple,        # No type checking inside
    #'union': None                # Not supported
}
