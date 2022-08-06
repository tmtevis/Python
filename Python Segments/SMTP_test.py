import smtplib

gmail_user = 'youremailhere@gmail.com'
gmail_password = 'password'

sent_from = gmail_user
to = 'awildtylerappears@gmail.com'
subject = 'Super Important Message'
body = 'testing testing 123'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, to, subject, body)
print(email_text)


try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
except:
    print('Something went wrong...')