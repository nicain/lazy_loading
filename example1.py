def Data(LazyMixin):
    def __init__(self, api):
        self.a = self.LazyProperty(api.get_a)
        self.b = self.LazyProperty(api.get_b)


def Analysis(LazyMixin):
    def __init__(self, data, api=None):

        self.api = api if api is not None else self
        self.data = data
        self.c = self.LazyProperty(api.get_c, data)
        self.d = self.LazyProperty(api.get_d, data)

    @staticmethod
    def get_c(data):
        return data.a * 10

    @staticmethod
    def get_d(data):
        return data.b * 100


class ComplicatedAnalyzer:
    def get_c(self, data):
        return MapReduce(data.a * 10)

    def get_d(self, data):
        return MapReduce(data.b * 100)


class AnalysisReaderWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_c(self, data):
        pass

    def get_d(self, data):
        pass

    def write_c(self):
        pass

    def write_d(self):
        pass
