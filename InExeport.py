import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import csv
import TCPGlobalVar as gl
import SQDB as DB
import ConectConfWin as ConectConf


def Export():

    #ﾃﾞｰﾀ作成
    ExportDic = ['']*gl.ChMax
    
    for i in range(gl.ChMax):
        ExportDic[i]={}

    for i in range(gl.DeviceMax):
        ExportDic[i]['Device'] = gl.DeviceConfDic[i]['Device']
        ExportDic[i]['IPAddress']=gl.DeviceConfDic[i]['IPAddress']
        ExportDic[i]['Port']=str(gl.DeviceConfDic[i]['Port'])
        
    for i in range(gl.ChMax):
        ExportDic[i]['DeviceNo'] = gl.app.DeviceNoCombo[i].get()
        ExportDic[i]['Address']=gl.app.AddressText[i].get()
        ExportDic[i]['Init']=gl.app.InitValueText[i].get()
        ExportDic[i]['UpDown']=gl.app.UDValueText[i].get()
        ExportDic[i]['Comment']=gl.app.CommentText[i].get()
        ExportDic[i]['VarType']=gl.app.VarTypecombo[i].get()
        ExportDic[i]['AI0']=gl.app.AI0ValueText[i].get()
        ExportDic[i]['AI100']=gl.app.AI100ValueText[i].get()
        ExportDic[i]['User0']=gl.app.User0ValueText[i].get()
        ExportDic[i]['User100']=gl.app.User100ValueText[i].get()
        ExportDic[i]['CurrentVal']=str(gl.IOConfDic[i].get('CurrentVal', '') if isinstance(gl.IOConfDic[i], dict) else '')
    for i in range(gl.ChMax):
        ExportDic[i]['Sensor']=gl.SensorConfDic[i]['Sensor']
        ExportDic[i]['In1']=gl.SensorConfDic[i]['In1']
        ExportDic[i]['In2']=gl.SensorConfDic[i]['In2']
        ExportDic[i]['Out1']=gl.SensorConfDic[i]['Out1']
        ExportDic[i]['Out2']=gl.SensorConfDic[i]['Out2']
        ExportDic[i]['Out1Inv']=gl.SensorConfDic[i]['Out1Inv']
        ExportDic[i]['Out2Inv']=gl.SensorConfDic[i]['Out2Inv']
        ExportDic[i]['DigitsCoef']=gl.SensorConfDic[i]['DigitsCoef']
        ExportDic[i]['CalcCoef']=gl.SensorConfDic[i]['CalcCoef']
        ExportDic[i]['Ratio']=gl.SensorConfDic[i]['Ratio']
        ExportDic[i]['TimeLag']=gl.SensorConfDic[i]['TimeLag']
        ExportDic[i]['Disable']=gl.SensorConfDic[i]['Disable']
        
    idir = gl.MyPath
    CSVPath = filedialog.asksaveasfilename(title = 'エクスポート',filetypes=[("CSV",".csv")],initialfile='設定データ',initialdir = idir,defaultextension="csv")#パス選択
    if CSVPath == '':
        return
    try:
        CSVFile = open(CSVPath,'w',newline="")
        CSVwriter = csv.DictWriter(CSVFile,gl.Key)
        CSVwriter.writeheader()
        CSVwriter.writerows(ExportDic)
    except:
        messagebox.showinfo('エラー','保存できませんでした。')


