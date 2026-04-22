import re
import string
from struct import pack,unpack
import CommandCommonProcess as ComProc


def Convert(ArrayAddres,AddDic,flag) :
    
    #flagで処理変更
    #flag = True  →　Write

    AddresCount = 0
    command=""
    AddresCommand = ""
    WordCount = 0
    LongCount = 0
    
    for n in range(len(ArrayAddres)):
        if ArrayAddres[n] != "" and (AddDic[ArrayAddres[n]]['WFlag'] or not flag):
            bitflag = False
            bittobyte = False
            AddDevice =""
            Addres=""
            ByteAddres=""
            DataType = ''
            ExNo=''

            Addres = ArrayAddres[n]
            Addres = Addres.upper()

            if Addres.endswith(("L")) :
                bittobyte = True 
                Addres = Addres.rstrip('L')
            WordFlag = False
            
            if AddDic[ArrayAddres[n]]['Var'] == 'Short' or AddDic[ArrayAddres[n]]['Var'] == 'UShort':
                WordFlag = True
                WordCount += 1
                DataType = '02'
            else :
                LongCount += 1
                DataType = '03'

            AddDevice = Addres[0:2]
            Addres = Addres[2:]
            
            if Addres == "":
                print("アドレスエラー:アドレスに数値無し")
                return

            if AddDevice in ("MW","ML","MF") :
                if Addres.isdecimal():
                    if int(Addres) < 0 or int(Addres) > 1048575 :
                        Addres = ''
                    else:
                        Addres=hex(int(Addres))[2:]#0xを撤去
                        ExNo = '4D'

            elif AddDevice in ("GW","GL","GF") :
                if Addres.isdecimal():
                    if int(Addres) < 0 or int(Addres) > 2097151 :
                        Addres = ''
                    else:
                        Addres=hex(int(Addres))[2:]
                        ExNo = '47'

            elif AddDevice in ("SW","SL","SF") :
                if len(Addres) == len(re.findall('[' + string.hexdigits + ']', Addres)) :#16進以外含んでないか
                    if int(Addres,16) < 0 or int(Addres,16) > 65535 :
                        Addres = ''
                    else:
                        ExNo = '53'

            elif AddDevice in ("IW","IL","IF") :
                if len(Addres) == len(re.findall('[' + string.hexdigits + ']', Addres)) :#16進以外含んでないか
                    if int(Addres,16) < 0 or int(Addres,16) > 65535 :
                        Addres = ''
                    else:
                        ExNo = '49'

            elif AddDevice in ("OW","OL","OF") :
                if len(Addres) == len(re.findall('[' + string.hexdigits + ']', Addres)) :#16進以外含んでないか
                    if int(Addres,16) < 0 or int(Addres,16) > 65535 :
                        Addres = ''
                    else:
                        ExNo = '4F'
            

            if not AddDevice or not Addres or not ExNo :
                print("未定義のアドレスエラー:たぶん空白")
                return

            '''
            if AddDic[ArrayAddres[n]]['Var'] == 'Short' or AddDic[ArrayAddres[n]]['Var'] == 'UShort':
                if not AddDevice[1]=='W' :
                    print("アドレスと型不一致")
                    return
            if AddDic[ArrayAddres[n]]['Var'] == 'Long' or AddDic[ArrayAddres[n]]['Var'] == 'ULong':
                if not AddDevice[1]=='L' :
                    print("アドレスと型不一致")
                    return
            if AddDic[ArrayAddres[n]]['Var'] == 'Float':
                if not AddDevice[1]=='F' :
                    print("アドレスと型不一致")
                    return
            '''

            AddresCount = AddresCount + 1

            #bitｱﾄﾞﾚｽ時処理
            if bitflag :
                if not bittobyte :
                    print("bitアドレス,Hは未対応です")
                    return
            

            #ｺﾏﾝﾄﾞに変換して最後尾に足していく
            ByteAddres = ('00000000'+ Addres)[-8:]#後ろから8文字抜取
            ByteAddres = ByteAddres[6:] + ByteAddres[4:6] + ByteAddres[2:4] + ByteAddres[:2]#LL,LH,HL,HHに並び替え
            ByteAddressCommand =  ExNo + DataType + ByteAddres

            if AddDic[ArrayAddres[n]]['AI0'] != '' :
                ComProc.UserToAI(AddDic,ArrayAddres[n])
            else :
                AddDic[ArrayAddres[n]]['WAIVal'] = AddDic[ArrayAddres[n]]['WVal']

            if flag : #WriteCommand
                BinaryValue = ComProc.WValueConv(ArrayAddres[n],AddDic)
                
                HexValue = BinaryValue.hex()#ﾊﾞｲﾄ配列を16進表記に
                #AddDic[ArrayAddres[n]]['WhVal'] = HexValue#いちおうDicに格納
                ByteAddressCommand = ByteAddressCommand + HexValue#ｺﾏﾝﾄﾞの後ろに書きたい値のﾊﾞｲﾄ配列を付与

            #AddressCommandNow = ByteAddressCommand + ExNo + '00'

            AddresCommand = AddresCommand + ByteAddressCommand #出来たｺﾏﾝﾄﾞ合体
        AddDic[ArrayAddres[n]]['WFlag'] = False

    if flag and AddresCommand == '':#書込み時ｺﾏﾝﾄﾞ発生ﾁｪｯｸ
        return ''

    #ﾃﾞｰﾀﾊﾞｲﾄ数ｺﾏﾝﾄﾞ化
    if flag :
        DataCountCommand = hex(WordCount*8+LongCount*10+6)
    else:
        DataCountCommand = hex(AddresCount*6+6)
    DataCountCommand = str(DataCountCommand[2:])#hex表記の'0x'を撤去
    DataCountCommand = ('0000'+ DataCountCommand)[-4:]#後ろから4文字抜取
    DataCountCommand = DataCountCommand[2:] + DataCountCommand[:2]

    #ファンクションコード
    if flag :#書き込み
        FCCommand = '43' + '4E'
    else:
        FCCommand = '43' + '4D'

    #CPU番号 2バイト目は未使用
    CPUNo = '10'+'00'

    #ｱﾄﾞﾚｽ数ｺﾏﾝﾄﾞ化
    AddressCountCommand = hex(AddresCount)
    AddressCountCommand = str(AddressCountCommand)[2:]#hex表記の'0x'を撤去
    AddressCountCommand = ('0000'+ AddressCountCommand)[-4:]#後ろから4文字抜取
    AddressCountCommand = AddressCountCommand[2:] + AddressCountCommand[:2]

    #ヘッダ以外コマンド合体
    command = DataCountCommand + FCCommand + CPUNo + AddressCountCommand + AddresCommand

    CommandLength = int(len(command)/2)+12#ﾊﾞｲﾄ長算出してヘッダ分を足す
    CommandLength = hex(CommandLength)[2:]#16進にして0xを除去
    CommandLength = ('0000'+ CommandLength)[-4:]#2ﾊﾞｲﾄに
    CommandLength = CommandLength[2:] + CommandLength[:2]

    #ヘッダコマンド 11=Memobus 識別番号 送信先チャネル　送信元チャネル 未使用 データ長 未使用*2

    HeaderCommand='11' + '00' + '00' + '00' + '0000' + CommandLength + '0000' + '0000'

    #ｺﾏﾝﾄﾞ合体
    command = HeaderCommand + command
    command = bytes.fromhex(command)#ﾊﾞｲﾄ列に変換
    
    return command

