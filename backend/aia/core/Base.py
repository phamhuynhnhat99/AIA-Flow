from uuid import uuid4

class IDCtr:
    """
    A simple ascending integer ID counter.
    """

    def __init__(self):
        self.ctr = -1

    def new_ctr(self):
        self.ctr = "dndnode_" + str(uuid4())
        return self.ctr

    def set(self, ctr):
        self.ctr = ctr


class Base:
    """
    Base class for all abstract components. It provides:
    ...
    """

    _global_id_ctr = IDCtr()
    _global_objs = {}

    @classmethod
    def obj_from_global_id(cls, id: int):
        return cls._global_objs.get(id)

    complete_data_function = lambda data: data

    @staticmethod
    def complete_data(data: dict):
        return Base.complete_data_function(data)


    version: str = None

    # non-static

    def __init__(self):
        self.global_id = self._global_id_ctr.new_ctr()
        self._global_objs[self.global_id] = self

        self.prev_global_id = None
        self.prev_version = None

    def update_ctr(self, ctr):
        self._global_id_ctr.set(ctr=ctr)


    def data(self) -> dict:
        """
        Convert the object to a JSON compatible dict.
        Reserved field names are 'GID' and 'version'.
        """
        return {
            'GID': self.global_id,

            # version optional
            **({'version': self.version}
                if self.version is not None
                else {})
        }

    def load(self, data: dict):
        if dict is not None:
            self.prev_global_id = data['GID']
            self._global_objs[self.prev_global_id] = self
            self.prev_version = data.get('version')