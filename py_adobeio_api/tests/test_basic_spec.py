from libs.adobe_rest import load_config_file, AdobeIORestAPI

def test_config_loader():
    loaded_file = load_config_file("config.json")
    assert "launch" in loaded_file

def test_company_listing():
    loaded_config_file = load_config_file("config.json")
    rest_api = AdobeIORestAPI(loaded_config_file)
    response = rest_api.rest_get("https://reactor.adobe.io/companies")
    assert "data" in response
    assert len(response["data"])>0