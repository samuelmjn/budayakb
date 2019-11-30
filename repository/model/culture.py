class Culture:
    def __init__(self, name, obj_type, province, url):
        self.name = name
        self.type = obj_type
        self.province = province
        self.url = url

    def __str__(self):
        return str(self.name+","+self.type+","+self.province+","+self.url)