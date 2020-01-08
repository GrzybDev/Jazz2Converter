from src.DataClasses.Anims.Mappings import Entry

class AnimSetMapping(object):

    def __init__(self, type):
        self.map = []

    def Get(self, set, anim):
        pass

    def __Add(self, category, name, palette="Std.Palette", skipNormalMap=False, addBorder=0, allowRealtimePalette=False):
        entry = Entry()

        entry.AddBorder = addBorder
        entry.AllowRealtimePalette = allowRealtimePalette
        entry.Category = category
        entry.Name = name
        entry.Palette = palette
        entry.SkipNormalMap = skipNormalMap

        self.tempSet.append(entry)

    def __NextSet(self):
        self.map.append(self.tempSet)
        self.tempSet = []

    def Get(self, setID, animID):
        try:
            return self.map[setID][animID]
        except IndexError:
            entry = Entry()
            entry.Category = "Unidentified"
            entry.Name = str(setID) + "_" + str(animID)
            return entry


animMapping = AnimSetMapping("anim")
sampleMapping = AnimSetMapping("sample")
