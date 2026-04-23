import math
import TCPGlobalVar as gl
import PIDControl as PID
iscloseNo = 0.00000001#センサーの読込値と書込み値の近似値判定範囲 大きい方が緩い

def _get_device_no(idx):
    combo = gl.app.DeviceNoCombo[idx]
    if combo is None:
        return None
    return int(combo.get()) - 1

def EdgeSensor(i,now):

    In1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In1'])-1)
    if In1DeviceNo is None:
        return
    In1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In1'])-1].get()
    if gl.SensorConfDic[i]['Out1'] != '' :
        Out1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out1'])-1)
        if Out1DeviceNo is None:
            return
        Out1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out1'])-1].get()
    if gl.SensorConfDic[i]['Out2'] != '' :
        Out2DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out2'])-1)
        if Out2DeviceNo is None:
            return
        Out2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out2'])-1].get()
        
    #桁合わせ処理
    if math.isclose(gl.AllAddDic[In1DeviceNo][In1Address]['RVal'],gl.AllAddDic[In1DeviceNo][In1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['WVal']#AI変換誤差無視の為
    else:
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['RVal']
    if gl.SensorConfDic[i]['DigitsCoef'] != '':
        In1Val = In1Val * float(gl.SensorConfDic[i]['DigitsCoef'])
        
    #現在位置
    if gl.SensorConfDic[i]['Out1'] != '' :
        #if math.isclose(gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal'],gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal']#AI変換誤差無視の為
        #else:
        #    Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal']
    if gl.SensorConfDic[i]['Out2'] != '' :
        #if math.isclose(gl.AllAddDic[Out2DeviceNo][Out2Address]['RVal'],gl.AllAddDic[Out2DeviceNo][Out2Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        Out2Val = gl.AllAddDic[Out2DeviceNo][Out2Address]['WVal']#AI変換誤差無視の為
        #else:
        #    Out2Val = gl.AllAddDic[Out2DeviceNo][Out2Address]['RVal']

    #初期値記憶
    if i in gl.EdgeSensorDic :
        if gl.EdgeSensorDic[i]['Init'] != True :
            gl.EdgeSensorDic[i]={'Init':True,'In1PreVal':In1Val}
            return
    else:
        gl.EdgeSensorDic[i]={'Init':True,'In1PreVal':In1Val}
        return
        
    #変化値算出
    CalcVal = In1Val - gl.EdgeSensorDic[i]['In1PreVal'] 
    
    #比率
    if gl.SensorConfDic[i]['Ratio'] !='':
        CalcVal = CalcVal * float(gl.SensorConfDic[i]['Ratio'])

    #揺動直行変換
    if gl.SensorConfDic[i]['CalcCoef'] != '' :
        if gl.SensorConfDic[i]['CalcCoef'] != 1 :
            CalcVal = math.tan(math.radians(CalcVal))*float(gl.SensorConfDic[i]['CalcCoef'])#揺動半径から、直行移動量を算出

    #前回値更新
    gl.EdgeSensorDic[i]['In1PreVal'] = In1Val

    #処理要否
    if CalcVal == 0 :
        return    

    #反転
    if gl.SensorConfDic[i]['Out1'] != '' :
        if  not gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] :#テキストボックス直打ち実施有無判定
            if gl.SensorConfDic[i]['Out1Inv'] :#補正反転で軸+でｾﾝｻ+
                gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = Out1Val + CalcVal
            else:
                gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = Out1Val - CalcVal
            gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] = True
    if gl.SensorConfDic[i]['Out2'] != '' :
        if not gl.AllAddDic[Out2DeviceNo][Out2Address]['WFlag'] :#テキストボックス直打ち実施有無判定
            if gl.SensorConfDic[i]['Out2Inv'] :
                gl.AllAddDic[Out2DeviceNo][Out2Address]['WVal'] = Out2Val + CalcVal
            else:
                gl.AllAddDic[Out2DeviceNo][Out2Address]['WVal'] = Out2Val - CalcVal
            gl.AllAddDic[Out2DeviceNo][Out2Address]['WFlag'] = True
            


