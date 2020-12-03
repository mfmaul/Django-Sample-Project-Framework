from django.db import connections, transaction
from django.db.utils import DEFAULT_DB_ALIAS, load_backend

def create_connection(alias=DEFAULT_DB_ALIAS):
    connections.ensure_defaults(alias)
    connections.prepare_test_settings(alias)
    db = connections.databases[alias]
    backend = load_backend(db['ENGINE'])
    return backend.DatabaseWrapper(db, alias)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class dbcmd:
    def __init__(self):
        self.commandText = ''
        self.commandType = ''
        self.params = {}
        self.conn = create_connection()
        self.cur = self.conn.cursor()

    def closeConnection(self, isTrans = False):
        self.cur.close()
        # if isTrans:
        #     self.conn.commit()
        self.conn.close()
    
    def addInParameter(self, param_name, param_value):
        self.params[len(self.params)] = {'param_name': param_name, 'param_value': param_value, 'param_type': 'in'}
    
    def addOutParameter(self, param_name, param_value):
        self.params[len(self.params)] = {'param_name': param_name, 'param_value': param_value, 'param_type': 'out'}
    
    def clearParameter(self):
        self.params = {}
    
    def Execute(self):
        with transaction.atomic():
            if self.commandType == 'StoredProcedure':
                param = [self.params[n]['param_value'] for n in range(len(self.params))]
                self.cur.callproc(self.commandText, param)
                res = dictfetchall(self.cur)
                for param in self.params:
                    if self.params[param]['param_type'] == 'out':
                        self.cur.execute('SELECT ' + '@_' + self.commandText + '_' + str(param))
                        self.params[param]['param_value'] = self.cur.fetchall()[0][0]
                res_param = { self.params[n]['param_name']:self.params[n]['param_value'] for n in self.params if self.params[n]['param_type'] == 'out' }
                return dbcmdresult(res, res_param)
            if self.commandType == 'Query':
                self.cur.execute(self.commandText)
                res = dictfetchall(self.cur)
                return dbcmdresult(res, {})
    
    def ExecuteNonResult(self):
        with transaction.atomic():
            if self.commandType == 'StoredProcedure':
                param = [self.params[n]['param_value'] for n in range(len(self.params))]
                self.cur.callproc(self.commandText, param)
                res = dictfetchall(self.cur)
                for param in self.params:
                    if self.params[param]['param_type'] == 'out':
                        self.cur.execute('SELECT ' + '@_' + self.commandText + '_' + str(param))
                        self.params[param]['param_value'] = self.cur.fetchall()[0][0]
                res_param = { self.params[n]['param_name']:self.params[n]['param_value'] for n in self.params if self.params[n]['param_type'] == 'out' }
            if self.commandType == 'Query':
                self.cur.execute(self.commandText)
                res = dictfetchall(self.cur)

class dbcmdresult:
    def __init__(self, result, out):
        self.record = result
        self.out = out
    

