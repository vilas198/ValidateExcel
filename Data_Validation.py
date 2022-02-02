import re
from datetime import datetime
import numpy as np

data=np.arange(0,101)

'''
This method is used for invalid record Validation
'''
def validationlist(df):
    duplicate = df[df.duplicated()]
    duplist = []
    for index, row in duplicate.iterrows():
        duplist.append(' Row No - ' + str(index + 1) + ' ' + row['Name'] + ' ' + str(row['Test 1']))
    invaliddate=[]
    mandate=[]
    notexist=[]
    validlist=[]
    invalidemail=[]
    #logging.debug("capturing invaliddate,mandate column,not exit list,invalid email")
    #print("capturing invaliddate,mandate column,not exit list,invalid email")
    for index, row in df.iterrows():
        if validateDate(row['Date'])==False:
            #print(index)
            invaliddate.append(' Row No - ' +str(index+1) + ' ' + row['Name'] + '    ' +str(row['Test 1']))
        if row['Test 1']<=0:#?
            mandate.append(' Row No - ' +str(index+1) + ' ' + row['Name'] + ' ' +str(row['Test 1']))
        if row['Test 1'] not in data:
            notexist.append(' Row No - ' +str(index+1) + ' '  + row['Name'] + ' ' +str(row['Test 1']))
        if validateemail(row['Email'])==False:
            invalidemail.append(' Row No - ' +str(index+1) + ' '  + row['Name'] + ' ' + str(row['Test 1']))
        else:
            validlist.append(row['Name'] + ' ' +str(row['Test 1'])) #index can be used
    #EL.WriteExcelLogs(duplist, invaliddate, mandate, notexist, invalidemail)
    return duplist, invaliddate, mandate, notexist, invalidemail



'''
This method is used for email Validation
'''
def validateemail(email):
    validate_conditon="^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"
    #print(email)
    if re.search(validate_conditon,email):
        if " " in email:
            return False
        else:
            return True
    else:
        return False

'''
This method is used for date Validation
'''
def validateDate(value):
    format = "%Y-%m-%d"
    if type(value) is datetime:
        if value is None:
            return True
        try:
            value = value.strftime(format)
            return True
        except ValueError:
            return False
    try:
        if type(value) is str:
            datetime.strptime(value, format)
            return True
    except ValueError:
        return False
    return False