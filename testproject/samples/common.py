import uuid
import samples.dbmanager as dbm

def Guid():
    return str(uuid.uuid4()).upper()

def AutoCounter(FieldName, TableName, FieldCriteria, ValueCriteria, LengthOfString, NumericOnly=0):
    db = dbm.dbcmd()
    db.commandText = 'proc_AutoCounter'
    db.commandType = 'StoredProcedure'
    db.addInParameter('FieldName', FieldName)
    db.addInParameter('TableName', TableName)
    db.addInParameter('FieldCriteria', FieldCriteria)
    db.addInParameter('ValueCriteria', ValueCriteria)
    db.addInParameter('LengthOfString', LengthOfString)
    db.addInParameter('NumericOnly', NumericOnly)
    result = db.Execute()
    db.clearParameter()
    db.closeConnection(False)

    result = result.record[0]
    return result['AutoCode']

def PrepareModelDict(param=[], data={}):
    tmp_data = {}
    for key in param:
        try:
            tmp_data[key] = data[key]
        except:
            tmp_data[key] = None
    
    return tmp_data
    
def PrepareListModelDict(param=[], data=[]):
    list_data = []
    for row in data:
        tmp_data = {}
        for key in param:
            try:
                tmp_data[key] = row[key]
            except:
                tmp_data[key] = None
        list_data.append(tmp_data)
    
    return list_data