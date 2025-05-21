import os
import smtplib
import ssl
from email.message import EmailMessage
from .config import (
    EMAIL_FROM,
    SMTP_SERVER,
    SMTP_PORT,
    LOGIN_EMAIL,
    LOGIN_PASSWORD
)

def send_email_with_csv(to_emails, file_paths, email_subject, logger, report_summary=None):
    """
    Sends an email with one or more files attached.

    Args:
        to_emails (list or str): Recipients' email addresses.
        file_paths (list): List of file paths to attach.
        email_subject (str): Subject of the email.
        logger (logging.Logger): Logger instance for logging events.
        report_summary (str): Summary content to include in the email body.
    """
    try:
        logger.info("Preparing email with subject: '%s'", email_subject)

        msg = EmailMessage()
        msg["Subject"] = email_subject
        msg["From"] = EMAIL_FROM
        msg["To"] = to_emails if isinstance(to_emails, str) else ', '.join(to_emails)

        # Set the email body content
        body = report_summary if report_summary else "Please find attached the weekly reports."
        msg.set_content(body)

        # Attach each file
        for file_path in file_paths:
            if not os.path.exists(file_path):
                logger.warning("File not found: %s", file_path)
                continue

            with open(file_path, "rb") as file:
                filename = os.path.basename(file_path)
                # Use appropriate MIME type for .xlsx or .csv
                maintype = "application"
                subtype = "vnd.openxmlformats-officedocument.spreadsheetml.sheet" if filename.endswith(".xlsx") else "octet-stream"
                msg.add_attachment(file.read(), maintype=maintype, subtype=subtype, filename=filename)
                logger.info("Attached file: %s", filename)

        # Send the email using SMTP over SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(LOGIN_EMAIL, LOGIN_PASSWORD)
            logger.info("Logged in as: %s", LOGIN_EMAIL)
            server.send_message(msg)

        logger.info("✅ Email sent successfully to: %s", msg['To'])

    except smtplib.SMTPException as error:
        logger.error("❌ Failed to send email. SMTP Error: %s", str(error), exc_info=True)
