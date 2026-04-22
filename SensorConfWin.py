from ast import And
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import inspect
import time
import WidgetBind as Bind
import TCPGlobalVar as gl

#通信設定画面表示
def SensorConf() :

    deffont = gl.deffont
    fsizes = gl.fsizes
    
    winwidth=800
    winheight = gl.winheight


    if gl.SensorConfWin ==  None or not gl.SensorConfWin.winfo_exists()  :
        _t_start = time.perf_counter()

        gl.SensorConfWin = tk.Toplevel()
        gl.SensorConfWin.withdraw()
        gl.SensorConfWin.geometry(str(winwidth)+"x"+str(winheight))
        gl.SensorConfWin.title("センサー設定")
        gl.SensorConfWin.grid_rowconfigure(0, weight=0)
        gl.SensorConfWin.grid_rowconfigure(1, weight=0)  # 固定ヘッダー行
        gl.SensorConfWin.grid_rowconfigure(2, weight=1)  # キャンバス行
        gl.SensorConfWin.grid_columnconfigure(0, weight=1)

        # ツールバーフレーム
        toolbar_frame = tk.Frame(gl.SensorConfWin)
        toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        gl.app.ConfClearbutton = tk.Button(toolbar_frame, text="設定クリア", command=lambda : ConfClear())
        gl.app.ConfClearbutton.grid(row=0, column=0, padx=2, pady=2)

        # 固定ヘッダーフレーム（スクロールしない / row=1）
        sensor_header_frame = tk.Frame(gl.SensorConfWin, relief='flat')
        sensor_header_frame.grid(row=1, column=0, sticky="ew")

        gl.app.Sensormainm_frame = tk.Frame(gl.SensorConfWin)
        gl.app.Sensormainm_frame.grid(row=2, column=0, sticky="nsew")
        gl.app.Sensormainm_frame.grid_rowconfigure(0, weight=1)
        gl.app.Sensormainm_frame.grid_columnconfigure(0, weight=1)

        gl.app.Sensorcanvas = tk.Canvas(gl.app.Sensormainm_frame, highlightthickness=0)
        gl.app.SensorFrame  = tk.Frame(gl.app.Sensorcanvas, highlightthickness=0)
        gl.app.Sensorcanvas.grid(row=0, column=0, sticky="nsew")
        gl.app.Sensorcanvas.create_window(0, 0, window=gl.app.SensorFrame, anchor="nw")

        gl.app.Sensorybar = tk.Scrollbar(gl.SensorConfWin, orient=tk.VERTICAL)
        gl.app.Sensorybar.grid(row=2, column=1, sticky=tk.N+tk.S)
        gl.app.Sensorcanvas.config(yscrollcommand=gl.app.Sensorybar.set)
        gl.app.Sensorcanvas.yview_moveto(0)

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

        # 固定ヘッダーラベル (sensor_header_frame に配置 / スクロールしない)
        # カラム幅は update_idletasks() 後にデータフレームの実測値に合わせて同期する
        tk.Label(sensor_header_frame, text="No",         font=(deffont, fsizes), anchor='center').grid(row=0, column=C_NO,      padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="ｾﾝｻ種",      font=(deffont, fsizes), anchor='center').grid(row=0, column=C_SENSOR,  padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="Ch1",        font=(deffont, fsizes), anchor='center').grid(row=0, column=C_IN1,     padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="Ch2",        font=(deffont, fsizes), anchor='center').grid(row=0, column=C_IN2,     padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="Ch3",        font=(deffont, fsizes), anchor='center').grid(row=0, column=C_OUT1,    padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="Ch4",        font=(deffont, fsizes), anchor='center').grid(row=0, column=C_OUT2,    padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="出力1\n反転", font=(deffont, fsizes), anchor='center').grid(row=0, column=C_OUT1INV, padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="出力2\n反転", font=(deffont, fsizes), anchor='center').grid(row=0, column=C_OUT2INV, padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="ﾊﾟﾗ1",       font=(deffont, fsizes), anchor='center').grid(row=0, column=C_PARA1,   padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="ﾊﾟﾗ2",       font=(deffont, fsizes), anchor='center').grid(row=0, column=C_PARA2,   padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="ﾊﾟﾗ3",       font=(deffont, fsizes), anchor='center').grid(row=0, column=C_PARA3,   padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="ﾊﾟﾗ4",       font=(deffont, fsizes), anchor='center').grid(row=0, column=C_PARA4,   padx=2, pady=2, sticky='ew')
        tk.Label(sensor_header_frame, text="無効",        font=(deffont, fsizes), anchor='center').grid(row=0, column=C_DISABLE, padx=2, pady=2, sticky='ew')

        # ウィジェットリストを None で初期化（バーチャルスクロール対応）
        # 未描画行は None のまま。描画済み行のみ実際のウィジェットが入る。
        gl.app.SensorNolabel  = [None] * gl.ChMax
        gl.app.SensorCombo    = [None] * gl.ChMax
        gl.app.In1Combo       = [None] * gl.ChMax
        gl.app.In2Combo       = [None] * gl.ChMax
        gl.app.Out1Combo      = [None] * gl.ChMax
        gl.app.Out2Combo      = [None] * gl.ChMax
        gl.app.Out1InvCheck   = [None] * gl.ChMax
        gl.app.Out1InvVal     = [None] * gl.ChMax
        gl.app.Out2InvCheck   = [None] * gl.ChMax
        gl.app.Out2InvVal     = [None] * gl.ChMax
        gl.app.DigitsCoefText = [None] * gl.ChMax
        gl.app.CalcCoefText   = [None] * gl.ChMax
        gl.app.RatioText      = [None] * gl.ChMax
        gl.app.TimeLagText    = [None] * gl.ChMax
        gl.app.DisableCheck   = [None] * gl.ChMax
        gl.app.DisableVal     = [None] * gl.ChMax

        # ---- バーチャルスクロール状態 ----
        # 表示中の行のみウィジェットを生成し、未表示行は grid_rowconfigure(minsize)
        # でスクロール高さだけ確保する。2600 ウィジェット一括生成を回避。
        _rendered = set()  # ウィジェットが存在する行番号 (1-based)
        _row_h    = [32]   # 実測行高さ [px]（update_idletasks 後に更新）
        _BUFFER   = 3      # 上下バッファ行数
        canvas    = gl.app.Sensorcanvas

        # ---- スクロールデバウンス ----
        # スクロールバーを素早く動かした場合、ウィジェット生成を 150ms 遅延させて
        # 連続発火による固まりを防ぐ。キャンバスの視覚スクロール自体は即時実行。
        _scroll_after_id = [None]

        def _schedule_update():
            if _scroll_after_id[0] is not None:
                gl.SensorConfWin.after_cancel(_scroll_after_id[0])
            _scroll_after_id[0] = gl.SensorConfWin.after(150, _update_visible_rows)

        # ---- マウスホイール ----
        def _on_mousewheel(event):
            Bind.mouse_y_scroll(event, canvas, None)
            _schedule_update()

        def _on_mousewheel_combo(event, combo_widget):
            Bind.mouse_y_scroll(event, canvas, combo_widget)
            _schedule_update()

        # ---- 1行分のウィジェット生成 ----
        def _build_row(i):
            """行 i (1-based) のウィジェットをグリッドに生成する。"""
            if i in _rendered:
                return
            _rendered.add(i)
            idx = i - 1

            # minsize プレースホルダーを解除してウィジェットで高さを決める
            gl.app.SensorFrame.grid_rowconfigure(i, minsize=0)

            lbl = tk.Label(gl.app.SensorFrame, text=i, font=(deffont, fsizes))
            lbl.grid(row=i, column=C_NO, padx=2)
            lbl.bind("<MouseWheel>", lambda e: _on_mousewheel(e))
            lbl.bind("<FocusIn>",    lambda e: Bind.TipDel(e))
            gl.app.SensorNolabel[idx] = lbl

            combo = ttk.Combobox(gl.app.SensorFrame, values=gl.SensorList, font=(deffont, fsizes), width=8)
            combo.grid(row=i, column=C_SENSOR, padx=2)
            combo.bind('<FocusOut>',          lambda e, a=combo, b=gl.SensorList, c=idx: (Bind.ComboChange(e, a, b), SensorSelect(e, b, c)))
            combo.bind("<<ComboboxSelected>>", lambda e, a=gl.SensorList, b=idx: SensorSelect(e, a, b))
            combo.bind("<MouseWheel>",        lambda e, a=combo: _on_mousewheel_combo(e, a))
            combo.bind("<FocusIn>",           lambda e: Bind.TipDel(e))
            gl.app.SensorCombo[idx] = combo

            in1 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
            in1.grid(row=i, column=C_IN1, padx=2)
            in1.bind('<FocusOut>',  lambda e, a=in1, b=gl.EnableCh: Bind.ComboChange(e, a, b))
            in1.bind("<MouseWheel>", lambda e, a=in1: _on_mousewheel_combo(e, a))
            in1.bind("<FocusIn>",   lambda e: Bind.TipDel(e))
            gl.app.In1Combo[idx] = in1

            in2 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
            in2.grid(row=i, column=C_IN2, padx=2)
            in2.bind('<FocusOut>',  lambda e, a=in2, b=gl.EnableCh: Bind.ComboChange(e, a, b))
            in2.bind("<MouseWheel>", lambda e, a=in2: _on_mousewheel_combo(e, a))
            in2.bind("<FocusIn>",   lambda e: Bind.TipDel(e))
            gl.app.In2Combo[idx] = in2

            out1 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
            out1.grid(row=i, column=C_OUT1, padx=2)
            out1.bind('<FocusOut>',  lambda e, a=out1, b=gl.EnableCh: Bind.ComboChange(e, a, b))
            out1.bind("<MouseWheel>", lambda e, a=out1: _on_mousewheel_combo(e, a))
            out1.bind("<FocusIn>",   lambda e: Bind.TipDel(e))
            gl.app.Out1Combo[idx] = out1

            out2 = ttk.Combobox(gl.app.SensorFrame, values=gl.EnableCh, font=(deffont, fsizes), width=3)
            out2.grid(row=i, column=C_OUT2, padx=2)
            out2.bind('<FocusOut>',  lambda e, a=out2, b=gl.EnableCh: Bind.ComboChange(e, a, b))
            out2.bind("<MouseWheel>", lambda e, a=out2: _on_mousewheel_combo(e, a))
            out2.bind("<FocusIn>",   lambda e: Bind.TipDel(e))
            gl.app.Out2Combo[idx] = out2

            out1inv_val   = tk.BooleanVar()
            out1inv_check = ttk.Checkbutton(gl.app.SensorFrame, variable=out1inv_val)
            out1inv_check.grid(row=i, column=C_OUT1INV, padx=2)
            out1inv_check.bind("<MouseWheel>", lambda e: _on_mousewheel(e))
            out1inv_check.bind("<FocusIn>",    lambda e: Bind.TipDel(e))
            gl.app.Out1InvVal[idx]   = out1inv_val
            gl.app.Out1InvCheck[idx] = out1inv_check

            out2inv_val   = tk.BooleanVar()
            out2inv_check = ttk.Checkbutton(gl.app.SensorFrame, variable=out2inv_val)
            out2inv_check.grid(row=i, column=C_OUT2INV, padx=2)
            out2inv_check.bind("<MouseWheel>", lambda e: _on_mousewheel(e))
            out2inv_check.bind("<FocusIn>",    lambda e: Bind.TipDel(e))
            gl.app.Out2InvVal[idx]   = out2inv_val
            gl.app.Out2InvCheck[idx] = out2inv_check

            para1 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
            para1.grid(row=i, column=C_PARA1, padx=2)
            para1.bind('<FocusOut>',  lambda e, a=para1: Bind.TextFloatCheck(e, a))
            para1.bind("<MouseWheel>", lambda e: _on_mousewheel(e))
            para1.bind("<FocusIn>",   lambda e: Bind.TipDel(e))
            gl.app.DigitsCoefText[idx] = para1

            para2 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
            para2.grid(row=i, column=C_PARA2, padx=2)
            para2.bind('<FocusOut>',  lambda e, a=para2: Bind.TextFloatCheck(e, a))
            para2.bind("<MouseWheel>", lambda e: _on_mousewheel(e))
            para2.bind("<FocusIn>",   lambda e: Bind.TipDel(e))
            gl.app.CalcCoefText[idx] = para2

            para3 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
            para3.grid(row=i, column=C_PARA3, padx=2)
            para3.bind('<FocusOut>',  lambda e, a=para3: Bind.TextFloatCheck(e, a))
            para3.bind("<MouseWheel>", lambda e: _on_mousewheel(e))
            para3.bind("<FocusIn>",   lambda e: Bind.TipDel(e))
            gl.app.RatioText[idx] = para3

            para4 = tk.Entry(gl.app.SensorFrame, font=(deffont, fsizes), width=8)
            para4.grid(row=i, column=C_PARA4, padx=2)
            para4.bind('<FocusOut>',  lambda e, a=para4: Bind.TextFloatCheck(e, a))
            para4.bind("<MouseWheel>", lambda e: _on_mousewheel(e))
            para4.bind("<FocusIn>",   lambda e: Bind.TipDel(e))
            gl.app.TimeLagText[idx] = para4

            disable_val   = tk.BooleanVar()
            disable_check = ttk.Checkbutton(gl.app.SensorFrame, variable=disable_val)
            disable_check.grid(row=i, column=C_DISABLE, padx=2)
            disable_check.bind("<MouseWheel>", lambda e: _on_mousewheel(e))
            disable_check.bind("<FocusIn>",    lambda e: Bind.TipDel(e))
            gl.app.DisableVal[idx]   = disable_val
            gl.app.DisableCheck[idx] = disable_check

            # SensorConfDic → ウィジェットに値反映
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
            if combo.get():
                SensorSelect('', gl.SensorList, idx)

        # ---- 表示中の行番号を計算 ----
        def _get_visible_range():
            h = canvas.winfo_height()
            if h <= 1:
                return 1, 20
            y0 = canvas.canvasy(0)
            y1 = canvas.canvasy(h)
            rh = max(1, _row_h[0])
            first = max(1, int(y0 / rh))
            last  = min(gl.ChMax, int(y1 / rh) + 1)
            return first, last

        # ---- スクロール後に必要な行を生成 ----
        def _update_visible_rows():
            first, last = _get_visible_range()
            first_buf = max(1, first - _BUFFER)
            last_buf  = min(gl.ChMax, last + _BUFFER)
            new_rows = False
            for i in range(first_buf, last_buf + 1):
                if i not in _rendered:
                    _build_row(i)
                    new_rows = True
            if new_rows:
                canvas.config(scrollregion=canvas.bbox('all'))

        # ---- スクロールバーコマンド（行生成を伴う） ----
        def _do_yview(*args):
            canvas.yview(*args)
            _schedule_update()

        gl.app.Sensorybar.config(command=_do_yview)
        gl.app.SensorFrame.bind("<MouseWheel>",  lambda e: _on_mousewheel(e))
        gl.app.Sensorcanvas.bind("<MouseWheel>", lambda e: _on_mousewheel(e))

        # ---- 初期描画: 最初の FIRST_ROWS 行のみウィジェット生成 ----
        FIRST_ROWS = 20
        for i in range(1, FIRST_ROWS + 1):
            _build_row(i)

        # 初期 FIRST_ROWS 行のみ update_idletasks（少行数なので高速）
        _t0 = time.perf_counter()
        gl.SensorConfWin.update_idletasks()

        # 実際の行高さを計測してプレースホルダーサイズに使用
        # SensorFrame にはヘッダーなし（データ行のみ）なので FIRST_ROWS で割る
        total_h = gl.app.SensorFrame.winfo_reqheight()
        _row_h[0] = max(1, total_h // FIRST_ROWS)

        # 各列幅を max(ヘッダーラベル幅, データウィジェット幅) に揃える
        # 小さい方はセル内に自動で余白を持つ形となる
        for _col in range(13):
            _hb = sensor_header_frame.grid_bbox(column=_col, row=0)
            _db = gl.app.SensorFrame.grid_bbox(column=_col, row=1)
            _cw = max(_hb[2] if _hb else 0, _db[2] if _db else 0)
            if _cw > 0:
                sensor_header_frame.grid_columnconfigure(_col, minsize=_cw)
                gl.app.SensorFrame.grid_columnconfigure(_col, minsize=_cw)

        # ウィンドウ幅をコンテンツ幅に合わせて自動調整（IO読書ウィンドウと同様）
        gl.SensorConfWin.update_idletasks()
        frame_w     = gl.app.SensorFrame.winfo_reqwidth()
        scrollbar_w = gl.app.Sensorybar.winfo_reqwidth()
        if scrollbar_w <= 1:
            scrollbar_w = gl.app.Sensorybar.winfo_width()
        fit_width = frame_w + scrollbar_w
        gl.SensorConfWin.geometry(str(fit_width) + "x" + str(winheight))

        # 残り行: ウィジェットなし、minsize でスクロール高さだけ確保
        for i in range(FIRST_ROWS + 1, gl.ChMax + 1):
            gl.app.SensorFrame.grid_rowconfigure(i, minsize=_row_h[0])
        canvas.config(scrollregion=canvas.bbox('all'))

        # ウィンドウ表示
        gl.SensorConfWin.deiconify()
        gl.SensorConfWin.grab_set()
        gl.SensorConfWin.focus_set()
        gl.SensorConfWin.protocol('WM_DELETE_WINDOW', SensorConfWincallback)
        gl.app.SensorFrame.bind("<Configure>",
            lambda e: canvas.config(scrollregion=canvas.bbox('all')))

    else:
        gl.SensorConfWin.lift()
        gl.SensorConfWin.focus_set()


#-----------------------------------------

def ConfClear():
    if inspect.stack()[1].function != 'DefConf':
        if not messagebox.askyesno('設定クリア','現在の入力をクリアしますか？') :
            return

    _empty = {'Sensor':'','In1':'','In2':'','Out1':'','Out2':'',
              'Out1Inv':False,'Out2Inv':False,
              'DigitsCoef':'','CalcCoef':'','Ratio':'','TimeLag':'','Disable':False}
    # 全行: SensorConfDic をクリア / 描画済み行: ウィジェットもクリア
    for i in range(gl.ChMax):
        gl.SensorConfDic[i] = dict(_empty)
        if gl.app.SensorCombo[i] is not None:
            gl.app.SensorCombo[i].set('')
            gl.app.In1Combo[i].set('')
            gl.app.In2Combo[i].set('')
            gl.app.Out1Combo[i].set('')
            gl.app.Out2Combo[i].set('')
            gl.app.Out1InvVal[i].set(False)
            gl.app.Out2InvVal[i].set(False)
            gl.app.DigitsCoefText[i].delete(0, tk.END)
            gl.app.CalcCoefText[i].delete(0, tk.END)
            gl.app.RatioText[i].delete(0, tk.END)
            gl.app.TimeLagText[i].delete(0, tk.END)
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
    # 変数に値格納（バーチャルスクロール対応）
    # 描画済み行はウィジェットから読む / 未描画行は gl.SensorConfDic をそのまま維持
    for i in range(gl.ChMax):
        if gl.app.SensorCombo[i] is not None:
            gl.SensorConfDic[i] = {
                'Sensor':    gl.app.SensorCombo[i].get(),
                'In1':       gl.app.In1Combo[i].get(),
                'In2':       gl.app.In2Combo[i].get(),
                'Out1':      gl.app.Out1Combo[i].get(),
                'Out2':      gl.app.Out2Combo[i].get(),
                'Out1Inv':   gl.app.Out1InvVal[i].get(),
                'Out2Inv':   gl.app.Out2InvVal[i].get(),
                'DigitsCoef':gl.app.DigitsCoefText[i].get(),
                'CalcCoef':  gl.app.CalcCoefText[i].get(),
                'Ratio':     gl.app.RatioText[i].get(),
                'TimeLag':   gl.app.TimeLagText[i].get(),
                'Disable':   gl.app.DisableVal[i].get(),
            }

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