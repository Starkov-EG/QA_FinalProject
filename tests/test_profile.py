import json
import allure

@allure.title("Тест получения информации о текущем профиле")
def test_account(dropbox_client_api):
    response = dropbox_client_api.post(path_type="account")
    print((response.text,))
    assert json.loads(response.text)["name"]["surname"] == "Starkov"


@allure.title("Тест проверки свободного места")
def test_space(dropbox_client_api):
    response = dropbox_client_api.post(path_type="space")
    print((response.text,))
    used = int(json.loads(response.text)["used"])
    allocated = int(json.loads(response.text)["allocation"]["allocated"])
    assert float(used/allocated) < 0.5