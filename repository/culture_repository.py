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
            try:
                self.entries[request.name]
                raise Exception("culture already exists:", request.name)
            except KeyError:
                self.entries[request.name] = request

    # Find All: Returning all cultures in storage
    def find_all(self):
        if len(self.entries) == 0:
            return None
        return (self.entries.values())

    # Count All: Returning count of all cultures
    def count_all(self):
        res = len(self.entries)
        return res

    # Search: accepting search keyword and field as QueryType enum type
    # Keyword will be handled based on its QueryType
    def search(self, keyword, field):
        if field == QueryType.NAME: # Search by Name
            try:
                res = self.entries[keyword]
                return res
            except ValueError:
                return None

        elif field == QueryType.TYPE: # Search by Type
            res = []
            for _, v in self.entries.items():
                if v.type == keyword:
                    res.append(str(v))
            return res, len(res)

        elif field == QueryType.PROVINCE: # Search by Province
            res = []
            for _, v in self.entries.items():
                if v.province == keyword:
                    res.append(str(v))
            return res, len(res)

    # Delete: delete data from storage by name index
    def delete(self, name):
        try:
            del self.entries[name]
        except ValueError:
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