def Dancer(i,flag,now):

    if not flag :#径演算付きではない
        In1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In1'])-1)#自軸
        if In1DeviceNo is None:
            return
        In1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In1'])-1].get()
        In2DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In2'])-1)#参照
        if In2DeviceNo is None:
            return
        In2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In2'])-1].get()
    else:
        DiameterNo = int(gl.SensorConfDic[i]['In1'])-1
        In1DeviceNo = _get_device_no(int(gl.SensorConfDic[DiameterNo]['In1'])-1)#自軸
        if In1DeviceNo is None:
            return
        In1Address = gl.app.AddressText[int(gl.SensorConfDic[DiameterNo]['In1'])-1].get()
        In2DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In2'])-1)#参照軸
        if In2DeviceNo is None:
            return
        In2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In2'])-1].get()
        In3DeviceNo = _get_device_no(int(gl.SensorConfDic[DiameterNo]['Out1'])-1)#径センサ
        if In3DeviceNo is None:
            return
        In3Address = gl.app.AddressText[int(gl.SensorConfDic[DiameterNo]['Out1'])-1].get()

        if gl.SensorConfDic[DiameterNo]['In2'] != '' :#径演算径Ch選択有
            In4DeviceNo = _get_device_no(int(gl.SensorConfDic[DiameterNo]['In2'])-1)
            if In4DeviceNo is None:
                return
            In4Address = gl.app.AddressText[int(gl.SensorConfDic[DiameterNo]['In2'])-1].get()

    Out1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out1'])-1)
    if Out1DeviceNo is None:
        return
    Out1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out1'])-1].get()

    #桁合わせ処理
    if math.isclose(gl.AllAddDic[In1DeviceNo][In1Address]['RVal'],gl.AllAddDic[In1DeviceNo][In1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['WVal']#AI変換誤差無視の為
    else:
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['RVal']
    if math.isclose(gl.AllAddDic[In2DeviceNo][In2Address]['RVal'],gl.AllAddDic[In2DeviceNo][In2Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In2Val = gl.AllAddDic[In2DeviceNo][In2Address]['WVal']#AI変換誤差無視の為
    else:
        In2Val = gl.AllAddDic[In2DeviceNo][In2Address]['RVal']

    if not flag :#径演算付きではない
        if gl.SensorConfDic[i]['DigitsCoef'] != '':
            In1Val = In1Val * float(gl.SensorConfDic[i]['DigitsCoef'])
            In2Val = In2Val * float(gl.SensorConfDic[i]['DigitsCoef'])
    else:
        if gl.SensorConfDic[i]['DigitsCoef'] != '':
            In1Val = In1Val * float(gl.SensorConfDic[DiameterNo]['DigitsCoef'])
        if gl.SensorConfDic[i]['DigitsCoef'] != '':
            In2Val = In2Val * float(gl.SensorConfDic[i]['DigitsCoef'])
        #if math.isclose(gl.AllAddDic[In3DeviceNo][In3Address]['RVal'],gl.AllAddDic[In3DeviceNo][In3Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In3Val = gl.AllAddDic[In3DeviceNo][In3Address]['WVal']#AI変換誤差無視の為
        #else:
        #    In3Val = gl.AllAddDic[In3DeviceNo][In3Address]['RVal']

        if gl.SensorConfDic[DiameterNo]['In2'] != '' :#径演算径Ch選択有
            if math.isclose(gl.AllAddDic[In4DeviceNo][In4Address]['RVal'],gl.AllAddDic[In4DeviceNo][In4Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
                In4Val = gl.AllAddDic[In4DeviceNo][In4Address]['WVal']#AI変換誤差無視の為
            else:
                In4Val = gl.AllAddDic[In4DeviceNo][In4Address]['RVal']

    #現在角度
    #if math.isclose(gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal'],gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
    Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal']#AI変換誤差無視の為
    #else:
    #    Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal']

    #自軸速度変換(最小径速度→現在径速度)
    if flag :#径演算付き
        if gl.SensorConfDic[DiameterNo]['In2'] != '' :#径演算径Ch選択有
            if In4Val!=0:
                In1Val = In3Val / In4Val * In1Val
        else:
            In1Val = In3Val / float(gl.SensorConfDic[DiameterNo]['Ratio']) * In1Val

    #初期値記憶
    if i in gl.DancerDic :
        if gl.DancerDic[i]['Init'] != True :
            gl.DancerDic[i]={'Init':True,'In1PreVal':In1Val,'In2PreVal':In2Val,'PreTime':now,'Out1PreVal':0}
            return
    else:
        gl.DancerDic[i]={'Init':True,'In1PreVal':In1Val,'In2PreVal':In2Val,'PreTime':now,'Out1PreVal':0}
        return
    
    #変化値算出
    #if flag :#径演算付き
        #if gl.DiameterSensorDic[DiameterNo]['Out1PreVal'] != 0 and In3Val != 0 :
            #In1Val = In3Val /gl.DiameterSensorDic[DiameterNo]['Out1PreVal'] * In1Val #今回径/前回径 * 速度
            #In1Val = In3Val / float(gl.SensorConfDic[i]['Ratio'])

    CalcVal = In1Val - In2Val#自軸-参照軸
    CalcVal = (CalcVal + gl.DancerDic[i]['In1PreVal'] - gl.DancerDic[i]['In2PreVal'])/2#前回値との平均 正式な速度
    Time = now - gl.DancerDic[i]['PreTime']#前回からの経過時間
    CalcVal = CalcVal * Time #箔の出量
    CalcVal = CalcVal / 2 #動滑車の原理で移動距離半分
    if gl.SensorConfDic[i]['CalcCoef'] != "":
        if float(gl.SensorConfDic[i]['CalcCoef']) != 1 :
            CalcVal = math.degrees(math.atan(CalcVal / float(gl.SensorConfDic[i]['CalcCoef'])))#ﾀﾞﾝｻｰ半径から、角度を算出

    #比率
    #if gl.SensorConfDic[i]['Ratio'] !='':
    #    CalcVal = CalcVal * float(gl.SensorConfDic[i]['Ratio'])

    #前回値更新
    gl.DancerDic[i]['In1PreVal'] = In1Val
    gl.DancerDic[i]['In2PreVal'] = In2Val
    gl.DancerDic[i]['PreTime'] = now

    #処理要否
    if CalcVal == 0 :
        return

    #反転
    if not gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] :
        if gl.SensorConfDic[i]['Out1Inv'] :
            gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = Out1Val - CalcVal
        else:
            gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = Out1Val + CalcVal
        gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] = True



def TensionMeter(i,flag,now):
    
    if not flag :#径演算付きではない
        In1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In1'])-1)#自軸
        if In1DeviceNo is None:
            return
        In1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In1'])-1].get()
        In2DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In2'])-1)#参照
        if In2DeviceNo is None:
            return
        In2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In2'])-1].get()
    else:
        DiameterNo = int(gl.SensorConfDic[i]['In1'])-1
        In1DeviceNo = _get_device_no(int(gl.SensorConfDic[DiameterNo]['In1'])-1)#自軸
        if In1DeviceNo is None:
            return
        In1Address = gl.app.AddressText[int(gl.SensorConfDic[DiameterNo]['In1'])-1].get()
        In2DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In2'])-1)#参照軸
        if In2DeviceNo is None:
            return
        In2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In2'])-1].get()
        In3DeviceNo = _get_device_no(int(gl.SensorConfDic[DiameterNo]['Out1'])-1)#径センサ
        if In3DeviceNo is None:
            return
        In3Address = gl.app.AddressText[int(gl.SensorConfDic[DiameterNo]['Out1'])-1].get()

        if gl.SensorConfDic[DiameterNo]['In2'] != '' :#径演算径Ch選択有
            In4DeviceNo = _get_device_no(int(gl.SensorConfDic[DiameterNo]['In2'])-1)#径演算径
            if In4DeviceNo is None:
                return
            In4Address = gl.app.AddressText[int(gl.SensorConfDic[DiameterNo]['In2'])-1].get()

    Out1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out1'])-1)
    if Out1DeviceNo is None:
        return
    Out1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out1'])-1].get()

    #if not flag :#径演算付きではない
        #In1DeviceNo = int(gl.app.DeviceNoCombo[int(gl.SensorConfDic[i]['In1'])-1].get())-1#自軸
        #In1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In1'])-1].get()
        #In2DeviceNo = int(gl.app.DeviceNoCombo[int(gl.SensorConfDic[i]['In2'])-1].get())-1#参照
        #In2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In2'])-1].get()
    #else:
        #DiameterNo = int(gl.SensorConfDic[i]['In1'])-1
        #In1DeviceNo = int(gl.app.DeviceNoCombo[int(gl.SensorConfDic[DiameterNo]['In1'])-1].get())-1#自軸
        #In1Address = gl.app.AddressText[int(gl.SensorConfDic[DiameterNo]['In1'])-1].get()
        #In2DeviceNo = int(gl.app.DeviceNoCombo[int(gl.SensorConfDic[i]['In2'])-1].get())-1#参照軸
        #In2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In2'])-1].get()
        #In3DeviceNo = int(gl.app.DeviceNoCombo[int(gl.SensorConfDic[DiameterNo]['Out1'])-1].get())-1
        #In3Address = gl.app.AddressText[int(gl.SensorConfDic[DiameterNo]['Out1'])-1].get()

    #Out1DeviceNo = int(gl.app.DeviceNoCombo[int(gl.SensorConfDic[i]['Out1'])-1].get())-1
    #Out1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out1'])-1].get()
    
    #桁合わせ処理
    if math.isclose(gl.AllAddDic[In1DeviceNo][In1Address]['RVal'],gl.AllAddDic[In1DeviceNo][In1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['WVal']#AI変換誤差無視の為
    else:
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['RVal']
    if math.isclose(gl.AllAddDic[In2DeviceNo][In2Address]['RVal'],gl.AllAddDic[In2DeviceNo][In2Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In2Val = gl.AllAddDic[In2DeviceNo][In2Address]['WVal']#AI変換誤差無視の為
    else:
        In2Val = gl.AllAddDic[In2DeviceNo][In2Address]['RVal']

    if not flag :#径演算付きではない
        if gl.SensorConfDic[i]['DigitsCoef'] != '':
            In1Val = In1Val * float(gl.SensorConfDic[i]['DigitsCoef'])
            In2Val = In2Val * float(gl.SensorConfDic[i]['DigitsCoef'])
    else:
        if gl.SensorConfDic[i]['DigitsCoef'] != '':
            In1Val = In1Val * float(gl.SensorConfDic[DiameterNo]['DigitsCoef'])
        if gl.SensorConfDic[i]['DigitsCoef'] != '':
            In2Val = In2Val * float(gl.SensorConfDic[i]['DigitsCoef'])
        #if math.isclose(gl.AllAddDic[In3DeviceNo][In3Address]['RVal'],gl.AllAddDic[In3DeviceNo][In3Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In3Val = gl.AllAddDic[In3DeviceNo][In3Address]['WVal']#AI変換誤差無視の為
        #else:
            #In3Val = gl.AllAddDic[In3DeviceNo][In3Address]['RVal']

        if gl.SensorConfDic[DiameterNo]['In2'] != '' :#径演算径Ch選択有
            if math.isclose(gl.AllAddDic[In4DeviceNo][In4Address]['RVal'],gl.AllAddDic[In4DeviceNo][In4Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
                In4Val = gl.AllAddDic[In4DeviceNo][In4Address]['WVal']#AI変換誤差無視の為
            else:
                In4Val = gl.AllAddDic[In4DeviceNo][In4Address]['RVal']

    #if not flag :#径演算付き
        #if gl.SensorConfDic[i]['DigitsCoef'] != '':
            #In1Val = In1Val * float(gl.SensorConfDic[i]['DigitsCoef'])
            #In2Val = In2Val * float(gl.SensorConfDic[i]['DigitsCoef'])
    #else:
        #if gl.SensorConfDic[i]['DigitsCoef'] != '':
            #In1Val = In1Val * float(gl.SensorConfDic[DiameterNo]['DigitsCoef'])
        #if gl.SensorConfDic[i]['DigitsCoef'] != '':
            #In2Val = In2Val * float(gl.SensorConfDic[i]['DigitsCoef'])
        #if math.isclose(gl.AllAddDic[In3DeviceNo][In3Address]['RVal'],gl.AllAddDic[In3DeviceNo][In3Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
            #In3Val = gl.AllAddDic[In3DeviceNo][In3Address]['WVal']#AI変換誤差無視の為
        #else:
            #In3Val = gl.AllAddDic[In3DeviceNo][In3Address]['RVal']

    #現在張力
    #if math.isclose(gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal'],gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
    Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal']#AI変換誤差無視の為
    #else:
        #Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal']

    #自軸速度変換(最小径速度→現在径速度)
    if flag :#径演算付き
        if gl.SensorConfDic[DiameterNo]['In2'] != '' :#径演算径Ch選択有
            if In4Val!=0:
                In1Val = In3Val / In4Val * In1Val
        else:
            In1Val = In3Val / float(gl.SensorConfDic[DiameterNo]['Ratio']) * In1Val

    #現在張力
    #if math.isclose(gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal'],gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        #Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal']#AI変換誤差無視の為
    #else:
        #Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal']

    #初期値記憶
    if i in gl.TensionMeterDic :
        if gl.TensionMeterDic[i]['Init'] != True :
            gl.TensionMeterDic[i]={'Init':True,'In1PreVal':In1Val,'In2PreVal':In2Val,'PreTime':now}
            return
    else:
        gl.TensionMeterDic[i]={'Init':True,'In1PreVal':In1Val,'In2PreVal':In2Val,'PreTime':now}
        return
        
    #変化値算出
    if flag :#径演算付き
        if gl.DiameterSensorDic[DiameterNo]['Out1PreVal'] != 0 and In3Val != 0 :
            In1Val = In3Val /gl.DiameterSensorDic[DiameterNo]['Out1PreVal'] * In1Val #前回径/今回径 * 速度
            
    CalcVal = In2Val - In1Val#参照軸-自軸
    CalcVal = (CalcVal + gl.TensionMeterDic[i]['In2PreVal'] - gl.TensionMeterDic[i]['In1PreVal'])/2#前回値との平均 正式な速度
    Time = now - gl.TensionMeterDic[i]['PreTime']#前回からの経過時間

    CalcVal = CalcVal * Time #箔の出量

    CalcVal = CalcVal * float(gl.SensorConfDic[i]['CalcCoef'])#箔のばね定数から、張力を算出

    #比率
    #if gl.SensorConfDic[i]['Ratio'] !='':
    #    CalcVal = CalcVal * float(gl.SensorConfDic[i]['Ratio'])

    #前回値更新
    gl.TensionMeterDic[i]['In1PreVal'] = In1Val
    gl.TensionMeterDic[i]['In2PreVal'] = In2Val
    gl.TensionMeterDic[i]['PreTime'] = now

    #処理要否
    if CalcVal == 0 :
        return
        
    #反転
    if not gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] :
        if gl.SensorConfDic[i]['Out1Inv'] :
            gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = Out1Val - CalcVal
        else:
            gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = Out1Val + CalcVal
        gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] = True


def DiameterSensor(i,now):
    
    In1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In1'])-1)
    if In1DeviceNo is None:
        return
    In1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In1'])-1].get()
    Out1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out1'])-1)
    if Out1DeviceNo is None:
        return
    Out1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out1'])-1].get()
    
    if gl.SensorConfDic[i]['In2'] != '' :#径演算径Ch選択有
        In2DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In2'])-1)
        if In2DeviceNo is None:
            return
        In2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In2'])-1].get()
    
    #桁合わせ処理
    if math.isclose(gl.AllAddDic[In1DeviceNo][In1Address]['RVal'],gl.AllAddDic[In1DeviceNo][In1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['WVal']#AI変換誤差無視の為
    else:
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['RVal']
    if gl.SensorConfDic[i]['DigitsCoef'] != '':
        In1Val = In1Val * float(gl.SensorConfDic[i]['DigitsCoef'])

    if gl.SensorConfDic[i]['In2'] != '' :#径演算径Ch選択有
        if math.isclose(gl.AllAddDic[In2DeviceNo][In2Address]['RVal'],gl.AllAddDic[In2DeviceNo][In2Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
            In2Val = gl.AllAddDic[In2DeviceNo][In2Address]['WVal']#AI変換誤差無視の為
        else:
            In2Val = gl.AllAddDic[In2DeviceNo][In2Address]['RVal']
    
    #現在径
    #if math.isclose(gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal'],gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
    Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal']#AI変換誤差無視の為
    #else:
    #    Out1Val = gl.AllAddDic[Out1DeviceNo][Out1Address]['RVal']

    #速度変換(最小径速度→現在径速度)
    if gl.SensorConfDic[i]['In2'] != '' :#径演算径Ch選択有
        if In2Val!=0:
            In1Val = Out1Val / In2Val * In1Val
    else:
        In1Val = Out1Val / float(gl.SensorConfDic[i]['Ratio']) * In1Val

    #初期値記憶
    if i in gl.DiameterSensorDic :
        if gl.DiameterSensorDic[i]['Init'] != True :
            gl.DiameterSensorDic[i]={'Init':True,'In1PreVal':In1Val,'Out1PreVal':Out1Val,'PreTime':now}#,'PreCalc':0
            return
    else:
        gl.DiameterSensorDic[i]={'Init':True,'In1PreVal':In1Val,'Out1PreVal':Out1Val,'PreTime':now}#,'PreCalc':0
        return
    
    
    if Out1Val == 0 or In1Val == 0 :
        gl.DiameterSensorDic[i]['In1PreVal'] = In1Val
        gl.DiameterSensorDic[i]['PreTime'] = now
        return
        
    #変化値算出
    CalcVal = In1Val
    CalcVal = (CalcVal + gl.DiameterSensorDic[i]['In1PreVal'])/2#前回値との平均 正式な速度

    Time = now - gl.DiameterSensorDic[i]['PreTime']#前回からの経過時間
    CalcVal = CalcVal * Time #箔の出量
    CalcVal = float(gl.SensorConfDic[i]['CalcCoef']) * CalcVal#厚み×出量で断面積

    #比率
    #if gl.SensorConfDic[i]['Ratio'] !='':
    #    CalcVal = CalcVal * float(gl.SensorConfDic[i]['Ratio'])

    #前回値更新
    gl.DiameterSensorDic[i]['In1PreVal'] = In1Val
    gl.DiameterSensorDic[i]['PreTime'] = now
    gl.DiameterSensorDic[i]['Out1PreVal'] = Out1Val

    #処理要否
    if CalcVal == 0 :
        return
    #print(str(Out1Address) + ':' + str(gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag']))
    #反転　書込み
    if not gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] :#テキストボックス直打ち実施有無判定
        if gl.SensorConfDic[i]['Out1Inv'] :
            CalcVal = (Out1Val/2*Out1Val/2 * math.pi) + CalcVal #径の断面積-箔の出量の面積
        else:
            CalcVal = (Out1Val/2*Out1Val/2 * math.pi) - CalcVal #径の断面積+箔の出量の面積
        CalcVal = math.sqrt(CalcVal / math.pi)*2 #径算出

        gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = CalcVal
        gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] = True



def Equal(i,now):

    In1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In1'])-1)
    if In1DeviceNo is None:
        return
    In1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In1'])-1].get()
    if gl.SensorConfDic[i]['Out1'] != '' :
        Out1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out1'])-1)
        if Out1DeviceNo is None:
            return
        Out1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out1'])-1].get()
    if gl.SensorConfDic[i]['Out2'] != '' :
        Out2DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out2'])-1)
        if Out2DeviceNo is None:
            return
        Out2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out2'])-1].get()
        
    #入力値
    if math.isclose(gl.AllAddDic[In1DeviceNo][In1Address]['RVal'],gl.AllAddDic[In1DeviceNo][In1Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['WVal']#AI変換誤差無視の為
    else:
        In1Val = gl.AllAddDic[In1DeviceNo][In1Address]['RVal']

    #変化値算出
    CalcVal = In1Val
    
    #比率
    if gl.SensorConfDic[i]['Ratio'] !='':
        CalcVal = CalcVal * float(gl.SensorConfDic[i]['Ratio'])

    #オフセット
    if gl.SensorConfDic[i]['DigitsCoef'] != '':#オフセット値
        CalcVal = CalcVal + float(gl.SensorConfDic[i]['DigitsCoef'])


    #反転
    if gl.SensorConfDic[i]['Out1'] != '' :
        if not gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] :
            if gl.SensorConfDic[i]['Out1Inv'] :#補正反転で軸+でｾﾝｻ-
                gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = - CalcVal
            else:
                gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = CalcVal
            gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] = True
    if gl.SensorConfDic[i]['Out2'] != '' :
        if not gl.AllAddDic[Out2DeviceNo][Out2Address]['WFlag'] :
            if gl.SensorConfDic[i]['Out2Inv'] :
                gl.AllAddDic[Out2DeviceNo][Out2Address]['WVal'] = - CalcVal
            else:
                gl.AllAddDic[Out2DeviceNo][Out2Address]['WVal'] =  CalcVal
            gl.AllAddDic[Out2DeviceNo][Out2Address]['WFlag'] = True
            


def BitCalcOut(i,now):
    In2NotFlag = False
    In3NotFlag = False
    WriteFlag = False
    #判定値
    if gl.SensorConfDic[i]['In1'] != '' :
        In1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In1'])-1)
        if In1DeviceNo is None:
            return
        In1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In1'])-1].get()
    
    #出力値
    if gl.SensorConfDic[i]['Out2'] != '' :
        Out1DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out2'])-1)
        if Out1DeviceNo is None:
            return
        Out1Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out2'])-1].get()
    #if gl.SensorConfDic[i]['Out2'] != '' :
    #    Out2DeviceNo = int(gl.app.DeviceNoCombo[int(gl.SensorConfDic[i]['Out2'])-1].get())-1
    #    Out2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out2'])-1].get()

    #OFF時出力値
    if gl.SensorConfDic[i]['In2'] != '' :
        In2DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['In2'])-1)
        if In2DeviceNo is None:
            return
        In2Address = gl.app.AddressText[int(gl.SensorConfDic[i]['In2'])-1].get()

        #入力値
        if math.isclose(gl.AllAddDic[In2DeviceNo][In2Address]['RVal'],gl.AllAddDic[In2DeviceNo][In2Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
            In2Val = gl.AllAddDic[In2DeviceNo][In2Address]['WVal']#AI変換誤差無視の為
        else:
            In2Val = gl.AllAddDic[In2DeviceNo][In2Address]['RVal']
    elif gl.SensorConfDic[i]['CalcCoef'] != '':
        In2Val = float(gl.SensorConfDic[i]['CalcCoef'])
    else:
        In2NotFlag  = True

    #ON時出力値
    if gl.SensorConfDic[i]['Out1'] != '' :
        In3DeviceNo = _get_device_no(int(gl.SensorConfDic[i]['Out1'])-1)
        if In3DeviceNo is None:
            return
        In3Address = gl.app.AddressText[int(gl.SensorConfDic[i]['Out1'])-1].get()

        #入力値
        if math.isclose(gl.AllAddDic[In3DeviceNo][In3Address]['RVal'],gl.AllAddDic[In3DeviceNo][In3Address]['WVal'],abs_tol=iscloseNo) :#近似値なら
            In3Val = gl.AllAddDic[In3DeviceNo][In3Address]['WVal']#AI変換誤差無視の為
        else:
            In3Val = gl.AllAddDic[In3DeviceNo][In3Address]['RVal']
    elif gl.SensorConfDic[i]['Ratio'] != '':
        In3Val = float(gl.SensorConfDic[i]['Ratio'])
    else:
        In3NotFlag = True
    
        
    
    In1Val = int(gl.AllAddDic[In1DeviceNo][In1Address]['RVal'])

    flag = In1Val & 2**int(gl.SensorConfDic[i]['DigitsCoef'])
    
    if not gl.SensorConfDic[i]['Out1Inv'] :#反転
        if flag == 0 :
            if not In2NotFlag:
                #変化値算出
                CalcVal = In2Val
                WriteFlag = True
        else:
            if not In3NotFlag:
                CalcVal = In3Val
                WriteFlag = True
    else:
        if flag != 0 :
            if not In2NotFlag:
                #変化値算出
                CalcVal = In2Val
                WriteFlag = True
        else:
            if not In3NotFlag:
                CalcVal = In3Val
                WriteFlag = True
            
    if not WriteFlag:
        return

    
    #比率
    if gl.SensorConfDic[i]['TimeLag'] !='':
        CalcVal = CalcVal * float(gl.SensorConfDic[i]['TimeLag'])

    #オフセット
    #if gl.SensorConfDic[i]['CalcCoef'] != '':#オフセット値
    #    CalcVal = CalcVal + float(gl.SensorConfDic[i]['CalcCoef'])


    #反転
    #if gl.SensorConfDic[i]['Out1'] != '' :
    #    if gl.SensorConfDic[i]['Out1Inv'] :#補正反転で軸+でｾﾝｻ-
    #        gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = - CalcVal
    #    else:
    if not gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] :
        gl.AllAddDic[Out1DeviceNo][Out1Address]['WVal'] = CalcVal
        gl.AllAddDic[Out1DeviceNo][Out1Address]['WFlag'] = True
    #if gl.SensorConfDic[i]['Out2'] != '' :
    #    if gl.SensorConfDic[i]['Out2Inv'] :
    #        gl.AllAddDic[Out2DeviceNo][Out2Address]['WVal'] = - CalcVal
    #    else:
    #        gl.AllAddDic[Out2DeviceNo][Out2Address]['WVal'] =  CalcVal
    #    gl.AllAddDic[Out2DeviceNo][Out2Address]['WFlag'] = True

