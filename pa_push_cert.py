import requests, sys, os
name = sys.argv[1]
ts = time.time()
certname = str(name)

passphrase = "your incredibly secure password"

api_key="your palo alto firewall api key"

pa_host="yourfirewall.yourorg.local"

api_uri="https://" + pa_host + "/api/?type=import&category=keypair&format=pkcs12&certificate_name=" + certname + "&passphrase=" + passphrase + "&key=" + api_key

command="openssl pkcs12 -export -out le_export.pkcs12 -inkey privkey.pem -in cert.pem -certfile chain.pem -passout pass:" + passphrase
os.system(command)

files = {'file': ('lets_encrypt_certificate.pkcs12', open('le_export.pkcs12', 'rb') , 'application/x-pkcs12')}
response = requests.post(api_uri, files=files ,verify=False)
print(response.text)
