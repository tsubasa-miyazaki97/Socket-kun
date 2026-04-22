import os
import sqlite3
import TCPGlobalVar as gl
import ConectConfWin as ConectConf
import SensorConfWin as SensorConf
import IORW
sqlite3.register_adapter(bool, lambda b: str(b))
sqlite3.register_converter('BOOL', lambda l: l.decode().strip().capitalize() == 'True' if l is not None else False)

def DBConnect():
    
    #DB作成、接続(このパス先に保存)
    gl.Conn = sqlite3.connect(os.path.join(gl.MyPath, 'IODB.db'), detect_types=sqlite3.PARSE_DECLTYPES)
    gl.Conn.row_factory = DictFactory
    gl.Cur=gl.Conn.cursor()

def TableCreate():
    
    DBConnect()

    #テーブル削除したい時実行
    #gl.Cur.execute('DROP TABLE IOConf ;')

    #通信設定テーブル有無確認して作成
    gl.Cur.execute("SELECT * FROM sqlite_master WHERE type='table' and name='DeviceConf'")
    if not gl.Cur.fetchone():
        gl.Cur.execute('CREATE TABLE DeviceConf (id int primary key, Device varchar(1024), IPAddress varchar(1024), Port varchar(1024))')

        for i in range(gl.DeviceMax):
            gl.Cur.execute("REPLACE INTO DeviceConf VALUES (?,?,?,?)",(i,'','',''))

    #IO設定テーブル有無確認して作成
    gl.Cur.execute("SELECT * FROM sqlite_master WHERE type='table' and name='IOConf'")
    if not gl.Cur.fetchone():
        gl.Cur.execute('CREATE TABLE IOConf (id int primary key, DeviceNo varchar(1024), Address varchar(1024),\
                Init varchar(1024), UpDown varchar(1024), Comment varchar(1024), VarType varchar(1024), AI0 varchar(1024),\
                    AI100 varchar(1024), User0 varchar(1024), User100 varchar(1024), CurrentVal varchar(1024))')

        for i in range(gl.ChMax):
            gl.Cur.execute("REPLACE INTO IOConf VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",\
                            (i,'','','','','','','','','','',''))
    else:
        #既存テーブルへのCurrentVal列追加(マイグレーション)
        try:
            gl.Cur.execute('ALTER TABLE IOConf ADD COLUMN CurrentVal varchar(1024) DEFAULT ""')
        except sqlite3.OperationalError as e:
            if 'duplicate column name' not in str(e):
                raise  #列重複以外のエラーは再送出

    #センサー設定テーブル有無確認して作成
    gl.Cur.execute("SELECT * FROM sqlite_master WHERE type='table' and name='SensorConf'")
    if not gl.Cur.fetchone():
        gl.Cur.execute('''CREATE TABLE SensorConf (id int primary key, Sensor varchar(1024), In1 varchar(1024), In2 varchar(1024),
                    Out1 varchar(1024), Out2 varchar(1024), Out1Inv BOOL, Out2Inv BOOL,
                        DigitsCoef varchar(1024), CalcCoef varchar(1024), Ratio varchar(1024), TimeLag varchar(1024), Disable BOOL);''')
        
        for i in range(gl.ChMax):
            gl.Cur.execute("REPLACE INTO SensorConf VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                            (i,'','','','','',False,False,'','','','',False))

    gl.Conn.commit()#保存
    gl.Conn.close()


def ValGet():

    DBConnect()

    gl.Cur.execute("select * from DeviceConf")
    gl.DeviceConfDic = gl.Cur.fetchall()

    gl.Cur.execute("select * from IOConf")
    gl.IOConfDic = gl.Cur.fetchall()

    gl.Cur.execute("select * from SensorConf")
    gl.SensorConfDic = gl.Cur.fetchall()

    #初期値記憶の為
    ConectConf.EnableCheck()
    IORW.EnableCheck()
    SensorConf.EnableCheck()

    gl.Conn.commit()#保存
    gl.Conn.close()

def BackUp():

    DBConnect()

#DBに値格納
    for i in range(gl.DeviceMax):
        gl.Cur.execute("REPLACE INTO DeviceConf VALUES (?,?,?,?)",\
                        (i,gl.DeviceConfDic[i]['Device'],gl.DeviceConfDic[i]['IPAddress'],str(gl.DeviceConfDic[i]['Port'])))

    for i in range(gl.ChMax):
        d = gl.IOConfDic[i] if isinstance(gl.IOConfDic[i], dict) else {}
        gl.Cur.execute("REPLACE INTO IOConf VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                        (i, d.get('DeviceNo',''), d.get('Address',''), d.get('Init',''),
                         d.get('UpDown',''), d.get('Comment',''), d.get('VarType',''),
                         d.get('AI0',''), d.get('AI100',''), d.get('User0',''),
                         d.get('User100',''), d.get('CurrentVal','')))

    for i in range(gl.ChMax):
        gl.Cur.execute("REPLACE INTO SensorConf VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                        (i,gl.SensorConfDic[i]['Sensor'],gl.SensorConfDic[i]['In1'],gl.SensorConfDic[i]['In2'],\
                        gl.SensorConfDic[i]['Out1'],gl.SensorConfDic[i]['Out2'],gl.SensorConfDic[i]['Out1Inv'],\
                        gl.SensorConfDic[i]['Out2Inv'],gl.SensorConfDic[i]['DigitsCoef'],gl.SensorConfDic[i]['CalcCoef'],\
                        gl.SensorConfDic[i]['Ratio'],gl.SensorConfDic[i]['TimeLag'],gl.SensorConfDic[i]['Disable']))
    
    gl.Conn.commit()#保存
    gl.Conn.close()

def DictFactory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

