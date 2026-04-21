import tkinter as tk
import SocketConectTest as ConectTest
from tkinter import messagebox
from tkinter import ttk
import inspect
import WidgetBind as Bind
import TCPGlobalVar as gl

#通信設定画面表示
def ConectConf() :

    deffont = 'Helvetica'
    fsizes = '10'

    if gl.ConectConfWin ==  None or not gl.ConectConfWin.winfo_exists()  :
        gl.ConectConfWin = tk.Toplevel()
        gl.ConectConfWin.geometry("800x400")
        gl.ConectConfWin.title("通信設定")
        gl.ConectConfWin.grab_set()
        gl.ConectConfWin.focus_set()
#-----------------------------------------
    #DeviceList=["PC10G","MP"]

    f1frow = 80
    f1fcol = 50
    f1row = 40
    f1col = 100

    # 接続テストボタン
    gl.app.Testbutton = tk.Button(gl.ConectConfWin, text="接続テスト", command=lambda : ConectTestdef())
    gl.app.Testbutton.place(x=260,y=0)
    # ﾃﾞﾌｫﾙﾄ設定ボタン   
    gl.app.Defbutton = tk.Button(gl.ConectConfWin, text="デフォルト設定", command=lambda : DefConf())
    gl.app.Defbutton.place(x=460,y=0)
    # 設定クリアボタン
    gl.app.ConfClearbutton = tk.Button(gl.ConectConfWin, text="設定クリア", command=lambda : ConfClear())
    gl.app.ConfClearbutton.place(x=660,y=0)

    #ﾃﾞﾊﾞｲｽNo
    gl.app.DeviceNoLabel = tk.Label(gl.ConectConfWin, text="デバイスNo", font=(deffont, fsizes))
    gl.app.DeviceNoLabel.place(x=f1fcol-f1fcol/2,y=f1frow)

    gl.app.Nolabel=[]
    for i in range(1,gl.DeviceMax+1) :
        gl.app.Nolabel.insert(i,tk.Label(gl.ConectConfWin, text=i , font=(deffont,fsizes)))
        gl.app.Nolabel[i-1].place(x=f1fcol,y=i*f1row+f1frow)

    #接続機器
    gl.app.DeviceLabel = tk.Label(gl.ConectConfWin, text="接続機器", font=(deffont, fsizes))
    gl.app.DeviceLabel.place(x=f1fcol+f1col,y=f1frow)

    gl.app.DeviceCombo=[]
    for i in range(1,gl.DeviceMax+1) :
        gl.app.DeviceCombo.insert(i, ttk.Combobox(gl.ConectConfWin,values=gl.DeviceList, font=(deffont, fsizes)))
        gl.app.DeviceCombo[i-1].place(x=f1fcol+f1col,y=i*f1row+f1frow)
        gl.app.DeviceCombo[i-1].bind('<FocusOut>',lambda event,arg1=gl.app.DeviceCombo[i-1],arg2=gl.DeviceList:Bind.ComboChange(event,arg1,arg2))

    #IPｱﾄﾞﾚｽ
    gl.app.IPLabel = tk.Label(gl.ConectConfWin, text="IPアドレス", font=(deffont, fsizes))
    gl.app.IPLabel.place(x=f1fcol+f1col*3,y=f1frow)

    gl.app.IPText=[]
    for i in range(1,gl.DeviceMax+1) :

        gl.app.IPText.insert(i,tk.Entry(gl.ConectConfWin, font=(deffont, fsizes)))
        gl.app.IPText[i-1].place(x=f1fcol+f1col*3,y=i*f1row+f1frow)

    #PORT
    gl.app.PortLabel = tk.Label(gl.ConectConfWin, text="PORT", font=(deffont, fsizes))
    gl.app.PortLabel.place(x=f1fcol+f1col*5,y=f1frow)

    gl.app.PortText=[]
    for i in range(1,gl.DeviceMax+1) :
        gl.app.PortText.insert(i,tk.Entry(gl.ConectConfWin,text = '',font=(deffont, fsizes)))
        gl.app.PortText[i-1].place(x=f1fcol+f1col*5,y=i*f1row+f1frow)
        gl.app.PortText[i-1].bind('<FocusOut>',lambda event,arg1=gl.app.PortText[i-1]:Bind.TextUIntCheck(event,arg1))
    
    #各ウィジェットに文字反映
    for i in range(gl.DeviceMax) :
        gl.app.DeviceCombo[i].set(gl.DeviceConfDic[i]['Device'])
        gl.app.IPText[i].insert(tk.END,gl.DeviceConfDic[i]['IPAddress'])
        gl.app.PortText[i].insert(tk.END,gl.DeviceConfDic[i]['Port'])
    
    #ウインドウ閉じをキャッチ
    gl.ConectConfWin.protocol('WM_DELETE_WINDOW',ConectConfWincallback)
