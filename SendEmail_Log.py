import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
      The main deal.  Sets up an argument parser and calls send email and
      clean_logs need to read from confige
"""
def trysendemail(subject,body,port,smtp_server,sender_email,receiver_email,password,filenm,bcc_email,fname):
    print("Started email...")
    #print(port, smtp_server, sender_email, receiver_email, password, filenm)
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = bcc_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = filenm #"AWS.pdf"  # In same directory as script
    #fname=filename.split('\\')

    #fname=fname[-1]
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
        "Content-Disposition",
        f"attachment; filename= {fname}",
        )
        #print("attaching email...")
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()
        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        #print("context email...")
        with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

    print("Sent email...")

if __name__ == "__main__":
    subject = "An email with attachment from Python for sending log"
    body = "This is an email with attachment sent from Python for sending log"
    port = 465  # For SSL(587)
    smtp_server = "smtp.gmail.com"
    sender_email = "doitwithfocus@gmail.com"  # Enter your address
    receiver_email = "vilaspatil198@gmail.com"  # Enter receiver address
    password = "patil@2020"
    filenm="D:\Tutor\PythonTutoor\ExcelOperations\Logs\logger.log"
    trysendemail(subject, body, port, smtp_server, sender_email, receiver_email, password, filenm,sender_email)