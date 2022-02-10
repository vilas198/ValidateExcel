import pandas as pd
import numpy as np
import logging
from configparser import ConfigParser
import SendEmail_Log as smail
import Excel_ReadfromAWS as ERA
import WriteLogInFiles as EL
import Data_Validation as DV
import Consume_ConfigAPI as RC

logging.basicConfig(filename=".\Logs\logger.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s'
                    )

data=np.arange(0,100)
# read aws configurartion from init file
def ReadAWSconfig():
    try:
        aws_id=configur.get('AWS','aws_id')
        aws_secret = configur.get('AWS', 'aws_secret')
        bucket_name = configur.get('AWS', 'bucket_name')
        object_key = configur.get('AWS', 'object_key')
        return  aws_id,aws_secret,bucket_name,object_key
    except Exception as ex:
        print(str(ex))

def ReadEmailconfig():
    try:
        port = configur.get('mail','port') #465   For SSL(587)
        smtp_server =configur.get('mail','smtp_server')
        sender_email = configur.get('mail','sender_email')
        receiver_email = configur.get('mail','receiver_email')
        bcc_email = configur.get('mail', 'bcc_email')
        password = configur.get('mail','password')
        return port,smtp_server,sender_email,receiver_email,bcc_email,password
    except Exception as ex:
        print(str(ex))
# Define `main()` function
def main(folderpath,filename):
    logging.debug("Reading excel file")
    excel_file_path = folderpath+'/' + filename
    try:
        df = pd.read_excel(filename)
    except:
        logging.warning('unable to read file')
    else:
        logging.debug("defult value for empty email")
        df.Email.fillna('default',inplace=True)

    '''
    Removing special characters for all columns
    '''
    for column in df.columns:
        #print(column)
        if column=='Name':
            df[column] = df[column].str.replace(r'\W',"", regex=True)
    logging.debug("special characters removed")

    format = "%Y-%m-%d"
    logging.debug("validating started")
    duplist, invaliddate, mandate, notexist, invalidemail=DV.validationlist(df)
    fname=EL.WriteExcelLogs(duplist, invaliddate, mandate, notexist, invalidemail,".\\Outbound\\")
    logging.debug("Fetching all the invalid list")
    #Errdict=ErrorDict(duplist, invaliddate, mandate, notexist, invalidemail)
    #fname =EL.writeerrorsCSV(Errdict,".\\Outbound\\")
    return fname

'''
This method is used for converting list into dictionary
'''
def ErrorDict(duplist, invaliddate, mandate, notexist, invalidemail):
    errors = {}
    errors['duplist'] = duplist
    errors['invaliddate'] = invaliddate
    errors['mandate'] = mandate
    errors['notexist'] = notexist
    errors['invalidemail'] = invalidemail
    return errors



# Execute `main()` function
if __name__=="__main__":
    try:
        logging.info('Program started..')
        configur=ConfigParser()
        configur.read('.\Config\setting.ini')
        folderpath=configur.get('debug','folderpath')
        filename=configur.get('debug','filename')

        #Reading AWS configuration
        aws_id,aws_secret,bucket_name,object_key,status=RC.readAWS_Config()
        print("reading status form aws")
        print(status)
        if status==0:
            print("Error while Reading aws configuration from service")
            logging.debug("Error while Reading aws configuration from service")
            aws_id, aws_secret, bucket_name, object_key = ReadAWSconfig()

        print(aws_id,aws_secret,bucket_name,object_key,status)


        # Downloading Excel from AWS
        obj = ERA.awsoperations(aws_id, aws_secret, bucket_name, object_key)
        status=obj.DownloadExcelFromAWS()
        #print("downlaod status{}".format(status))
        if status==1:
            #Reading Excel file and validation
            fname = main(folderpath, filename)
            #aws_id, aws_secret, bucket_name, object_key = ReadAWSconfig()
            object_name = 'ErrorLog_0123202212.csv'

            object_name=fname.split('\\')  #
            #Uploading Error file on AWS
            obj.uploadlogToAWS(fname,object_name[-1]) # use os to extract name
            subject = "An email with attachment from Python for sending log test2"
            body = """This is an email with attachment sent from Python for sending log test2" \
                   "Bucket Name {0} 
                   \n File uploaded on s3:{1} url : {2} """.format(bucket_name, object_name[-1],"https://"+bucket_name+".s3.us-east-2.amazonaws.com/"+object_name[-1])
        else:
            print("Error occured while downloading file")
            logging.log("Error occured while downloading file")
            subject = "Error while downloading, An email with attachment from Python for sending log test2"
            body = "Error while downloading, This is an email with attachment sent from Python for sending log test2"

        #url share
        port, smtp_server, sender_email, receiver_email, bcc_email, password,status= RC.readEmail_Config()
        if status==0:
            print("Error while Reading email configuration from service")
            logging.debug("Error while Reading email configuration from service")
            port, smtp_server, sender_email, receiver_email, bcc_email, password=ReadEmailconfig()
        filenm = ".\\Outbound\\"+object_name[-1]
        #print(filenm)
        smail.trysendemail(subject,body,port,smtp_server,sender_email,receiver_email,password,filenm,bcc_email,object_name[-1])
        print("Email sent with log..")
    except NameError:
        logging.warning('Name Error occured')
    except:
        logging.warning('unknown Error occured')
    else:
        logging.info('Program ended..')

