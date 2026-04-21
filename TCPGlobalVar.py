from sqlite3 import connect
import os

#------------Const-------------
#GUI
winwidth = 700#変わらない？
winheight = 500
winmaxwidth = 1100

deffont = 'Helvetica'
fsizes = '10'
fsizem = '35'

ShortMin = -32767
ShortMax = 32767
UShortMin = 0
UShortMax = 65535
LongMin = -2147483648
LongMax = 2147483648
ULongMin = 0
ULongMax = 4294967296


DeviceMax = 5
ChMax = 200
DeviceList=["PC10G","MP","OMRON[CJ]","ﾀﾞﾐｰ(接続先無)","OPCUA"]
SensorList=['ｴｯｼﾞｾﾝｻ','ﾀﾞﾝｻｰ','径演算ﾀﾞﾝｻｰ','張力計','径演算張力計','径ｾﾝｻ','ｲｺｰﾙ(=)','Bit演算出力']
VarTypeList = ['Short','UShort','Long','ULong','Float']#,'Float(16bit)']
MyPath = os.path.dirname(os.path.abspath(__file__))
TraceTime = ['ｽｷｬﾝﾀｲﾑ','20','50','100']

Key = ['Device','IPAddress','Port','DeviceNo','Address','Init','UpDown','Comment','VarType','AI0','AI100','User0','User100',\
    'Sensor','In1','In2','Out1','Out2','Out1Inv','Out2Inv','DigitsCoef','CalcCoef','Ratio','TimeLag','Disable']

CJInitHeader = '46494E530000000C000000000000000000000000'

#------------Variable----------
app = None
#通信設定画面初期値
ConectConfWin = None
#センサー設定画面初期値
SensorConfWin = None

#表示に使うから、わかりやすく１～
#Device有効ﾘｽﾄ
EnableDevice = [] # 1~DeviceMax
#Ch有効ﾘｽﾄ
EnableCh = [] # 1~ChMax
#センサー有効ﾘｽﾄ
EnableSensor = [] # 1~ChMax

#DB用
Conn=None
Cur=None

#IO読書中
IORWBusy = False

#アドレス用変数
PC10GAddress = ['']*ChMax
MPAddress = ['']*ChMax
CJAddress = ['']*ChMax
OPCUAAddress = ['']*ChMax
DummyAddress = ['']*ChMax

#現在値テキスト用変数
ValueText=['']*ChMax
ValueTextFocus=[0]*ChMax

#周期計測
Period = ['']*DeviceMax

#ﾄﾚｰｽ
TraceFlag = None

CJHeader = ['46494E53','00','000000020000000080000200000000','00','0000']#FINS、ﾃﾞｰﾀｻｲｽﾞ、固定、IP、固定
CJMyIP = ''
CJMemory = ''#関係ない所も読書しないといけないから、記憶用
CJMinAddress = 6144
CJMaxAddress = 0
CJWMinAddress = 6144
CJWMaxAddress = 0

#------------Dictionary----------
#DB用
DeviceConfDic = []#配列内にDicで格納
IOConfDic = []#配列内にDicで格納 0~ChMax
SensorConfDic = []#配列内にDicで格納 0~ChMax

#アドレス用
PC10GAddDic = {}#Key=Add , ReadValue(hex),WriteValue(hex),Variable,ReadValue,WriteValue,Ch
MPAddDic = {}#Key=Add , Read(hex),Write(hex),Variable,Variable,ReadValue,WriteValue,Ch
CJAddDic = {}#Key=Add , Read(hex),Write(hex),Variable,Variable,ReadValue,WriteValue,Ch
OPCUAAddDic = {}#Key=Add , Read(hex),Write(hex),Variable,Variable,ReadValue,WriteValue,Ch
DummyAddDic = {}#Key=Add , Read(hex),Write(hex),Variable,Variable,ReadValue,WriteValue,Ch
AllAddDic = {}#上記Dicを格納

#センサー処理用
EdgeSensorDic={} #Key＝Ch　初期化ﾌﾗｸﾞ、入力軸前回値
DancerDic={} #Key＝Ch　初期化ﾌﾗｸﾞ、入力軸前回値
TensionMeterDic={} #Key＝Ch　初期化ﾌﾗｸﾞ、入力軸前回値
DiameterSensorDic={} #Key＝Ch　初期化ﾌﾗｸﾞ、入力軸前回値

#ﾄﾚｰｽ用
TraceDic=[]#配列内にTrace内容をDicで格納
