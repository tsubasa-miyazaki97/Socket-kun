import re
import string
from struct import pack,unpack
import CommandCommonProcess as ComProc

def Convert(ArrayAddres,AddDic,flag) :
    
    #flagで処理変更
    #flag = True  →　Write

    AddresCount = 0
    AddresCommand = ""
    command=""
    WordCount = 0
    LongCount = 0
    
    for n in range(len(ArrayAddres)):
        if ArrayAddres[n] != "" and (AddDic[ArrayAddres[n]]['WFlag'] or not flag):
            bitflag = False
            bittobyte = False
            NomalFlag = False
            DRFlag = False
            AddDevice =""
            ByteAddres=""
            Addres=""
            ExNo=""
            DROffset = ''
            Addres = ArrayAddres[n]
            Addres = Addres.upper()

            if Addres.endswith(("L")) :
                bittobyte = True 
                Addres = Addres.rstrip('L')
            WordFlag = False
            if AddDic[ArrayAddres[n]]['Var'] == 'Short' or AddDic[ArrayAddres[n]]['Var'] == 'UShort':
                WordFlag = True
                WordCount += 1
            else :
                LongCount += 1
            

            if not "-" in Addres and Addres.startswith(("P","K","V","T","C","X","Y","M","S","N","R","D")) :
                print("アドレスエラー:P*-無し")
                return

            if Addres.startswith(('P1-','P2-','P3-')) : #P1,P2,P3
                if Addres.startswith("P1-") :
                    ExNo  = "0d"
                    Addres = Addres.replace("P1-","")
                elif Addres.startswith("P2-") :
                    ExNo  = "0e"
                    Addres = Addres.replace("P2-","")
                elif Addres.startswith("P3-") :
                    ExNo  = "0f"
                    Addres = Addres.replace("P3-","")

                AddDevice = Addres[0:1]
                Addres = Addres[1:]
                if Addres == "":
                    print("アドレスエラー:アドレスに数値無し")
                    return

                if  not re.compile(r'P|K|V|T|C|X|Y|M|S|N|R|D').match(AddDevice) :
                    print("アドレスエラー:P*-に続かないアドレス")
                    return

                if AddDevice in ('P','K','V','T','C','X','Y','M','L') :
                    bitflag = True

                if len(Addres) == len(re.findall('[' + string.hexdigits + ']', Addres)) :
                    if bitflag :
                        NomalFlag = int(Addres,16) < int("0x100",16)   
                    else:
                        NomalFlag = int(Addres,16) < int("0x1000",16)
                    

                if AddDevice == "P" :
                    if NomalFlag :
                        ByteAddres = "0000"
                    else :
                        ByteAddres = "C000"
                elif AddDevice == "K" :
                    ByteAddres = "0040"
                elif AddDevice == "V" :
                    if NomalFlag :
                        ByteAddres = "00A0"
                    else :
                        ByteAddres = "C100"
                elif re.compile(r'T|C').match(AddDevice) :
                    if NomalFlag :
                        ByteAddres = "00C0"
                    else :
                        ByteAddres = "C200"
                elif re.compile(r'X|Y').match(AddDevice) :
                    ByteAddres = "0200"
                elif AddDevice == "M" :
                    if NomalFlag :
                        ByteAddres = "0300"
                    else :
                        ByteAddres = "C300"
                elif AddDevice == "S" :
                    if NomalFlag :
                        ByteAddres = "0400"
                    else :
                        ByteAddres = "C800"
                elif AddDevice == "N" :
                    if NomalFlag :
                        ByteAddres = "0C00"
                    else :
                        ByteAddres = "D000"
                elif AddDevice == "R" :
                    ByteAddres = "1000"
                elif AddDevice == "D" :
                    if NomalFlag :
                        ByteAddres = "2000"
                    else :
                        ByteAddres = "4000"
                

            elif Addres.startswith(("EP","EK","EV","ET","EC","EL","EX","EY","EM","ES","EN","H")) :
                ExNo  = "01"
                bitflag = True
                if Addres.startswith("H"):
                    AddDevice = Addres[0:1]
                    Addres = Addres[1:]
                    if Addres == "":
                        print("アドレスエラー:アドレスに数値無し")
                        return
                else :
                    AddDevice = Addres[0:2]
                    Addres = Addres[2:]
                    if Addres == "":
                        print("アドレスエラー:アドレスに数値無し")
                        return

                if AddDevice == "EP" :
                    ByteAddres = "0000"
                elif AddDevice == "EK" :
                    ByteAddres = "0200"
                elif AddDevice == "EV" :
                    ByteAddres = "0400"
                elif re.compile(r'ET|EC').match(AddDevice) :
                    ByteAddres = "0600"
                elif AddDevice == "EL" :
                    ByteAddres = "0700"
                elif re.compile(r'EX|EY').match(AddDevice) :
                    ByteAddres = "0B00"
                elif AddDevice == "EM" :
                    ByteAddres = "0C00"
                elif AddDevice == "ES" :
                    ByteAddres = "1000"
                    bitflag = False
                elif AddDevice == "EN" :
                    ByteAddres = "2000"
                    bitflag = False

                if AddDevice == "H" :
                    ByteAddres = "3000"
                    bitflag = False

            elif Addres.startswith(("GX","GY","GM")) :
                ExNo  = "02"
                bitflag = True
                AddDevice = Addres[0:2]
                Addres = Addres[2:]
                if Addres == "":
                    print("アドレスエラー:アドレスに数値無し")
                    return

                if re.compile(r'GX|GY').match(AddDevice):
                    ByteAddres = "C000"
                elif AddDevice == "GM" :
                    ByteAddres = "E000"

            elif Addres.startswith("U") :
                ByteAddres = "0000"
                AddDevice = Addres[0:1]
                Addres = Addres[1:]
                DRFlag = True
                if Addres == "":
                    print("アドレスエラー:アドレスに数値無し")
                    return
                
                if len(Addres) == len(re.findall('[' + string.hexdigits + ']', Addres)) :
                    if int(Addres,16) < int("0x8000",16) :
                        ExNo  = "03"
                        DROffset = "0x0"
                    elif int(Addres,16) < int("0x10000",16) :
                        ExNo  = "04"
                        DROffset = "0x8000"
                    elif int(Addres,16) < int("0x18000",16) :
                        ExNo  = "05"
                        DROffset = "0x10000"
                    else :
                        ExNo  = "06"
                        DROffset = "0x18000"

            elif Addres.startswith("EB") :
                ByteAddres = "0000"
                AddDevice = Addres[0:2]
                Addres = Addres[2:]
                DRFlag = True
                if Addres == "":
                    print("アドレスエラー:アドレスに数値無し")
                    return

                if len(Addres) == len(re.findall('[' + string.hexdigits + ']', Addres)) :
                    if int(Addres,16) < int("0x8000",16) :
                        ExNo  = "10"
                        DROffset = "0x0"
                    elif int(Addres,16) < int("0x10000",16) :
                        ExNo  = "11"
                        DROffset = "0x8000"
                    elif int(Addres,16) < int("0x18000",16) :
                        ExNo  = "12"
                        DROffset = "0x10000"
                    elif int(Addres,16) < int("0x20000",16) :
                        ExNo  = "13"
                        DROffset = "0x18000"
                    elif int(Addres,16) < int("0x28000",16) :
                        ExNo  = "14"
                        DROffset = "0x20000"
                    elif int(Addres,16) < int("0x30000",16) :
                        ExNo  = "15"
                        DROffset = "0x28000"
                    elif int(Addres,16) < int("0x38000",16) :
                        ExNo  = "16"
                        DROffset = "0x30000"
                    else :
                        ExNo  = "17"
                        DROffset = "0x38000"

            if not AddDevice or not Addres or not ExNo or not ByteAddres  :
                print("未定義のアドレスエラー:たぶん空白")
                return

            AddresCount = AddresCount + 1
            
            if not len(Addres) == len(re.findall('[' + string.hexdigits + ']', Addres)) :
                print("アドレスエラー:アドレスの数値部分が16進ではない")
                return

            #bitｱﾄﾞﾚｽ時処理
            if bitflag :
                if not bittobyte :
                    print("bitアドレス,Hは未対応です")
                    return
            

            #ｺﾏﾝﾄﾞに変換して最後尾に足していく
            if DRFlag :
                ByteAddres = hex(int(str(ByteAddres),16) + (int(str(Addres),16)-int(DROffset,16))*2)
            else :
                if NomalFlag:
                    ByteAddres = hex(int(str(ByteAddres),16) + int(str(Addres),16)*2)
                else:
                    if bitflag:
                        ByteAddres = hex(int(str(ByteAddres),16) + (int(str(Addres),16)-int('100',16))*2)
                    else :
                        ByteAddres = hex(int(str(ByteAddres),16) + (int(str(Addres),16)-int('1000',16))*2)
            ByteAddres = str(ByteAddres[2:])#hex表記の'0x'を撤去
            ByteAddres = ('0000'+ ByteAddres)[-4:]#後ろから4文字抜取
            ByteAddres = ByteAddres[2:] + ByteAddres[:2]
            ByteAddressCommand = ByteAddres + ExNo + '00'

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

            if not WordFlag or LongCount == 0 :#WordだったらLongの前の最後尾
                AddresCommand = AddresCommand + ByteAddressCommand  #ﾛﾝｸﾞなら基本2byteとExNoだから、最後は00
            else:
                
                if not flag :#読込
                    AddresCommand = AddresCommand[:-LongCount*8] + ByteAddressCommand + AddresCommand[-LongCount*8:]
                else:
                    AddresCommand = AddresCommand[:-LongCount*16] + ByteAddressCommand + AddresCommand[-LongCount*16:]
        AddDic[ArrayAddres[n]]['WFlag'] = False
    
    if flag and AddresCommand == '':#書込み時ｺﾏﾝﾄﾞ発生ﾁｪｯｸ
        return ''
        
    #ﾃﾞｰﾀﾊﾞｲﾄ数ｺﾏﾝﾄﾞ化
    if flag :
        DataCountCommand = hex(WordCount*6+LongCount*8+5)
    else:
        DataCountCommand = hex(AddresCount*4+5)
    DataCountCommand = str(DataCountCommand[2:])#hex表記の'0x'を撤去
    DataCountCommand = ('0000'+ DataCountCommand)[-4:]#後ろから4文字抜取
    DataCountCommand = DataCountCommand[2:] + DataCountCommand[:2]

    #ｱﾄﾞﾚｽ数ｺﾏﾝﾄﾞ化
    #Word分
    WordCountCommand = hex(WordCount)
    WordCountCommand = str(WordCountCommand)[2:]#hex表記の'0x'を撤去
    WordCountCommand = ('00'+ WordCountCommand)[-2:]#後ろから2文字抜取
    AddressCountCommand = '0000' + WordCountCommand#ビットとﾊﾞｲﾄの次に付与ﾄ
    #Long分
    LongCountCommand = hex(LongCount)
    LongCountCommand = str(LongCountCommand)[2:]#hex表記の'0x'を撤去
    LongCountCommand = ('00'+ LongCountCommand)[-2:]#後ろから2文字抜取
    AddressCountCommand = AddressCountCommand + LongCountCommand#ﾛﾝｸﾞを最後に付与

    #各ｺﾏﾝﾄﾞ合体
    #0000固定　ｺﾏﾝﾄﾞ以降のﾊﾞｲﾄ数(2byte)　ｺﾏﾝﾄﾞ(1byte)多点読出　ﾛﾝｸﾞのﾃﾞｰﾀ点数(可変)　各ﾊﾞｲﾄｱﾄﾞﾚｽとExNo(可変)
    if not flag :
        command = '0000' + DataCountCommand + 'c4' + AddressCountCommand + AddresCommand
    else :
        command = '0000' + DataCountCommand + 'c5' + AddressCountCommand + AddresCommand
        
    command = bytes.fromhex(command)#ﾊﾞｲﾄ列に変換


    return command

def ValueGet(ArrayAddress,AddDic,Response):

    HexResponse=Response.hex()#扱いやすい？ようにﾊﾞｲﾄ配列を16進に変換
    #WordとLongの総数
    try:
        WordMax = int(HexResponse[14:16],16)
        LongMax = int(HexResponse[16:18],16)#使わんかも
    except Exception as e:
        print(f"ValueGetヘッダ解析エラー: {e}")
        return

    #抜き取る時の番号
    WordCount = 0
    LongCount = 0
    
    for n in range(len(ArrayAddress)):
        if ArrayAddress[n] != '' :
            try:
                if AddDic[ArrayAddress[n]]['Var'] == 'Short' or AddDic[ArrayAddress[n]]['Var'] == 'UShort' :
                    WordCount += 1
                    HexValue = HexResponse[18+WordCount*4-4:18+WordCount*4]#切り出し
                else:
                    LongCount += 1
                    HexValue = HexResponse[18+WordMax*4+LongCount*8-8:18+WordMax*4+LongCount*8]#Word総数分スキップして切り出し

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
    MidResponse = Response.hex()[2:]#ヘッダ部?除去
    if str(MidResponse).startswith('00'):#エラーコード無いこと
        return True
    return False