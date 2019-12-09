import enum

class QueryType(enum.Enum):
    NAME = 1
    TYPE = 2
    PROVINCE = 3

class CultureRepository(object):
    def __init__(self):
        self.entries = {} # Data stored in a dict with key=name and value=Culture model

    # Create: accepting list of Culture model and add it to the dict
    # This method will raise exception if the data already exists, because
    # adding existing data will be considered same as updating
    def create(self, requests):
        for request in requests:
            request.name = request.name.title()
            request.type = request.type.title()
            request.province = request.province.title()
            self.entries[request.name] = request

    # Find All: Returning all cultures in storage
    def find_all(self):
        if len(self.entries) == 0:
            return None
        return (self.entries.values())

    def find_by_name(self, name):
        res = self.entries[name]
        return res

    # Count All: Returning count of all cultures
    def count_all(self):
        res = len(self.entries)
        return res

    # Search: accepting search keyword and field as QueryType enum type
    # Keyword will be handled based on its QueryType
    def search(self, keyword, field):
        if field == QueryType.NAME: # Search by Name
            res = []
            for _, v in self.entries.items():
                if keyword.lower() in v.name.lower():
                    res.append(v)
            return res, len(res)

        elif field == QueryType.TYPE: # Search by Type
            res = []
            for _, v in self.entries.items():
                if keyword.lower() in v.type.lower():
                    res.append(v)
            return res, len(res)

        elif field == QueryType.PROVINCE: # Search by Province
            res = []
            for _, v in self.entries.items():
                if keyword.lower() in v.province.lower():
                    res.append(v)
            return res, len(res)

    # Delete: delete data from storage by name index
    def delete(self, name):
        try:
            del self.entries[name]
        except ValueError:
            raise Exception("object not found")

    # Update: update data from storage
    def update(self, req):
        try:
            self.entries[req.name]
            self.entries.update({req.name: req})
        except KeyError:
            raise Exception("object not found")
    
    # Count by Type: Generating set of types and counting the count of each data type and storing it in a dict
    # with key=type and value=count
    def count_by_type(self):
        types = set()
        res = {}
        for _, v in self.entries.items():
            types.add(v.type)
            if v.type in types:
                if v.type in res.keys():
                    res[v.type] += 1
                else:
                    res[v.type] = 1
        return dict(sorted(res.items(), key=lambda t: t[1], reverse=True))

    # Count by Province: Generating set of provinces and counting the count of each data province and storing it in a dict
    # with key=province and value=count
    def count_by_province(self):
        provinces = set()
        res = {}
        for _, v in self.entries.items():
            provinces.add(v.province)
            if v.province in provinces:
                if v.province in res.keys():
                    res[v.province] += 1
                else:
                    res[v.province] = 1
        return dict(sorted(res.items(), key=lambda t: t[1], reverse=True))