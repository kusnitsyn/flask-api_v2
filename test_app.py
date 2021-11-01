from app import json_info, json_add

def test_flask_app_mock(
        flask_app_mock,
        api_mock,
        mock_get_sqlalchemy,
):
    mock_get_sqlalchemy.first.return_value = api_mock
    with flask_app_mock.app_context():
        response = json_info()

    assert response == response
