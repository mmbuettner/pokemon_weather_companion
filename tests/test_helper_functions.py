from src.helper_functions import api_request, compare_dataframes

from unittest.mock import patch
import json


@patch('src.helper_functions.requests.get')
def test_api_request(mock_get):
    mock_response = {'key1': 'value1', 'key2': 'value2'}
    mock_get.return_value.text = json.dumps(mock_response)

    result = api_request('https://example.com/api')
    assert result == mock_response
    mock_get.assert_called_once_with('https://example.com/api')


def test_compare_dataframes():
    test_db_list = [{'key1': 'value1'}, {'key2': 'value2'}]
    test_api_list = [{'key1': 'value1'}, {'key3': 'value3'}]
    mock_response = [{'key3': 'value3'}]
    empty_mock_response = []
    result = compare_dataframes(test_db_list, test_api_list)
    assert result == mock_response
    assert not result == empty_mock_response
