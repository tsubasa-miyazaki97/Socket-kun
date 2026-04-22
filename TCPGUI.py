import tkinter as tk
from functools import partial
import os
import ConectConfWin as ConectConf
import SensorConfWin as SensorConf
from tkinter import ttk
import WidgetBind as Bind
import TCPGlobalVar as gl
import SQDB as DB
import IORW
import Trace
import InExeport


class App(tk.Tk):
    
    # 呪文
    def __init__(self, *args, **kwargs):

        # 呪文
        tk.Tk.__init__(self, *args, **kwargs)

        # ウィジェット構築中は非表示にして描画コストを削減
        self.withdraw()

        # ウィンドウタイトルを決定
        self.title("IO読書")

        # ウィンドウの大きさを決定
        self.geometry(str(gl.winwidth)+"x"+str(gl.winheight))

        # ツールバー行(row=0)は固定、キャンバス行(row=1)を伸縮
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

#-----------------------------------toolbar_frame--------------------------

        # ツールバーフレーム（row=0 / スクロールしない）
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        tc = 0  # ツールバー列カウンタ

        # IO読書開始ボタン
        self.RWStartButton = tk.Button(toolbar_frame, text="IO読書開始", command=lambda: IORW.IORW())
        self.RWStartButton.grid(row=0, column=tc, padx=2, pady=2)
        tc += 1
        ### ｽｷｬﾝﾀｲﾑデバイスラベル作成
        ScanTimeDevicelabel = tk.Label(toolbar_frame, text='ﾃﾞﾊﾞｲｽNo', font=(gl.deffont, gl.fsizes))
        ScanTimeDevicelabel.grid(row=0, column=tc, padx=2)
        tc += 1
        ###ｽｷｬﾝﾀｲﾑ表示切替コンボボックス
        self.Periodcombo = ttk.Combobox(toolbar_frame, values=gl.EnableDevice, font=(gl.deffont, gl.fsizes), width=1)
        self.Periodcombo.grid(row=0, column=tc, padx=2)
        self.Periodcombo.bind('<FocusOut>', lambda event, arg1=self.Periodcombo, arg2=gl.EnableDevice: Bind.ComboChange(event, arg1, arg2))
        self.Periodcombo.set(1)
        tc += 1
        ### ｽｷｬﾝﾀｲﾑラベル作成
        ScanTimelabel = tk.Label(toolbar_frame, text='ｽｷｬﾝﾀｲﾑ', font=(gl.deffont, gl.fsizes))
        ScanTimelabel.grid(row=0, column=tc, padx=2)
        tc += 1
        ### ｽｷｬﾝﾀｲﾑ作成
        self.ScanTime = tk.Label(toolbar_frame, text=0, font=(gl.deffont, gl.fsizes), width=5, anchor='e')
        self.ScanTime.grid(row=0, column=tc, padx=2)
        tc += 1
        ### ｽｷｬﾝﾀｲﾑ単位作成
        self.ScanTimems = tk.Label(toolbar_frame, text='ms', font=(gl.deffont, gl.fsizes))
        self.ScanTimems.grid(row=0, column=tc, padx=2)
        tc += 1
        # トレースボタン
        self.TraceButton = tk.Button(toolbar_frame, text="ﾄﾚｰｽ開始", command=lambda: Trace.TracePush())
        self.TraceButton.grid(row=0, column=tc, padx=2)
        tc += 1
        ### ﾄﾚｰｽｽｷｬﾝﾀｲﾑラベル作成
        TraceScanTimelabel = tk.Label(toolbar_frame, text='ﾄﾚｰｽｽｷｬﾝﾀｲﾑ', font=(gl.deffont, gl.fsizes))
        TraceScanTimelabel.grid(row=0, column=tc, padx=2)
        tc += 1
        ###ﾄﾚｰｽｽｷｬﾝﾀｲﾑコンボボックス
        self.Tracecombo = ttk.Combobox(toolbar_frame, values=gl.TraceTime, font=(gl.deffont, gl.fsizes), width=7)
        self.Tracecombo.grid(row=0, column=tc, padx=2)
        self.Tracecombo.bind('<FocusOut>', lambda event, arg1=self.Tracecombo, arg2=gl.TraceTime: Bind.ComboChange(event, arg1, arg2))
        self.Tracecombo.set(gl.TraceTime[0])
        tc += 1
        ### ﾄﾚｰｽｽｷｬﾝﾀｲﾑ単位作成
        self.TraceScanTimems = tk.Label(toolbar_frame, text='ms', font=(gl.deffont, gl.fsizes))
        self.TraceScanTimems.grid(row=0, column=tc, padx=2)
        tc += 1
        # 右寄せ用スペーサー
        spacer = tk.Label(toolbar_frame, text="")
        spacer.grid(row=0, column=tc, sticky="ew")
        toolbar_frame.grid_columnconfigure(tc, weight=1)
        tc += 1
        # 通信設定ボタン
        self.changePageButton = tk.Button(toolbar_frame, text="通信設定", command=lambda: ConectConfdef())
        self.changePageButton.grid(row=0, column=tc, padx=2)
        tc += 1
        # センサー設定ボタン
        self.SensorConfButton = tk.Button(toolbar_frame, text="ｾﾝｻｰ設定", command=lambda: SensorConfdef())
        self.SensorConfButton.grid(row=0, column=tc, padx=2)
        tc += 1
        # IO設定クリアボタン
        self.IOClearConfButton = tk.Button(toolbar_frame, text="IO設定ｸﾘｱ", command=lambda: Bind.IOConfClear())
        self.IOClearConfButton.grid(row=0, column=tc, padx=2)
        tc += 1
        # ｴｸｽﾎﾟｰﾄボタン
        self.ExportButton = tk.Button(toolbar_frame, text="ｴｸｽﾎﾟｰﾄ", command=lambda: InExeport.Export())
        self.ExportButton.grid(row=0, column=tc, padx=2)
        tc += 1
        # インポートボタン
        self.InportButton = tk.Button(toolbar_frame, text="ｲﾝﾎﾟｰﾄ", command=lambda: InExeport.Inport())
        self.InportButton.grid(row=0, column=tc, padx=2)

