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
        self.title("ｿｹｯﾄ君")

        # ウィンドウの大きさを決定（起動時はフル幅で全ボタン・テキストボックスを表示）
        self.geometry(str(gl.winmaxwidth)+"x"+str(gl.winheight))

        # ツールバー行(row=0)は固定、固定ヘッダー行(row=1)は固定、キャンバス行(row=2)を伸縮
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)  # 固定ヘッダー行
        self.grid_rowconfigure(2, weight=1)  # キャンバス行
        self.grid_columnconfigure(0, weight=1)

#-----------------------------------toolbar_frame--------------------------

        # ツールバーフレーム（row=0 / スクロールしない）
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.toolbar_frame_ref = toolbar_frame

        tc = 0  # ツールバー列カウンタ

        # IOモニタ開始ボタン
        self.RWStartButton = tk.Button(toolbar_frame, text="IO_R/W開始", command=lambda: IORW.IORW())
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
        ScanTimelabel = tk.Label(toolbar_frame, text='R/Wｽｷｬﾝﾀｲﾑ', font=(gl.deffont, gl.fsizes))
        ScanTimelabel.grid(row=0, column=tc, padx=2)
        tc += 1
        ### ｽｷｬﾝﾀｲﾑ作成
        self.ScanTime = tk.Label(toolbar_frame, text=0, font=(gl.deffont, gl.fsizes), width=4, anchor='e')
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
        self.Tracecombo = ttk.Combobox(toolbar_frame, values=gl.TraceTime, font=(gl.deffont, gl.fsizes), width=11)
        self.Tracecombo.grid(row=0, column=tc, padx=2)
        self.Tracecombo.bind('<FocusOut>', lambda event, arg1=self.Tracecombo, arg2=gl.TraceTime: Bind.ComboChange(event, arg1, arg2))
        self.Tracecombo.set(gl.TraceTime[0])
        tc += 1
        ### ﾄﾚｰｽｽｷｬﾝﾀｲﾑ単位作成
        self.TraceScanTimems = tk.Label(toolbar_frame, text='ms', font=(gl.deffont, gl.fsizes))
        self.TraceScanTimems.grid(row=0, column=tc, padx=2)
        tc += 1
        ###表示範囲切替ボタン（位置は_adjust_layout()でplace配置）起動時はフル幅なので◀
        self.WinWidthButton = tk.Button(toolbar_frame, text="◀", command=lambda: Bind.WinWidthSwitch())

        # 右側ボタン群（固定位置にplace配置するため専用フレームにまとめる）
        self.right_toolbar = tk.Frame(toolbar_frame)
        # 通信設定ボタン
        self.changePageButton = tk.Button(self.right_toolbar, text="通信設定", command=lambda: ConectConfdef())
        self.changePageButton.pack(side='left', padx=2, pady=2)
        # センサー設定ボタン
        self.SensorConfButton = tk.Button(self.right_toolbar, text="ｾﾝｻｰ設定", command=lambda: SensorConfdef())
        self.SensorConfButton.pack(side='left', padx=2, pady=2)
        # IO設定クリアボタン
        self.IOClearConfButton = tk.Button(self.right_toolbar, text="IO設定ｸﾘｱ", command=lambda: Bind.IOConfClear())
        self.IOClearConfButton.pack(side='left', padx=2, pady=2)
        # ｴｸｽﾎﾟｰﾄボタン
        self.ExportButton = tk.Button(self.right_toolbar, text="ｴｸｽﾎﾟｰﾄ", command=lambda: InExeport.Export())
        self.ExportButton.pack(side='left', padx=2, pady=2)
        # インポートボタン
        self.InportButton = tk.Button(self.right_toolbar, text="ｲﾝﾎﾟｰﾄ", command=lambda: InExeport.Inport())
        self.InportButton.pack(side='left', padx=2, pady=2)

#-----------------------------------固定ヘッダー / canvas / main_frame--------------------

        # 固定ヘッダーフレーム（row=1 / スクロールしない）
        self.io_header_frame = tk.Frame(self)
        self.io_header_frame.grid(row=1, column=0, sticky="ew")

        # スクロールバー設置
        self.canvas = tk.Canvas(self, width=gl.winwidth, height=gl.winheight, highlightthickness=0)
        self.canvas.grid(row=2, column=0, sticky="nsew")

        self.ybar = tk.Scrollbar(self, orient=tk.VERTICAL)  # 縦スクロールバー配置
        self.ybar.grid(row=2, column=1, sticky=tk.N+tk.S)
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
        C_VARTYPE   = 9
        C_AI0       = 10
        C_AI100     = 11
        C_USER0     = 12
        C_USER100   = 13

