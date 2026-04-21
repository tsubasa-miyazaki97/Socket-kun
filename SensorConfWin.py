from ast import And
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import inspect
import WidgetBind as Bind
import TCPGlobalVar as gl

#通信設定画面表示
def SensorConf() :

    deffont = gl.deffont
    fsizes = gl.fsizes
    
    winwidth=800
    winheight = gl.winheight


    if gl.SensorConfWin ==  None or not gl.SensorConfWin.winfo_exists()  :
        gl.SensorConfWin = tk.Toplevel()
        gl.SensorConfWin.geometry(str(winwidth)+"x"+str(winheight))
        gl.SensorConfWin.title("センサー設定")
        gl.SensorConfWin.grab_set()
        gl.SensorConfWin.focus_set()
        gl.SensorConfWin.grid_rowconfigure(0, weight=0)
        gl.SensorConfWin.grid_rowconfigure(1, weight=1)
        gl.SensorConfWin.grid_columnconfigure(0, weight=1)

        # ツールバーフレーム
        toolbar_frame = tk.Frame(gl.SensorConfWin)
        toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        # 設定クリアボタン
        gl.app.ConfClearbutton = tk.Button(toolbar_frame, text="設定クリア", command=lambda : ConfClear())
        gl.app.ConfClearbutton.grid(row=0, column=0, padx=2, pady=2)
