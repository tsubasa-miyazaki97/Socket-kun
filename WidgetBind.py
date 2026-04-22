
import tkinter as tk
from tkinter import ttk
import time
import threading
from tkinter import messagebox
import TCPGlobalVar as gl

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        gl.TipWindow = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        gl.TipWindow.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()        

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def TipDel(event):#コンボボックス選択時の消えないToolTipを消す
    gl.app.lift()#IO画面最前面
    gl.SensorConfWin.lift()#センサー設定最前面

#値増加
def ValueUp(num):
    if gl.app.DeviceNoCombo[num].get() != '' and gl.app.AddressText[num].get() != '':
        if gl.app.UDValueText[num].get() != '':
            gl.AllAddDic[int(gl.app.DeviceNoCombo[num].get())-1][gl.app.AddressText[num].get()]['WVal'] =\
                gl.AllAddDic[int(gl.app.DeviceNoCombo[num].get())-1][gl.app.AddressText[num].get()]['RVal'] + float(gl.app.UDValueText[num].get())
            gl.AllAddDic[int(gl.app.DeviceNoCombo[num].get())-1][gl.app.AddressText[num].get()]['WFlag'] = True
        else :
            messagebox.showinfo('設定エラー','増減値を入力してください。')

#値加減
def ValueDown(num):
    if gl.app.DeviceNoCombo[num].get() != '' and gl.app.AddressText[num].get() != '':
        if gl.app.UDValueText[num].get() != '':
            gl.AllAddDic[int(gl.app.DeviceNoCombo[num].get())-1][gl.app.AddressText[num].get()]['WVal'] =\
                gl.AllAddDic[int(gl.app.DeviceNoCombo[num].get())-1][gl.app.AddressText[num].get()]['RVal'] - float(gl.app.UDValueText[num].get())
            gl.AllAddDic[int(gl.app.DeviceNoCombo[num].get())-1][gl.app.AddressText[num].get()]['WFlag'] = True
        else:
            messagebox.showinfo('設定エラー','増減値を入力してください。')

def ComboChange(event,Combobox,List):#,Combobox,List
    if Combobox.get() =="":
        return
    if Combobox.get() in List :
        return
    if Combobox.get().isdecimal():
        if int(Combobox.get()) in List :
            return
    Combobox.set('')

def TextFloatCheck(event,TextBox):
    if not FloatCheck(TextBox.get()) :
        TextBox.delete(0,tk.END)
        
def TextIntCheck(event,TextBox):
    if not IntCheck(TextBox.get()) :
        TextBox.delete(0,tk.END)
        
def TextUIntCheck(event,TextBox):
    if not UIntCheck(TextBox.get()) :
        TextBox.delete(0,tk.END)
    
def FloatCheck(Text):
    try:
        float(Text)
    except:
        return
    return True
def IntCheck(Text):
    try:
        int(Text)
    except:  
        return
    return True
def UIntCheck(Text):
    try:
        int(Text)
        if int(Text) < 0 :
            return   
    except: 
        return
    return True

def ValueTextFocusIn(event,num,ValueTextFocus):
    ValueTextFocus[num] = True

def ValueTextFocusOut(event,num,ValueTextFocus):
    ValueTextFocus[num] = False

def ValueTextEnter(event,num,ValueText):
    if event.keysym == 'Return':
        if ValueText[num] != '' :
            if FloatCheck(ValueText[num].get()) :
                gl.AllAddDic[int(gl.app.DeviceNoCombo[num].get())-1][gl.app.AddressText[num].get()]['WVal'] = float(ValueText[num].get())
                gl.AllAddDic[int(gl.app.DeviceNoCombo[num].get())-1][gl.app.AddressText[num].get()]['WFlag'] = True

def mouse_y_scroll(event,Canvas,child):
    if event.delta > 0:
        Canvas.yview_scroll(-1, 'units')
    elif event.delta < 0:
        Canvas.yview_scroll(1, 'units')
    if isinstance(child,tk.ttk.Combobox):#コンボボックスがスクロールで値変わるの防止
        if (str(child['state']) == 'normal'):
            child['state']='disabled'
            Thread1 = threading.Thread(target=normalset, daemon=True,args=(child,))
            Thread1.start()

'''def _configure_interior(event,Canvas,child):
    size = (max(child.winfo_reqwidth(),gl.winmaxwidth),
        max(child.winfo_reqheight(),gl.winheight))
    Canvas.config(scrollregion=(0,0,size[0],size[1]))
#    tk.messagebox.showinfo(child.winfo_reqheight())
    if child.winfo_reqwidth() != Canvas.winfo_reqwidth():
        Canvas.config(width = child.winfo_reqwidth())
    if child.winfo_reqheight() != Canvas.winfo_reqheight():
        Canvas.config(height = child.winfo_reqheight())
        tk.messagebox.showinfo(Canvas.winfo_reqheight())
'''

def normalset(child):#コンボボックスがスクロールで値変わるの防止の復帰
    time.sleep(0.001)
    child['state']='normal'
        

def IOConfClear():
    if not messagebox.askyesno('IO設定クリア','現在の入力をクリアしますか？') :
        return

    #各ウィジェットｸﾘｱ
    for i in range(1,gl.ChMax+1) :
        gl.app.DeviceNoCombo[i-1].set('')
        gl.app.AddressText[i-1].delete(0,tk.END)
        gl.app.InitValueText[i-1].delete(0,tk.END)
        gl.app.UDValueText[i-1].delete(0,tk.END)
        gl.app.CommentText[i-1].delete(0,tk.END)
        gl.app.VarTypecombo[i-1].delete(0,tk.END)
        gl.app.AI0ValueText[i-1].delete(0,tk.END)
        gl.app.AI100ValueText[i-1].delete(0,tk.END)
        gl.app.User0ValueText[i-1].delete(0,tk.END)
        gl.app.User100ValueText[i-1].delete(0,tk.END)


def WinWidthSwitch() :
    if gl.app.WinWidthButton['text'] == "◀" :
        # ウィンドウサイズを縮小
        gl.app.WinWidthButton['text'] = "▶"
        gl.app.geometry(str(gl.winwidth) + "x" + str(gl.winheight))
    else:
        # ウィンドウサイズを元に戻す
        gl.app.WinWidthButton['text'] = "◀"
        gl.app.geometry(str(gl.winmaxwidth) + "x" + str(gl.winheight))



