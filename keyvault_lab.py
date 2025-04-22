from dotenv import load_dotenv
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

def main():
    global ai_endpoint
    global cog_key
    
    try:

        load_dotenv()
        ai_endpoint=os.getenv('AI_END_POINT')
        #keyvault_name=os.getenv('KEYVAULT_NAME')
        sp_app_id=os.getenv('APP_ID')
        sp_app_passwrd=os.getenv('APP_PASSWD')
        tenant_id=os.getenv('TENANT_ID')
        keyvault_url=os.getenv('KEYVAULT_URL')

        credential=ClientSecretCredential(tenant_id,sp_app_id,sp_app_passwrd)

        keyvault_credential=SecretClient(keyvault_url,credential)

        cog_key=keyvault_credential.get_secret('Azure-Service-key').value

        Usertxt=''
        while Usertxt.lower() != 'quit':
            Usertxt = input('\nPlease enter your input(quit to stop):\n')
            if Usertxt.lower() != 'quit':
                Language=getLanguage(Usertxt)
                print('Language is ',Language)
    
    except Exception as ex:
        print(ex)


def getLanguage(text):

    Ai_credential=AzureKeyCredential(cog_key)

    client_id = TextAnalyticsClient(ai_endpoint,Ai_credential)

    result = client_id.detect_language(documents=[text])[0]

    return result.primary_language.name

if __name__ == "__main__":
    main()