#-----------------------------------------

        gl.app.Sensormainm_frame = tk.Frame(gl.SensorConfWin)#切替用ﾌﾚｰﾑ
        gl.app.Sensormainm_frame.grid(row=1, column=0)
        #スクロールバー設置
        gl.app.Sensorcanvas = tk.Canvas(gl.app.Sensormainm_frame,width=winwidth,height=winheight-30)#スクロールバー置けるウィジェット(キャンバス)配置

        gl.app.SensorFrame = tk.Frame(gl.app.Sensorcanvas,width=winwidth,height=30.6*gl.ChMax)#キャンバス上にﾌﾚｰﾑ設置
        gl.app.Sensorcanvas.grid(row=0,column=0)
        gl.app.Sensorcanvas.create_window(0,0,window=gl.app.SensorFrame,anchor="nw")#キャンバスにフレーム設置
        gl.app.Sensorcanvas.config(scrollregion=gl.app.Sensorcanvas.bbox('all'))#フレームにフィットするようにキャンバスのスクロール可能範囲を変更
        gl.app.SensorFrame.bind("<Configure>",lambda e: gl.app.Sensorcanvas.config(scrollregion=gl.app.Sensorcanvas.bbox('all')))

        gl.app.Sensorybar = tk.Scrollbar(gl.SensorConfWin,orient=tk.VERTICAL)#縦スクロールバー配置
        gl.app.Sensorybar.grid(row=1,column=1,sticky=tk.N+tk.S)
        gl.app.Sensorybar.config(command=gl.app.Sensorcanvas.yview)#縦スクロール用ｺﾏﾝﾄﾞ
        gl.app.Sensorcanvas.config(yscrollcommand=gl.app.Sensorybar.set)#キャンバスにスクロールバーの動きを反映
        gl.app.Sensorcanvas.yview_moveto(0)#キャンバスのスクロールを初期化
        gl.app.SensorFrame.bind("<MouseWheel>",lambda event,arg1=gl.app.Sensorcanvas,arg2=gl.app.SensorFrame: Bind.mouse_y_scroll(event,arg1,arg2))#マウスホイール関数をﾌﾚｰﾑにｾｯﾄ

        # 列定数
        C_NO      = 0
        C_SENSOR  = 1
        C_IN1     = 2
        C_IN2     = 3
        C_OUT1    = 4
        C_OUT2    = 5
        C_OUT1INV = 6
        C_OUT2INV = 7
        C_PARA1   = 8
        C_PARA2   = 9
        C_PARA3   = 10
        C_PARA4   = 11
        C_DISABLE = 12

        # ヘッダー行 (row=0)
        tk.Label(gl.app.SensorFrame, text="No",     font=(deffont, fsizes)).grid(row=0, column=C_NO,      padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="ｾﾝｻ種",  font=(deffont, fsizes)).grid(row=0, column=C_SENSOR,  padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="Ch1",    font=(deffont, fsizes)).grid(row=0, column=C_IN1,     padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="Ch2",    font=(deffont, fsizes)).grid(row=0, column=C_IN2,     padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="Ch3",    font=(deffont, fsizes)).grid(row=0, column=C_OUT1,    padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="Ch4",    font=(deffont, fsizes)).grid(row=0, column=C_OUT2,    padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="出力1\n反転", font=(deffont, fsizes)).grid(row=0, column=C_OUT1INV, padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="出力2\n反転", font=(deffont, fsizes)).grid(row=0, column=C_OUT2INV, padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="ﾊﾟﾗ1",   font=(deffont, fsizes)).grid(row=0, column=C_PARA1,   padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="ﾊﾟﾗ2",   font=(deffont, fsizes)).grid(row=0, column=C_PARA2,   padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="ﾊﾟﾗ3",   font=(deffont, fsizes)).grid(row=0, column=C_PARA3,   padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="ﾊﾟﾗ4",   font=(deffont, fsizes)).grid(row=0, column=C_PARA4,   padx=2, pady=2)
        tk.Label(gl.app.SensorFrame, text="無効",    font=(deffont, fsizes)).grid(row=0, column=C_DISABLE, padx=2, pady=2)

        # データ行
        gl.app.SensorNolabel=[]
        gl.app.SensorCombo=[]
        gl.app.In1Combo=[]
        gl.app.In2Combo=[]
        gl.app.Out1Combo=[]
        gl.app.Out2Combo=[]
        gl.app.Out1InvCheck=[]
        gl.app.Out1InvVal = []
        gl.app.Out2InvCheck=[]
        gl.app.Out2InvVal = []
        gl.app.DigitsCoefText=[]
        gl.app.CalcCoefText=[]
        gl.app.RatioText=[]
        gl.app.TimeLagText=[]
        gl.app.DisableCheck=[]
        gl.app.DisableVal = []

        for i in range(1,gl.ChMax+1) :
            r = i  # row (0=ヘッダー, 1..ChMax=データ)

            lbl = tk.Label(gl.app.SensorFrame, text=i, font=(deffont, fsizes))
            lbl.grid(row=r, column=C_NO, padx=2)
            gl.app.SensorNolabel.insert(i, lbl)

            combo = ttk.Combobox(gl.app.SensorFrame, values=gl.SensorList, font=(deffont, fsizes), width=8)
            combo.grid(row=r, column=C_SENSOR, padx=2)
            combo.bind('<FocusOut>', lambda event, arg1=combo, arg2=gl.SensorList, arg3=i-1: (Bind.ComboChange(event,arg1,arg2), SensorSelect(event,arg2,arg3)))
            combo.bind("<<ComboboxSelected>>", lambda event, arg1=gl.SensorList, arg2=i-1: SensorSelect(event,arg1,arg2))
            gl.app.SensorCombo.insert(i, combo)

            in1 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
            in1.grid(row=r, column=C_IN1, padx=2)
            in1.bind('<FocusOut>', lambda event, arg1=in1, arg2=gl.EnableCh: Bind.ComboChange(event,arg1,arg2))
            gl.app.In1Combo.insert(i, in1)

            in2 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
            in2.grid(row=r, column=C_IN2, padx=2)
            in2.bind('<FocusOut>', lambda event, arg1=in2, arg2=gl.EnableCh: Bind.ComboChange(event,arg1,arg2))
            gl.app.In2Combo.insert(i, in2)

            out1 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
            out1.grid(row=r, column=C_OUT1, padx=2)
            out1.bind('<FocusOut>', lambda event, arg1=out1, arg2=gl.EnableCh: Bind.ComboChange(event,arg1,arg2))
            gl.app.Out1Combo.insert(i, out1)

            out2 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
            out2.grid(row=r, column=C_OUT2, padx=2)
            out2.bind('<FocusOut>', lambda event, arg1=out2, arg2=gl.EnableCh: Bind.ComboChange(event,arg1,arg2))
            gl.app.Out2Combo.insert(i, out2)

            out1inv_val = tk.BooleanVar()
            out1inv_check = ttk.Checkbutton(gl.app.SensorFrame, variable=out1inv_val)
            out1inv_check.grid(row=r, column=C_OUT1INV, padx=2)
            gl.app.Out1InvVal.insert(i, out1inv_val)
            gl.app.Out1InvCheck.insert(i, out1inv_check)

            out2inv_val = tk.BooleanVar()
            out2inv_check = ttk.Checkbutton(gl.app.SensorFrame, variable=out2inv_val)
            out2inv_check.grid(row=r, column=C_OUT2INV, padx=2)
            gl.app.Out2InvVal.insert(i, out2inv_val)
            gl.app.Out2InvCheck.insert(i, out2inv_check)

            para1 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
            para1.grid(row=r, column=C_PARA1, padx=2)
            para1.bind('<FocusOut>', lambda event, arg1=para1: Bind.TextFloatCheck(event,arg1))
            gl.app.DigitsCoefText.insert(i, para1)

            para2 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
            para2.grid(row=r, column=C_PARA2, padx=2)
            para2.bind('<FocusOut>', lambda event, arg1=para2: Bind.TextFloatCheck(event,arg1))
            gl.app.CalcCoefText.insert(i, para2)

            para3 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
            para3.grid(row=r, column=C_PARA3, padx=2)
            para3.bind('<FocusOut>', lambda event, arg1=para3: Bind.TextFloatCheck(event,arg1))
            gl.app.RatioText.insert(i, para3)

            para4 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
            para4.grid(row=r, column=C_PARA4, padx=2)
            para4.bind('<FocusOut>', lambda event, arg1=para4: Bind.TextFloatCheck(event,arg1))
            gl.app.TimeLagText.insert(i, para4)

            disable_val = tk.BooleanVar()
            disable_check = ttk.Checkbutton(gl.app.SensorFrame, variable=disable_val)
            disable_check.grid(row=r, column=C_DISABLE, padx=2)
            gl.app.DisableVal.insert(i, disable_val)
            gl.app.DisableCheck.insert(i, disable_check)

        #マウスホイール動作ｾｯﾄ
        framechild = gl.app.SensorFrame.winfo_children()
        for child in framechild :
            child.bind("<MouseWheel>",lambda event,arg1=gl.app.Sensorcanvas,arg2=child: Bind.mouse_y_scroll(event,arg1,arg2))
            child.bind("<FocusIn>",lambda event: Bind.TipDel(event))


        #各ウィジェットに文字反映
        for i in range(gl.ChMax) :
            gl.app.SensorCombo[i].set(gl.SensorConfDic[i]['Sensor'])
            gl.app.In1Combo[i].set(gl.SensorConfDic[i]['In1'])
            gl.app.In2Combo[i].set(gl.SensorConfDic[i]['In2'])
            gl.app.Out1Combo[i].set(gl.SensorConfDic[i]['Out1'])
            gl.app.Out2Combo[i].set(gl.SensorConfDic[i]['Out2'])
            gl.app.Out1InvVal[i].set(gl.SensorConfDic[i]['Out1Inv'])
            gl.app.Out2InvVal[i].set(gl.SensorConfDic[i]['Out2Inv'])
            gl.app.DigitsCoefText[i].insert(tk.END,gl.SensorConfDic[i]['DigitsCoef'])
            gl.app.CalcCoefText[i].insert(tk.END,gl.SensorConfDic[i]['CalcCoef'])
            gl.app.RatioText[i].insert(tk.END,gl.SensorConfDic[i]['Ratio'])
            gl.app.TimeLagText[i].insert(tk.END,gl.SensorConfDic[i]['TimeLag'])
            gl.app.DisableVal[i].set(gl.SensorConfDic[i]['Disable'])
            SensorSelect('',gl.SensorList,i)

        #ウインドウ閉じをキャッチ
        gl.SensorConfWin.protocol('WM_DELETE_WINDOW',SensorConfWincallback)
    else:
        gl.SensorConfWin.lift()
        gl.SensorConfWin.focus_set()


