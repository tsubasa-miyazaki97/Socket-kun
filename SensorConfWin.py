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
        # ウィジェット構築中は非表示にして描画コストを削減
        gl.SensorConfWin.withdraw()
        gl.SensorConfWin.geometry(str(winwidth)+"x"+str(winheight))
        gl.SensorConfWin.title("センサー設定")
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
        gl.app.Sensormainm_frame.grid(row=1, column=0, sticky="nsew")
        gl.app.Sensormainm_frame.grid_rowconfigure(0, weight=1)
        gl.app.Sensormainm_frame.grid_columnconfigure(0, weight=1)
        #スクロールバー設置
        gl.app.Sensorcanvas = tk.Canvas(gl.app.Sensormainm_frame, highlightthickness=0)#スクロールバー置けるウィジェット(キャンバス)配置

        gl.app.SensorFrame = tk.Frame(gl.app.Sensorcanvas, highlightthickness=0)#キャンバス上にﾌﾚｰﾑ設置
        gl.app.Sensorcanvas.grid(row=0, column=0, sticky="nsew")
        gl.app.Sensorcanvas.create_window(0,0,window=gl.app.SensorFrame,anchor="nw")#キャンバスにフレーム設置
        gl.app.Sensorcanvas.config(scrollregion=gl.app.Sensorcanvas.bbox('all'))#フレームにフィットするようにキャンバスのスクロール可能範囲を変更

        gl.app.Sensorybar = tk.Scrollbar(gl.SensorConfWin,orient=tk.VERTICAL)#縦スクロールバー配置
        gl.app.Sensorybar.grid(row=1,column=1,sticky=tk.N+tk.S)
        gl.app.Sensorybar.config(command=gl.app.Sensorcanvas.yview)#縦スクロール用ｺﾏﾝﾄﾞ
        gl.app.Sensorcanvas.config(yscrollcommand=gl.app.Sensorybar.set)#キャンバスにスクロールバーの動きを反映
        gl.app.Sensorcanvas.yview_moveto(0)#キャンバスのスクロールを初期化
        gl.app.SensorFrame.bind("<MouseWheel>",lambda event,arg1=gl.app.Sensorcanvas,arg2=gl.app.SensorFrame: Bind.mouse_y_scroll(event,arg1,arg2))#マウスホイール関数をﾌﾚｰﾑにｾｯﾄ
        gl.app.Sensorcanvas.bind("<MouseWheel>",lambda event: Bind.mouse_y_scroll(event,gl.app.Sensorcanvas,None))#キャンバス空白部分のマウスホイール対応

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

        # ヘッダー構築完了後に早期表示・グラブ（行生成前に画面を出す）
        gl.SensorConfWin.deiconify()
        gl.SensorConfWin.grab_set()
        gl.SensorConfWin.focus_set()
        gl.SensorConfWin.update()

        # データ行: None で事前確保 (遅延構築対応)
        gl.app.SensorNolabel   = [None] * gl.ChMax
        gl.app.SensorCombo     = [None] * gl.ChMax
        gl.app.In1Combo        = [None] * gl.ChMax
        gl.app.In2Combo        = [None] * gl.ChMax
        gl.app.Out1Combo       = [None] * gl.ChMax
        gl.app.Out2Combo       = [None] * gl.ChMax
        gl.app.Out1InvCheck    = [None] * gl.ChMax
        gl.app.Out1InvVal      = [None] * gl.ChMax
        gl.app.Out2InvCheck    = [None] * gl.ChMax
        gl.app.Out2InvVal      = [None] * gl.ChMax
        gl.app.DigitsCoefText  = [None] * gl.ChMax
        gl.app.CalcCoefText    = [None] * gl.ChMax
        gl.app.RatioText       = [None] * gl.ChMax
        gl.app.TimeLagText     = [None] * gl.ChMax
        gl.app.DisableCheck    = [None] * gl.ChMax
        gl.app.DisableVal      = [None] * gl.ChMax

        # 未構築行のデフォルト空値 (BackUp / ConfClear で使用)
        _EMPTY_ROW = {'Sensor':'','In1':'','In2':'','Out1':'','Out2':'',
                      'Out1Inv':False,'Out2Inv':False,'DigitsCoef':'',
                      'CalcCoef':'','Ratio':'','TimeLag':'','Disable':False}

        # 最初のバッチは大きめにして初期表示を速くする
        FIRST_BATCH = 40
        BATCH       = 50

        # ペンディング after() ジョブを追跡 (ウィンドウ破棄時にキャンセル)
        gl._sensor_build_job = None

        def _build_batch(start):
            if gl.SensorConfWin is None or not gl.SensorConfWin.winfo_exists():
                gl._sensor_build_job = None
                return
            canvas = gl.app.Sensorcanvas
            end = min(start + (FIRST_BATCH if start == 1 else BATCH), gl.ChMax + 1)

            for i in range(start, end):
                r = i  # row (0=ヘッダー, 1..ChMax=データ)
                idx = i - 1  # SensorConfDic は 0-indexed

                lbl = tk.Label(gl.app.SensorFrame, text=i, font=(deffont, fsizes))
                lbl.grid(row=r, column=C_NO, padx=2)
                gl.app.SensorNolabel[idx] = lbl

                combo = ttk.Combobox(gl.app.SensorFrame, values=gl.SensorList, font=(deffont, fsizes), width=8)
                combo.grid(row=r, column=C_SENSOR, padx=2)
                combo.bind('<FocusOut>', lambda event, arg1=combo, arg2=gl.SensorList, arg3=idx: (Bind.ComboChange(event,arg1,arg2), SensorSelect(event,arg2,arg3)))
                combo.bind("<<ComboboxSelected>>", lambda event, arg1=gl.SensorList, arg2=idx: SensorSelect(event,arg1,arg2))
                combo.bind("<MouseWheel>", lambda event, a=canvas, b=combo: Bind.mouse_y_scroll(event, a, b))
                gl.app.SensorCombo[idx] = combo

                in1 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
                in1.grid(row=r, column=C_IN1, padx=2)
                in1.bind('<FocusOut>', lambda event, arg1=in1, arg2=gl.EnableCh: Bind.ComboChange(event,arg1,arg2))
                in1.bind("<MouseWheel>", lambda event, a=canvas, b=in1: Bind.mouse_y_scroll(event, a, b))
                gl.app.In1Combo[idx] = in1

                in2 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
                in2.grid(row=r, column=C_IN2, padx=2)
                in2.bind('<FocusOut>', lambda event, arg1=in2, arg2=gl.EnableCh: Bind.ComboChange(event,arg1,arg2))
                in2.bind("<MouseWheel>", lambda event, a=canvas, b=in2: Bind.mouse_y_scroll(event, a, b))
                gl.app.In2Combo[idx] = in2

                out1 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
                out1.grid(row=r, column=C_OUT1, padx=2)
                out1.bind('<FocusOut>', lambda event, arg1=out1, arg2=gl.EnableCh: Bind.ComboChange(event,arg1,arg2))
                out1.bind("<MouseWheel>", lambda event, a=canvas, b=out1: Bind.mouse_y_scroll(event, a, b))
                gl.app.Out1Combo[idx] = out1

                out2 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
                out2.grid(row=r, column=C_OUT2, padx=2)
                out2.bind('<FocusOut>', lambda event, arg1=out2, arg2=gl.EnableCh: Bind.ComboChange(event,arg1,arg2))
                out2.bind("<MouseWheel>", lambda event, a=canvas, b=out2: Bind.mouse_y_scroll(event, a, b))
                gl.app.Out2Combo[idx] = out2

                out1inv_val   = tk.BooleanVar()
                out1inv_check = ttk.Checkbutton(gl.app.SensorFrame, variable=out1inv_val)
                out1inv_check.grid(row=r, column=C_OUT1INV, padx=2)
                gl.app.Out1InvVal[idx]   = out1inv_val
                gl.app.Out1InvCheck[idx] = out1inv_check

                out2inv_val   = tk.BooleanVar()
                out2inv_check = ttk.Checkbutton(gl.app.SensorFrame, variable=out2inv_val)
                out2inv_check.grid(row=r, column=C_OUT2INV, padx=2)
                gl.app.Out2InvVal[idx]   = out2inv_val
                gl.app.Out2InvCheck[idx] = out2inv_check

                para1 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
                para1.grid(row=r, column=C_PARA1, padx=2)
                para1.bind('<FocusOut>', lambda event, arg1=para1: Bind.TextFloatCheck(event,arg1))
                para1.bind("<MouseWheel>", lambda event, a=canvas, b=para1: Bind.mouse_y_scroll(event, a, b))
                gl.app.DigitsCoefText[idx] = para1

                para2 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
                para2.grid(row=r, column=C_PARA2, padx=2)
                para2.bind('<FocusOut>', lambda event, arg1=para2: Bind.TextFloatCheck(event,arg1))
                para2.bind("<MouseWheel>", lambda event, a=canvas, b=para2: Bind.mouse_y_scroll(event, a, b))
                gl.app.CalcCoefText[idx] = para2

                para3 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
                para3.grid(row=r, column=C_PARA3, padx=2)
                para3.bind('<FocusOut>', lambda event, arg1=para3: Bind.TextFloatCheck(event,arg1))
                para3.bind("<MouseWheel>", lambda event, a=canvas, b=para3: Bind.mouse_y_scroll(event, a, b))
                gl.app.RatioText[idx] = para3

                para4 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
                para4.grid(row=r, column=C_PARA4, padx=2)
                para4.bind('<FocusOut>', lambda event, arg1=para4: Bind.TextFloatCheck(event,arg1))
                para4.bind("<MouseWheel>", lambda event, a=canvas, b=para4: Bind.mouse_y_scroll(event, a, b))
                gl.app.TimeLagText[idx] = para4

                disable_val   = tk.BooleanVar()
                disable_check = ttk.Checkbutton(gl.app.SensorFrame, variable=disable_val)
                disable_check.grid(row=r, column=C_DISABLE, padx=2)
                gl.app.DisableVal[idx]   = disable_val
                gl.app.DisableCheck[idx] = disable_check

                # ウィジェットに値を反映
                combo.set(gl.SensorConfDic[idx]['Sensor'])
                in1.set(gl.SensorConfDic[idx]['In1'])
                in2.set(gl.SensorConfDic[idx]['In2'])
                out1.set(gl.SensorConfDic[idx]['Out1'])
                out2.set(gl.SensorConfDic[idx]['Out2'])
                out1inv_val.set(gl.SensorConfDic[idx]['Out1Inv'])
                out2inv_val.set(gl.SensorConfDic[idx]['Out2Inv'])
                para1.insert(tk.END, gl.SensorConfDic[idx]['DigitsCoef'])
                para2.insert(tk.END, gl.SensorConfDic[idx]['CalcCoef'])
                para3.insert(tk.END, gl.SensorConfDic[idx]['Ratio'])
                para4.insert(tk.END, gl.SensorConfDic[idx]['TimeLag'])
                disable_val.set(gl.SensorConfDic[idx]['Disable'])

                # センサー種別に応じたウィジェット有効/無効の初期設定
                # 空行はデフォルト状態 (全有効) なので SensorSelect 呼び出しをスキップして高速化
                # センサーが選択済みの行のみ SensorSelect を呼び出す
                if gl.SensorConfDic[idx]['Sensor']:
                    SensorSelect('', gl.SensorList, idx)
                else:
                    in2.config(state='normal')
                    out2.config(state='normal')
                    out2inv_check.config(state='normal')
                    para2.config(state='normal')

            canvas.config(scrollregion=canvas.bbox('all'))

            if end <= gl.ChMax:
                # 次のバッチをイベントループに委ねる（ユーザー操作を都度受け付けるため）
                gl._sensor_build_job = gl.SensorConfWin.after(0, _build_batch, end)
            else:
                gl._sensor_build_job = None
                # 全行構築完了後の最終セットアップ
                gl.SensorConfWin.protocol('WM_DELETE_WINDOW', SensorConfWincallback)
                # スクロール範囲を確定し、以降の変更に追従するよう<Configure>をバインド
                gl.app.SensorFrame.bind("<Configure>", lambda e: gl.app.Sensorcanvas.config(scrollregion=gl.app.Sensorcanvas.bbox('all')))

        # 最初のバッチをイベントループ経由で開始（ウィンドウを即座に操作可能にするため）
        gl._sensor_build_job = gl.SensorConfWin.after(0, _build_batch, 1)

    else:
        gl.SensorConfWin.lift()
        gl.SensorConfWin.focus_set()


