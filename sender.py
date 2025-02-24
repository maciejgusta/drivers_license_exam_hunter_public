def run_sender(sender="maciej.gusta@gmail.com", recipient="maciej.gusta@gmail.com", PROVINCE="mazowickie", ORGANIZATION="bemowo", CATEGORY="B", DATETIME=None, TIMEDELTA_DAYS=7, EXAM_TYPE=True):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from datetime import datetime, timedelta
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # AMAZON SES CREDENTIALS LOADED FROM ENV
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    # AMAZON SES SMTP SERVER DETAILS
    SMTP_SERVER = 'email-smtp.eu-central-1.amazonaws.com'
    SMTP_PORT = 587

    # EMAIL FORMATTING (FOR BETTER LOOKS AND READABILITY)
    polish_weekdays = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']

    formatted_datetime = DATETIME.strftime("%d.%m.%Y %H:%M")
    weekday =  polish_weekdays[DATETIME.weekday()]
    subject = f'Nowy termin egzaminu {"praktycznego" if EXAM_TYPE else "teoretycznego"} odpowiadający użytkownikowi'
    body= f'Nowy termin egzaminu {"praktycznego" if EXAM_TYPE else "teoretycznego"} w {ORGANIZATION}, {PROVINCE}: {formatted_datetime} ({weekday})'

    # CHECK IF THE AVAILABLE EXAM IN WITHIN THE TIMERANGE SPECIFIED BY THE USER
    if (abs(datetime.now() - DATETIME) <= timedelta(days=TIMEDELTA_DAYS)):
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # SEND THE EMAIL, TRUE IF SENT SUCCESFULLY, FALSE IF ERROR OR EXAM NOT WITHIN THE TIMERANGE
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(sender, recipient, msg.as_string())

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    return False