#-----------------------------------------

def ConfClear():
    if inspect.stack()[1].function != 'DefConf':
        if not messagebox.askyesno('設定クリア','現在の入力をクリアしますか？') :
            return
    
    for i in range(1,gl.ChMax+1) :#内容クリア
        gl.app.SensorCombo[i-1].set('')
        gl.app.In1Combo[i-1].set('')
        gl.app.In2Combo[i-1].set('')
        gl.app.Out1Combo[i-1].set('')
        gl.app.Out2Combo[i-1].set('')
        gl.app.Out1InvVal[i-1].set(False)
        gl.app.Out2InvVal[i-1].set(False)
        gl.app.DigitsCoefText[i-1].delete(0,tk.END)
        gl.app.CalcCoefText[i-1].delete(0,tk.END)
        gl.app.RatioText[i-1].delete(0,tk.END)
        gl.app.TimeLagText[i-1].delete(0,tk.END)
        gl.app.DisableVal[i-1].set(False)

def SensorSelect(event,list,num):
    if gl.app.SensorCombo[num].get() in list :
        #ツールチップ
        gl.app.In1Combo[num]['values']=gl.EnableCh
        if gl.app.SensorCombo[num].get() == list[0]:#ｴｯｼﾞｾﾝｻ
            Bind.CreateToolTip(gl.app.In1Combo[num], 'EPCCPC軸(mm)')
            Bind.CreateToolTip(gl.app.In2Combo[num], '')
            Bind.CreateToolTip(gl.app.Out1Combo[num], 'ｴｯｼﾞｾﾝｻ(mm)')
            Bind.CreateToolTip(gl.app.Out2Combo[num], 'ｴｯｼﾞｾﾝｻ(mm)')
            Bind.CreateToolTip(gl.app.DigitsCoefText[num], 'EPCCPC軸係数(未入力可)')
            Bind.CreateToolTip(gl.app.CalcCoefText[num], '揺動半径(mm)\n(直行は未入力)')
            Bind.CreateToolTip(gl.app.RatioText[num], '比率')
            Bind.CreateToolTip(gl.app.TimeLagText[num], '')
        elif gl.app.SensorCombo[num].get() == list[1]:#ﾀﾞﾝｻｰ
            Bind.CreateToolTip(gl.app.In1Combo[num], 'ﾀﾞﾝｻｰ軸(mm/sec)')
            Bind.CreateToolTip(gl.app.In2Combo[num], '参照軸(mm/sec)')
            Bind.CreateToolTip(gl.app.Out1Combo[num], '角度ｾﾝｻ(deg)')
            Bind.CreateToolTip(gl.app.Out2Combo[num], '')
            Bind.CreateToolTip(gl.app.DigitsCoefText[num], 'ﾀﾞﾝｻｰ軸単位変換係数(m/min→mm/sec等)')
            Bind.CreateToolTip(gl.app.CalcCoefText[num], 'ﾀﾞﾝｻｰ半径(mm)')
            Bind.CreateToolTip(gl.app.RatioText[num], '')
            Bind.CreateToolTip(gl.app.TimeLagText[num], '')
        elif gl.app.SensorCombo[num].get() == list[2]:#径演算付きﾀﾞﾝｻｰ
            Bind.CreateToolTip(gl.app.In1Combo[num], '径ｾﾝｻ設定No')
            Bind.CreateToolTip(gl.app.In2Combo[num], '参照軸(mm/sec)')
            Bind.CreateToolTip(gl.app.Out1Combo[num], '角度ｾﾝｻ(deg)')
            Bind.CreateToolTip(gl.app.Out2Combo[num], '')
            Bind.CreateToolTip(gl.app.DigitsCoefText[num], 'ﾀﾞﾝｻｰ軸単位変換係数(m/min→mm/sec等)')
            Bind.CreateToolTip(gl.app.CalcCoefText[num], 'ﾀﾞﾝｻｰ半径(mm)(直行は未入力可)')
            Bind.CreateToolTip(gl.app.RatioText[num], '')
            Bind.CreateToolTip(gl.app.TimeLagText[num], '')
            gl.app.In1Combo[num]['values']=gl.EnableSensor
        elif gl.app.SensorCombo[num].get() == list[3]:#張力系
            Bind.CreateToolTip(gl.app.In1Combo[num], '張力軸(mm/sec)')
            Bind.CreateToolTip(gl.app.In2Combo[num], '参照軸(mm/sec)')
            Bind.CreateToolTip(gl.app.Out1Combo[num], '張力計(N)')
            Bind.CreateToolTip(gl.app.Out2Combo[num], '')
            Bind.CreateToolTip(gl.app.DigitsCoefText[num], '張力軸単位変換係数(m/min→mm/sec等)')
            Bind.CreateToolTip(gl.app.CalcCoefText[num], '張力定数(mm/N)')
            Bind.CreateToolTip(gl.app.RatioText[num], '')
            Bind.CreateToolTip(gl.app.TimeLagText[num], '')
        elif gl.app.SensorCombo[num].get() == list[4]:#径演算付き張力系
            Bind.CreateToolTip(gl.app.In1Combo[num], '径ｾﾝｻ設定No')
            Bind.CreateToolTip(gl.app.In2Combo[num], '参照軸')
            Bind.CreateToolTip(gl.app.Out1Combo[num], '張力計')
            Bind.CreateToolTip(gl.app.Out2Combo[num], '')
            Bind.CreateToolTip(gl.app.DigitsCoefText[num], '張力軸単位変換係数(m/min→mm/sec等)')
            Bind.CreateToolTip(gl.app.CalcCoefText[num], '張力定数(mm/N)')
            Bind.CreateToolTip(gl.app.RatioText[num], '')
            Bind.CreateToolTip(gl.app.TimeLagText[num], '')
            gl.app.In1Combo[num]['values']=gl.EnableSensor
        elif gl.app.SensorCombo[num].get() == list[5]:#径ｾﾝｻ
            Bind.CreateToolTip(gl.app.In1Combo[num], '巻出巻取軸速度(mm/sec)')
            Bind.CreateToolTip(gl.app.In2Combo[num], '径演算径(mm)(速度が演算径速度の場合選択)')
            Bind.CreateToolTip(gl.app.Out1Combo[num], '径ｾﾝｻ')
            Bind.CreateToolTip(gl.app.Out2Combo[num], '')
            Bind.CreateToolTip(gl.app.DigitsCoefText[num], '巻出巻取単位変換係数(m/min→mm/sec等)')
            Bind.CreateToolTip(gl.app.CalcCoefText[num], '箔厚み(mm)')
            Bind.CreateToolTip(gl.app.RatioText[num], '最小径(mm)(速度が最小径速度の場合入力)')
            Bind.CreateToolTip(gl.app.TimeLagText[num], '')
        elif gl.app.SensorCombo[num].get() == list[6]:#ｲｺｰﾙ
            Bind.CreateToolTip(gl.app.In1Combo[num], '入力値')
            Bind.CreateToolTip(gl.app.In2Combo[num], '')
            Bind.CreateToolTip(gl.app.Out1Combo[num], '出力値')
            Bind.CreateToolTip(gl.app.Out2Combo[num], '出力値')
            Bind.CreateToolTip(gl.app.DigitsCoefText[num], 'ｵﾌｾｯﾄ値')
            Bind.CreateToolTip(gl.app.CalcCoefText[num], '入力値係数(未入力可)')
            Bind.CreateToolTip(gl.app.RatioText[num], '比率')
            Bind.CreateToolTip(gl.app.TimeLagText[num], '')
        elif gl.app.SensorCombo[num].get() == list[7]:#Bit演算出力
            Bind.CreateToolTip(gl.app.In1Combo[num], '判定信号Ch')
            Bind.CreateToolTip(gl.app.In2Combo[num], 'OFF時出力参照値(ﾊﾟﾗ2入力時未入力可)')
            Bind.CreateToolTip(gl.app.Out1Combo[num], 'ON時出力参照値(ﾊﾟﾗ3入力時未入力可)')
            Bind.CreateToolTip(gl.app.Out2Combo[num], '出力値')
            Bind.CreateToolTip(gl.app.DigitsCoefText[num], 'Ch1の何Bit目で判定か')
            Bind.CreateToolTip(gl.app.CalcCoefText[num], 'OFF時出力設定値(Ch2設定時未入力可)')
            Bind.CreateToolTip(gl.app.RatioText[num], 'ON時出力設定値(Ch3設定時未入力可)')
            Bind.CreateToolTip(gl.app.TimeLagText[num], '比率(未入力可)')
            Bind.CreateToolTip(gl.app.Out1InvCheck[num], 'Bit信号OFFにて出力時、ﾁｪｯｸ')
            Bind.CreateToolTip(gl.app.Out2InvCheck[num], '')

        #有効無効処理
        if gl.app.SensorCombo[num].get() == list[1] or gl.app.SensorCombo[num].get() == list[2] or \
            gl.app.SensorCombo[num].get() == list[3] or gl.app.SensorCombo[num].get() == list[4] or \
            gl.app.SensorCombo[num].get() == list[5]  :#ﾀﾞﾝｻｰ or 張力計 or 径ｾﾝｻ

            gl.app.Out2Combo[num]['state'] = 'disabled'
            gl.app.Out2InvCheck[num]['state'] = 'disabled'
            gl.app.In2Combo[num]['state'] = 'normal'
            gl.app.CalcCoefText[num]['state'] = 'normal'
            return
        elif gl.app.SensorCombo[num].get() == list[0] or gl.app.SensorCombo[num].get() == list[6]  :#ｴｯｼﾞｾﾝｻ or ｲｺｰﾙ
            gl.app.In2Combo[num]['state'] = 'disabled'
            gl.app.Out2Combo[num]['state'] = 'normal'
            gl.app.Out2InvCheck[num]['state'] = 'normal'
            gl.app.CalcCoefText[num]['state'] = 'normal'
            return
        elif gl.app.SensorCombo[num].get() == list[7]:
            gl.app.In2Combo[num]['state'] = 'normal'
            gl.app.Out2Combo[num]['state'] = 'normal'
            gl.app.Out2InvCheck[num]['state'] = 'disabled'
            gl.app.CalcCoefText[num]['state'] = 'normal'
            return

        #elif gl.app.SensorCombo[num].get() == list[5] :
        #    gl.app.In2Combo[num]['state'] = 'disabled'
        #    gl.app.Out2Combo[num]['state'] = 'disabled'
        #    gl.app.Out2InvCheck[num]['state'] = 'disabled'
        #    gl.app.CalcCoefText[num]['state'] = 'normal'
        #    return

    #未入力時
    gl.app.In2Combo[num]['state'] = 'normal'
    gl.app.Out2Combo[num]['state'] = 'normal'
    gl.app.Out2InvCheck[num]['state'] = 'normal'
    gl.app.CalcCoefText[num]['state'] = 'normal'
    Bind.CreateToolTip(gl.app.In1Combo[num], '')
    Bind.CreateToolTip(gl.app.In2Combo[num], '')
    Bind.CreateToolTip(gl.app.Out1Combo[num], '')
    Bind.CreateToolTip(gl.app.Out2Combo[num], '')
    Bind.CreateToolTip(gl.app.DigitsCoefText[num], '')
    Bind.CreateToolTip(gl.app.CalcCoefText[num], '')
    Bind.CreateToolTip(gl.app.RatioText[num], '')
    Bind.CreateToolTip(gl.app.TimeLagText[num], '')
    Bind.CreateToolTip(gl.app.Out1InvCheck[num], '')
    Bind.CreateToolTip(gl.app.Out2InvCheck[num], '')


        
