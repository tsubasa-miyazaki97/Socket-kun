from ctypes import addressof
from email.headerregistry import Address
from msilib import datasizemask
from operator import truediv
from pickle import TRUE
import re
import string
from struct import pack,unpack
from urllib import response
import TCPGlobalVar as gl
from tkinter import messagebox
import CommandCommonProcess as ComProc

#以下ﾃﾞｰﾀｻｲｽﾞはByte
SENDCOMMAND_HEADER_DATASIZE = 26#送信ｺﾏﾝﾄﾞﾍｯﾀﾞの総ﾃﾞｰﾀｻｲｽﾞ
SENDCOMMAND_HEADER_IGNORE_DATASIZE = 8#送信ｺﾏﾝﾄﾞで送るﾃﾞｰﾀｻｲｽﾞに含めないﾃﾞｰﾀｻｲｽﾞ

RECEIVE_HEADER_DATASIZE = 26#受信ｺﾏﾝﾄﾞﾍｯﾀﾞの総ﾃﾞｰﾀｻｲｽﾞ
RECEIVE_COMMAND_DATASIZE = 4#受信時のｺﾏﾝﾄﾞﾃﾞｰﾀｻｲｽﾞ

SEND_COMMANDTYPE_DATASIZE = 2#読書のｺﾏﾝﾄﾞ種類のﾃﾞｰﾀｻｲｽﾞ
SEND_IOTYPE_DATASIZE = 1#読書のIO種別のﾃﾞｰﾀｻｲｽﾞ
SEND_STARTADDRESS_DATASIZE = 3#開始アドレスのﾃﾞｰﾀｻｲｽﾞ
SEND_DATACOUNT_DATASIZE = 2#要素数のﾃﾞｰﾀｻｲｽﾞ
SEND_COMMAND_DATASIZE = SEND_COMMANDTYPE_DATASIZE + SEND_IOTYPE_DATASIZE + SEND_STARTADDRESS_DATASIZE + SEND_DATACOUNT_DATASIZE#ﾍｯﾀﾞ以外のｺﾏﾝﾄﾞのﾃﾞｰﾀｻｲｽﾞ

RECEIVE_DATA_EXTRACT_OFFSETSIZE = RECEIVE_HEADER_DATASIZE + RECEIVE_COMMAND_DATASIZE#受信データ内容抜取時のオフセット値

