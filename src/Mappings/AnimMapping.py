from src.DataClasses.Anims.Mappings import Entry

class AnimSetMapping(object):

    def __init__(self, type):
        self.map = []

    def Get(self, set, anim):
        try:
            return self.map[set][anim]
        except IndexError:
            return Entry()


animMapping = AnimSetMapping("anim")
sampleMapping = AnimSetMapping("sample")