def BackUp():
    #変数に値格納
    for i in range(gl.ChMax):
        gl.SensorConfDic[i] = {'Sensor':gl.app.SensorCombo[i].get(),'In1':gl.app.In1Combo[i].get(),'In2':gl.app.In2Combo[i].get(),\
                'Out1':gl.app.Out1Combo[i].get(),'Out2':gl.app.Out2Combo[i].get(),'Out1Inv':gl.app.Out1InvVal[i].get(),\
                'Out2Inv':gl.app.Out2InvVal[i].get(),'DigitsCoef':gl.app.DigitsCoefText[i].get(),'CalcCoef':gl.app.CalcCoefText[i].get(),\
                'Ratio':gl.app.RatioText[i].get(),'TimeLag':gl.app.TimeLagText[i].get(),'Disable':gl.app.DisableVal[i].get()}

#サブウインドウを閉じ受付時の処理
def SensorConfWincallback():
    
    BackUp()

    if not EnableCheck() :
        return
        
    gl.SensorConfWin.destroy()

def EnableCheck():

    gl.EnableSensor=[]
    #変数に値格納
    for i in range(gl.ChMax):

        if not gl.SensorConfDic[i]['Disable'] :#無効じゃない
            if gl.SensorConfDic[i]['Sensor'] != '' :#センサーが選択されている
                if gl.SensorConfDic[i]['In1'] != '' :#入力1が入力されている
                    if gl.SensorConfDic[i]['Sensor'] != gl.SensorList[2] and gl.SensorConfDic[i]['Sensor'] != gl.SensorList[4]:#径演算ﾀﾞﾝｻｰ・張力ではない
                        if int(gl.SensorConfDic[i]['In1']) not in gl.EnableCh:#Ch判定
                            messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の入力1で未使用Chが設定されています。\n修正か無効化してください。')
                            return
                    else:
                        DiameterNo = int(gl.SensorConfDic[i]['In1'])-1
                        #if int(gl.SensorConfDic[i]['In1']) not in gl.EnableSensor:#ｾﾝｻｰ判定
                        if gl.SensorConfDic[DiameterNo]['Disable'] or gl.SensorConfDic[DiameterNo]['Sensor'] != gl.SensorList[5]:
                            messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の入力1で未使用Chが設定されています。\n修正か無効化してください。')
                            return

                else:
                    messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の入力1が未入力です。\n修正か無効化してください。')
                    return
                if gl.SensorConfDic[i]['In2'] != ''  :#入力2が入力されている
                    if int(gl.SensorConfDic[i]['In2']) not in gl.EnableCh:
                        messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の入力2で未使用Chが設定されています。\n修正か無効化してください。')
                        return
                elif gl.SensorConfDic[i]['Sensor'] != gl.SensorList[0] and gl.SensorConfDic[i]['Sensor'] != gl.SensorList[5] \
                    and gl.SensorConfDic[i]['Sensor'] != gl.SensorList[6] and gl.SensorConfDic[i]['Sensor'] != gl.SensorList[7]:#ｴｯｼﾞｾﾝｻor径ｾﾝｻorｲｺｰﾙ以外
                    messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の入力2が未入力です。\n修正か無効化してください。')
                    return
                if gl.SensorConfDic[i]['Out1'] != '' :#出力1が入力されている
                    if int(gl.SensorConfDic[i]['Out1']) not in gl.EnableCh:
                        messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の出力1で未使用Chが設定されています。\n修正か無効化してください。')
                        return
                if gl.SensorConfDic[i]['Out2'] != '' :#出力2が入力されている
                    if int(gl.SensorConfDic[i]['Out2']) not in gl.EnableCh:
                        messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の出力2で未使用Chが設定されています。\n修正か無効化してください。')
                        return

                if gl.SensorConfDic[i]['Sensor'] != gl.SensorList[0] and gl.SensorConfDic[i]['Sensor'] != gl.SensorList[6] \
                     and gl.SensorConfDic[i]['Sensor'] != gl.SensorList[7]:#ｴｯｼﾞｾﾝｻorｲｺｰﾙじゃない
                    if gl.SensorConfDic[i]['Out1'] == '' :        
                        messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の出力1が未入力です。\n修正か無効化してください。')
                        return
                    if gl.SensorConfDic[i]['CalcCoef'] == '' :
                        if gl.SensorConfDic[i]['Sensor'] != gl.SensorList[1] and gl.SensorConfDic[i]['Sensor'] != gl.SensorList[2] :#ﾀﾞﾝｻｰ、径演算ﾀﾞﾝｻｰじゃない
                            messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'のﾊﾟﾗﾒｰﾀ2が未入力です。\n修正か無効化してください。')
                            return
                else:
                    if gl.SensorConfDic[i]['Out1'] == '' and  gl.SensorConfDic[i]['Out2'] == '' :       
                        messagebox.showinfo('センサー設定エラー','設定No'+str(i+1)+'の出力が未入力です。\n修正か無効化してください。')
                        return
                    
                gl.EnableSensor.append(i+1)

    return True