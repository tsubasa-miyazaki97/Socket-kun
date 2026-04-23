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
        gl.ConectConfWin.title("通信設定")
        gl.ConectConfWin.grab_set()
        gl.ConectConfWin.focus_set()
        gl.ConectConfWin.grid_rowconfigure(1, weight=1)
        gl.ConectConfWin.grid_columnconfigure(0, weight=1)
#-----------------------------------------

        # ツールバーフレーム
        toolbar_frame = tk.Frame(gl.ConectConfWin)
        toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # 接続テストボタン
        gl.app.Testbutton = tk.Button(toolbar_frame, text="接続テスト", command=lambda : ConectTestdef())
        gl.app.Testbutton.grid(row=0, column=0, padx=2, pady=2)
        # ﾃﾞﾌｫﾙﾄ設定ボタン
        gl.app.Defbutton = tk.Button(toolbar_frame, text="デフォルト設定", command=lambda : DefConf())
        gl.app.Defbutton.grid(row=0, column=1, padx=2, pady=2)
        # 設定クリアボタン
        gl.app.ConfClearbutton = tk.Button(toolbar_frame, text="設定クリア", command=lambda : ConfClear())
        gl.app.ConfClearbutton.grid(row=0, column=2, padx=2, pady=2)

        # コンテンツフレーム
        content_frame = tk.Frame(gl.ConectConfWin)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # ヘッダー行 (row=0)
        tk.Label(content_frame, text="デバイスNo", font=(deffont, fsizes)).grid(row=0, column=0, padx=5, pady=4)
        tk.Label(content_frame, text="接続機器", font=(deffont, fsizes)).grid(row=0, column=1, padx=5, pady=4)
        tk.Label(content_frame, text="IPアドレス", font=(deffont, fsizes)).grid(row=0, column=2, padx=5, pady=4)
        tk.Label(content_frame, text="PORT", font=(deffont, fsizes)).grid(row=0, column=3, padx=5, pady=4)

        # データ行
        conect_nolabel=[]
        gl.app.DeviceCombo=[]
        gl.app.IPText=[]
        gl.app.PortText=[]
        for i in range(1,gl.DeviceMax+1) :
            r = i  # row (0=ヘッダー, 1..DeviceMax=データ)

            lbl = tk.Label(content_frame, text=i, font=(deffont, fsizes))
            lbl.grid(row=r, column=0, padx=5, pady=2)
            conect_nolabel.insert(i, lbl)

            combo = ttk.Combobox(content_frame, values=gl.DeviceList, font=(deffont, fsizes), width=16)
            combo.grid(row=r, column=1, padx=5, pady=2)
            combo.bind('<FocusOut>', lambda event, arg1=combo, arg2=gl.DeviceList: Bind.ComboChange(event, arg1, arg2))
            gl.app.DeviceCombo.insert(i, combo)

            ip = tk.Entry(content_frame, font=(deffont, fsizes), width=16)
            ip.grid(row=r, column=2, padx=5, pady=2)
            gl.app.IPText.insert(i, ip)

            port = tk.Entry(content_frame, font=(deffont, fsizes), width=16)
            port.grid(row=r, column=3, padx=5, pady=2)
            port.bind('<FocusOut>', lambda event, arg1=port: Bind.TextUIntCheck(event, arg1))
            gl.app.PortText.insert(i, port)

        #各ウィジェットに文字反映
        for i in range(gl.DeviceMax) :
            gl.app.DeviceCombo[i].set(gl.DeviceConfDic[i]['Device'])
            gl.app.IPText[i].insert(tk.END,gl.DeviceConfDic[i]['IPAddress'])
            gl.app.PortText[i].insert(tk.END,gl.DeviceConfDic[i]['Port'])
        
        #ウィンドウサイズを内容に合わせて自動調整
        gl.ConectConfWin.update_idletasks()
        gl.ConectConfWin.geometry(
            f"{gl.ConectConfWin.winfo_reqwidth()}x{gl.ConectConfWin.winfo_reqheight()}"
        )
        #ウインドウ閉じをキャッチ
        gl.ConectConfWin.protocol('WM_DELETE_WINDOW',ConectConfWincallback)
    else:
        gl.ConectConfWin.lift()
        gl.ConectConfWin.focus_set()
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
        if gl.app.DeviceNoCombo[i] is not None:
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
