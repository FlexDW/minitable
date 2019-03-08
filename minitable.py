
from collections import namedtuple
from operator import attrgetter

class minitable:

    def __init__(self, name, fields, types, key=None):

        self.name = name
        self.fields = fields
        self.types = types
        self.row = namedtuple(name, fields)

        if key:
            self.key = key
            self.keygetter = attrgetter(*key)  # simple way of returning a tuple of the key values for the dict key
            self.rows = dict()
        else:
            self.key = None
            self.keygetter = None
            self.rows = list()

    def validate_input(self, *fields):
        """
        Used internally to validate data before insert or update
        """
        
        assert len(fields) == len(self.types), 'Input Validation Failed: Number of fields passed different to expected'
        validated_fields = [None] * len(fields)

        for i, field in enumerate(fields):
            try:
                validated_fields[i] =  self.types[i](fields[i])
            except (TypeError, ValueError) as type_val_error:
                raise Exception('Input Validation Failed: Cannot coerce input to target schema')\
                        .with_traceback(type_val_error.__traceback__)

        return validated_fields

    def insert(self, *fields):
        """
        Docstring
        """

        validated_fields = self.validate_input(*fields)
        new_row = self.row(*validated_fields)

        if self.key:
            assert self.keygetter(new_row) not in self.rows, 'Insert Failed: Key already exists'
            self.rows[self.keygetter(new_row)] = new_row
        else:
            self.rows.append(new_row)
    
    def update(self, *fields):
        """
        Updates data where a key is defined.
        If no key is defined, an assertion error is raised.
        If a key is defined but the key is not already in the list, the row is inserted.
        """

        assert self.key is not None, 'Update Failed: Update is only valid on tables where a key is defined'
        validated_fields = self.validate_input(*fields)
        update_row = self.row(*validated_fields)
        self.rows[self.keygetter(update_row)] = update_row

    def select(self, columns):
        """
        Returns a subset or re-arrangement of columns as a new minitable.
        The new minitable is always key-less, a key can be added using the set_key method. 
        Transformations cannot be done in the select statement, they must be added as 
          named columns prior to the select.

        """

        assert all( type(col) is str   for col in columns ), 'Unexpected arg type: columns must be a collection of type str'
        assert all( col in self.fields for col in columns ), 'Column mismatch: possible column names are:' + str(self.fields)

