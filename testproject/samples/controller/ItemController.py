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

def ItemRecipeListData(PageIndex=1, PageSize=None, item_uid='', item_code='', SearchBy=None, Keywords=None):
    db = dbm.dbcmd()
    db.commandText = 'usp_mst_item_recipe_ListData'
    db.commandType = 'StoredProcedure'
    db.addInParameter('PageIndex', PageIndex)
    db.addInParameter('PageSize', PageSize)
    db.addInParameter('item_uid', item_uid)
    db.addInParameter('item_code', item_code)
    db.addInParameter('SearchBy', SearchBy)
    db.addInParameter('Keywords', Keywords)
    db.addOutParameter('RecordCount', 0)
    result = db.Execute()
    RecordCount = result.out['RecordCount']
    db.clearParameter()

    db.closeConnection()

    data = {
        'recipeDetailList': result.record,
        'recipeDetailTotalRecords': RecordCount
    }
    
    return data

def ItemGetData(uid):
    data = {}
    header = ItemListData(SearchBy='A.uid', Keywords=uid)['List'][0]
    header_item_code = header['item_code']
    detail = ItemRecipeListData(item_uid=uid, item_code=header_item_code)
    data.update(header)
    data.update(detail)
    return data

def ItemSaveUpdate(header, detail):
    headerSaveParam = ['uid', 'item_code', 'item_name', 'price', 'item_type', 'rowstatus', 'modified_by'] # ini parameter yg dikirim ke sp saveupdate
    header = common.PrepareModelDict(headerSaveParam, header)

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
    db.clearParameter()

    detailSaveParam = ['uid', 'item_uid', 'item_code', 'item_name', 'bahan_uid', 'bahan_code', 'bahan_name', 'qty', 'unit_code', 'rowstatus', 'modified_by']
    for row in detail:
        row['item_uid'] = header['uid']
        row['item_code'] = header['item_code']
        row['item_name'] = header['item_name']
        row['modified_by'] = header['modified_by']

        row = common.PrepareModelDict(detailSaveParam, row)

        db.commandText = 'usp_mst_item_recipe_SaveUpdate'
        db.commandType = 'StoredProcedure'
        db.addInParameter('uid', row['uid'] if row['uid'] else common.Guid())
        db.addInParameter('item_uid', row['item_uid'])
        db.addInParameter('item_code', row['item_code'])
        db.addInParameter('item_name', row['item_name'])
        db.addInParameter('bahan_uid', row['bahan_uid'])
        db.addInParameter('bahan_code', row['bahan_code'])
        db.addInParameter('bahan_name', row['bahan_name'])
        db.addInParameter('qty', row['qty'])
        db.addInParameter('unit_code', row['unit_code'])
        db.addInParameter('rowstatus', row['rowstatus'])
        db.addInParameter('modified_by', row['modified_by'])
        db.ExecuteNonResult()
        db.clearParameter()

    db.closeConnection()

    return header
    

