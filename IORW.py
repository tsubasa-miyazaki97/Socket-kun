import socket
import time
from tkinter import messagebox
import threading
import SocketConectTest as ConectTest
import PC10TCPCommand as PC10Command
import MPTCPCommand as MPCommand
import CJTCPCommand as CJCommand
import DummyTCPCommand as DummyCommand
import OPCUACommand as OPCUACommand
import TCPGlobalVar as gl
import WidgetBind as Bind
import SensorProcess as SenProc
import SensorConfWin as SensorConf
import SQDB as DB
from asyncua import Client
from asyncua import ua
import asyncio

def IORW():
    
    if not gl.IORWBusy :
        #各ウィジェットの値確認
        #読書ｱﾄﾞﾚｽ以外が数値か確認#######################################
        BackUp()
        if not EnableCheck():
            return
        if not SensorConf.EnableCheck():
            return
        
        #PC10GとMPアドレス振り分け
        #初期化
        DeviceListDic={} # 0~
        AddressDic={} # 0~
        gl.AllAddDic.clear()

        for i in gl.EnableDevice :
                DeviceListDic[i-1] = {'DeviceCnt':0}
                AddressDic[i-1] = []

        for i in gl.EnableCh :
            if gl.app.DeviceNoCombo[i-1].get() != "" :#ﾃﾞﾊﾞｲｽNoで振り分け

                DeviceNo = int(gl.app.DeviceNoCombo[i-1].get())-1
                Address = gl.app.AddressText[i-1].get()

                if not DeviceNo in gl.AllAddDic.keys() :
                    gl.AllAddDic[DeviceNo]={}
                if not gl.app.AddressText[i-1].get() in gl.AllAddDic[DeviceNo].keys() :
                    DeviceListDic[DeviceNo]['DeviceCnt'] += 1
                    AddressDic[DeviceNo].append(Address)
                    savedVal = gl.IOConfDic[i-1].get('CurrentVal', '') if isinstance(gl.IOConfDic[i-1], dict) else ''
                    try:
                        initRVal = float(savedVal) if savedVal not in ('', None) else 0
                    except (ValueError, TypeError):
                        initRVal = 0
                    gl.AllAddDic[DeviceNo][Address]= \
                        {'Var':gl.app.VarTypecombo[i-1].get(),'RVal':initRVal,'WVal':0,'Ch':i-1,'RAIVal':0,'WAIVal':0,'WFlag':False,\
                        'AI0':gl.app.AI0ValueText[i-1].get(),'AI100':gl.app.AI100ValueText[i-1].get(),\
                        'User0':gl.app.User0ValueText[i-1].get(),'User100':gl.app.User100ValueText[i-1].get()} 
                
        for i in gl.EnableDevice:#無入力ﾁｪｯｸ
            if DeviceListDic[i-1]['DeviceCnt'] != 0:
                break
            if i == gl.EnableDevice[-1]:
                messagebox.showinfo('エラー','通信設定に設定したデバイスを入力してください') 

        RWThread = {}
        for i in gl.EnableDevice:
            if DeviceListDic[i-1]['DeviceCnt'] != 0:
                if gl.DeviceConfDic[i-1]['Device'] == gl.DeviceList[0]:#PC10
                    Command=PC10Command
                elif gl.DeviceConfDic[i-1]['Device'] == gl.DeviceList[1]:#MP
                    Command=MPCommand
                elif gl.DeviceConfDic[i-1]['Device'] == gl.DeviceList[2]:#CJ
                    Command=CJCommand
                elif gl.DeviceConfDic[i-1]['Device'] == gl.DeviceList[3]:#Dummy
                    Command=DummyCommand
                elif gl.DeviceConfDic[i-1]['Device'] == gl.DeviceList[4]:#OPCUA
                    Command=OPCUACommand
                
                if gl.DeviceConfDic[i-1]['Device'] != gl.DeviceList[3]:#Dummy以外処理 :
                    SocketCommand = Command.Convert(AddressDic[i-1],gl.AllAddDic[i-1],False)
                    if not SocketCommand :
                        messagebox.showinfo('アドレス設定エラー','デバイスNo' + str(i) + 'のChのアドレスを確認してください')
                        return
                RWThread[i-1]=threading.Thread(target=IORWdef, daemon=True,args=(AddressDic[i-1],gl.AllAddDic[i-1],i-1,Command))

        #接続処理開始
        #=========================================================================調整のためｺﾒﾝﾄｱｳﾄ
        #if gl.DeviceConfDic[DeviceNo]['Device'] != "ﾀﾞﾐｰ(接続先無)":#Dummy以外処理 :
        if not ConectTest.Test():
            return

        #設定をDBにﾊﾞｯｸｱｯﾌﾟ
        DB.BackUp()
        
        #フォーム無効化処理
        gl.app.RWStartButton['text']='IO_R/W停止'
        gl.app.changePageButton['state']='disabled'
        gl.app.SensorConfButton['state']='disabled'
        gl.app.IOClearConfButton['state']='disabled'
        for i in gl.EnableCh:
            gl.app.DeviceNoCombo[i-1]['state']='disabled'
            gl.app.AddressText[i-1]['state']='disabled'
            gl.app.VarTypecombo[i-1]['state']='disabled'
            gl.app.ValueUpButton[i-1]['state']='normal'
            gl.app.ValueDownButton[i-1]['state']='normal'

        gl.app.Periodcombo.current(0)

        #センサー辞書初期化
        gl.EdgeSensorDic={}
        gl.DancerDic={}
        gl.TensionMeterDic={}
        gl.DiameterSensorDic={}
        
        #起動中
        gl.IORWBusy = True
        #RWThread = []
        for i in gl.EnableDevice:
            if DeviceListDic[i-1]['DeviceCnt'] != 0:

                RWThread[i-1].start()
            
        ### フォームへの値反映をメインスレッドで実行
        gl.app.after(0, ValueUpdate)

    else :
        gl.IORWBusy = False
        gl.TraceFlag = False
        gl.app.RWStartButton['text']='IO_R/W開始'
        gl.app.TraceButton['text']='ﾄﾚｰｽ開始'
        gl.app.changePageButton['state']='normal'
        gl.app.SensorConfButton['state']='normal'
        gl.app.IOClearConfButton['state']='normal'
        for i in gl.EnableCh:
            gl.app.DeviceNoCombo[i-1]['state']='normal'
            gl.app.AddressText[i-1]['state']='normal'
            gl.app.VarTypecombo[i-1]['state']='normal'
            gl.app.ValueUpButton[i-1]['state']='disabled'
            gl.app.ValueDownButton[i-1]['state']='disabled'
        gl.app.ScanTime['text'] = '0'

        
