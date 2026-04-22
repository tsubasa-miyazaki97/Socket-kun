import time
import threading
from tkinter import messagebox
from tkinter import filedialog
import tkinter
import csv
import TCPGlobalVar as gl

def TracePush():
    if not gl.IORWBusy :
        messagebox.showinfo('エラー','IO_R/Wを実施してください。')
        return
    if not gl.TraceFlag :
        gl.app.TraceButton['text']='ﾄﾚｰｽ停止'
        gl.TraceFlag = True
        TraceThread = threading.Thread(target=TraceStart, daemon=True)
        TraceThread.start()
    else:
        gl.app.TraceButton['text']='ﾄﾚｰｽ開始'
        gl.TraceFlag = False

def TraceStart():
    TraceTime = 0
    if gl.app.Tracecombo.get() != gl.TraceTime[0] :
        ScanTime=int(gl.app.Tracecombo.get())
    now = time.time()
    gl.TraceDic.clear()
    RowCnt = 0
    Key=['Row','Time']

    while gl.TraceFlag :
        if gl.app.Tracecombo.get() == gl.TraceTime[0] :
            ScanTime = float(gl.app.ScanTime['text'])
        gl.TraceDic.append({})#ｽｷｬﾝ毎に配列にDic作成
        TraceTime = TraceTime + time.time() - now#累積時間
        now = time.time()#前ｽｷｬﾝ時間

        gl.TraceDic[RowCnt]['Row'] = RowCnt#何回目
        gl.TraceDic[RowCnt]['Time'] = int(TraceTime*1000)#経過時間

        for Ch in gl.EnableCh:#有効Chの現在値取得
            Dev = int(gl.app.DeviceNoCombo[Ch-1].get())-1
            Add = gl.app.AddressText[Ch-1].get()
            gl.TraceDic[RowCnt][Add] = gl.AllAddDic[Dev][Add]['RVal']
            
            if RowCnt == 0 :
                Key.append(Add)

        RowCnt += 1
        
        Remain = ScanTime / 1000 - (time.time() - now)#設定ｽｷｬﾝﾀｲﾑのあまり

        if Remain > 0:
            time.sleep(Remain)

    #ﾄﾚｰｽ終了処理
    if not messagebox.askyesno('ﾄﾚｰｽ結果','ﾄﾚｰｽ完了。\n保存しますか？') :
        return
    idir = gl.MyPath
    CSVPath = filedialog.asksaveasfilename(title = '名前を付けて保存',filetypes=[("CSV",".csv")],initialfile='ﾄﾚｰｽ結果',initialdir = idir,defaultextension="csv")#パス選択
    if CSVPath == '':
        return
    try:
        with open(CSVPath,'w',newline="") as CSVFile:
            CSVwriter = csv.DictWriter(CSVFile,Key)#,delimiter='\t')
            CSVwriter.writeheader()
            CSVwriter.writerows(gl.TraceDic)
    except Exception:
        messagebox.showinfo('エラー','保存できませんでした。')

