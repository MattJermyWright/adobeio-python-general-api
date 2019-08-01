# Adobe.io API Integration in Python  

I'd like to say that Adobe.io API's are well documented and thorough enough so that any capable developer could easily implement the API without too much difficulty.  Regretably, that's not the case.  So this public repository is my half-hearted attempt to fill in the gaps as of 31 Jul 2019.

## Dependencies & Setup: 
- Python 3.7.1 or greater. It might work on other versions, but this is what I'm using
- Python [Requests](http://docs.python-requests.org/en/master/) library
- [JSON Web Token support](https://pypi.org/project/jwt/)
- [loguru](https://github.com/Delgan/loguru), modified with environment variables as needed.

## APIs tested with this library:
- GDPR Adobe.io API
- Adobe Launch API

## Steps to Take
### Step 1: Assume this will be a hard process
- While Adobe does demonstrate a solid 'API-first' culture, that doesn't mean their APIs are either complete or easy-to-use.  Make sure you've carved out enough time, have adequate access to Adobe Support, and good direction from whoever is asking you to do this.
### Step 2: Setup your Integration at Adobe.io
- This part can easily take multiple days, so make sure you have an Experience Cloud Admin handy to help you out with permissions.
#### As of 19 Feb 2019:
  - You must have Experience Cloud Admin Access.   I can't get any GDPR API settings to show up in the Adobe.IO integraiton site without this.
  - You must have Adobe Analytics Product Admin Access.  Again, without this, you won't see the GDPR option show up
  - There seems to be some known latency from the time you are given rights to the time that it shows up.  Give it 'overnight' for all the permissions to ferment and replicate.  Make sure you logout / log-back-into the experience cloud on Adobe.io to verify.
- Once you have access to setup an integration, you'll need to generate certificates.  To save you hunting that command down, use something like this:
```sh
# Generate the public / private key certs
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout test-gdpr-priv.pem -out test-gdpr-pub.crt
# In case you want to verify the JWT payload at all, you'll need
# the public key accessible in a readible format
openssl x509 -in test-gdpr-pub.crt -pubkey -noout > test-gdpr-pub.pem
```
### Step 4: Install the Package:
```sh
pip install py_adobeio_api
```

### Step 5: Create a config JSON file
You should use the config-example.json as a template and name it something unique.  Fill out the correct information as required.  Make sure to reference the correct location of the API Secret key file you created earlier.

### Step 6: Test it out
**Simple GET request:**
```python
from py_adobeio_api import *

loaded_config_file = load_config_file("config.json")
rest_api = AdobeIORestAPI(loaded_config_file)

# See https://developer.adobelaunch.com/api/reference/1.0/companies/list/ on details of response
response = rest_api.rest_get("https://reactor.adobe.io/companies")
```

**POST Request:**
```python
company_id = "COf9abab66787b45f699ae63921687xxxx" # Make sure to use a real company ID
# See https://developer.adobelaunch.com/api/reference/1.0/properties/create/ on details of how to create a property
# Data
create_payload = {
  "data": {
    "attributes": {
      "name": "Kessel Example Property",
      "domains": [
        "example.com"
      ],
      "platform": "web"
    },
    "type": "properties"
  }
}
response = rest_api.rest_post(f"https://reactor.adobe.io/companies/{company_id}/properties", create_payload)
```