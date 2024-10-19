import threading
from tkinter import *
from tkinter import ttk, messagebox
import datetime as d
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mydb import Database

data = Database(db='expense.db')

db_lock = threading.Lock()

def saveRecord():
    if validate_date(dopvar.get()):
        with db_lock:
            data.insertRecord(item_name.get(), item_amt.get(), dopvar.get(), category_var.get())
        refreshData()

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    dopvar.set('')

def fetch_records():
    threading.Thread(target=fetch_records_background, args=(tv,)).start()

def fetch_records_background(tv):
    tv.delete(*tv.get_children())  
    with db_lock:
        f = data.fetchRecord('SELECT rowid, * FROM expense_record')
        for rec in f:
            tv.insert(parent='', index='end', iid=rec[0], values=(rec[0], rec[1], rec[2], rec[3], rec[4]))

def select_record(event):
    selected = tv.focus()
    val = tv.item(selected, 'values')
    if val:
        try:
            if len(val) >= 5:
                namevar.set(val[1])
                amtvar.set(val[2])
                dopvar.set(val[3])
                category_var.set(val[4])
        except Exception as ep:
            print("Error:", ep)

def update_record():
    selected = tv.focus()
    val = tv.item(selected, 'values')
    try:
        selected_rowid = val[0]
        with db_lock:
            data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), category_var.get(), selected_rowid)
            tv.item(selected, values=(selected_rowid, namevar.get(), amtvar.get(), dopvar.get(), category_var.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)
    refreshData()
    clearEntries()

def totalSpent():
    with db_lock:
        f = data.fetchRecord("SELECT SUM(item_price) FROM expense_record")
    total_spent = f[0][0] if f and f[0][0] else 0
    messagebox.showinfo('Total Spent:', f"Total Expenses: {total_spent}")

def refreshData():
    tv.delete(*tv.get_children())
    fetch_records()
    update_pie_chart()
        
def deleteRow():
    selected = tv.focus()
    val = tv.item(selected, 'values')
    if val:
        selected_rowid = val[0]
        with db_lock:
            data.removeRecord(selected_rowid)
        tv.delete(selected)
        refreshData()

def validate_date(date_text):
    try:
        date_obj = d.datetime.strptime(date_text, '%Y-%m-%d').date()
        if date_obj > d.date.today():
            messagebox.showerror('Error', 'Future date is not allowed.')
            return False
        return True
    except ValueError:
        messagebox.showerror('Error', 'Incorrect date format, should be YYYY-MM-DD.')
        return False

def update_pie_chart():
    categories = data.fetchDistinctCategories()

    if not categories:
        plt.clf()
        plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center',
                 fontsize=12, color='gray')
        canvas.draw()
        return

    category_total = {category: 0 for category in categories}

    with db_lock:
        f = data.fetchRecord('SELECT category, item_price FROM expense_record')
        for rec in f:
            category_total[rec[0]] += rec[1]

    total_spent = sum(category_total.values())
    if total_spent == 0:
        plt.clf()
        plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center',
                 fontsize=12, color='gray')
        canvas.draw()
        return

    category_ratio = {category: total / total_spent * 100 for category, total in category_total.items()}

    plt.clf()  
    plt.pie(category_ratio.values(), labels=category_ratio.keys(), autopct='%1.1f%%',
            textprops={'fontsize': 8})  
    plt.title('Expense Ratio', fontsize=12)  
    canvas.draw()

ws = Tk()
ws.title('EXPENSE Tracker ')

f = ('Times new roman', 12)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()
category_var = StringVar()

f2 = Frame(ws)
f2.pack()

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill='both')

Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W, padx=5, pady=5)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W, padx=5, pady=5)
Label(f1, text='PURCHASED DATE', font=f).grid(row=2, column=0, sticky=W, padx=5, pady=5)
Label(f1, text='CATEGORY', font=f).grid(row=3, column=0, sticky=W, padx=5, pady=5)

item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)
category_entry = ttk.Combobox(f1, textvariable=category_var, values=["Food", "Traveling", "Daily Expense", "Other Expense"])

item_name.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
item_amt.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
transaction_date.grid(row=2, column=1, sticky=EW, padx=5, pady=5)
category_entry.grid(row=3, column=1, sticky=EW, padx=5, pady=5)

submit_btn = Button(
    f1,
    text='Save Record',
    font=f,
    command=saveRecord,
    bg='#42602D',
    fg='white',
)

clr_btn = Button(
    f1,
    text='Clear Entry',
    font=f,
    command=clearEntries,
    bg='#D9B036',
    fg='white',
)

quit_btn = Button(
    f1,
    text='Exit',
    font=f,
    command=lambda: ws.destroy(),
    bg='#D33532',
    fg='white'
)

total_sep = Button(
    f1,
    text='Total Spent',
    font=f,
    bg='#486966',
    command=totalSpent
)

update_btn = Button(
    f1,
    text='Update',
    font=f,
    command=update_record,
    bg='#C2BB00'
)
del_btn = Button(
    f1,
    text='Delete',
    font=f,
    command=deleteRow,
    bg='#BD2A2E'
)

submit_btn.grid(row=0, column=2, sticky=EW, padx=5, pady=5)
clr_btn.grid(row=1, column=2, sticky=EW, padx=5, pady=5)
quit_btn.grid(row=2, column=2, sticky=EW, padx=5, pady=5)
total_sep.grid(row=0, column=3, sticky=EW, padx=5, pady=5)
update_btn.grid(row=1, column=3, sticky=EW, padx=5, pady=5)
del_btn.grid(row=2, column=3, sticky=EW, padx=5, pady=5)

tv = ttk.Treeview(f2, columns=(1, 2, 3, 4, 5), show='headings', height=8)
tv.pack(side='left', fill='both', expand=True)

tv.column(1, anchor=CENTER, stretch=NO, width=50)  
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.column(5, anchor=CENTER)
tv.heading(1, text='Serial No.')
tv.heading(2, text='ITEM NAME')
tv.heading(3, text='ITEM PRICE')
tv.heading(4, text='PURCHASE DATE')
tv.heading(5, text='CATEGORY')

tv.bind("<ButtonRelease-1>", select_record)

style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

fetch_records_background(tv)

pie_chart_container = Frame(f2, width=800, height=500)  
pie_chart_container.pack(side='left', fill='both', expand=True)
fig, ax = plt.subplots(figsize=(5, 5)) 
canvas = FigureCanvasTkAgg(fig, master=pie_chart_container)
canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)

update_pie_chart()

ws.mainloop()
