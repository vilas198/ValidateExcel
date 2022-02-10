import requests
def readAWS_Config():
    try:
        status = 1
        url1 = "http://127.0.0.1:5000//api/v1/resources/readAWSconfig"
        response = requests.get(url1)
        res = response.json()
        aws_id = res['aws_id']
        aws_secret = res['aws_secret']
        bucket_name = res['bucket_name']
        object_key = res['object_key']
    except Exception as ex:
        status=0
        aws_id = 0
        aws_secret = 0
        bucket_name = 0
        object_key = 0
        print(str(ex))
    return aws_id, aws_secret, bucket_name, object_key,status

def readEmail_Config():
    try:
        status=1
        url1 = "http://127.0.0.1:5000//api/v1/resources/reademail"
        response = requests.get(url1)
        res = response.json()
        port = res['port']
        smtp_server = res['smtp_server']
        sender_email = res['sender_email']
        receiver_email = res['receiver_email']
        bcc_email = res['bcc_email']
        password = res['password']
    except Exception as ex:
        status = 0
        port = 0
        smtp_server = 0
        sender_email = 0
        receiver_email = 0
        bcc_email = 0
        password = 0
    return port, smtp_server, sender_email, receiver_email, bcc_email, password,status
'''
for i in res:
    print(res[i],'\n')
'''