def Inport():

    idir = gl.MyPath
    CSVPath = filedialog.askopenfilename(title = 'インポート',filetypes=[("CSV",".csv")],initialdir = idir,defaultextension="csv")#パス選択
    if CSVPath == '':
        return
    try:
        CSVFile = open(CSVPath,'r',newline="")
        CSVreader = csv.DictReader(CSVFile)
        data = [row for row in CSVreader]
    except:
        messagebox.showinfo('エラー','保存できませんでした。')
    
    for key in data[0]:
        if key not in gl.Key:
            messagebox.showinfo('エラー','ヘッダーが一致しませんでした')
            return

    if len(data) != gl.DeviceMax and len(data) != gl.ChMax :
        Anser=messagebox.askyesno('注意','エクスポートデータとソケット君のデータ数が一致しません。\n'+'エクスポートデータ='+str(len(data))+
        '\nソケット君Deviceデータ='+ str(gl.DeviceMax) +'　ソケット君Chデータ='+str(gl.ChMax) +'\nソケット君のデータ数に合わせてインポートしてもよろしいですか？')

        if not Anser:
            return
        
        if len(data) > gl.DeviceMax:
            DeviceMax = gl.DeviceMax
        else:
            DeviceMax = len(data)
        if len(data) > gl.ChMax:
            ChMax = gl.ChMax
        else:
            ChMax = len(data)
    else:
        DeviceMax = gl.DeviceMax
        ChMax = gl.ChMax


    for i in range(DeviceMax):
        gl.DeviceConfDic[i]['Device']=data[i]['Device']
        gl.DeviceConfDic[i]['IPAddress']=data[i]['IPAddress']
        gl.DeviceConfDic[i]['Port']=data[i]['Port']
        
    for i in range(ChMax):
        gl.app.DeviceNoCombo[i].set('')
        gl.app.AddressText[i].delete(0,tk.END)
        gl.app.InitValueText[i].delete(0,tk.END)
        gl.app.UDValueText[i].delete(0,tk.END)
        gl.app.CommentText[i].delete(0,tk.END)
        gl.app.VarTypecombo[i].set('')
        gl.app.AI0ValueText[i].delete(0,tk.END)
        gl.app.AI100ValueText[i].delete(0,tk.END)
        gl.app.User0ValueText[i].delete(0,tk.END)
        gl.app.User100ValueText[i].delete(0,tk.END)
        
        gl.app.DeviceNoCombo[i].insert(0,data[i]['DeviceNo'])
        gl.app.AddressText[i].insert(0,data[i]['Address'])
        gl.app.InitValueText[i].insert(0,data[i]['Init'])
        gl.app.UDValueText[i].insert(0,data[i]['UpDown'])
        gl.app.CommentText[i].insert(0,data[i]['Comment'])
        gl.app.VarTypecombo[i].insert(0,data[i]['VarType'])
        gl.app.AI0ValueText[i].insert(0,data[i]['AI0'])
        gl.app.AI100ValueText[i].insert(0,data[i]['AI100'])
        gl.app.User0ValueText[i].insert(0,data[i]['User0'])
        gl.app.User100ValueText[i].insert(0,data[i]['User100'])
        gl.IOConfDic[i]['CurrentVal'] = data[i].get('CurrentVal', '')

    for i in range(ChMax):
        gl.SensorConfDic[i]['Sensor']=data[i]['Sensor']
        gl.SensorConfDic[i]['In1']=data[i]['In1']
        gl.SensorConfDic[i]['In2']=data[i]['In2']
        gl.SensorConfDic[i]['Out1']=data[i]['Out1']
        gl.SensorConfDic[i]['Out2']=data[i]['Out2']
        gl.SensorConfDic[i]['Out1Inv']=data[i]['Out1Inv']
        gl.SensorConfDic[i]['Out2Inv']=data[i]['Out2Inv']
        gl.SensorConfDic[i]['DigitsCoef']=data[i]['DigitsCoef']
        gl.SensorConfDic[i]['CalcCoef']=data[i]['CalcCoef']
        gl.SensorConfDic[i]['Ratio']=data[i]['Ratio']
        gl.SensorConfDic[i]['TimeLag']=data[i]['TimeLag']
        gl.SensorConfDic[i]['Disable']=data[i]['Disable']

    DB.BackUp()

    DB.ValGet()

    ConectConf.IOConfWinChange()