### IO読書
def IORWdef(ArrayAddress,AddDic,DeviceNo,Command):
    
    if gl.DeviceConfDic[DeviceNo]['Device'] != "ﾀﾞﾐｰ(接続先無)":#Dummy以外処理 :

        host = gl.DeviceConfDic[DeviceNo]['IPAddress']
        port = int(gl.DeviceConfDic[DeviceNo]['Port'])
        ReadCommand = Command.Convert(ArrayAddress,AddDic,False)
        #=========================================================================調整のためｺﾒﾝﾄｱｳﾄ
        
        if gl.DeviceConfDic[DeviceNo]['Device'] != gl.DeviceList[4] :#Socket処理
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            time.sleep(0.1)#これ抜くと安川がSendで接続切られる
            client.settimeout(1)#レシーブ時1Sでタイムアウト
            client.connect((host, port))
            
            if gl.DeviceConfDic[DeviceNo]['Device'] == gl.DeviceList[2]:#CJだけ最初に別処理
                gl.CJMemory = ''
                gl.CJMinAddress = 6144
                gl.CJMaxAddress = 0
                client.send(bytes.fromhex(gl.CJInitHeader))
                Response = client.recv(1024)
                if len(Response.hex()) != 24*2 or Response.hex()[12*2:16*2] != '00000000' :
                    messagebox.showinfo('CJInitレスポンスエラー','読込結果がエラーでした。宮崎に言ってください') 
                    return
                gl.CJMyIP = Response.hex()[19*2:20*2]
                gl.CJHeader[3] = gl.CJMyIP
                
            ReadCommand = Command.Convert(ArrayAddress,AddDic,False)#別処理でコマンド消えるから再生成

        elif gl.DeviceConfDic[DeviceNo]['Device'] == gl.DeviceList[4] :#OPCUA

            url = f"opc.tcp://{host}:{port}/"
            client = Client(url=url)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try :
                loop.run_until_complete(client.connect())
            except Exception as e:
                print(f"接続エラー: {e}")
                
            objects = client.get_objects_node()
            children = loop.run_until_complete(objects.get_children())
            objects = client.nodes.objects
            user_ns_candidates = set()
                    
            # 子ノードを探索
            for child in children:
                try:   # ←【追加】子ノード探索エラーハンドリング
                    grand_children = loop.run_until_complete(child.get_children())
                    for node in grand_children:
                        try:   # ←【追加】ノード判定エラーハンドリング
                            node_class = loop.run_until_complete(node.read_node_class())
                            if node_class == ua.NodeClass.Variable:
                                ns_idx = node.nodeid.NamespaceIndex
                                print("変数ノード発見:", node, "NodeId:", node.nodeid)
                                if ns_idx != 0:
                                    user_ns_candidates.add(ns_idx)
                                    print("ユーザー変数が存在するNamespaceIndex:", user_ns_candidates)
                        except Exception as e:
                            print(f"ノード判定エラー: {e}")
                except Exception as e:
                    print(f"子ノード取得エラー: {e}")

            # 最初に見つかったユーザー名前空間を採用
            if user_ns_candidates:
                ns_index = list(user_ns_candidates)[0]
                print("選択された ns_index:", ns_index)
            else :
                messagebox.showinfo('エラー', '変数が見つかりません')
                return
            ReadCommand = Command.get_node(client,ReadCommand,ns_index,False)
                
        
        #最初の読込
    if gl.DeviceConfDic[DeviceNo]['Device'] != "ﾀﾞﾐｰ(接続先無)":#Dummy以外処理 :
        if gl.DeviceConfDic[DeviceNo]['Device'] != gl.DeviceList[4] :#Socket
            client.send(ReadCommand)
            Response = client.recv(1024)
            if not Command.ValueCheck(Response)  :
                messagebox.showinfo('レスポンスエラー1','読込結果がエラーでした。宮崎に言ってください') 
                return
        elif gl.DeviceConfDic[DeviceNo]['Device'] == gl.DeviceList[4] :#OPCUA
            try :
                Response = loop.run_until_complete(client.read_values(ReadCommand))
            except Exception as e:
                print(f"読み出しエラー: {e}")
            Result = Command.ValueCheck(Response,ArrayAddress)
            if Result != ""  :
                messagebox.showinfo('読み込みエラー1',f'[{Result}]の読込結果がNone(読込失敗)でした。変数名を確認してください') 
                return

        Command.ValueGet(ArrayAddress,AddDic,Response)
    #else:#Dummy処理
        

    #初期値反映
    for n in range(len(ArrayAddress)):
        if ArrayAddress[n] != '':
            if gl.app.InitValueText[AddDic[ArrayAddress[n]]['Ch']].get() != '':#初期値テキストありなら反映
                AddDic[ArrayAddress[n]]['WVal'] = float(gl.app.InitValueText[AddDic[ArrayAddress[n]]['Ch']].get())
                AddDic[ArrayAddress[n]]['WFlag'] = True
            else :
                AddDic[ArrayAddress[n]]['WVal'] = AddDic[ArrayAddress[n]]['RVal']

    if gl.DeviceConfDic[DeviceNo]['Device'] != "ﾀﾞﾐｰ(接続先無)":#Dummy以外処理 :
        #初期値書き込み
        WriteCommand = Command.Convert(ArrayAddress,AddDic,True)
        if WriteCommand != '':
            if gl.DeviceConfDic[DeviceNo]['Device'] != gl.DeviceList[4] :#Socket
                client.send(WriteCommand)
                Response = client.recv(1024)
                if not Command.ValueCheck(Response)  :
                    messagebox.showinfo('レスポンスエラー2','書込結果がエラーでした。宮崎に言ってください') 
                    return
            elif gl.DeviceConfDic[DeviceNo]['Device'] == gl.DeviceList[4] :#OPCUA
                WriteCommand = Command.get_node(client,WriteCommand,ns_index,True)
                if WriteCommand != []:
                    nodes,write_values = zip(*WriteCommand)
                    try :
                        loop.run_until_complete(client.write_values(nodes, write_values))
                    except Exception as e:
                        print(f"書き込みエラー: {e}")
                
        
    now = time.time()
    
    while gl.IORWBusy:
        
        if gl.DeviceConfDic[DeviceNo]['Device'] != "ﾀﾞﾐｰ(接続先無)":#Dummy以外処理 :
            if gl.DeviceConfDic[DeviceNo]['Device'] != gl.DeviceList[4] :#Socket
                try:
                    client.send(ReadCommand)
                    Response = client.recv(1024)
                except (socket.timeout, ConnectionResetError, OSError) as e:
                    messagebox.showinfo('通信エラー', f'デバイスNo{DeviceNo+1}との通信が切断されました。\n({e})')
                    break
                if not Command.ValueCheck(Response)  :
                    messagebox.showinfo('レスポンスエラー3','読込結果がエラーでした。宮崎に言ってください') 
                    return
            elif gl.DeviceConfDic[DeviceNo]['Device'] == gl.DeviceList[4] :#OPCUA
                try :
                    Response = loop.run_until_complete(client.read_values(ReadCommand))
                except Exception as e:
                    print(f"読み出しエラー: {e}")
                Result = Command.ValueCheck(Response,ArrayAddress)
                if Result != ""  :
                    messagebox.showinfo('読み込みエラー3',f'[{Result}]の読込結果がNone(読込失敗)でした。変数名を確認してください') 
                    return


        else:
            Response = ""
        Command.ValueGet(ArrayAddress,AddDic,Response)
        
        SensorCorrect(time.time())

        if gl.DeviceConfDic[DeviceNo]['Device'] != "ﾀﾞﾐｰ(接続先無)":#Dummy以外処理 :

            WriteCommand = Command.Convert(ArrayAddress,AddDic,True)
        
            if WriteCommand != '':
                if gl.DeviceConfDic[DeviceNo]['Device'] != gl.DeviceList[4] :#Socket
                    try:
                        client.send(WriteCommand)
                        Response = client.recv(1024)
                    except (socket.timeout, ConnectionResetError, OSError) as e:
                        messagebox.showinfo('通信エラー', f'デバイスNo{DeviceNo+1}との通信が切断されました。\n({e})')
                        break
                    if not Command.ValueCheck(Response)  :
                        messagebox.showinfo('レスポンスエラー4','書込結果がエラーでした。宮崎に言ってください') 
                        return

                elif gl.DeviceConfDic[DeviceNo]['Device'] == gl.DeviceList[4] :#OPCUA
                    WriteCommand = Command.get_node(client,WriteCommand,ns_index,True)
                    if WriteCommand != []:
                        nodes,write_values = zip(*WriteCommand)
                        nodes = list(nodes)
                        write_values = list(write_values)
                        try :
                            loop.run_until_complete(client.write_values(nodes, write_values))
                        except Exception as e:
                            print(f"書き込みエラー: {e}")

        elif gl.DeviceConfDic[DeviceNo]['Device'] == "ﾀﾞﾐｰ(接続先無)":#Dummy処理 :
            WriteCommand = Command.Convert(ArrayAddress,AddDic,True)
        
        #ｽｷｬﾝﾀｲﾑ
        gl.Period[DeviceNo] = '{:.01f}'.format((time.time()-now)*1000)
        now = time.time()
        if int(gl.app.Periodcombo.get())-1 == DeviceNo :
            gl.app.ScanTime['text']=gl.Period[DeviceNo]
        #待ち(他スレッドへ処理を譲る)
        time.sleep(0.001)
    
    if gl.DeviceConfDic[DeviceNo]['Device'] != "ﾀﾞﾐｰ(接続先無)":#Dummy以外処理 :
        #終了後の処理
        if gl.DeviceConfDic[DeviceNo]['Device'] != gl.DeviceList[4] :#Socket
            client.close()
        elif gl.DeviceConfDic[DeviceNo]['Device'] == gl.DeviceList[4] :#OPCUA
            loop.run_until_complete(client.disconnect())
    

