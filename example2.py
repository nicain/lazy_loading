from lazy_property import LazyPropertyMixin
from processing import compute_complicated_analysis
from metadata_api import MetadataApi
from data_api import DataApi

import json

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
        self.complicated_analysis = self.LazyProperty(self.data_object.get_complicated_analysis)

    @staticmethod
    def get_complicated_analysis(data_object):
        return compute_complicated_analysis(data_object.x, data_object.y)

class MarshallAnalysisClass(object):

    def __init__(self, save_file_name):
        self.save_file_name = save_file_name

    def save(self, analysis_object):

        with open(self.save_file_name, 'w') as f:
            json.dump(
                {'complicated_analysis': analysis_object.complicated_analysis}, f)

    def get_complicated_analysis(self, *args, **kwargs):
        return json.load(open(self.save_file_name, 'r'))['complicated_analysis']

    

if __name__ == "__main__":

    ophys_experiment_id = 222222
    metadata_api = MetadataApi()
    data_api = DataApi()

    data_object = DataClass(ophys_experiment_id, data_api, metadata_api)
    analysis_object = AnalysisClass(data_object)

    m = MarshallAnalysisClass('analysis_object.json')
    m.save(analysis_object)

    print(AnalysisClass(m).complicated_analysis == analysis_object.complicated_analysis)
