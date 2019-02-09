from lazy_property import LazyPropertyMixin
from processing import compute_complicated_analysis
from metadata_api import MetadataApi
from data_api import DataApi


class DataClass(LazyPropertyMixin):

    def __init__(self, ophys_experiment_id, data_api, metadata_api):

        self.ophys_experiment_id = ophys_experiment_id
        self.data_api = data_api
        self.metadata_api = metadata_api

        self.ophys_container_id = self.LazyProperty(self.metadata_api.get_ophys_container_id, ophys_experiment_id=ophys_experiment_id)
        self.x = self.LazyProperty(self.data_api.get_x, ophys_experiment_id=self.ophys_experiment_id)
        self.y = self.LazyProperty(self.data_api.get_y, ophys_container_id=self.ophys_container_id)


class AnalysisClass(LazyPropertyMixin):

    def __init__(self, data_object):

        self.data_object = data_object
        self.ophys_experiment_id = self.data_object.ophys_experiment_id

        self.complicated_analysis = self.LazyProperty(self.get_complicated_analysis)

    def get_complicated_analysis(self):
        return compute_complicated_analysis(self.data_object.x, self.data_object.y)


if __name__ == "__main__":

    ophys_experiment_id = 222222
    metadata_api = MetadataApi()
    data_api = DataApi()

    data_object = DataClass(ophys_experiment_id, data_api, metadata_api)
    analysis_object = AnalysisClass(data_object)

    print(analysis_object.complicated_analysis)