def ValueUpdate():
    if not gl.IORWBusy:
        return
    ## ﾌｫｰﾑの値変更
    for i in gl.EnableCh:
        if gl.app.DeviceNoCombo[i-1].get() != '':
            if gl.ValueText[i-1] != gl.AllAddDic[int(gl.app.DeviceNoCombo[i-1].get())-1][gl.app.AddressText[i-1].get()]['RVal'] :
                if not gl.ValueTextFocus[i-1] :
                    gl.ValueText[i-1].set(gl.AllAddDic[int(gl.app.DeviceNoCombo[i-1].get())-1][gl.app.AddressText[i-1].get()]['RVal'])
    gl.app.after(16, ValueUpdate)  # 約60fps(16ms)でUIを更新


def SensorCorrect(now):
    
    for idx in gl.EnableSensor:
        i = idx - 1  # 0-based index
        if gl.SensorConfDic[i]['Sensor'] == gl.SensorList[0] :
            SenProc.EdgeSensor(i,now)
        elif gl.SensorConfDic[i]['Sensor'] == gl.SensorList[1] or gl.SensorConfDic[i]['Sensor'] == gl.SensorList[2] :
            SenProc.Dancer(i,gl.SensorConfDic[i]['Sensor'] == gl.SensorList[2],now)
        elif gl.SensorConfDic[i]['Sensor'] == gl.SensorList[3] or gl.SensorConfDic[i]['Sensor'] == gl.SensorList[4] :
            SenProc.TensionMeter(i,gl.SensorConfDic[i]['Sensor'] == gl.SensorList[4],now)
        elif gl.SensorConfDic[i]['Sensor'] == gl.SensorList[5] :
            SenProc.DiameterSensor(i,now)
        elif gl.SensorConfDic[i]['Sensor'] == gl.SensorList[6] :
            SenProc.Equal(i,now)
        elif gl.SensorConfDic[i]['Sensor'] == gl.SensorList[7] :
            SenProc.BitCalcOut(i,now)

