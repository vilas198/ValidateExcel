import numpy as np
import pandas as pd
from datetime import datetime

def WriteExcelLogs(duplist, invaliddate, mandate, notexist, invalidemail,filepath):
    # Create a Dataframe
    #print("excel logging")
    #print(duplist)
    df1 = pd.DataFrame(duplist)
    df2 = pd.DataFrame(invaliddate)
    df3 = pd.DataFrame(mandate)
    df4 = pd.DataFrame(notexist)
    df5 = pd.DataFrame(invalidemail)
    #df2 = pd.DataFrame(np.random.rand(100).reshape(50,2),columns=['a','b'])
    # Excel path
    now = datetime.now()
    date_time = now.strftime("%m%d%Y%H")
    excelpath = filepath + "Error_" + date_time + ".xlsx"
    #excelpath = '.\Outbound\path_to_your_excel.xlsx'
    # Write your dataframes to difference sheets

    with pd.ExcelWriter(excelpath) as writer:
        df1.to_excel(writer,sheet_name='Duplicate List')
        df2.to_excel(writer,sheet_name = 'Invalid Date list')
        df3.to_excel(writer, sheet_name='Mandate Column Missing')
        df4.to_excel(writer, sheet_name='Invalid range List')
        df5.to_excel(writer, sheet_name='Invalid Email List')
    return excelpath
'''
This method is used for writing invalid list into CSV file
'''
def writeerrorsCSV(Errdict,filepath):
    now = datetime.now()
    date_time = now.strftime("%m%d%Y%H")
    dff = pd.DataFrame.from_dict(Errdict,orient="index")
    fname=filepath + "Error_" + date_time + ".csv"
    dff.to_csv(filepath + "Error_" + date_time + ".csv")
    return fname
'''
This method is used for writing invalid list into text file
'''
def writeerrorsTxt(Errdict,filepath):
    now = datetime.now()
    date_time = now.strftime("%m%d%Y%H")
    with open(filepath+date_time+".txt","a") as f:
        f.write("#"*50)
        f.write("\nlogging information for {} :\n".format(datetime.now()))
        f.write("#" * 50)
        for d in Errdict:
            if d=='duplist':
                f.write("\nDuplicate Records are--> \n")
                f.write(str(Errdict[d]))
                f.write("\n")
            if d == 'invaliddate':
                f.write("Invalid dates -->\n")
                f.write(str(Errdict[d]))
                f.write("\n")
            if d == 'mandate':
                f.write("Mandate column data missing dates--> \n")
                f.write(str(Errdict[d]))
                f.write("\n")
            if d == 'notexist':
                f.write("column Test 1 data mismatch with list specified -->\n")
                f.write(str(Errdict[d]))
                f.write("\n")
            if d == 'invalidemail':
                f.write("Invalid email specified -->\n")
                f.write(str(Errdict[d]))
                f.write("\n")
