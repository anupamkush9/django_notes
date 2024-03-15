# Email send curl request
'''
curl --location --request POST 'http://127.0.0.1:8000/notes/send_mail/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=NHrY6JjztRpqdVQwC8pbgNsXHZwT97rt5ZuYOevP7ASBzNRpSf3Bp4zwwkhki8Wb' \
--data-raw '{
    "subject":"This is a demo subject",
    "message": "This is dummy message",
    "recipient": "<email_id>"
}'
'''