#-----------------------------------------

def ConfClear():
    if inspect.stack()[1].function != 'DefConf':
        if not messagebox.askyesno('設定クリア','現在の入力をクリアしますか？') :
            return

    _empty = {'Sensor':'','In1':'','In2':'','Out1':'','Out2':'',
              'Out1Inv':False,'Out2Inv':False,'DigitsCoef':'',
              'CalcCoef':'','Ratio':'','TimeLag':'','Disable':False}

    for i in range(gl.ChMax) :#内容クリア（バッチ構築中は構築済みの行のみ）
        if gl.app.SensorCombo[i] is None:
            # 未構築行: SensorConfDic を直接クリア
            gl.SensorConfDic[i] = _empty.copy()
            continue
        gl.app.SensorCombo[i].set('')
        gl.app.In1Combo[i].set('')
        gl.app.In2Combo[i].set('')
        gl.app.Out1Combo[i].set('')
        gl.app.Out2Combo[i].set('')
        gl.app.Out1InvVal[i].set(False)
        gl.app.Out2InvVal[i].set(False)
        gl.app.DigitsCoefText[i].delete(0,tk.END)
        gl.app.CalcCoefText[i].delete(0,tk.END)
        gl.app.RatioText[i].delete(0,tk.END)
        gl.app.TimeLagText[i].delete(0,tk.END)
        gl.app.DisableVal[i].set(False)

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
    #変数に値格納 (未構築行は SensorConfDic の値をそのまま維持)
    for i in range(gl.ChMax):
        if gl.app.SensorCombo[i] is None:
            continue  # 未構築行: 起動時に読み込んだ SensorConfDic の値が正
        gl.SensorConfDic[i] = {'Sensor':gl.app.SensorCombo[i].get(),'In1':gl.app.In1Combo[i].get(),'In2':gl.app.In2Combo[i].get(),\
                'Out1':gl.app.Out1Combo[i].get(),'Out2':gl.app.Out2Combo[i].get(),'Out1Inv':gl.app.Out1InvVal[i].get(),\
                'Out2Inv':gl.app.Out2InvVal[i].get(),'DigitsCoef':gl.app.DigitsCoefText[i].get(),'CalcCoef':gl.app.CalcCoefText[i].get(),\
                'Ratio':gl.app.RatioText[i].get(),'TimeLag':gl.app.TimeLagText[i].get(),'Disable':gl.app.DisableVal[i].get()}

#サブウインドウを閉じ受付時の処理
def SensorConfWincallback():

    # バックグラウンドでの行構築ジョブが残っていればキャンセル
    if getattr(gl, '_sensor_build_job', None) is not None:
        try:
            gl.SensorConfWin.after_cancel(gl._sensor_build_job)
        except Exception:
            pass
        gl._sensor_build_job = None

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