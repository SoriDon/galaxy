import textwrap

from galaxy_test.base.populators import (
    DatasetCollectionPopulator,
    DatasetPopulator,
)
from ._framework import ApiTestCase


class DatasetsApiTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        self.dataset_populator = DatasetPopulator(self.galaxy_interactor)
        self.dataset_collection_populator = DatasetCollectionPopulator(self.galaxy_interactor)
        self.history_id = self.dataset_populator.new_history()

    def test_index(self):
        index_response = self._get("datasets")
        self._assert_status_code_is(index_response, 200)

    def test_search_datasets(self):
        hda_id = self.dataset_populator.new_dataset(self.history_id)['id']
        payload = {'limit': 1, 'offset': 0}
        index_response = self._get("datasets", payload).json()
        assert len(index_response) == 1
        assert index_response[0]['id'] == hda_id
        hdca_id = self.dataset_collection_populator.create_list_in_history(self.history_id,
                                                                           contents=["1\n2\n3"]).json()['id']
        payload = {'limit': 3, 'offset': 0}
        index_response = self._get("datasets", payload).json()
        assert len(index_response) == 3
        assert index_response[0]['id'] == hdca_id
        assert index_response[0]['history_content_type'] == 'dataset_collection'
        assert index_response[2]['id'] == hda_id
        assert index_response[2]['history_content_type'] == 'dataset'
        payload = {'limit': 2, 'offset': 0, 'q': ['history_content_type'], 'qv': ['dataset']}
        index_response = self._get("datasets", payload).json()
        assert index_response[1]['id'] == hda_id

    def test_search_by_tag(self):
        hda_id = self.dataset_populator.new_dataset(self.history_id)['id']
        update_payload = {
            'tags': ['cool:new_tag', 'cool:another_tag'],
        }
        updated_hda = self._put(
            "histories/{history_id}/contents/{hda_id}".format(history_id=self.history_id, hda_id=hda_id),
            update_payload).json()
        assert 'cool:new_tag' in updated_hda['tags']
        assert 'cool:another_tag' in updated_hda['tags']
        payload = {'limit': 10, 'offset': 0, 'q': ['history_content_type', 'tag'], 'qv': ['dataset', 'cool:new_tag']}
        index_response = self._get("datasets", payload).json()
        assert len(index_response) == 1
        payload = {'limit': 10, 'offset': 0, 'q': ['history_content_type', 'tag-contains'],
                   'qv': ['dataset', 'new_tag']}
        index_response = self._get("datasets", payload).json()
        assert len(index_response) == 1
        payload = {'limit': 10, 'offset': 0, 'q': ['history_content_type', 'tag-contains'], 'qv': ['dataset', 'notag']}
        index_response = self._get("datasets", payload).json()
        assert len(index_response) == 0

    def test_search_by_tool_id(self):
        self.dataset_populator.new_dataset(self.history_id)
        payload = {'limit': 1, 'offset': 0, 'q': ['history_content_type', 'tool_id'], 'qv': ['dataset', 'upload1']}
        assert len(self._get("datasets", payload).json()) == 1
        payload = {'limit': 1, 'offset': 0, 'q': ['history_content_type', 'tool_id'], 'qv': ['dataset', 'uploadX']}
        assert len(self._get("datasets", payload).json()) == 0
        payload = {'limit': 1, 'offset': 0, 'q': ['history_content_type', 'tool_id-contains'], 'qv': ['dataset', 'pload1']}
        assert len(self._get("datasets", payload).json()) == 1
        self.dataset_collection_populator.create_list_in_history(self.history_id,
                                                                 name="search by tool id",
                                                                 contents=["1\n2\n3"]).json()
        self.dataset_populator.wait_for_history(self.history_id)
        payload = {'limit': 10, 'offset': 0, 'history_id': self.history_id, 'q': ['name', 'tool_id'],
                   'qv': ['search by tool id', 'upload1']}
        result = self._get("datasets", payload).json()
        assert result[0]['name'] == 'search by tool id', result
        payload = {'limit': 1, 'offset': 0, 'q': ['history_content_type', 'tool_id'],
                   'qv': ['dataset_collection', 'uploadX']}
        result = self._get("datasets", payload).json()
        assert len(result) == 0

    def test_invalid_search(self):
        payload = {'limit': 10, 'offset': 0, 'q': ['history_content_type', 'tag-invalid_op'], 'qv': ['dataset', 'notag']}
        index_response = self._get("datasets", payload)
        self._assert_status_code_is(index_response, 400)
        assert index_response.json()['err_msg'] == 'bad op in filter'

    def test_search_returns_only_accessible(self):
        hda_id = self.dataset_populator.new_dataset(self.history_id)['id']
        with self._different_user():
            payload = {'limit': 10, 'offset': 0, 'q': ['history_content_type'], 'qv': ['dataset']}
            index_response = self._get("datasets", payload).json()
            for item in index_response:
                assert hda_id != item['id']

    def test_show(self):
        hda1 = self.dataset_populator.new_dataset(self.history_id)
        show_response = self._get("datasets/%s" % (hda1["id"]))
        self._assert_status_code_is(show_response, 200)
        self.__assert_matches_hda(hda1, show_response.json())

    def __assert_matches_hda(self, input_hda, query_hda):
        self._assert_has_keys(query_hda, "id", "name")
        assert input_hda["name"] == query_hda["name"]
        assert input_hda["id"] == query_hda["id"]

    def test_display(self):
        contents = textwrap.dedent("""\
        1   2   3   4
        A   B   C   D
        10  20  30  40
        """)
        hda1 = self.dataset_populator.new_dataset(self.history_id, content=contents)
        self.dataset_populator.wait_for_history(self.history_id)
        display_response = self._get("histories/{}/contents/{}/display".format(self.history_id, hda1["id"]), {
            'raw': 'True'
        })
        self._assert_status_code_is(display_response, 200)
        assert display_response.text == contents

    def test_tag_change(self):
        hda_id = self.dataset_populator.new_dataset(self.history_id)['id']
        payload = {
            'item_id': hda_id,
            'item_class': 'HistoryDatasetAssociation',
            'item_tags': ['cool:tag_a', 'cool:tag_b', 'tag_c', 'name:tag_d', '#tag_e'],
        }
        self._put("tags", payload).json()
        updated_hda = self._get(
            "histories/{history_id}/contents/{hda_id}".format(history_id=self.history_id, hda_id=hda_id)).json()
        assert 'cool:tag_a' in updated_hda['tags']
        assert 'cool:tag_b' in updated_hda['tags']
        assert 'tag_c' in updated_hda['tags']
        assert 'name:tag_d' in updated_hda['tags']
        assert 'name:tag_e' in updated_hda['tags']

    def test_update_datatype(self):
        hda_id = self.dataset_populator.new_dataset(self.history_id)['id']
        original_hda = self._get(
            "histories/{history_id}/contents/{hda_id}".format(history_id=self.history_id, hda_id=hda_id)).json()
        assert original_hda['extension'] == 'txt'
        assert original_hda['data_type'] == 'galaxy.datatypes.data.Text'
        assert 'scatterplot' not in [viz['name'] for viz in original_hda['visualizations']]

        update_while_incomplete_response = self._put(  # try updating datatype before upload is complete
            "histories/{history_id}/contents/{hda_id}".format(history_id=self.history_id, hda_id=hda_id),
            {'datatype': 'tabular'})
        self._assert_status_code_is(update_while_incomplete_response, 500)

        self.dataset_populator.wait_for_history(self.history_id)  # now wait for upload to complete

        successful_updated_hda_response = self._put(
            "histories/{history_id}/contents/{hda_id}".format(history_id=self.history_id, hda_id=hda_id),
            {'datatype': 'tabular'}).json()
        assert successful_updated_hda_response['extension'] == 'tabular'
        assert successful_updated_hda_response['data_type'] == 'galaxy.datatypes.tabular.Tabular'
        assert 'scatterplot' in [viz['name'] for viz in successful_updated_hda_response['visualizations']]

        invalidly_updated_hda_response = self._put(  # try updating with invalid datatype
            "histories/{history_id}/contents/{hda_id}".format(history_id=self.history_id, hda_id=hda_id),
            {'datatype': 'invalid'})
        self._assert_status_code_is(invalidly_updated_hda_response, 400)
