import pytest
import requests


def pytest_addoption(parser):
    parser.addoption("--file", action="store", default="/Uploads/file_to_upload.txt", help="test file")
    parser.addoption("--file_new_name", action="store", default="/Uploads/file_new_name.txt", help="new name for test file")
    parser.addoption("--token", action="store", default="Bearer 6mzdgnl7_rAAAAAAAAAAF6bc4_pdzqj23vsifPH5xehqjtFt8cNfWN-5Wq_sM5t7", help="token")


@pytest.fixture(scope="session")
def dropbox_client_content(request):
    file = request.config.getoption("--file")
    token = request.config.getoption("--token")
    url = "https://content.dropboxapi.com"
    return DropBox(url, token, file)

@pytest.fixture(scope="session")
def dropbox_client_api(request):
    file = request.config.getoption("--file")
    file_new_name = request.config.getoption("--file_new_name")
    token = request.config.getoption("--token")
    url = "https://api.dropboxapi.com"
    return DropBox(url, token, file, file_new_name)


class DropBox:
    """
    Упрощенный клиент для работы с API
    Инициализируется базовым url на который пойдут запросы
    """
    paths = {
        "/": "/",
        "upload": "/2/files/upload",
        "download": "/2/files/download",
        "move": "/2/files/move_v2",
        "get_link": "/2/files/get_temporary_link",
        "list": "/2/files/list_folder",
        "search": "/2/files/search_v2",
        "metadata": "/2/files/get_metadata",
        "delete": "/2/files/delete_v2",
        "account": "/2/users/get_current_account",
        "space": "/2/users/get_space_usage"
    }

    def __init__(self, url, token, file=None, file_new_name=None):
        self.file = file
        self.token = token
        self.base_url = url
        self.file_new_name = file_new_name

    def post(self, path_type="/", params=None, data=None, add_headers={}):
        url = self.base_url + self.paths[path_type]
        auth_headers = {'Authorization': self.token}
        headers = {**auth_headers, **add_headers}
        print("POST request to {}".format(url))
        print(headers)
        return requests.post(url=url, params=params, data=data, headers=headers)

    def get(self, path="/", params=None):
        url = self.base_address + path
        print("GET request to {}".format(url))
        return requests.get(url=url, params=params)

    def get_status(self):
        return self.status