def Convert(ArrayAddres,AddDic,flag) :
    
    #flagで処理変更
    #flag = True  →　Write

    #AddresCount = 0
    command=""
    AddresCommand = ""
    #WordCount = 0
    #LongCount = 0
    BinaryValue = 0
    WMemory = ''

    gl.CJWMinAddress = 6144
    gl.CJWMaxAddress = 0

    if gl.CJMemory =='' or flag :#初回読込か、書込み
        for n in range(len(ArrayAddres)):
            if ArrayAddres[n] != "":
                WordFlag = False
                Addres = ArrayAddres[n]
                AddDevice = Addres[0:3]
                Addres = Addres[3:]

                if AddDic[ArrayAddres[n]]['Var'] == 'Short' or AddDic[ArrayAddres[n]]['Var'] == 'UShort':
                    WordFlag = True
                
                if gl.CJMemory =='':#初回読込だったら
                    if gl.CJMaxAddress <= int(Addres) :
                        if WordFlag :
                            gl.CJMaxAddress = int(Addres)
                        else:
                            gl.CJMaxAddress = int(Addres)+1#2word読み出したいから、要素数に＋１
                    if gl.CJMinAddress >= int(Addres) :
                        gl.CJMinAddress = int(Addres)
                        
                elif AddDic[ArrayAddres[n]]['WFlag'] and flag :#書込みで書込み値ﾌﾗｸﾞありなら
                    if gl.CJWMaxAddress <= int(Addres) :
                        if WordFlag :
                            gl.CJWMaxAddress = int(Addres)
                        else:
                            gl.CJWMaxAddress = int(Addres)+1#2word読み出したいから、要素数に＋１
                    if gl.CJWMinAddress >= int(Addres) :
                        gl.CJWMinAddress = int(Addres)
        if flag and gl.CJWMinAddress <= gl.CJWMaxAddress:
            #書込み用のメモリ格納
            WMemory = gl.CJMemory[(gl.CJWMinAddress-gl.CJMinAddress)*4:(gl.CJWMinAddress-gl.CJMinAddress+gl.CJWMaxAddress-gl.CJWMinAddress+1)*4]

    if flag and WMemory == '':#書込み時ｺﾏﾝﾄﾞ発生ﾁｪｯｸ
        return ''


    for n in range(len(ArrayAddres)):
        if ArrayAddres[n] != "" and (AddDic[ArrayAddres[n]]['WFlag'] or not flag):
            #bitflag = False
            #bittobyte = False
            AddDevice ="" #アドレスの種類(PLC)
            Addres="" #アドレスの数値
            ByteAddres="" #アドレスをコマンド化したもの
            DataType = '' #wordかlongか
            ExNo='' #アドレスの種類(コマンド)

            Addres = ArrayAddres[n]
            Addres = Addres.upper()#小文字を大文字化

            #if Addres.endswith(("L")) :
            #    bittobyte = True 
            #    Addres = Addres.rstrip('L')
            WordFlag = False
            
            if AddDic[ArrayAddres[n]]['Var'] == 'Short' or AddDic[ArrayAddres[n]]['Var'] == 'UShort':
                WordFlag = True
                #WordCount += 1
                #DataType = '02'
            #else :
                #LongCount += 1
                #DataType = '03'

            AddDevice = Addres[0:3]
            Addres = Addres[3:]
            HexAddres = ''
            
            if Addres == "":
                print("アドレスエラー:アドレスに数値無し")
                return

            if AddDevice in ("CIO") :
                if Addres.isdecimal():
                    if int(Addres) < 0 or int(Addres) > 6144 :
                        Addres = ''
                    else:
                         
                        HexAddres=hex(int(Addres))[2:]#0xを撤去
                        ExNo = 'B0'

            if not AddDevice or not HexAddres or not ExNo :
                print("未定義のアドレスエラー:たぶん空白")
                return


            if AddDic[ArrayAddres[n]]['AI0'] != '' :
                ComProc.UserToAI(AddDic,ArrayAddres[n])
            else :
                AddDic[ArrayAddres[n]]['WAIVal'] = AddDic[ArrayAddres[n]]['WVal']

            if flag : #WriteCommand
                BinaryValue = ComProc.WValueConv(ArrayAddres[n],AddDic)
                
                HexValue = BinaryValue.hex()#ﾊﾞｲﾄ配列を16進表記に
                if WordFlag :
                    HexValue = ('0000'+ HexValue)[-4:]#後ろから4文字抜取
                else :
                    HexValue = ('00000000'+ HexValue)[-8:]#後ろから8文字抜取
                HexValue=HexValue[2:4]+HexValue[0:2]+HexValue[6:8]+HexValue[4:6]#並び替え
                if int(Addres) == gl.CJWMinAddress :

                    WMemory = HexValue + WMemory[len(HexValue):]#最小アドレスなら、先頭に値上書き
                else:

                    WMemory = WMemory[:(int(Addres)-gl.CJWMinAddress)*4] + HexValue + WMemory[(int(Addres)-gl.CJWMinAddress)*4+len(HexValue):]#アドレス分オフセットした箇所に上書き

                #AddDic[ArrayAddres[n]]['WhVal'] = HexValue#いちおうDicに格納
                #ByteAddressCommand = ByteAddressCommand + HexValue#ｺﾏﾝﾄﾞの後ろに書きたい値のﾊﾞｲﾄ配列を付与

            #AddressCommandNow = ByteAddressCommand + ExNo + '00'
        AddDic[ArrayAddres[n]]['WFlag'] = False

            #AddresCommand = AddresCommand + ByteAddressCommand #出来たｺﾏﾝﾄﾞ合体
    

    #開始アドレス
    if flag :
        StartAddress = str(hex(gl.CJWMinAddress))
    else:
        StartAddress = str(hex(gl.CJMinAddress))
    #StartAddress = str(gl.CJMinAddress)#アドレスを10進で指定
    StartAddress = StartAddress[2:]#hex表記の'0x'を撤去
    StartAddress = ('0000'+ StartAddress)[-4:]#後ろから4文字抜取
    StartAddress = StartAddress + '00'#ビット情報

    #要素数
    if flag :
        AddressCount = gl.CJWMaxAddress - gl.CJWMinAddress + 1#要素数
    else:
        AddressCount = gl.CJMaxAddress - gl.CJMinAddress + 1#要素数
    AddressCount = str(hex(AddressCount))
    AddressCount = AddressCount[2:]#hex表記の'0x'を撤去
    AddressCount = ('0000'+ AddressCount)[-4:]#後ろから4文字抜取

    #ファンクションコード
    if flag :#書き込み
        FCCommand = '01' + '02'
    else:
        FCCommand = '01' + '01'

    command = FCCommand + ExNo + StartAddress + AddressCount#共通コマンド作成

    if flag :
        command = command + WMemory#gl.CJMemory#書き込み時、書込みﾃﾞｰﾀ付与

    #サイズ
    DataSize = SENDCOMMAND_HEADER_DATASIZE - SENDCOMMAND_HEADER_IGNORE_DATASIZE + SEND_COMMAND_DATASIZE
    if flag :
        DataSize = DataSize + (gl.CJWMaxAddress - gl.CJWMinAddress + 1)*2#1要素につき2byte
    DataSize = str(hex(DataSize))
    DataSize = DataSize[2:]#hex表記の'0x'を撤去
    DataSize = ('00000000'+ DataSize)[-8:]#後ろから8文字抜取
    gl.CJHeader[1] = DataSize

    #CPU番号 2バイト目は未使用
    #CPUNo = '10'+'00'

    #ｱﾄﾞﾚｽ数ｺﾏﾝﾄﾞ化
    #AddressCountCommand = hex(AddresCount)
    #AddressCountCommand = str(AddressCountCommand)[2:]#hex表記の'0x'を撤去
    #AddressCountCommand = ('0000'+ AddressCountCommand)[-4:]#後ろから4文字抜取
    #AddressCountCommand = AddressCountCommand[2:] + AddressCountCommand[:2]

    #ヘッダ以外コマンド合体
    #command = DataCountCommand + FCCommand + CPUNo + AddressCountCommand + AddresCommand

    #CommandLength = int(len(command)/2)+12#ﾊﾞｲﾄ長算出してヘッダ分を足す
    #CommandLength = hex(CommandLength)[2:]#16進にして0xを除去
    #CommandLength = ('0000'+ CommandLength)[-4:]#2ﾊﾞｲﾄに
    #CommandLength = CommandLength[2:] + CommandLength[:2]

    #ヘッダコマンド 11=Memobus 識別番号 送信先チャネル　送信元チャネル 未使用 データ長 未使用*2

    #HeaderCommand='11' + '00' + '00' + '00' + '0000' + CommandLength + '0000' + '0000'

    #ｺﾏﾝﾄﾞ合体
    command = ''.join(gl.CJHeader) + command
    command = bytes.fromhex(command)#ﾊﾞｲﾄ列に変換
    return command

