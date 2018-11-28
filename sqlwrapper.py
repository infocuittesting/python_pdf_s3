import psycopg2
import json
import datetime
def dbfetch(sql):
     print(sql)
     try:
      con = psycopg2.connect(user='uawhauxngssmim',password='2bb78e6924fc159b238fce76bfd2e3efa1b0827cbc99c3dd1fc207ec555d6ae3',host='ec2-79-125-110-209.eu-west-1.compute.amazonaws.com',port='5432',database='d4n8gqnv5nkqri')
      cur = con.cursor()
     except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
     cur.execute(sql)
     result = cur.fetchall()
     fresult = []
     for i in result:
         for res in i:
             fresult.append(res)
     return(fresult)
def dbput(sql):
    try:
      con = psycopg2.connect(user='uawhauxngssmim',password='2bb78e6924fc159b238fce76bfd2e3efa1b0827cbc99c3dd1fc207ec555d6ae3',host='ec2-79-125-110-209.eu-west-1.compute.amazonaws.com',port='5432',database='d4n8gqnv5nkqri')
      cur = con.cursor()
    except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
    cur.execute(sql)
    con.commit()
    return sql
def dbget(sql):
     try:
      con = psycopg2.connect(user='uawhauxngssmim',password='2bb78e6924fc159b238fce76bfd2e3efa1b0827cbc99c3dd1fc207ec555d6ae3',host='ec2-79-125-110-209.eu-west-1.compute.amazonaws.com',port='5432',database='d4n8gqnv5nkqri')
      cur = con.cursor()
     except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
     cur.execute(sql)
     def myconverter(o):
            if isinstance(o, datetime.date):
                return o.__str__()  
     columns = cur.description
     result = [{columns[index][0]:column for index, column in enumerate(value)}   for value in cur.fetchall()]
     fresult= json.dumps(result,indent=3,default=myconverter)
     return(fresult) 
def Dict2Str(dictin,joiner=','):
    # make dict to str, with the format key='value'
    #tmpstr=''
    tmplist=[]
    for k,v in dictin.items():
        # if v is list, so, generate 
        # "k in (v[0], v[1], ...)"
        if isinstance(v, (list, tuple)):
            tmp = str(k)+' in ('+ ','.join(map(lambda x:'\''+str(x)+'\'',v)) +') '
        else:
            tmp = str(k)+'='+'\''+str(v)+'\''
        tmplist.append(' '+tmp+' ')
    return joiner.join(tmplist)
def gen_insert(table,dicts):
    '''
    >>> kdict = {'name':'lin','age':22} 
    >>> geninsertsql('persons',kdict)
    insert into person (name,age) values ('lin',22)
    '''
    sql = 'insert into %s '%table
    ksql = []
    vsql = []
    for k,v in dicts.items():
        ksql.append(str(k))
        vsql.append('\''+str(v)+'\'')
    sql += ' ('+','.join(ksql)+') '
    sql += ' values ('+','.join(vsql)+')'
    #return sql
    return(dbput(sql))

def gen_select(table,keys="*",conddicts=None):
    if isinstance(keys, (tuple,list)):
        keys=','.join(map(str,keys))
    sql = 'select %s '%keys
    sql += ' from %s '%table
    if conddicts:
        sql += ' where %s '%Dict2Str(conddicts,'and')
    print (sql)
    return (dbget(sql))
def gen_update(table,dicts,conddicts):
    # conddicts maybe the Condition, in sql, where key='value' or key in (value)
    # dicts are the values to update
    sql = ''
    sql += 'update %s '%table
    sql += ' set %s'%Dict2Str(dicts)
    sql += ' where %s'%Dict2Str(conddicts,'and')
    print(sql)
    return(dbput(sql))
    
def gensql(imp,*args, **kwds):
    if imp == "insert":
        return gen_insert(*args, **kwds)
    elif imp == "update":
        return gen_update(*args, **kwds)
    elif imp == "select":
        return gen_select(*args, **kwds)
    else:
        return None  

#print(gensql('insert','test',d))
#print(gensql('select','test','*',d))
#print(gensql('update','test',d,e))
