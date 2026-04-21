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

        # ウィンドウタイトルを決定
        self.title("IO読書")

        # ウィンドウの大きさを決定
        self.geometry(str(gl.winmaxwidth)+"x"+str(gl.winheight))

        # ウィンドウのグリッドを 1x1 にする
        # この処理をコメントアウトすると配置がズレる
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
#-----------------------------------main_frame-----------------------------

        frow = 30
        fcol = 20
        row = 30
        col = 70
        
        # メインページフレーム作成
        self.mainm_frame = tk.Frame()#切替用ﾌﾚｰﾑ
        self.mainm_frame.grid(row=0, column=0)#,sticky="nsew")

        #スクロールバー設置
        #self.canvas = tk.Canvas(self.mainm_frame,width=gl.winmaxwidth,height=gl.winheight)#スクロールバー置けるウィジェット(キャンバス)配置
        self.canvas = tk.Canvas(self,width=gl.winmaxwidth,height=gl.winheight)
        self.main_frame = tk.Frame(self.canvas,width=gl.winmaxwidth*10,height=30.6*gl.ChMax)#キャンバス上にﾌﾚｰﾑ設置
        self.canvas.grid(row=0,column=0,sticky="nsew")
        self.canvas.create_window(0,0,window=self.main_frame,anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox('all'))#フレームにフィットするようにキャンバスのスクロール可能範囲を変更
        self.main_frame.bind("<Configure>",lambda e: self.canvas.config(scrollregion=self.canvas.bbox('all')))

        self.ybar = tk.Scrollbar(self,orient=tk.VERTICAL)#縦スクロールバー配置
        self.ybar.grid(row=0,column=1,sticky=tk.N+tk.S)
        self.ybar.config(command=self.canvas.yview)#縦スクロール用ｺﾏﾝﾄﾞ
        self.canvas.config(yscrollcommand=self.ybar.set)#キャンバスにスクロールバーの動きを反映
        self.canvas.yview_moveto(0)#キャンバスのスクロールを初期化
        self.main_frame.bind("<MouseWheel>",lambda event,arg1=self.canvas,arg2=self.main_frame: Bind.mouse_y_scroll(event,arg1,arg2))#マウスホイール関数をｾｯﾄ

        #self.main_frame.bind("<Configure>",lambda event,arg1=self.canvas,arg2=self.main_frame:Bind._configure_interior(event,arg1,arg2))#ウィンドウリサイズ関数

        #背景ﾗﾍﾞﾙ
        self.BGlabel = tk.Label(self.canvas,text='',font=(gl.deffont, gl.fsizes),width=gl.winmaxwidth,height=3)
        self.BGlabel.place(x=0,y=0)
        # IO読書開始ボタン
        self.RWStartButton = tk.Button(self.canvas, text="IO読書開始", command=lambda : IORW.IORW())
        self.RWStartButton.place(x=0,y=0)
        ### ｽｷｬﾝﾀｲﾑデバイスラベル作成
        ScanTimeDevicelabel = tk.Label(self.canvas,text='ﾃﾞﾊﾞｲｽNo',font=(gl.deffont, gl.fsizes))
        ScanTimeDevicelabel.place(x=col,y=0)
        ###ｽｷｬﾝﾀｲﾑ表示切替コンボボックス
        col += 60
        self.Periodcombo=ttk.Combobox(self.canvas,values=gl.EnableDevice, font=(gl.deffont, gl.fsizes),width=1)
        self.Periodcombo.place(x=col,y=0)
        self.Periodcombo.bind('<FocusOut>',lambda event,arg1=self.Periodcombo,arg2=gl.EnableDevice:Bind.ComboChange(event,arg1,arg2))
        self.Periodcombo.set(1)
        ### ｽｷｬﾝﾀｲﾑラベル作成
        col += 30
        ScanTimelabel = tk.Label(self.canvas,text='ｽｷｬﾝﾀｲﾑ',font=(gl.deffont, gl.fsizes))
        ScanTimelabel.place(x=col,y=0)
        ### ｽｷｬﾝﾀｲﾑ作成
        col += 60
        self.ScanTime = tk.Label(self.canvas,text=0,font=(gl.deffont, gl.fsizes),width=5,anchor='e')
        self.ScanTime.place(x=col,y=0)
        ### ｽｷｬﾝﾀｲﾑ単位作成
        col += 60
        self.ScanTimems = tk.Label(self.canvas,text='ms',font=(gl.deffont, gl.fsizes))
        self.ScanTimems.place(x=col,y=0)
        # 通信設定ボタン
        col += 25
        self.changePageButton = tk.Button(self.canvas, text="通信設定", command=lambda : ConectConfdef())
        self.changePageButton.place(x=col,y=0)
        # センサー設定ボタン
        col += 65
        self.SensorConfButton = tk.Button(self.canvas, text="ｾﾝｻｰ設定", command=lambda : SensorConfdef())
        self.SensorConfButton.place(x=col,y=0)
        # IO設定クリアボタン
        col += 59
        self.IOClearConfButton = tk.Button(self.canvas, text="IO設定ｸﾘｱ", command=lambda : Bind.IOConfClear())
        self.IOClearConfButton.place(x=col,y=0)
        # トレースボタン
        col += 70
        self.TraceButton = tk.Button(self.canvas, text="ﾄﾚｰｽ開始", command=lambda : Trace.TracePush())
        self.TraceButton.place(x=col,y=0)
        ###ﾄﾚｰｽｽｷｬﾝﾀｲﾑコンボボックス
        col += 60
        self.Tracecombo=ttk.Combobox(self.canvas,values=gl.TraceTime, font=(gl.deffont, gl.fsizes),width=7)
        self.Tracecombo.place(x=col,y=0)
        self.Tracecombo.bind('<FocusOut>',lambda event,arg1=self.Tracecombo,arg2=gl.TraceTime:Bind.ComboChange(event,arg1,arg2))
        self.Tracecombo.set(gl.TraceTime[0])
        ### ﾄﾚｰｽｽｷｬﾝﾀｲﾑ単位作成
        col += 75
        self.TraceScanTimems = tk.Label(self.canvas,text='ms',font=(gl.deffont, gl.fsizes))
        self.TraceScanTimems.place(x=col,y=0)
        ###表示範囲切替ボタン
        col += 25
        self.WinWidthButton = tk.Button(self.canvas, text="◀", command=lambda : Bind.WinWidthSwitch())
        self.WinWidthButton.place(x=col,y=0)
        # ｴｸｽﾎﾟｰﾄボタン
        col += 70
        self.ExportButton = tk.Button(self.canvas, text="ｴｸｽﾎﾟｰﾄ", command=lambda : InExeport.Export())
        self.ExportButton.place(x=col,y=0)
        
        # インポートボタン
        col += 80
        self.InportButton = tk.Button(self.canvas, text="ｲﾝﾎﾟｰﾄ", command=lambda : InExeport.Inport())
        self.InportButton.place(x=col,y=0)


        col = 35
        # ChNoラベル
        self.ChNoLabel = tk.Label(self.canvas, text="ChNo", font=(gl.deffont, gl.fsizes))
        self.ChNoLabel.place(x=fcol-fcol/2,y=frow)
        self.Nolabel=[]
        for i in range(1,gl.ChMax+1) :
            self.Nolabel.insert(i,tk.Label(self.main_frame, text=i , font=(gl.deffont,gl.fsizes)))
            self.Nolabel[i-1].place(x=fcol,y=i*row+frow)
            
        # ﾃﾞﾊﾞｲｽNoラベル
        self.DeviceNoLabel = tk.Label(self.canvas, text="ﾃﾞﾊﾞｲｽNo", font=(gl.deffont, gl.fsizes))
        self.DeviceNoLabel.place(x=fcol-fcol/2+col,y=frow)
        #ﾃﾞﾊﾞｲｽNoﾃｷｽﾄﾎﾞｯｸｽ
        self.DeviceNoCombo=[]
        for i in range(1,gl.ChMax+1) :
            self.DeviceNoCombo.insert(i,ttk.Combobox(self.main_frame,values=gl.EnableDevice, font=(gl.deffont, gl.fsizes),width=2))
            self.DeviceNoCombo[i-1].place(x=fcol+col,y=i*row+frow)
            self.DeviceNoCombo[i-1].bind('<FocusOut>',lambda event,arg1=self.DeviceNoCombo[i-1],arg2=gl.EnableDevice:Bind.ComboChange(event,arg1,arg2))

        # 読書アドレスラベル
        col += 55
        self.RWAddressLabel = tk.Label(self.canvas, text="読書ｱﾄﾞﾚｽ", font=(gl.deffont, gl.fsizes))
        self.RWAddressLabel.place(x=fcol+col,y=frow)
        #読書アドレスﾃｷｽﾄﾎﾞｯｸｽ
        self.AddressText=[]
        for i in range(1,gl.ChMax+1) :
            self.AddressText.insert(i,tk.Entry(self.main_frame , font=(gl.deffont,gl.fsizes),width=12))
            self.AddressText[i-1].place(x=fcol+col,y=i*row+frow)

        # 現在値ラベル
        col += 95
        self.ValueLabel = tk.Label(self.canvas, text="現在値", font=(gl.deffont, gl.fsizes))
        self.ValueLabel.place(x=fcol+col,y=frow)
        #現在値ﾃｷｽﾄﾎﾞｯｸｽ
        self.ValueText=[]
        for i in range(1,gl.ChMax+1) :
            gl.ValueText[i-1]= tk.StringVar()
            self.ValueText.insert(i,tk.Entry(self.main_frame ,textvariable=gl.ValueText[i-1], font=(gl.deffont,gl.fsizes),width=12))
            self.ValueText[i-1].place(x=fcol+col,y=i*row+frow)
            self.ValueText[i-1].bind('<FocusIn>',lambda event,arg1=i-1,arg2=gl.ValueTextFocus:Bind.ValueTextFocusIn(event,arg1,arg2))
            self.ValueText[i-1].bind('<FocusOut>',lambda event,arg1=i-1,arg2=gl.ValueTextFocus:Bind.ValueTextFocusOut(event,arg1,arg2))
            self.ValueText[i-1].bind('<KeyRelease>',lambda event,arg1=i-1,arg2=gl.ValueText:Bind.ValueTextEnter(event,arg1,arg2))
        
        #値増減ﾗﾍﾞﾙ
        col += 95
        self.ValueUDLabel = tk.Label(self.canvas, text="増減ﾎﾞﾀﾝ", font=(gl.deffont, gl.fsizes))
        self.ValueUDLabel.place(x=fcol+col,y=frow)
        #値増減ﾎﾞﾀﾝ
        self.ValueUpButton=[]
        self.ValueDownButton=[]
        for i in range(1,gl.ChMax+1) :
            self.ValueUpButton.insert(i,tk.Button(self.main_frame, text='▲' , font=(gl.deffont,gl.fsizes),command = partial(Bind.ValueUp,i-1)))
            self.ValueUpButton[i-1].place(x=fcol+col+25,y=i*row+frow)
            self.ValueDownButton.insert(i,tk.Button(self.main_frame, text='▼' , font=(gl.deffont,gl.fsizes),command = partial(Bind.ValueDown,i-1)))
            self.ValueDownButton[i-1].place(x=fcol+col,y=i*row+frow)
            self.ValueUpButton[i-1]['state']='disabled'
            self.ValueDownButton[i-1]['state']='disabled'

        # 増減値ラベル
        col += 60
        self.UDLabel = tk.Label(self.canvas, text="増減値", font=(gl.deffont, gl.fsizes))
        self.UDLabel.place(x=fcol+col,y=frow)
        #増減値ﾃｷｽﾄﾎﾞｯｸｽ
        self.UDValueText=[]
        for i in range(1,gl.ChMax+1) :
            self.UDValueText.insert(i,tk.Entry(self.main_frame , font=(gl.deffont,gl.fsizes),width=7))
            self.UDValueText[i-1].place(x=fcol+col,y=i*row+frow)
            self.UDValueText[i-1].bind('<FocusOut>',lambda event,arg1=self.UDValueText[i-1]:Bind.TextFloatCheck(event,arg1))
        
        # 初期値ラベル
        col += 60
        self.InitLabel = tk.Label(self.canvas, text="初期値", font=(gl.deffont, gl.fsizes))
        self.InitLabel.place(x=fcol+col,y=frow)
        #初期値ﾃｷｽﾄﾎﾞｯｸｽ
        self.InitValueText=[]
        for i in range(1,gl.ChMax+1) :
            self.InitValueText.insert(i,tk.Entry(self.main_frame , font=(gl.deffont,gl.fsizes),width=7))
            self.InitValueText[i-1].place(x=fcol+col,y=i*row+frow)
            self.InitValueText[i-1].bind('<FocusOut>',lambda event,arg1=self.InitValueText[i-1]:Bind.TextFloatCheck(event,arg1))
        
        
        # ｺﾒﾝﾄラベル
        col += 60
        self.CommentLabel = tk.Label(self.canvas, text="ｺﾒﾝﾄ", font=(gl.deffont, gl.fsizes))
        self.CommentLabel.place(x=fcol+col,y=frow)
        #ｺﾒﾝﾄﾃｷｽﾄﾎﾞｯｸｽ
        self.CommentText=[]
        for i in range(1,gl.ChMax+1) :
            self.CommentText.insert(i,tk.Entry(self.main_frame , font=(gl.deffont,gl.fsizes),width=26))
            self.CommentText[i-1].place(x=fcol+col,y=i*row+frow)

        # 型ラベル
        col += 195
        self.VarTypeLabel = tk.Label(self.canvas, text="型", font=(gl.deffont, gl.fsizes))
        self.VarTypeLabel.place(x=fcol+col,y=frow)
        #型ﾎﾞｯｸｽ
        self.VarTypecombo=[]
        for i in range(1,gl.ChMax+1) :
            self.VarTypecombo.insert(i, ttk.Combobox(self.main_frame,values=gl.VarTypeList, font=(gl.deffont, gl.fsizes),width=5))
            self.VarTypecombo[i-1].place(x=fcol+col,y=i*row+frow)
            self.VarTypecombo[i-1].bind('<FocusOut>',lambda event,arg1=self.VarTypecombo[i-1],arg2=gl.VarTypeList:Bind.ComboChange(event,arg1,arg2))
        
        # 0%AI値ラベル
        col += 65
        self.AI0Label = tk.Label(self.canvas, text="0%AI値", font=(gl.deffont, gl.fsizes))
        self.AI0Label.place(x=fcol+col,y=frow)
        #0%AI値ﾃｷｽﾄﾎﾞｯｸｽ
        self.AI0ValueText=[]
        for i in range(1,gl.ChMax+1) :
            self.AI0ValueText.insert(i,tk.Entry(self.main_frame , font=(gl.deffont,gl.fsizes),width=7))
            self.AI0ValueText[i-1].place(x=fcol+col,y=i*row+frow)
            self.AI0ValueText[i-1].bind('<FocusOut>',lambda event,arg1=self.AI0ValueText[i-1]:Bind.TextFloatCheck(event,arg1))
        # 100%AI値ラベル
        col += 60
        self.AI100Label = tk.Label(self.canvas, text="100%AI値", font=(gl.deffont, gl.fsizes))
        self.AI100Label.place(x=fcol+col,y=frow)
        #100%AI値ﾃｷｽﾄﾎﾞｯｸｽ
        self.AI100ValueText=[]
        for i in range(1,gl.ChMax+1) :
            self.AI100ValueText.insert(i,tk.Entry(self.main_frame , font=(gl.deffont,gl.fsizes),width=12))
            self.AI100ValueText[i-1].place(x=fcol+col,y=i*row+frow)
            self.AI100ValueText[i-1].bind('<FocusOut>',lambda event,arg1=self.AI100ValueText[i-1]:Bind.TextFloatCheck(event,arg1))
            
        # 0%User値ラベル
        col += 95
        self.User0Label = tk.Label(self.canvas, text="0%ﾕｰｻﾞ値", font=(gl.deffont, gl.fsizes))
        self.User0Label.place(x=fcol+col,y=frow)
        #0%User値ﾃｷｽﾄﾎﾞｯｸｽ
        self.User0ValueText=[]
        for i in range(1,gl.ChMax+1) :
            self.User0ValueText.insert(i,tk.Entry(self.main_frame , font=(gl.deffont,gl.fsizes),width=7))
            self.User0ValueText[i-1].place(x=fcol+col,y=i*row+frow)
            self.User0ValueText[i-1].bind('<FocusOut>',lambda event,arg1=self.User0ValueText[i-1]:Bind.TextFloatCheck(event,arg1))
        # 100%User値ラベル
        col += 65
        self.User100Label = tk.Label(self.canvas, text="100%ﾕｰｻﾞ値", font=(gl.deffont, gl.fsizes))
        self.User100Label.place(x=fcol+col,y=frow)
        #100%User値ﾃｷｽﾄﾎﾞｯｸｽ
        self.User100ValueText=[]
        for i in range(1,gl.ChMax+1) :
            self.User100ValueText.insert(i,tk.Entry(self.main_frame , font=(gl.deffont,gl.fsizes),width=12))
            self.User100ValueText[i-1].place(x=fcol+col,y=i*row+frow)
            self.User100ValueText[i-1].bind('<FocusOut>',lambda event,arg1=self.User100ValueText[i-1]:Bind.TextFloatCheck(event,arg1))
        
        #フレーム内全ウィジェットにマウスホイール関数ｾｯﾄ
        mainframechild = self.main_frame.winfo_children()
        for child in mainframechild :
            child.bind("<MouseWheel>",lambda event,arg1=self.canvas,arg2=child: Bind.mouse_y_scroll(event,arg1,arg2))#マウスホイール関数をｾｯﾄ
        

        #各ウィジェットに文字反映
        
        for i in range(gl.ChMax) :
            self.DeviceNoCombo[i].insert(0,str(gl.IOConfDic[i]['DeviceNo']))
            self.AddressText[i].insert(0,str(gl.IOConfDic[i]['Address']))
            self.InitValueText[i].insert(0,str(gl.IOConfDic[i]['Init']))
            self.UDValueText[i].insert(0,str(gl.IOConfDic[i]['UpDown']))
            self.CommentText[i].insert(0,str(gl.IOConfDic[i]['Comment']))
            self.VarTypecombo[i].insert(0,str(gl.IOConfDic[i]['VarType']))
            self.AI0ValueText[i].insert(0,str(gl.IOConfDic[i]['AI0']))
            self.AI100ValueText[i].insert(0,str(gl.IOConfDic[i]['AI100']))
            self.User0ValueText[i].insert(0,str(gl.IOConfDic[i]['User0']))
            self.User100ValueText[i].insert(0,str(gl.IOConfDic[i]['User100']))

#--------------------------------------------------------------------------

        #main_frameを一番上に表示
        self.mainm_frame.tkraise()
        #ウインドウ閉じをキャッチ
        self.protocol("WM_DELETE_WINDOW",callback)

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