import json
import samples.dbmanager as dbm
import samples.common as common

# Create your views here.
def ItemListData(PageIndex=1, PageSize=None, item_type=None, SearchBy=None, Keywords=None):
    db = dbm.dbcmd()
    db.commandText = 'usp_mst_item_ListData'
    db.commandType = 'StoredProcedure'
    db.addInParameter('PageIndex', PageIndex)
    db.addInParameter('PageSize', PageSize)
    db.addInParameter('item_type', item_type)
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

def ItemGetData(uid):
    return ItemListData(SearchBy='A.uid', Keywords=uid)

def ItemSaveUpdate(header):
    saveParam = ['uid', 'item_code', 'item_name', 'price', 'item_type', 'rowstatus', 'modified_by'] # ini parameter yg dikirim ke sp saveupdate
    header = common.PrepareModelDict(saveParam, header)

    if not header['uid']:
        header['uid'] = common.Guid()
        header['item_code'] = common.AutoCounter('item_code', 'mst_item', 'item_code', 'ITM', 4) # FieldName, TableName, FieldCriteria, ValueCriteria, LengthOfString
        print(header['item_code'])
    
    db = dbm.dbcmd()
    db.commandText = 'usp_mst_item_SaveUpdate'
    db.commandType = 'StoredProcedure'
    db.addInParameter('uid', header['uid'])
    db.addInParameter('item_code', header['item_code'])
    db.addInParameter('item_name', header['item_name'])
    db.addInParameter('price', header['price'])
    db.addInParameter('item_type', header['item_type'])
    db.addInParameter('rowstatus', header['rowstatus'])
    db.addInParameter('modified_by', header['modified_by'])
    db.ExecuteNonResult()
    db.closeConnection()

    return header
    

