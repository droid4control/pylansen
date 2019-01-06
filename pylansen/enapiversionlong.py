from .enapicommandwithsvn import ENAPICommandWithSvn

class ENAPIVersionLong(ENAPICommandWithSvn):
    MIN_FARME_LEN = 9
    MAX_FARME_LEN = 9

    def __init__(self, data):
        super().__init__(data)
        self.Version = int(self.data[2])
        self.Major = int(self.data[3])
        self.Minor = int(self.data[4])

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, value):
        self._Version = value

    @property
    def Major(self):
        return self._Major

    @Major.setter
    def Major(self, value):
        self._Major = value

    @property
    def Minor(self):
        return self._Minor

    @Minor.setter
    def Minor(self, value):
        self._Minor = value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
