import json
import samples.dbmanager as dbm
import samples.common as common

# Create your views here.
def ListData(PageIndex=1, PageSize=None, SearchBy=None, Keywords=None):
    db = dbm.dbcmd()
    db.commandText = 'usp_mst_unit_ListData'
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
    header = ListData(SearchBy='A.uid', Keywords=uid)['List'][0]
    return header

def SaveUpdate(header):
    saveParam = ['uid', 'unit_code', 'unit_name', 'rowstatus', 'modified_by'] # ini parameter yg dikirim ke sp saveupdate
    header = common.PrepareModelDict(saveParam, header)

    if not header['unit_code']:
        raise ValueError('Unit Code cannot be null.')

    if not header['uid']:
        header['uid'] = common.Guid()
    
    db = dbm.dbcmd()
    db.commandText = 'usp_mst_unit_SaveUpdate'
    db.commandType = 'StoredProcedure'
    db.addInParameter('uid', header['uid'])
    db.addInParameter('unit_code', header['unit_code'])
    db.addInParameter('unit_name', header['unit_name'])
    db.addInParameter('rowstatus', header['rowstatus'])
    db.addInParameter('modified_by', header['modified_by'])
    db.ExecuteNonResult()
    db.closeConnection()

    return header
    

