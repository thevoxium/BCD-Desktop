import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


fromaddr = "thevoxium@bugbear646.bcd"
frompass = "********************"

def auto_email(toaddr, file_path_list, b0, b1, b2):
    toaddr = toaddr
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Mammograms Scans | Birads Classified Output"
    body = "Hello, these are your Scan Results: Birads 0: "+str(b0)+", Birads 1: "+str(b1)+", Birads 2: "+str(b2)
    msg.attach(MIMEText(body, 'plain'))

    i=1
    for file in file_path_list:
        filename = "Scan "+str(i)+".png"
        attachment = open(file, 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        i = i+1

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, frompass)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    print("Mail sent!")
    s.quit()
