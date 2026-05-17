import os

from dotenv import load_dotenv

from twilio.rest import Client


# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()


# =========================
# ENV VARIABLES
# =========================

ACCOUNT_SID = os.getenv(
    "TWILIO_ACCOUNT_SID"
)

AUTH_TOKEN = os.getenv(
    "TWILIO_AUTH_TOKEN"
)

TWILIO_WHATSAPP_NUMBER = os.getenv(
    "TWILIO_WHATSAPP_NUMBER"
)

YOUR_WHATSAPP_NUMBER = os.getenv(
    "YOUR_WHATSAPP_NUMBER"
)


# =========================
# TWILIO CLIENT
# =========================

client = Client(
    ACCOUNT_SID,
    AUTH_TOKEN
)


# =========================
# SEND ALERT
# =========================

def send_whatsapp_alert(message):

    response = client.messages.create(

        body=message,

        from_=TWILIO_WHATSAPP_NUMBER,

        to=YOUR_WHATSAPP_NUMBER
    )

    print(
        "\nTwilio SID:"
    )

    print(response.sid)