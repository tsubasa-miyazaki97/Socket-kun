
from telnetlib import theNULL
from tkinter import messagebox
import socket
import inspect
import TCPGlobalVar as gl
from asyncua import Client
import asyncio

def Test():

        #接続テスト可否判定
        Flag = True
        for i in range(1,gl.DeviceMax+1):#機器未入力ﾁｪｯｸ
            if gl.DeviceConfDic[i-1]['Device'] != "" :
                Flag = False
        if Flag == True :
            messagebox.showinfo('Error','接続機器が未入力です。\n機器を入力してください。')

        else :
            for i in range(1,gl.DeviceMax+1):#機器がﾘｽﾄ内かﾁｪｯｸ
                if gl.DeviceConfDic[i-1]['Device'] != "" :
                    if not gl.DeviceConfDic[i-1]['Device'] in gl.DeviceList :
                        Flag = True
            if Flag == True :
                messagebox.showinfo('Error','接続機器に対象外機器が入力されています。\n正しい機器を入力してください。')
                
            else :
                #IPとPORT未入力ﾁｪｯｸ
                Flag = False
                for i in range(1,gl.DeviceMax+1):
                    if gl.DeviceConfDic[i-1]['Device'] != "" and not gl.DeviceList[3] :
                        if gl.DeviceConfDic[i-1]['IPAddress'] == "":
                            Flag = True
                        if gl.DeviceConfDic[i-1]['Port'] == "":
                            Flag = True
                if Flag == True :
                    messagebox.showinfo('Error','機器入力箇所で、IPアドレスとPORTが未入力な箇所があります。\n入力、または削除してください。')
                else :
                    Flag = False
                    for i in range(1,gl.DeviceMax+1):
                        if gl.DeviceConfDic[i-1]['Device'] != "" and gl.DeviceConfDic[i-1]['Device'] != gl.DeviceList[3] :
                            IPCheck = gl.DeviceConfDic[i-1]['IPAddress'].split('.')
                            if len(IPCheck) == 4:#IP異常検知
                                Flag = False
                                for j in range(1,5) :
                                    if not IPCheck[i-1].isdecimal() :
                                        Flag = True 
                                if Flag == True :
                                    messagebox.showinfo('Error','IPアドレスが不正な値です。\n正しい値を入力してください。')
                                    break
                                for j in range(1,5) :
                                    if int(IPCheck[i-1]) < 0 or int(IPCheck[i-1]) > 255 :
                                        Flag = True
                                if Flag == True :
                                    messagebox.showinfo('Error','IPアドレスが不正な値です。\n正しい値を入力してください。')
                                    break
                                
                                if not gl.DeviceConfDic[i-1]['Port'].isdecimal() :#PORT異常検知
                                    Flag = True
                                    messagebox.showinfo('Error','PORTが不正な値です。\n正しい値を入力してください。')
                                    break
                                else :
                                    if int(gl.DeviceConfDic[i-1]['Port']) < 0 or int(gl.DeviceConfDic[i-1]['Port']) > 65535 :
                                        Flag = True
                                        messagebox.showinfo('Error','PORTが不正な値です。\n正しい値を入力してください。')
                                        break

                            else :
                                if gl.DeviceConfDic[i-1]['IPAddress'] != "localhost" :
                                    Flag = True
                                    messagebox.showinfo('Error','IPアドレスが不正な値です。\n正しい値を入力してください。')
                                    break
        if Flag == False :#機器とIPとPORT正常
            Result = ''

            #接続テスト処理
            for i in range(1,gl.DeviceMax+1):
                #Socketのﾃｽﾄ
                if gl.DeviceConfDic[i-1]['Device'] != "" and gl.DeviceConfDic[i-1]['Device'] != gl.DeviceList[3] and gl.DeviceConfDic[i-1]['Device'] != gl.DeviceList[4] :
                    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

                    host = gl.DeviceConfDic[i-1]['IPAddress']
                    port = int(gl.DeviceConfDic[i-1]['Port'])
                    
                    try:
                        if client.connect_ex((host, port)) == 0 :#正常通信
                            Result = Result + 'デバイスNo'+ str(i) + ' : 接続OK\n'
                            client.close
                        else :
                            Result = Result + 'デバイスNo'+ str(i) + ' : 接続NG\nIP,PORT,パソコンの設定,LANの確認をしてください。\n'
                    except KeyboardInterrupt :#ﾌﾟﾛｸﾞﾗﾑｷｬﾝｾﾙ時
                            Result = Result + 'デバイスNo'+ str(i) + ' : 接続NG\nﾌﾟﾛｸﾞﾗﾑがｷｬﾝｾﾙされました。\n'
                    except socket.gaierror :#IPかPORTが不正
                            Result = Result + 'デバイスNo'+ str(i) + ' : 接続NG\nIPかPORTの値が不正です。\n'
                elif gl.DeviceConfDic[i-1]['Device'] == gl.DeviceList[3] :#Dummy
                    Result = Result + 'デバイスNo'+ str(i) + ' : 接続OK\n'
                elif gl.DeviceConfDic[i-1]['Device'] == gl.DeviceList[4] :#OPCUA
                    
                    host = gl.DeviceConfDic[i-1]['IPAddress']
                    port = int(gl.DeviceConfDic[i-1]['Port'])

                    url = f"opc.tcp://{host}:{port}/"
                    client = Client(url=url)
                    loop = asyncio.get_event_loop()
                    try:
                        loop.run_until_complete(client.connect())
                        Result = Result + 'デバイスNo'+ str(i) + ' : 接続OK\n'
                        #接続解除
                        loop.run_until_complete(client.disconnect())
                    except :
                        Result = Result + 'デバイスNo'+ str(i) + ' : 接続NG\nIP,PORT,パソコンの設定,LANの確認をしてください。\n'


                    #client.close
            if inspect.stack()[1].function != 'ConectTestdef':
                if not 'NG' in Result :
                    return True
            messagebox.showinfo('接続テスト結果',Result)