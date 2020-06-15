#allure serve allure-results
import pytest
import json
import os.path
import allure


@allure.title("Загрузка файла")
def test1_upload_file(dropbox_client_content):
    file = dropbox_client_content.file
    headers = {'Content-Type': 'application/octet-stream',
               'Content-Disposition': 'attachment',
               'Dropbox-API-Arg': '{"path": "' + file + '", "mode": "overwrite", "autorename": true, "mute": true, "strict_conflict": false}'}
    files = open(".{}".format(file), 'rb')
    response = dropbox_client_content.post(path_type="upload", data=files, add_headers=headers)
    print(response.text)
    assert json.loads(response.text)["path_display"] == file


@allure.title("Скачивание файла")
def test_download(dropbox_client_content):
    download_path = './Downloads/'+dropbox_client_content.file.split("/")[2]
    headers = {'Content-Type': 'application/octet-stream',
               'Dropbox-API-Arg': '{"path": "' + dropbox_client_content.file + '"}'}
    answ = dropbox_client_content.post(path_type="download", add_headers=headers)
    file = open(download_path, 'w')
    file.write(answ.text)
    print((answ.text,))
    assert os.path.isfile(download_path)


@allure.title("Переименование файла")
def test_move(dropbox_client_api):
    headers = {'Content-Type': 'application/json'}
    data = {"from_path": dropbox_client_api.file, "to_path": dropbox_client_api.file_new_name}
    response = dropbox_client_api.post(path_type="move", add_headers=headers, data=json.dumps(data))
    print((response.text,))
    assert json.loads(response.text)["metadata"]["path_display"] == dropbox_client_api.file_new_name


@allure.title("Получение ссылки на файл")
def test_get_link(dropbox_client_api):
    headers = {'Content-Type': 'application/json'}
    data = {
        "path": dropbox_client_api.file_new_name,
    }
    response = dropbox_client_api.post(path_type="get_link", add_headers=headers, data=json.dumps(data))
    print((response.text,))
    assert json.loads(response.text)["link"].find("https://") != -1


@allure.title("Получение списка файлов в папке")
def test_list(dropbox_client_api):
    headers = {'Content-Type': 'application/json'}
    data = {
        "path": "/" + dropbox_client_api.file.split("/")[1],
        "recursive": False,
        "include_media_info": False,
        "include_deleted": False,
        "include_has_explicit_shared_members": False,
        "include_mounted_folders": True,
        "include_non_downloadable_files": True
    }
    response = dropbox_client_api.post(path_type="list", add_headers=headers, data=json.dumps(data))
    print((response.text,))
    new_file_in_list = False
    for list_entries in json.loads(response.text)["entries"]:
        if list_entries["path_display"] == dropbox_client_api.file_new_name:
            new_file_in_list = True
    assert new_file_in_list


@allure.title("Поиск файлов")
def test_search(dropbox_client_api):
    headers = {'Content-Type': 'application/json'}
    data = {
        "query": dropbox_client_api.file_new_name.split("/")[2],
        "include_highlights": False
    }
    response = dropbox_client_api.post(path_type="search", add_headers=headers, data=json.dumps(data))
    print((response.text,))
    file_is_found = False
    for match in json.loads(response.text)["matches"]:
        if match["metadata"]["metadata"]["path_display"] == dropbox_client_api.file_new_name:
            file_is_found = True
    assert file_is_found


@allure.title("Получение metadata файла")
def test_metadata(dropbox_client_api):
    headers = {'Content-Type': 'application/json'}
    data = {
        "path": dropbox_client_api.file_new_name,
        "include_media_info": False,
        "include_deleted": False,
        "include_has_explicit_shared_members": False
    }
    response = dropbox_client_api.post(path_type="metadata", add_headers=headers, data=json.dumps(data))
    print((response.text,))
    assert type(json.loads(response.text)["size"]) == int


@allure.title("Удаление файла")
def test_delete(dropbox_client_api):
    headers = {'Content-Type': 'application/json'}
    data = {
        "path": dropbox_client_api.file_new_name
    }
    response = dropbox_client_api.post(path_type="delete", add_headers=headers, data=json.dumps(data))
    print((response.text,))
    assert json.loads(response.text)["metadata"]["path_display"] == dropbox_client_api.file_new_name