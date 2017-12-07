import os

from flask import Flask
app = Flask(__name__)

from azure.keyvault import KeyVaultClient
from msrestazure.azure_active_directory import MSIAuthentication, ServicePrincipalCredentials

KEY_VAULT_URI = None # Replace by something like "https://xxxxxxxxx.vault.azure.net/"

def get_key_vault_credentials():
    """This tries to get a token using MSI, or fallback to SP env variables.
    """
    if "APPSETTING_WEBSITE_SITE_NAME" in os.environ:
        return MSIAuthentication(
            resource='https://vault.azure.net'
        )
    else:
        return ServicePrincipalCredentials(
            client_id=os.environ['AZURE_CLIENT_ID'],
            secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant=os.environ['AZURE_TENANT_ID']
        )

def run_example():
    """MSI Authentication example."""

    # Get credentials
    credentials = get_key_vault_credentials()

    # Create a KeyVault client
    key_vault_client = KeyVaultClient(
        credentials
    )

    key_vault_uri = os.environ.get("KEY_VAULT_URI", KEY_VAULT_URI)

    secret = key_vault_client.get_secret(
        key_vault_uri,  # Your KeyVault URL
        "secret",       # Name of your secret. If you followed the README 'secret' should exists
        ""              # The version of the secret. Empty string for latest
    )
    print("My secret value: {}".format(secret.value))
    print("Expires: {}".format(secret.attributes.expires))


@app.route('/')
def hello_world():
    # Get credentials
    credentials = get_key_vault_credentials()

    # Create a KeyVault client
    key_vault_client = KeyVaultClient(
        credentials
    )

    key_vault_uri = os.environ.get("KEY_VAULT_URI", KEY_VAULT_URI)

    secret = key_vault_client.get_secret(
        key_vault_uri,  # Your KeyVault URL
        "secret",       # Name of your secret. If you followed the README 'secret' should exists
        ""              # The version of the secret. Empty string for latest
    )
    return "My secret value is {}".format(secret.value)

if __name__ == '__main__':
  app.run()
