
from struct import pack,unpack
import TCPGlobalVar as gl
from tkinter import messagebox


def AIToUser(AddDic,Address):
    AI0 = int(AddDic[Address]['AI0'])
    AI100 = int(AddDic[Address]['AI100'])
    User0 = int(AddDic[Address]['User0'])
    User100 = int(AddDic[Address]['User100'])

    if AI100 == AI0 or User100 == User0:
        messagebox.showinfo('スケーリング設定エラー',
            f'アドレス[{Address}]のAIスケールまたはユーザースケールの\n'
            '最大値と最小値が同じ値です。\n'
            'スケーリング設定を確認してください。\nIO_R/Wを停止します。')
        gl.IORWBusy = False
        return

    '''
    if AddDic[Address]['RAIVal'] < AI0 :
        AddDic[Address]['RVal'] = User0
    elif AddDic[Address]['RAIVal'] > AI100 :
        AddDic[Address]['RVal'] = User100
    else :
    '''
    AddDic[Address]['RVal'] = round((AddDic[Address]['RAIVal']-AI0) / ((AI100 - AI0)/(User100-User0)),3) + User0



def UserToAI(AddDic,Address):
    AI0 = int(AddDic[Address]['AI0'])
    AI100 = int(AddDic[Address]['AI100'])
    User0 = int(AddDic[Address]['User0'])
    User100 = int(AddDic[Address]['User100'])

    if User100 == User0:
        messagebox.showinfo('スケーリング設定エラー',
            f'アドレス[{Address}]のユーザースケールの\n'
            '最大値と最小値が同じ値です。\n'
            'スケーリング設定を確認してください。\nIO_R/Wを停止します。')
        gl.IORWBusy = False
        return

    '''
    if AddDic[Address]['WVal'] < User0 :
        AddDic[Address]['WAIVal'] = AI0
    elif AddDic[Address]['WVal'] > User100 :
        AddDic[Address]['WAIVal'] = AI100
    else :
    '''
    AddDic[Address]['WAIVal'] = (AI100 - AI0)/(User100-User0) * (AddDic[Address]['WVal'] - User0) + AI0


def WValueConv(Address,AddDic) :
    BinaryValue = 0
    if AddDic[Address]['WFlag'] == False:
        BinaryValue = pack('h',int(AddDic[Address]['RAIVal']))#2ﾊﾞｲﾄの符号付き整数
        AddDic[Address]['WVal'] = AddDic[Address]['RVal']
    else:
        AddDic[Address]['WFlag'] = False
        if AddDic[Address]['Var'] == 'Short' :#型ごとにﾊﾞｲﾄ配列へ変換
            if int(AddDic[Address]['WAIVal']) >gl.ShortMax or int(AddDic[Address]['WAIVal']) < gl.ShortMin :
                messagebox.showinfo('書込み値ｴﾗｰ','値を'+str(gl.ShortMax) + '~' + str(gl.ShortMin) +'の範囲で入力してください')
                BinaryValue = pack('h',int(AddDic[Address]['RAIVal']))#2ﾊﾞｲﾄの符号付き整数
                AddDic[Address]['WVal'] = AddDic[Address]['RVal']
            else:
                BinaryValue = pack('h',int(AddDic[Address]['WAIVal']))#2ﾊﾞｲﾄの符号付き整数
        elif AddDic[Address]['Var'] == 'UShort':
            if int(AddDic[Address]['WAIVal']) >gl.UShortMax or int(AddDic[Address]['WAIVal']) < gl.UShortMin :
                messagebox.showinfo('書込み値ｴﾗｰ','値を'+str(gl.UShortMax) + '~' + str(gl.UShortMin) +'の範囲で入力してください')
                BinaryValue = pack('H',int(AddDic[Address]['RAIVal']))#2ﾊﾞｲﾄの符号無し整数
                AddDic[Address]['WVal'] = AddDic[Address]['RVal']
            else:
                BinaryValue = pack('H',int(AddDic[Address]['WAIVal']))#2ﾊﾞｲﾄの符号無し整数
        elif AddDic[Address]['Var'] == 'Long':
            if int(AddDic[Address]['WAIVal']) >gl.LongMax or int(AddDic[Address]['WAIVal']) < gl.LongMin :
                messagebox.showinfo('書込み値ｴﾗｰ','値を'+str(gl.LongMax) + '~' + str(gl.LongMin) +'の範囲で入力してください')
                BinaryValue = pack('l',int(AddDic[Address]['RAIVal']))#4ﾊﾞｲﾄの符号付き整数
                AddDic[Address]['WVal'] = AddDic[Address]['RVal']
            else:
                BinaryValue = pack('l',int(AddDic[Address]['WAIVal']))#4ﾊﾞｲﾄの符号付き整数
        elif AddDic[Address]['Var'] == 'ULong':
            if int(AddDic[Address]['WAIVal']) >gl.ULongMax or int(AddDic[Address]['WAIVal']) < gl.ULongMin :
                messagebox.showinfo('書込み値ｴﾗｰ','値を'+str(gl.ULongMax) + '~' + str(gl.ULongMin) +'の範囲で入力してください')
                BinaryValue = pack('L',int(AddDic[Address]['RAIVal']))#4ﾊﾞｲﾄの符号無し整数
                AddDic[Address]['WVal'] = AddDic[Address]['RVal']
            else:
                BinaryValue = pack('L',int(AddDic[Address]['WAIVal']))#4ﾊﾞｲﾄの符号無し整数
        elif AddDic[Address]['Var'] == 'Float':
            BinaryValue = pack('f',float(AddDic[Address]['WAIVal']))#4ﾊﾞｲﾄの実数
        #elif AddDic[Address]['Var'] == 'Float(16bit)':
        #    BinaryValue = pack('e',float(AddDic[Address]['WAIVal']))#2ﾊﾞｲﾄの実数
    return BinaryValue

    
def RValueConv(Address,AddDic,BinaryValue) :
    
    if AddDic[Address]['Var'] == 'Short' :#型ごとにﾊﾞｲﾄ配列へ変換
        AddValue, = unpack('h',BinaryValue)#2ﾊﾞｲﾄの符号付き整数
    elif AddDic[Address]['Var'] == 'UShort':
        AddValue, = unpack('H',BinaryValue)#2ﾊﾞｲﾄの符号無し整数
    elif AddDic[Address]['Var'] == 'Long':
        AddValue, = unpack('l',BinaryValue)#4ﾊﾞｲﾄの符号付き整数
    elif AddDic[Address]['Var'] == 'ULong':
        AddValue, = unpack('L',BinaryValue)#4ﾊﾞｲﾄの符号無し整数
    elif AddDic[Address]['Var'] == 'Float':
        print(Address)
        print(BinaryValue)
        AddValue, = unpack('f',BinaryValue)#4ﾊﾞｲﾄの実数
    #elif AddDic[Address]['Var'] == 'Float(16bit)':
    #    AddValue = unpack('e',BinaryValue)#2ﾊﾞｲﾄの実数
    else:
        AddValue = 0

    return AddValue