def ValueGet(ArrayAddress,AddDic,Response):

    HexResponse=Response.hex()#扱いやすい？ようにﾊﾞｲﾄ配列を16進に変換
    
    #抜き取る時の番号
    WordCount = 0
    LongCount = 0

    for n in range(len(ArrayAddress)):
        if ArrayAddress[n] != '' :
            try:
                if AddDic[ArrayAddress[n]]['Var'] == 'Short' or AddDic[ArrayAddress[n]]['Var'] == 'UShort' :
                    WordCount += 1
                    Offset = 4
                else:
                    LongCount += 1
                    Offset = 8
                HexValue = HexResponse[24+16+WordCount*4+LongCount*8-Offset:24+16+WordCount*4+LongCount*8]#切り出し

                BinaryValue = bytes.fromhex(HexValue)

                AddValue = ComProc.RValueConv(ArrayAddress[n],AddDic,BinaryValue)

                AddDic[ArrayAddress[n]]['RAIVal'] = AddValue
                
                if AddDic[ArrayAddress[n]]['AI0'] != '' :
                    ComProc.AIToUser(AddDic,ArrayAddress[n])
                else:
                    AddDic[ArrayAddress[n]]['RVal'] = AddDic[ArrayAddress[n]]['RAIVal']
                    #AddDic[ArrayAddress[n]]['RhVal'] = HexValue
            except Exception as e:
                print(f"ValueGetエラー [{ArrayAddress[n]}]: {e}")

def ValueCheck(Response) :
    MidResponse = Response.hex()[24:]#ヘッダ部除去
    MidResponse = MidResponse[10:]#LengthとFCとCPU番号除去
    if str(MidResponse).startswith('00'):#エラーコードが無いこと
        return True
    return False

