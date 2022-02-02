from configparser import ConfigParser
from flask import Flask, jsonify
app = Flask(__name__)
app.config["DEBUG"] = True
conf = ConfigParser()
conf.read('setting.ini')
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/readAWSconfig', methods=['GET'])
def readAWSconfig():
    try:
        aws_id = conf.get('AWS', 'aws_id')
        aws_secret = conf.get('AWS', 'aws_secret')
        bucket_name = conf.get('AWS', 'bucket_name')
        object_key = conf.get('AWS', 'object_key')
        a=aws_id, aws_secret, bucket_name, object_key
        #return jsonify(a)
        a= {"aws_id":aws_id,"aws_secret":aws_secret,"bucket_name":bucket_name,"object_key":object_key}
        return jsonify(a)
        #,aws_secret,bucket_name,object_key
    except Exception as ex:
        print(str(ex))

@app.route('/api/v1/resources/readAWSconfig1', methods=['GET'])
def readAWSconfig1():
    try:
        aws_id = conf.get('AWS', 'aws_id')
        aws_secret = conf.get('AWS', 'aws_secret')
        bucket_name = conf.get('AWS', 'bucket_name')
        object_key = conf.get('AWS', 'object_key')
        a=aws_id, aws_secret, bucket_name, object_key
        #return jsonify(a)
        a= {"aws_id":aws_id,"aws_secret":aws_secret,"bucket_name":bucket_name,"object_key":object_key}
        return jsonify(a)
        #,aws_secret,bucket_name,object_key
    except Exception as ex:
        print(str(ex))
# A route to return all of the available entries in our EmailConfiguration.
@app.route('/api/v1/resources/reademail', methods=['GET'])
def readEmailconfig():
    try:
        print("test")
        port = conf.get('mail', 'port') #465   For SSL(587)
        smtp_server =conf.get('mail', 'smtp_server')
        sender_email = conf.get('mail', 'sender_email')
        receiver_email = conf.get('mail', 'receiver_email')
        bcc_email = conf.get('mail', 'bcc_email')
        password = conf.get('mail', 'password')
        vmail=port,smtp_server,sender_email,receiver_email,bcc_email,password
        return jsonify(vmail)
        #return port,smtp_server,sender_email,receiver_email,bcc_email,password
    except Exception as ex:
        print(str(ex))

app.run()
