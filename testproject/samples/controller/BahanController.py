import json
import samples.dbmanager as dbm
import samples.common as common

# Create your views here.
def ListData(PageIndex=1, PageSize=None, SearchBy=None, Keywords=None):
    db = dbm.dbcmd()
    db.commandText = 'usp_mst_bahan_ListData'
    db.commandType = 'StoredProcedure'
    db.addInParameter('PageIndex', PageIndex)
    db.addInParameter('PageSize', PageSize)
    db.addInParameter('SearchBy', SearchBy)
    db.addInParameter('Keywords', Keywords)
    db.addOutParameter('RecordCount', 0)
    result = db.Execute()
    RecordCount = result.out['RecordCount']
    db.clearParameter()

    db.closeConnection()

    data = {
        'List': result.record,
        'TotalRecords': RecordCount
    }
    
    return data

def GetData(uid):
    return ListData(1, None, 'A.uid', uid)

def SaveUpdate(header):
    saveParam = ['uid', 'bahan_code', 'bahan_name', 'stock_qty', 'rowstatus', 'modified_by'] # ini parameter yg dikirim ke sp saveupdate
    header = common.PrepareModelDict(saveParam, header)

    if not header['uid']:
        header['uid'] = common.Guid()
        header['bahan_code'] = common.AutoCounter('bahan_code', 'mst_bahan', 'bahan_code', '', 5) # FieldName, TableName, FieldCriteria, ValueCriteria, LengthOfString
        print(header['bahan_code'])
    
    db = dbm.dbcmd()
    db.commandText = 'usp_mst_bahan_SaveUpdate'
    db.commandType = 'StoredProcedure'
    db.addInParameter('uid', header['uid'])
    db.addInParameter('bahan_code', header['bahan_code'])
    db.addInParameter('bahan_name', header['bahan_name'])
    db.addInParameter('stock_qty', header['stock_qty'])
    db.addInParameter('rowstatus', header['rowstatus'])
    db.addInParameter('modified_by', header['modified_by'])
    db.ExecuteNonResult()
    db.closeConnection()

    return header
    

