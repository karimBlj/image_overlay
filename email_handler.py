import requests
from typing import Dict

class EmailHandler:
    def __init__(
        self,
        sender     : str = "karim.belhadj@sideral.ai",
        account_id : str = "5329961000000002002"
    ) -> None:
        self.sender     = sender
        self.account_id = account_id

    def generate_token(self) -> str:
        print("Go to: https://api-console.zoho.eu/")
        print("Enter the scope: ZohoMail.messages.ALL")
        code = input("Enter generated token : ")
        body = {
            "grant_type" : "authorization_code",
            "code": code,
        }

        response = requests.post("https://accounts.zoho.eu/oauth/v2/token", data = body)
        access_token = response.json()["access_token"]
        self.access_token = access_token
        return access_token
    
    def send_email(
        self,
        to          : str,
        subject     : str,
        content     : str,
        ask_receipt : bool = True,
        ccAddress   : str | None = None,
        bccAddress  : str | None = None,
    ) -> Dict:
        if ccAddress is None:
            ccAddress = ""
        if bccAddress is None:
            bccAddress = ""
        headers = {
            'Accept'        : 'application/json',
            'Content-Type'  : 'application/json',
            'Authorization' : f'Zoho-oauthtoken {self.access_token}',
        }

        json_data = {
            "fromAddress" : self.sender,
            "toAddress"   : to,
            "subject"     : subject,
            "content"     : content,
            "askReceipt"  : "yes" if ask_receipt else "no",
            "ccAddress"   : ccAddress,
            "bccAddress"  : bccAddress,
        }
        
        response = requests.post(f'https://mail.zoho.eu/api/accounts/{self.account_id}/messages', headers=headers, json=json_data)
        print(response.text)
        return response.json()

    

# handler = EmailHandler()
# handler.generate_token()
# handler.send_email("rimukus@gmail.com", "Bonjour", "<h1>Comment t'es un BG</h1>Salut, je fais juste un test. Dis moi si ce mail arrive dans ta boite principale ou bien tes spams. En te remerciant par avance. <img src = 'https://firebasestorage.googleapis.com/v0/b/sideral-a95c0.appspot.com/o/base.jpg?alt=media&token=a8c179a4-cd25-4465-8878-5d3067701c8e'/>Karim")