#-----------------------------------データ行 バーチャルスクロール---------------

        # 全行分 StringVar を先に生成（未描画行でも ValueUpdate が .set() できるように）
        for _i in range(gl.ChMax):
            gl.ValueText[_i] = tk.StringVar()
            _cv = gl.IOConfDic[_i].get('CurrentVal', '') if isinstance(gl.IOConfDic[_i], dict) else ''
            if _cv:
                gl.ValueText[_i].set(_cv)

        # ウィジェットリストを None で初期化（未描画行は None のまま）
        self.Nolabel          = [None] * gl.ChMax
        self.DeviceNoCombo    = [None] * gl.ChMax
        self.AddressText      = [None] * gl.ChMax
        self.ValueText        = [None] * gl.ChMax
        self.ValueUpButton    = [None] * gl.ChMax
        self.ValueDownButton  = [None] * gl.ChMax
        self.UDValueText      = [None] * gl.ChMax
        self.InitValueText    = [None] * gl.ChMax
        self.CommentText      = [None] * gl.ChMax
        self.VarTypecombo     = [None] * gl.ChMax
        self.AI0ValueText     = [None] * gl.ChMax
        self.AI100ValueText   = [None] * gl.ChMax
        self.User0ValueText   = [None] * gl.ChMax
        self.User100ValueText = [None] * gl.ChMax

        # ---- バーチャルスクロール状態 ----
        _rendered        = set()   # 生成済み行番号 (1-based)
        _row_h           = [32]    # 実測行高さ [px]（update_idletasks 後に更新）
        _BUFFER          = 3       # 上下バッファ行数
        _scroll_after_id = [None]

        def _schedule_update():
            if _scroll_after_id[0] is not None:
                self.after_cancel(_scroll_after_id[0])
            _scroll_after_id[0] = self.after(150, _update_visible_rows)

        def _on_mousewheel_main(event):
            Bind.mouse_y_scroll(event, self.canvas, None)
            _schedule_update()

        def _on_mousewheel_combo(event, combo_widget):
            Bind.mouse_y_scroll(event, self.canvas, combo_widget)
            _schedule_update()

        def _build_row(i):
            """行 i (1-based) のウィジェットを生成する。"""
            if i in _rendered:
                return
            _rendered.add(i)
            idx = i - 1  # 0-based

            self.main_frame.grid_rowconfigure(i, minsize=0)

            # ChNo
            lbl = tk.Label(self.main_frame, text=i, font=(gl.deffont, gl.fsizes))
            lbl.grid(row=i, column=C_CHNO, padx=2)
            lbl.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            self.Nolabel[idx] = lbl

            # ﾃﾞﾊﾞｲｽNo
            combo = ttk.Combobox(self.main_frame, values=gl.EnableDevice, font=(gl.deffont, gl.fsizes), width=2)
            combo.grid(row=i, column=C_DEVICENO, padx=2)
            combo.bind('<FocusOut>',   lambda e, a=combo, b=gl.EnableDevice: Bind.ComboChange(e, a, b))
            combo.bind('<MouseWheel>', lambda e, a=combo: _on_mousewheel_combo(e, a))
            combo.insert(0, str(gl.IOConfDic[idx]['DeviceNo']))
            self.DeviceNoCombo[idx] = combo

            # 読書ｱﾄﾞﾚｽ
            addr = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=12)
            addr.grid(row=i, column=C_ADDRESS, padx=2)
            addr.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            addr.insert(0, str(gl.IOConfDic[idx]['Address']))
            self.AddressText[idx] = addr

            # 現在値（StringVar は gl.ValueText[idx] に生成済み）
            val = tk.Entry(self.main_frame, textvariable=gl.ValueText[idx], font=(gl.deffont, gl.fsizes), width=12)
            val.grid(row=i, column=C_VALUE, padx=2)
            val.bind('<FocusIn>',    lambda e, a=idx, b=gl.ValueTextFocus: Bind.ValueTextFocusIn(e, a, b))
            val.bind('<FocusOut>',   lambda e, a=idx, b=gl.ValueTextFocus: Bind.ValueTextFocusOut(e, a, b))
            val.bind('<KeyRelease>', lambda e, a=idx, b=gl.ValueText:      Bind.ValueTextEnter(e, a, b))
            val.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            self.ValueText[idx] = val

            # 値減少ボタン（▼）
            down = tk.Button(self.main_frame, text='▼', font=(gl.deffont, gl.fsizes), command=partial(Bind.ValueDown, idx))
            down.grid(row=i, column=C_VALUEDOWN, padx=2)
            down['state'] = 'normal' if gl.IORWBusy else 'disabled'
            down.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            self.ValueDownButton[idx] = down

            # 値増加ボタン（▲）
            up = tk.Button(self.main_frame, text='▲', font=(gl.deffont, gl.fsizes), command=partial(Bind.ValueUp, idx))
            up.grid(row=i, column=C_VALUEUP, padx=2)
            up['state'] = 'normal' if gl.IORWBusy else 'disabled'
            up.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            self.ValueUpButton[idx] = up

            # 増減値
            ud = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=7)
            ud.grid(row=i, column=C_UDVALUE, padx=2)
            ud.bind('<FocusOut>',   lambda e, a=ud: Bind.TextFloatCheck(e, a))
            ud.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            ud.insert(0, str(gl.IOConfDic[idx]['UpDown']))
            self.UDValueText[idx] = ud

            # 初期値
            init = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=7)
            init.grid(row=i, column=C_INIT, padx=2)
            init.bind('<FocusOut>',   lambda e, a=init: Bind.TextFloatCheck(e, a))
            init.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            init.insert(0, str(gl.IOConfDic[idx]['Init']))
            self.InitValueText[idx] = init

            # ｺﾒﾝﾄ
            comment = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=26)
            comment.grid(row=i, column=C_COMMENT, padx=2)
            comment.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            comment.insert(0, str(gl.IOConfDic[idx]['Comment']))
            self.CommentText[idx] = comment

            # 型
            vtype = ttk.Combobox(self.main_frame, values=gl.VarTypeList, font=(gl.deffont, gl.fsizes), width=5)
            vtype.grid(row=i, column=C_VARTYPE, padx=2)
            vtype.bind('<FocusOut>',   lambda e, a=vtype, b=gl.VarTypeList: Bind.ComboChange(e, a, b))
            vtype.bind('<MouseWheel>', lambda e, a=vtype: _on_mousewheel_combo(e, a))
            vtype.insert(0, str(gl.IOConfDic[idx]['VarType']))
            self.VarTypecombo[idx] = vtype

            # 0%AI値
            ai0 = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=7)
            ai0.grid(row=i, column=C_AI0, padx=2)
            ai0.bind('<FocusOut>',   lambda e, a=ai0: Bind.TextFloatCheck(e, a))
            ai0.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            ai0.insert(0, str(gl.IOConfDic[idx]['AI0']))
            self.AI0ValueText[idx] = ai0

            # 100%AI値
            ai100 = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=12)
            ai100.grid(row=i, column=C_AI100, padx=2)
            ai100.bind('<FocusOut>',   lambda e, a=ai100: Bind.TextFloatCheck(e, a))
            ai100.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            ai100.insert(0, str(gl.IOConfDic[idx]['AI100']))
            self.AI100ValueText[idx] = ai100

            # 0%User値
            user0 = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=7)
            user0.grid(row=i, column=C_USER0, padx=2)
            user0.bind('<FocusOut>',   lambda e, a=user0: Bind.TextFloatCheck(e, a))
            user0.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            user0.insert(0, str(gl.IOConfDic[idx]['User0']))
            self.User0ValueText[idx] = user0

            # 100%User値
            user100 = tk.Entry(self.main_frame, font=(gl.deffont, gl.fsizes), width=12)
            user100.grid(row=i, column=C_USER100, padx=2)
            user100.bind('<FocusOut>',   lambda e, a=user100: Bind.TextFloatCheck(e, a))
            user100.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
            user100.insert(0, str(gl.IOConfDic[idx]['User100']))
            self.User100ValueText[idx] = user100

            # IO_R/W実行中なら設定系を disabled、▲▼を normal に
            if gl.IORWBusy:
                combo['state'] = 'disabled'
                addr['state']  = 'disabled'
                vtype['state'] = 'disabled'

        # ---- 表示中の行番号を計算 ----
        def _get_visible_range():
            h = self.canvas.winfo_height()
            if h <= 1:
                return 1, 20
            y0 = self.canvas.canvasy(0)
            y1 = self.canvas.canvasy(h)
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
                self.canvas.config(scrollregion=self.canvas.bbox('all'))

        # ---- スクロールバーコマンド（行生成を伴う） ----
        def _do_yview(*args):
            self.canvas.yview(*args)
            _schedule_update()

        self.ybar.config(command=_do_yview)
        self.main_frame.bind('<MouseWheel>', lambda e: _on_mousewheel_main(e))
        self.canvas.bind('<MouseWheel>',     lambda e: _on_mousewheel_main(e))

        # ---- インポート後に描画済み行を gl.IOConfDic で再反映するメソッド ----
        def _refresh_rendered_rows():
            for _ri in sorted(_rendered):
                _idx = _ri - 1
                self.DeviceNoCombo[_idx].set('')
                self.DeviceNoCombo[_idx].insert(0, str(gl.IOConfDic[_idx]['DeviceNo']))
                self.AddressText[_idx].delete(0, tk.END)
                self.AddressText[_idx].insert(0, str(gl.IOConfDic[_idx]['Address']))
                self.InitValueText[_idx].delete(0, tk.END)
                self.InitValueText[_idx].insert(0, str(gl.IOConfDic[_idx]['Init']))
                self.UDValueText[_idx].delete(0, tk.END)
                self.UDValueText[_idx].insert(0, str(gl.IOConfDic[_idx]['UpDown']))
                self.CommentText[_idx].delete(0, tk.END)
                self.CommentText[_idx].insert(0, str(gl.IOConfDic[_idx]['Comment']))
                self.VarTypecombo[_idx].set('')
                self.VarTypecombo[_idx].insert(0, str(gl.IOConfDic[_idx]['VarType']))
                self.AI0ValueText[_idx].delete(0, tk.END)
                self.AI0ValueText[_idx].insert(0, str(gl.IOConfDic[_idx]['AI0']))
                self.AI100ValueText[_idx].delete(0, tk.END)
                self.AI100ValueText[_idx].insert(0, str(gl.IOConfDic[_idx]['AI100']))
                self.User0ValueText[_idx].delete(0, tk.END)
                self.User0ValueText[_idx].insert(0, str(gl.IOConfDic[_idx]['User0']))
                self.User100ValueText[_idx].delete(0, tk.END)
                self.User100ValueText[_idx].insert(0, str(gl.IOConfDic[_idx]['User100']))
                _cv = gl.IOConfDic[_idx].get('CurrentVal', '')
                gl.ValueText[_idx].set(_cv if _cv else '')

        self.refresh_rendered_rows = _refresh_rendered_rows

        # ---- 初期描画: 最初の FIRST_ROWS 行のみ生成 ----
        FIRST_ROWS = 20
        for _fi in range(1, min(FIRST_ROWS, gl.ChMax) + 1):
            _build_row(_fi)

