import psycopg2
from tkinter import *
from tkinter import ttk
import ast
from tkinter import messagebox

def run_query(query, parameters=()):
  conn = psycopg2.connect(dbname='studentdb', user='postgres', password='*******', host='localhost', port='5432')
  cur = conn.cursor()
  query_result = None
  try:
    cur.execute(query,parameters)
    if query.lower().startswith("select"):
      query_result = cur.fetchall()
  except psycopg2.Error as e:
    messagebox.showerror("Database Error", str(e))
  finally:
    conn.commit()
    conn.close()
  return query_result


def refresh_treeview():
  for item in tree.get_children():
    tree.delete(item)
  records = run_query("select * from students;")
  for record in records:
    tree.insert('',END,values=record)


def add_student():
  parameters = (name_entry.get(),address_entry.get(),age_entry.get(),phone_entry.get())
  run_query("insert into students(name, address, age, number) values (%s,%s, %s, %s)", parameters)
  messagebox.showinfo("Information", "Student data added successfully!")
  name_entry.delete(0, END); address_entry.delete(0, END); age_entry.delete(0, END); phone_entry.delete(0, END)
  refresh_treeview()


def remove_student():
  selected_items = tree.selection()[0]
  student_id = tree.item(selected_items)["values"][0]
  response = messagebox.askquestion("Question","Are you sure to delete this record?")
  if response == 'yes':
    run_query("delete from students where student_id=%s",(student_id,))
  else:
    return
  refresh_treeview()


def modify_student():
  selected_items = tree.selection()[0]
  student_id = tree.item(selected_items)["values"][0]
  parameters = (name_entry.get(),address_entry.get(),age_entry.get(),phone_entry.get())
  field_name = ''
  index = 0
  for new_value in parameters:
    if len(new_value) > 0:
      field_name = ['name', 'address', 'age', 'number'][index]
      query = f"update students set {field_name}=%s where student_id=%s"
      run_query(query, (new_value,student_id))   
    index+=1
  messagebox.showinfo("Information", "Student data modified successfully!")
  refresh_treeview()


# /////////////
root = Tk()
root.title="Student Management System"

frame =  LabelFrame(root, text="Student Data")
frame.grid(row=0,column=0,padx=20,pady=20,sticky="ew")

# Name
Label(frame, text="Name:").grid(row=0, column=0, padx=5,sticky="w")
name_entry = Entry(frame)
name_entry.grid(row=0, column=1, pady=5, sticky='ew')
# Addrress
Label(frame, text="Address:").grid(row=1, column=0, padx=5,sticky="w")
address_entry = Entry(frame)
address_entry.grid(row=1, column=1, pady=5, sticky='ew')
# Age
Label(frame, text="Age:").grid(row=2, column=0, padx=5,sticky="w")
age_entry = Entry(frame)
age_entry.grid(row=2, column=1, pady=5, sticky='ew')
# Number
Label(frame, text="Phone Number:").grid(row=3, column=0, padx=5,sticky="w")
phone_entry = Entry(frame)
phone_entry.grid(row=3, column=1, pady=5, sticky='ew')

# Buttons/////
button_frame = Frame(root)
button_frame.grid(row=1, column=0, pady=5, sticky="ew")

 
Button(button_frame, text="Add Student", command=add_student).grid(row=0,column=0,padx=10)
Button(button_frame, text="Modify Student", command=modify_student).grid(row=0,column=2,padx=10)
Button(button_frame, text="Remove Student", command=remove_student).grid(row=0,column=3,padx=10)

tree_frame = Frame(root)
tree_frame.grid(row=2, column=0, padx=10,sticky='nsew')
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode='browse')
tree.pack()
tree_scroll.config(command=tree.yview)

tree['columns']=("student_id", "name", "address", "age", "number")
tree.column("#0", width=0, stretch=NO)
tree.column("student_id",anchor=CENTER, width=80)
tree.column("name",anchor=CENTER, width=200)
tree.column("address",anchor=CENTER, width=200)
tree.column("age",anchor=CENTER, width=80)
tree.column("number",anchor=CENTER, width=200)

tree.heading("student_id", text="ID", anchor=CENTER)
tree.heading("name",text="Name", anchor=CENTER)
tree.heading("address",text="Address", anchor=CENTER)
tree.heading("age",text="Age", anchor=CENTER)
tree.heading("number",text="Number", anchor=CENTER)

refresh_treeview()
root.mainloop()