def ValueGet(ArrayAddress,AddDic,Response):

    HexResponse=Response.hex()#扱いやすい？ようにﾊﾞｲﾄ配列を16進に変換
    gl.CJMemory = HexResponse[RECEIVE_DATA_EXTRACT_OFFSETSIZE*2:]

    #抜き取る時の番号
    #WordCount = 0
    #LongCount = 0

    for n in range(len(ArrayAddress)):
        if ArrayAddress[n] != '' :
            if AddDic[ArrayAddress[n]]['Var'] == 'Short' or AddDic[ArrayAddress[n]]['Var'] == 'UShort' :
                #WordCount += 1
                Offset = 4
            else:
                #LongCount += 1
                Offset = 8
            Addres = int(ArrayAddress[n][3:])
            AddressOffset = Addres - gl.CJMinAddress#開始位置からどれだけオフセットするか(WORD)

            HexValue = HexResponse[RECEIVE_DATA_EXTRACT_OFFSETSIZE*2+AddressOffset*4:RECEIVE_DATA_EXTRACT_OFFSETSIZE*2+AddressOffset*4+Offset]#切り出し
            HexValue = HexValue[2:4]+HexValue[0:2]+HexValue[6:8]+HexValue[4:6]
            BinaryValue = bytes.fromhex(HexValue)

            AddValue = ComProc.RValueConv(ArrayAddress[n],AddDic,BinaryValue)
            

            AddDic[ArrayAddress[n]]['RAIVal'] = AddValue
            
            if AddDic[ArrayAddress[n]]['AI0'] != '' :
                ComProc.AIToUser(AddDic,ArrayAddress[n])
            else:
                AddDic[ArrayAddress[n]]['RVal'] = AddDic[ArrayAddress[n]]['RAIVal']
                #AddDic[ArrayAddress[n]]['RhVal'] = HexValue

def ValueCheck(Response) :
    MidResponse = Response.hex()[12*2:]#ヘッダ部除去
    #MidResponse = MidResponse[10:]#LengthとFCとCPU番号除去
    if str(MidResponse).startswith('00000000'):#エラーコードが無いこと
        
        return True