#--------------------------------------------------------------------------

        #ウインドウ閉じをキャッチ
        self.protocol("WM_DELETE_WINDOW", callback)

        # スクロール範囲を確定し、以降の変更に追従するよう<Configure>をバインド
        self.main_frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox('all')))

        # io_header_frame にヘッダーラベルを grid で配置（update_idletasks 前に構築して幅計測可能にする）
        _hf = self.io_header_frame
        _hfont = (gl.deffont, gl.fsizes)
        tk.Label(_hf, text="ChNo",       font=_hfont).grid(row=0, column=0,  padx=2, pady=2)
        tk.Label(_hf, text="ﾃﾞﾊﾞｲｽNo",   font=_hfont).grid(row=0, column=1,  padx=2, pady=2)
        tk.Label(_hf, text="読書ｱﾄﾞﾚｽ",   font=_hfont).grid(row=0, column=2,  padx=2, pady=2)
        tk.Label(_hf, text="現在値",       font=_hfont).grid(row=0, column=3,  padx=2, pady=2)
        tk.Label(_hf, text="増減ﾎﾞﾀﾝ",   font=_hfont).grid(row=0, column=4,  padx=2, pady=2, columnspan=2)
        tk.Label(_hf, text="増減値",       font=_hfont).grid(row=0, column=6,  padx=2, pady=2)
        tk.Label(_hf, text="初期値",       font=_hfont).grid(row=0, column=7,  padx=2, pady=2)
        tk.Label(_hf, text="ｺﾒﾝﾄ",        font=_hfont).grid(row=0, column=8,  padx=2, pady=2)
        tk.Label(_hf, text="型",           font=_hfont).grid(row=0, column=9,  padx=2, pady=2)
        tk.Label(_hf, text="0%AI値",      font=_hfont).grid(row=0, column=10, padx=2, pady=2)
        tk.Label(_hf, text="100%AI値",    font=_hfont).grid(row=0, column=11, padx=2, pady=2)
        tk.Label(_hf, text="0%ﾕｰｻﾞ値",   font=_hfont).grid(row=0, column=12, padx=2, pady=2)
        tk.Label(_hf, text="100%ﾕｰｻﾞ値", font=_hfont).grid(row=0, column=13, padx=2, pady=2)

        self.update_idletasks()  # レイアウト計算（非表示のまま）

        # 各列幅を max(ヘッダーラベル幅, データウィジェット幅) に揃える（FIRST_ROWS 行で計測）
        for _col in range(14):
            _hb = _hf.grid_bbox(column=_col, row=0)
            _db = self.main_frame.grid_bbox(column=_col, row=1)
            _cw = max(_hb[2] if _hb else 0, _db[2] if _db else 0)
            if _cw > 0:
                _hf.grid_columnconfigure(_col, minsize=_cw)
                self.main_frame.grid_columnconfigure(_col, minsize=_cw)

        # 実測行高さ → 未描画行のプレースホルダーに使用
        _total_h = self.main_frame.winfo_reqheight()
        _row_h[0] = max(1, _total_h // FIRST_ROWS)

        # 未描画行のスクロール高さをプレースホルダーで確保
        for _pi in range(FIRST_ROWS + 1, gl.ChMax + 1):
            self.main_frame.grid_rowconfigure(_pi, minsize=_row_h[0])

        self.main_frame.grid_rowconfigure(0, minsize=0)
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        self.deiconify()
        self.update_idletasks()
        self._adjust_layout()

    def _adjust_layout(self):
        """コメントテキストボックスの右端に合わせてWinWidthButtonと右側ボタン群を配置"""
        self.update_idletasks()

        # コメントテキストボックスの右端のx座標（ウィンドウ原点基準）
        comment_rootx = self.CommentText[0].winfo_rootx()
        root_rootx = self.winfo_rootx()
        comment_right = comment_rootx - root_rootx + self.CommentText[0].winfo_width() + 2  # +2はpadx分

        # スクロールバー幅（winfo_reqwidth で確実に取得、未描画時(=1)はwinfo_widthで補完）
        scrollbar_w = self.ybar.winfo_reqwidth()
        if scrollbar_w <= 1:  # 1はtkinterの未初期化時のデフォルト値
            scrollbar_w = self.ybar.winfo_width()

        # ナローウィンドウ幅を更新（コメント右端＋縦スクロールバー幅）
        gl.winwidth = comment_right + scrollbar_w

        # toolbar_frame内にWinWidthButtonをplace配置（右端がコメント右端に揃う）
        toolbar_h = self.toolbar_frame_ref.winfo_height()
        btn_w = self.WinWidthButton.winfo_reqwidth()
        btn_h = self.WinWidthButton.winfo_reqheight()
        btn_y = max(0, (toolbar_h - btn_h) // 2)
        self.WinWidthButton.place(x=comment_right - btn_w, y=btn_y)

        # 100%User値テキストボックスの右端のx座標（ウィンドウ原点基準）
        user100_rootx = self.User100ValueText[0].winfo_rootx()
        user100_right = user100_rootx - root_rootx + self.User100ValueText[0].winfo_width() + 2  # +2はpadx分

        # 右側ボタン群をtoolbar_frame内にplace配置
        # インポートボタン右端が100%ユーザー値テキストボックス右端に揃うよう配置。
        # ただしWinWidthButtonと重なる場合はcomment_right（WinWidthButtonの右端）に揃える。
        self.right_toolbar.update_idletasks()
        right_w = self.right_toolbar.winfo_reqwidth()
        right_h = self.right_toolbar.winfo_reqheight()
        right_x = max(user100_right - right_w, comment_right)
        right_y = max(0, (toolbar_h - right_h) // 2)
        self.right_toolbar.place(x=right_x, y=right_y)

        # フルウィンドウ幅を更新（インポートボタン右端＋縦スクロールバー幅）
        gl.winmaxwidth = right_x + right_w + scrollbar_w
        # フルウィンドウ表示中ならウィンドウ幅を調整
        if self.WinWidthButton['text'] == "◀":
            self.geometry(str(gl.winmaxwidth) + "x" + str(gl.winheight))

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