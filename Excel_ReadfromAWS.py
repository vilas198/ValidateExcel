import logging
import boto3
from botocore.exceptions import ClientError
import io
import pandas as pd
import json
import openpyxl

class awsoperations:
    def __init__(self,aws_id,aws_secret, bucket_name,object_key):
        self.aws_id=aws_id
        self.aws_secret=aws_secret
        self.bucket_name=bucket_name
        #self.file_name=file_name
        self.object_key = object_key


    def uploadlogToAWS(self,file_name, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        if object_name is None:
            object_name = file_name
        # Upload the file
        s3_client = boto3.client('s3', aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_secret)
        try:

            #print(self.aws_id, self.aws_secret, self.bucket_name, file_name,object_name)
            response = s3_client.upload_file(file_name, self.bucket_name, object_name)

        except ClientError as e:
            logging.error(e)
            return False
        return True

    def ReadExcelFromAWS(self):
        '''
        aws_id = 'AKIAUWCWPJOHSFMPZUEC'
        aws_secret = 'Jb2YMnCdjoADqKkR1dVJa6uEo4dqBw9ni8m9Lbwr'
        bucket_name = 'excellist2022'
        object_key = 'sample_scores.xlsx'
        '''
        #print('reading')
        #print(self.aws_id, self.aws_secret, self.bucket_name, self.object_key)
        s3 = boto3.client('s3', aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_secret)

        obj = s3.get_object(Bucket=self.bucket_name, Key=self.object_key)
        data = obj['Body'].read()
        df = pd.read_excel(io.BytesIO(data))
        return df

    def DownloadExcelFromAWS(self):
        '''
        aws_id = 'AKIAUWCWPJOHSFMPZUEC'
        aws_secret = 'Jb2YMnCdjoADqKkR1dVJa6uEo4dqBw9ni8m9Lbwr'
        bucket_name = 'excellist2022'
        object_key = 'sample_scores.xlsx'
        '''
        #print('reading')
        #print(self.aws_id, self.aws_secret, self.bucket_name, self.object_key)
        try:
            status=1
            s3 = boto3.resource('s3', aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_secret)
            s3.Bucket(self.bucket_name).download_file(self.object_key, ".\\Inbound\\"+self.object_key)
        except Exception as ex :
            print(str(ex))
            status=0
        finally:
            return status




if __name__ =="__main__":
    aws_id = 'AKIAUWCWPJOHSFMPZUEC'
    aws_secret = 'Jb2YMnCdjoADqKkR1dVJa6uEo4dqBw9ni8m9Lbwr'
    bucket_name = 'excellist2022'
    object_key='sample_scoresnew.xls'
    filename = 'D:\BR CSV Upload\ErrorLog_0123202212.csv'
    object_name = 'ErrorLog_0123202212.csv'
    #print(aws_id,aws_secret,bucket_name,filename,object_key,object_name)
    obj=awsoperations(aws_id,aws_secret,bucket_name,object_key)
    #df=obj.ReadExcelFromAWS()
    #print(df)
    obj.DownloadExcelFromAWS()
    #obj.uploadlogToAWS(filename,object_name)
    #ReadExcelFromAWS(aws_id, aws_secret,bucket_name,object_key)
    #uploadlogToAWS(aws_id, aws_secret, bucket_name,filename,object_name)
    print('uploaded..')

