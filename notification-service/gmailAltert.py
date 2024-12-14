import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GmailAlert:
    """
    A class to send email notifications using Gmail SMTP.
    """

    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        """
        Initialize the GmailAlert class.

        :param smtp_server: SMTP server address (e.g., smtp.gmail.com).
        :param smtp_port: SMTP server port (e.g., 587).
        :param email: Sender's Gmail address.
        :param password: App password for the sender's Gmail account.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_email(self, recipient_email: str, subject: str, body: str) -> dict:
        """
        Send an email notification.

        :param recipient_email: Recipient's email address.
        :param subject: Subject of the email.
        :param body: Body of the email.
        :return: A dictionary with success or error message.
        """
        try:
            # Set up the email components
            message = MIMEMultipart()
            message["From"] = self.email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.email, self.password)
                server.sendmail(self.email, recipient_email, message.as_string())

            return {"status": "success", "message": "Email sent successfully"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
