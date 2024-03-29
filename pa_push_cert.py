import requests, sys, os, syslog

#name of the certificate on the firewall. usually taken from file name of LE certificate.
name = sys.argv[1]
certname = str(name)

#todo: generate random password
passphrase = "your incredibly secure password"

# instructions to creat an api key https://docs.paloaltonetworks.com/pan-os/7-1/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/get-your-api-key.html
api_key="your palo alto firewall api key"

# the ip address or url to your pa firewall
pa_host="yourfirewall.yourorg.local"

#API URI to upload your ssl certificates to
api_uri="https://" + pa_host + "/api/?type=import&category=keypair&format=pkcs12&certificate_name=" + certname + "&passphrase=" + passphrase + "&key=" + api_key

#todo: use native python openssl libraries
command="openssl pkcs12 -export -out le_export.pkcs12 -inkey privkey.pem -in cert.pem -certfile chain.pem -passout pass:" + passphrase
os.system(command)

#configure the file object to send the paloalto with the generated pkcs12 archive.
#todo: use proper tempfile
files = {'file': ('lets_encrypt_certificate.pkcs12', open('le_export.pkcs12', 'rb') , 'application/x-pkcs12')}

#execute the api call
response = requests.post(api_uri, files=files ,verify=False)
#read http code and return an exit code back to the os to make it more script friendly.
if response.status_code == 200:
    print('Certificate Load: Success')
    syslog.syslog("Certificate Load: "+ name + "Success")
    commit_api_uri="https://" + pa_host + "/api/?type=commit&key=" + api_key + "&cmd=<commit></commit>"
    #execute the api commit call
    response = requests.get(commit_api_uri ,verify=False)
    #todo: read http code and return an exit code back to the os to make it more script friendly.
    if response.status_code == 200:
        print('PA Commit: Success')
        syslog.syslog('PA Commit('+ name +'): Success')
        exit(0)
    elif response.status_code == 404:
        print('PA Commit('+ name +'): Failed')
        syslog.syslog('PA Commit: Failure')
        exit(2)
elif response.status_code == 404:
    print('Certificate Load: Failed')
    syslog.syslog("Certificate Load: "+ name + "Failed")
    exit(1)
