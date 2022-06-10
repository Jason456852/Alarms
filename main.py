import tkinter as tk
from datetime import datetime, timedelta
import time
import threading as th


'''GUI settings'''
window = tk.Tk()
window.title("Alarm Clock")
window.resizable(False, False)
window.geometry("797x500")
'''sidebar'''
sidebar = tk.Frame(master=window, width=97, height=500, borderwidth=2)
sidebar.pack(side=tk.LEFT, expand=False)
'''buttons in sidebar'''
btn_add = tk.Button(master=sidebar, text="Add", width=12, relief=tk.GROOVE, command=lambda: add())
btn_add.place(x=0, y=0)
btn_show = tk.Button(master=sidebar, text="Show", width=12, relief=tk.GROOVE, command=lambda: show())
btn_show.place(x=0, y=30)
'''display side'''
display = tk.Frame(master=window, width=700, height=500, borderwidth=2, relief=tk.SUNKEN)
display.pack(fill=tk.BOTH, expand=True)

'''Class for alarms'''
class Alarms:
    def __init__(self, day_time):
        self.day = day_time[0]
        self.hour = day_time[1]
        self.minute = day_time[2]
        self.second = day_time[3]
        self.alert_time = self.alert_time_tag()
        self.time_period = self.time_period_tag()
        self.alarm_thread()
    
    def alert_time_tag(self):
        return (datetime.now() + timedelta(days=self.day, hours=self.hour, minutes=self.minute, seconds=self.second)).strftime("%m/%d/%Y, %H:%M:%S")
    
    def time_period_tag(self):
        tag = ""
        if self.day > 1:
            tag = str(self.day) + " days, "
        else:
            tag = str(self.day) + " day, "
        if self.hour > 1:
            tag += str(self.hour) + " hours, "
        else:
            tag += str(self.hour) + " hour, "
        if self.minute > 1:
            tag += str(self.minute) + " minutes, "
        else:
            tag += str(self.minute) + " minute, "
        if self.second > 1:
            tag += str(self.second) + " seconds"
        else:
            tag += str(self.second) + " second"
        return tag
    
    def check(self):
        print(f"thread for {self.time_period}")
        while True:
            if datetime.now().strftime("%m/%d/%Y, %H:%M:%S") == self.alert_time:
                print(f"Time's up. {self.time_period} has passed.")
                lbl_times_up = tk.Label(master=display, text=f"Time's up.\nTime period: {self.time_period}\nEnd time: {self.alert_time}")
                lbl_times_up.place(relx=0.52, rely=0.95, anchor="center")
                display.after(10000, lbl_times_up.destroy)
                display.bell()
                break
    
    def alarm_thread(self):
        t = th.Thread(target=self.check)
        t.start()

alarms_list = []

'''add function widgets'''
add_widgets = {"day":[tk.Label(master=display, text="Day:"), tk.Entry(master=display)],
               "hour":[tk.Label(master=display, text="Hour:"), tk.Entry(master=display)],
               "minute":[tk.Label(master=display, text="Minute:"), tk.Entry(master=display)],
               "second":[tk.Label(master=display, text="Second:"), tk.Entry(master=display)],
               "btn_enter_add":[tk.Button(master=display, text="Enter", relief=tk.GROOVE, command=lambda: adding())]}

'''add alarm function'''
def add():
    display.grid_columnconfigure(0, minsize=50)
    display.grid_columnconfigure(1, minsize=150)
    display.grid_columnconfigure(2, minsize=150)
    for widget in display.winfo_children():
        widget.grid_remove()
    for row, info in enumerate(add_widgets.values()):
        for column, widget in enumerate(info):
            widget.grid(row=row, column=column)

'''press enter to add'''
def adding():
    day_time = [0, 0, 0, 0]
    for i in range(4):
        temp = list(add_widgets.values())[i][1].get()
        if temp:
            day_time[i] = int(temp)
    alarms_list.append(Alarms(day_time))
    temp = tk.Label(master=display, text="Add alarm successfully!")
    temp.grid(row=2, column=3)
    display.after(3000, temp.destroy)
    

'''show function widgets'''
ent_page = tk.Entry(master=display)
btn_page = tk.Button(master=display, text="Enter", relief=tk.GROOVE, command=lambda: showing())

'''show alarm function'''
def show():
    display.grid_columnconfigure(0, minsize=100)
    display.grid_columnconfigure(1, minsize=300)
    display.grid_columnconfigure(2, minsize=300)
    for widget in display.winfo_children():
        widget.grid_remove()
    description = ["Index", "Alarm ends at:", "Inserted time:"]
    for n, i in enumerate(description):
        temp = tk.Label(master=display, text=i).grid(row=2, column=n)
    tk.Label(master=display, text="Page:").grid(row=0, column=0)
    ent_page.grid(row=0, column=1)
    btn_page.grid(row=0, column=2)
    line = "----"
    for i in range(11):
        line += "------------"
    tk.Label(master=display, text=line).grid(row=1, column=0, columnspan=3)
    tk.Label(master=display, text=line).grid(row=3, column=0, columnspan=3)
    
def showing():
    show()
    starting_index = 0
    ending_index = 15
    if ent_page.get() and int(ent_page.get()) > 0:
        starting_index = starting_index + (int(ent_page.get()) - 1) * 15
        ending_index = ending_index + (int(ent_page.get()) - 1) * 15
    for n, obj in enumerate(alarms_list[starting_index:ending_index]):
        tk.Label(master=display, text=n+1).grid(row=n+4, column=0)
        tk.Label(master=display, text=obj.alert_time).grid(row=n+4, column=1)
        tk.Label(master=display, text=obj.time_period).grid(row=n+4, column=2)

window.mainloop()