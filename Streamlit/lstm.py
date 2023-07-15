import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import os

def Lstm():
    # Título de la página de inicio
    st.title('TerraSafe - LSTM')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Streamlit/terra-safe-391718-99ac35bdf8d1.json'

    # # Load the client credentials
    # credentials = service_account.Credentials.from_service_account_info(
    #     {
    #         "client_id": "757021101808-9u6bl68jqhc7f4s7o63o3sa1e9cof40n.apps.googleusercontent.com",
    #         "client_secret": "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",
    #         "project_id": "terra-safe-391718",
    #         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #         "token_uri": "https://oauth2.googleapis.com/token",
    #         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #         "client_email": "santiagomartearena6@gmail.com",
    #         "type": "service_account",
    #         "project_id": "terra-safe-391718",
    #         "private_key_id": "99ac35bdf8d13cb1a8a54fb6d317f39415ba31f6",
    #         "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDhTo8dNuH0HEDU\nhtg+DVGgI3GPX8kCZX+riA9ruL4I88u18KDleDDIh6V64c6iwRo1awjSPIsevDPP\nzcu1sjE2LYVz4IspCnxPmop/smvnRk/2KO+iatPK/FTlHCPxQQJBq4sMIHikXl+T\n05bibA384vFep+m1BODBGYMYf5fM8HgyiSRCGd78MXGGxpcW53e1PP1ovRYNfMgD\n2WDUZPz3R8iHl/WmYvkvvxO5jHMwU4vpQOvxFN3wLhkmqNGQX9Ov2s0eamsjA5/K\nwCM/y2UOKCGE96AhPxvvd41s9lartRELfYaqowaIVqKm4Ip0ltFHKXMiO5yqXzqZ\nnDzev6TlAgMBAAECggEAAtzKLgFe/4A8EaeuZ8yTz2f8IXHp2a710uj+ihB7Zh1d\nA5moPkvnHj8pQo4y7+xhx2zVAZ3gK1DolA79CpW9acU7vLwqDRgHkxfI2f/dSuzv\nMqc/z+S3p5Ti4/DLwyMuF15u8FgyXRbyscCSpJNdrIQaUMfa7fXwqaTvH39Y6Z6K\nEoh4zy7o5EggT409twq/qRLRZ9sZdRQ4iTrIR455F5Gdnlk7tiGDgKZeRoS6fukJ\nyAjsi7tdLBKFt8oGQ1ze2fWyFqKWalmtfOzzngXHHj4jVg0gtTvNwhvLpomLcorJ\nCEXxntnGdqFGZvSUxOBM+O/xbMJMUCkJjpSllw8+lwKBgQDw7VzWtzpX2TzmN9Aw\nQYdn6Gzj0gHkP6Mszy+Hm1cjMp4knugrY1CeStcscUv9oAKhbCba4WodF1ZdWeIA\ni6RcGdNV4uWv2XmEpRtGRf2qd1VbMS5SX3NG0UA+GRax/Ljxyd4r/ldznroxlnMp\ngE5x0BycxrV7tvuV4RFG1HkprwKBgQDvZwZPheQzdqXzJ8PpQNVt5xjwi0OuCtiK\nF6tX5XJRzbVhVH82euQICboKXhNEp598xwW+mWHYbAlN1392+jKpNrJ6W++khQYv\noXwNVE2wJieeitPqa7GmvQb/qaJxkujff/wSNdxqNU1GlrK4pJv9MXOL6PJJrBWu\nIa0SRJhDqwKBgQDndvOxqXkY+zGB8G9IXTxsvKUYvyNoGSd4nliIjNpLi47Zmf1t\n6c2DNl3BadvbAAZm9VPjB5t99XTY3Mi/Q2mVvo4GPqXyqxoPMNyiSA3r3xgXM4nQ\nQ7mpeNGil1Hxj95TFWEonQOBpiY2C9f6MDWtLIbArDuhbuwIU6HYjbsWKwKBgQDr\nwb5SM92N3KsCMMfafZFxIKLLx6mHzICARVzkOz2AV57mUYrRgOXtEH8YVJqPAq+p\n9miu0Wes9H+ZG74X0b5wK0BKBR2TG7kC0PlUOxAihwB/PeIBObsCI6avwUMKq40P\nBH+dA1OjeAg4mpE4CkrfZYKPZoCrkn7rM5i3o7t67wKBgQCOnskA1ayUhg9bi84y\n5kbx0BAAXcI23zJoBPOw0J2GcNuPafm35wE2RtJOGH/yWb//2N5Lhs+QYVz+T1pe\nA3e2xJm7Ji1K4QcOeblc/lmhw9LgobgBx3FpbdBSajGXMOW63M/F5PMOXcX6VbsR\nJw0ugfbQ/uXBXefKq11ckqNB9w==\n-----END PRIVATE KEY-----\n",
    #         "client_email": "terrasafe@terra-safe-391718.iam.gserviceaccount.com",
    #         "client_id": "106648447302182770524",
    #         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #         "token_uri": "https://oauth2.googleapis.com/token",
    #         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #         "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/terrasafe%40terra-safe-391718.iam.gserviceaccount.com",
    #         "universe_domain": "googleapis.com"
    #     }
    # )

    # Create a BigQuery client with the credentials
    bq_client = bigquery.Client()

    # Query your table
    query = "SELECT * FROM `terra-safe-391718.AIRFLOW.USGS_CHI` LIMIT 100"
    df = bq_client.query(query).to_dataframe()

    # Display the table in Streamlit
    st.dataframe(df)
