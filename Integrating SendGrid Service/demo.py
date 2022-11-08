import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(api_key= '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' )
from_email = Email("19cs052@syedengg.co.in")
to_email = To("19cs051@syedengg.co.in")
subject = "Sending with SendGrid"
content = Content("text/plain", "Plasma Donor Application")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)