#-----------------------------------canvas / main_frame--------------------

        # スクロールバー設置
        self.canvas = tk.Canvas(self, width=gl.winwidth, height=gl.winheight, highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.ybar = tk.Scrollbar(self, orient=tk.VERTICAL)  # 縦スクロールバー配置
        self.ybar.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.ybar.config(command=self.canvas.yview)  # 縦スクロール用ｺﾏﾝﾄﾞ
        self.canvas.config(yscrollcommand=self.ybar.set)  # キャンバスにスクロールバーの動きを反映
        self.canvas.yview_moveto(0)  # キャンバスのスクロールを初期化

        # キャンバス上にフレーム設置（ヘッダー行 + データ行をまとめて grid 管理）
        self.main_frame = tk.Frame(self.canvas, width=gl.winmaxwidth*10, highlightthickness=0)
        self.canvas.create_window(0, 0, window=self.main_frame, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox('all'))  # フレームにフィットするようにキャンバスのスクロール可能範囲を変更
        self.main_frame.bind("<MouseWheel>", lambda event, arg1=self.canvas, arg2=self.main_frame: Bind.mouse_y_scroll(event, arg1, arg2))  # マウスホイール関数をｾｯﾄ
        self.canvas.bind("<MouseWheel>", lambda event: Bind.mouse_y_scroll(event, self.canvas, None))  # キャンバス空白部分のマウスホイール対応

#-----------------------------------列定数---------------------------------

        C_CHNO      = 0
        C_DEVICENO  = 1
        C_ADDRESS   = 2
        C_VALUE     = 3
        C_VALUEDOWN = 4
        C_VALUEUP   = 5
        C_UDVALUE   = 6
        C_INIT      = 7
        C_COMMENT   = 8
        C_WINBTN    = 9
        C_VARTYPE   = 10
        C_AI0       = 11
        C_AI100     = 12
        C_USER0     = 13
        C_USER100   = 14

#-----------------------------------ヘッダー行 (row=0)--------------------

        self.ChNoLabel = tk.Label(self.main_frame, text="ChNo", font=(gl.deffont, gl.fsizes))
        self.ChNoLabel.grid(row=0, column=C_CHNO, padx=2, pady=2)

        self.DeviceNoLabel = tk.Label(self.main_frame, text="ﾃﾞﾊﾞｲｽNo", font=(gl.deffont, gl.fsizes))
        self.DeviceNoLabel.grid(row=0, column=C_DEVICENO, padx=2, pady=2)

        self.RWAddressLabel = tk.Label(self.main_frame, text="読書ｱﾄﾞﾚｽ", font=(gl.deffont, gl.fsizes))
        self.RWAddressLabel.grid(row=0, column=C_ADDRESS, padx=2, pady=2)

        self.ValueLabel = tk.Label(self.main_frame, text="現在値", font=(gl.deffont, gl.fsizes))
        self.ValueLabel.grid(row=0, column=C_VALUE, padx=2, pady=2)

        self.ValueUDLabel = tk.Label(self.main_frame, text="増減ﾎﾞﾀﾝ", font=(gl.deffont, gl.fsizes))
        self.ValueUDLabel.grid(row=0, column=C_VALUEDOWN, padx=2, pady=2, columnspan=2)

        self.UDLabel = tk.Label(self.main_frame, text="増減値", font=(gl.deffont, gl.fsizes))
        self.UDLabel.grid(row=0, column=C_UDVALUE, padx=2, pady=2)

        self.InitLabel = tk.Label(self.main_frame, text="初期値", font=(gl.deffont, gl.fsizes))
        self.InitLabel.grid(row=0, column=C_INIT, padx=2, pady=2)

        self.CommentLabel = tk.Label(self.main_frame, text="ｺﾒﾝﾄ", font=(gl.deffont, gl.fsizes))
        self.CommentLabel.grid(row=0, column=C_COMMENT, padx=2, pady=2)

        ###表示範囲切替ボタン
        self.WinWidthButton = tk.Button(self.main_frame, text="▶", command=lambda: Bind.WinWidthSwitch())
        self.WinWidthButton.grid(row=0, column=C_WINBTN, padx=2, pady=2)

        self.VarTypeLabel = tk.Label(self.main_frame, text="型", font=(gl.deffont, gl.fsizes))
        self.VarTypeLabel.grid(row=0, column=C_VARTYPE, padx=2, pady=2)

        self.AI0Label = tk.Label(self.main_frame, text="0%AI値", font=(gl.deffont, gl.fsizes))
        self.AI0Label.grid(row=0, column=C_AI0, padx=2, pady=2)

        self.AI100Label = tk.Label(self.main_frame, text="100%AI値", font=(gl.deffont, gl.fsizes))
        self.AI100Label.grid(row=0, column=C_AI100, padx=2, pady=2)

        self.User0Label = tk.Label(self.main_frame, text="0%ﾕｰｻﾞ値", font=(gl.deffont, gl.fsizes))
        self.User0Label.grid(row=0, column=C_USER0, padx=2, pady=2)

        self.User100Label = tk.Label(self.main_frame, text="100%ﾕｰｻﾞ値", font=(gl.deffont, gl.fsizes))
        self.User100Label.grid(row=0, column=C_USER100, padx=2, pady=2)

#-----------------------------------データ行 (row=1..ChMax)---------------

        self.Nolabel = []
        self.DeviceNoCombo = []
        self.AddressText = []
        self.ValueText = []
        self.ValueUpButton = []
        self.ValueDownButton = []
        self.UDValueText = []
        self.InitValueText = []
        self.CommentText = []
        self.VarTypecombo = []
        self.AI0ValueText = []
        self.AI100ValueText = []
        self.User0ValueText = []
        self.User100ValueText = []

        for i in range(1, gl.ChMax+1):
            r = i  # grid row（0=ヘッダー、1以降=データ）

            # ChNo
            lbl = tk.Label(self.main_frame, text=i, font=(gl.deffont, gl.fsizes))
            lbl.grid(row=r, column=C_CHNO, padx=2)
            self.Nolabel.append(lbl)

            # ﾃﾞﾊﾞｲｽNo
            combo = ttk.Combobox(self.main_frame, values=gl.EnableDevice, font=(gl.deffont, gl.fsizes), width=2)
            combo.grid(row=r, column=C_DEVICENO, padx=2)
            combo.bind('<FocusOut>', lambda event, arg1=combo, arg2=gl.EnableDevice: Bind.ComboChange(event, arg1, arg2))
            self.DeviceNoCombo.append(combo)

            # 読書アドレス
            addr = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=12)
            addr.grid(row=r, column=C_ADDRESS, padx=2)
            self.AddressText.append(addr)

            # 現在値
            gl.ValueText[i-1] = tk.StringVar()
            val = tk.Entry(self.main_frame, textvariable=gl.ValueText[i-1], font=(gl.deffont, gl.fsizes), width=12)
            val.grid(row=r, column=C_VALUE, padx=2)
            val.bind('<FocusIn>', lambda event, arg1=i-1, arg2=gl.ValueTextFocus: Bind.ValueTextFocusIn(event, arg1, arg2))
            val.bind('<FocusOut>', lambda event, arg1=i-1, arg2=gl.ValueTextFocus: Bind.ValueTextFocusOut(event, arg1, arg2))
            val.bind('<KeyRelease>', lambda event, arg1=i-1, arg2=gl.ValueText: Bind.ValueTextEnter(event, arg1, arg2))
            self.ValueText.append(val)

            # 値減少ボタン（▼）
            down = tk.Button(self.main_frame, text='▼', font=(gl.deffont, gl.fsizes), command=partial(Bind.ValueDown, i-1))
            down.grid(row=r, column=C_VALUEDOWN, padx=2)
            down['state'] = 'disabled'
            self.ValueDownButton.append(down)

            # 値増加ボタン（▲）
            up = tk.Button(self.main_frame, text='▲', font=(gl.deffont, gl.fsizes), command=partial(Bind.ValueUp, i-1))
            up.grid(row=r, column=C_VALUEUP, padx=2)
            up['state'] = 'disabled'
            self.ValueUpButton.append(up)

            # 増減値
            ud = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=7)
            ud.grid(row=r, column=C_UDVALUE, padx=2)
            ud.bind('<FocusOut>', lambda event, arg1=ud: Bind.TextFloatCheck(event, arg1))
            self.UDValueText.append(ud)

            # 初期値
            init = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=7)
            init.grid(row=r, column=C_INIT, padx=2)
            init.bind('<FocusOut>', lambda event, arg1=init: Bind.TextFloatCheck(event, arg1))
            self.InitValueText.append(init)

            # ｺﾒﾝﾄ
            comment = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=26)
            comment.grid(row=r, column=C_COMMENT, padx=2)
            self.CommentText.append(comment)

            # 型
            vtype = ttk.Combobox(self.main_frame, values=gl.VarTypeList, font=(gl.deffont, gl.fsizes), width=5)
            vtype.grid(row=r, column=C_VARTYPE, padx=2)
            vtype.bind('<FocusOut>', lambda event, arg1=vtype, arg2=gl.VarTypeList: Bind.ComboChange(event, arg1, arg2))
            self.VarTypecombo.append(vtype)

            # 0%AI値
            ai0 = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=7)
            ai0.grid(row=r, column=C_AI0, padx=2)
            ai0.bind('<FocusOut>', lambda event, arg1=ai0: Bind.TextFloatCheck(event, arg1))
            self.AI0ValueText.append(ai0)

            # 100%AI値
            ai100 = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=12)
            ai100.grid(row=r, column=C_AI100, padx=2)
            ai100.bind('<FocusOut>', lambda event, arg1=ai100: Bind.TextFloatCheck(event, arg1))
            self.AI100ValueText.append(ai100)

            # 0%User値
            user0 = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=7)
            user0.grid(row=r, column=C_USER0, padx=2)
            user0.bind('<FocusOut>', lambda event, arg1=user0: Bind.TextFloatCheck(event, arg1))
            self.User0ValueText.append(user0)

            # 100%User値
            user100 = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=12)
            user100.grid(row=r, column=C_USER100, padx=2)
            user100.bind('<FocusOut>', lambda event, arg1=user100: Bind.TextFloatCheck(event, arg1))
            self.User100ValueText.append(user100)

        #フレーム内全ウィジェットにマウスホイール関数ｾｯﾄ
        mainframechild = self.main_frame.winfo_children()
        for child in mainframechild:
            child.bind("<MouseWheel>", lambda event, arg1=self.canvas, arg2=child: Bind.mouse_y_scroll(event, arg1, arg2))  # マウスホイール関数をｾｯﾄ

        #各ウィジェットに文字反映
        for i in range(gl.ChMax):
            self.DeviceNoCombo[i].insert(0, str(gl.IOConfDic[i]['DeviceNo']))
            self.AddressText[i].insert(0, str(gl.IOConfDic[i]['Address']))
            self.InitValueText[i].insert(0, str(gl.IOConfDic[i]['Init']))
            self.UDValueText[i].insert(0, str(gl.IOConfDic[i]['UpDown']))
            self.CommentText[i].insert(0, str(gl.IOConfDic[i]['Comment']))
            self.VarTypecombo[i].insert(0, str(gl.IOConfDic[i]['VarType']))
            self.AI0ValueText[i].insert(0, str(gl.IOConfDic[i]['AI0']))
            self.AI100ValueText[i].insert(0, str(gl.IOConfDic[i]['AI100']))
            self.User0ValueText[i].insert(0, str(gl.IOConfDic[i]['User0']))
            self.User100ValueText[i].insert(0, str(gl.IOConfDic[i]['User100']))
            cv = gl.IOConfDic[i].get('CurrentVal', '') if isinstance(gl.IOConfDic[i], dict) else ''
            if cv:
                gl.ValueText[i].set(cv)

#--------------------------------------------------------------------------

        #ウインドウ閉じをキャッチ
        self.protocol("WM_DELETE_WINDOW", callback)

        # スクロール範囲を確定し、以降の変更に追従するよう<Configure>をバインド
        self.main_frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox('all')))

        # 全ウィジェット構築完了後に表示
        self.deiconify()

def ConectConfdef():
    ConectConf.ConectConf()  

def SensorConfdef():
    IORW.BackUp()
    if not IORW.EnableCheck():
        return
    SensorConf.SensorConf()

def IOInitConf() :
    #ChNo取得して、その行の空白部分にﾃﾞﾌｫﾙﾄ設定入れる
    True

#ウインドウ閉じ受付時の処理
def callback():
    
    IORW.BackUp()
    
    if not IORW.EnableCheck():
        return
    if not SensorConf.EnableCheck():
        return

    DB.BackUp()

    gl.app.destroy()#ウインドウ閉じる処理

if __name__ == "__main__":

    DB.TableCreate()

    DB.ValGet()

    gl.app = App()
    
    gl.app.mainloop()