def BackUp():
    #変数に値格納
    for i in range(gl.ChMax):
        currentVal = ''
        try:
            if isinstance(gl.IOConfDic[i], dict):
                currentVal = gl.IOConfDic[i].get('CurrentVal', '')
            deviceNo = gl.app.DeviceNoCombo[i].get()
            address = gl.app.AddressText[i].get()
            if deviceNo != '' and address != '':
                dn = int(deviceNo) - 1
                if dn in gl.AllAddDic and address in gl.AllAddDic[dn]:
                    currentVal = str(gl.AllAddDic[dn][address]['WVal'])
        except (ValueError, KeyError, TypeError):
            pass
        gl.IOConfDic[i] = {'DeviceNo':gl.app.DeviceNoCombo[i].get(),'Address':gl.app.AddressText[i].get(),'Init':gl.app.InitValueText[i].get(),\
                        'UpDown':gl.app.UDValueText[i].get(),'Comment':gl.app.CommentText[i].get(),'VarType':gl.app.VarTypecombo[i].get(),'AI0':gl.app.AI0ValueText[i].get(),\
                        'AI100':gl.app.AI100ValueText[i].get(),'User0':gl.app.User0ValueText[i].get(),'User100':gl.app.User100ValueText[i].get(),\
                        'CurrentVal':currentVal}