#-----------------------------------------

def BackUp():
    #変数に値格納
    for i in range(gl.DeviceMax):
        gl.DeviceConfDic[i]['Device'] = gl.app.DeviceCombo[i].get()
        gl.DeviceConfDic[i]['IPAddress']=gl.app.IPText[i].get()
        gl.DeviceConfDic[i]['Port'] = gl.app.PortText[i].get()


def ConectTestdef():
    BackUp()
    ConectTest.Test()

def DefConf():
    if messagebox.askyesno('デフォルト設定','現在の入力をクリアして、デフォルト設定を適用しますか？') :
        ConfClear()
        gl.app.DeviceCombo[0].set('PC10G')
        gl.app.IPText[0].insert(tk.END,"192.168.1.3")
        gl.app.PortText[0].insert(tk.END,"1026")
        gl.app.DeviceCombo[1].set('MP')
        gl.app.IPText[1].insert(tk.END,'192.168.1.1')
        gl.app.PortText[1].insert(tk.END,'10002')

def ConfClear():
    if inspect.stack()[1].function != 'DefConf':
        if not messagebox.askyesno('設定クリア','現在の入力をクリアしますか？') :
            return
    
    for i in range(1,gl.DeviceMax+1) :#内容クリア
        gl.app.DeviceCombo[i-1].set('')
        gl.app.IPText[i-1].delete(0,tk.END)
        gl.app.PortText[i-1].delete(0,tk.END)

#サブウインドウを閉じ受付時の処理
def ConectConfWincallback():
    BackUp()

    if not EnableCheck() :
        return
    
    IOConfWinChange()
    
    gl.ConectConfWin.destroy()

def IOConfWinChange():

    for i in range(gl.ChMax):
        gl.app.DeviceNoCombo[i]['values']=gl.EnableDevice
        gl.app.DeviceNoCombo[i].bind('<FocusOut>',lambda event,arg1=gl.app.DeviceNoCombo[i-1],arg2=gl.EnableDevice:Bind.ComboChange(event,arg1,arg2))
    gl.app.Periodcombo['values']=gl.EnableDevice
    gl.app.Periodcombo.bind('<FocusOut>',lambda event,arg1=gl.app.Periodcombo,arg2=gl.EnableDevice:Bind.ComboChange(event,arg1,arg2))

def EnableCheck():
    
    gl.EnableDevice = []
    for i in range(gl.DeviceMax) :
        if gl.DeviceConfDic[i]['Device'] != '' and gl.DeviceConfDic[i]['IPAddress'] != '' and gl.DeviceConfDic[i]['Port'] != '' :
            gl.EnableDevice.append(i+1)
        elif gl.DeviceConfDic[i]['Device'] == 'ﾀﾞﾐｰ(接続先無)':
            gl.EnableDevice.append(i+1)
            
    if inspect.stack()[1].function == 'ValGet':
        return
    if len(gl.EnableDevice) > 0:
        return True
    messagebox.showinfo('エラー','通信可能な設定がありません。\n入力してください。') 
    return