def EnableCheck():
    
    gl.EnableCh=[]
    for i in range(gl.ChMax) :
        if gl.IOConfDic[i]['DeviceNo'] != '' or gl.IOConfDic[i]['Address'] != '' :
            if gl.IOConfDic[i]['DeviceNo'] == '' or gl.IOConfDic[i]['Address'] == '' :
                messagebox.showinfo('エラー','Ch'+str(i+1)+'のデバイスかアドレスが入力されていません。') 
                return
            if gl.IOConfDic[i]['VarType'] == '':
                messagebox.showinfo('エラー','Ch'+str(i+1)+'のデータ型が入力されていません。') 
                return
            if True in [gl.IOConfDic[i]['AI0']=='',gl.IOConfDic[i]['AI100']=='',\
                        gl.IOConfDic[i]['User0']=='',gl.IOConfDic[i]['User100']==''] :
                if False in [gl.IOConfDic[i]['AI0']=='',gl.IOConfDic[i]['AI100']=='',\
                        gl.IOConfDic[i]['User0']=='',gl.IOConfDic[i]['User100']==''] :
                    messagebox.showinfo('エラー','Ch'+str(i+1)+'のAI値User値の入力がまばらです。\n削除または入力してください。') 
                    return
                    
            gl.EnableCh.append(i+1)
    
    return True
