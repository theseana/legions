from os import read
from tkinter import *
from tkinter import messagebox
import json
import hashlib


def check_digit(a, b, c):
    print("tada!")
    cond1 = len(sv_card_number.get()) == 16
    cond2 = sv_card_number.get().isdigit()
    if cond1 and cond2:
        e1.config(bg='#78ffa0')
    else:
        e1.config(bg='#ff7a7a')


def to_shal(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def read_json(path):
    with open(path, "r") as file:
        return json.load(file)


def append_json (data,path):
    json_data=read_json(path)
    json_data.append(data)
    with open(path,"w") as file:
        json.dump(json_data, file, indent=4)


def write_json (data, path):
    with open(path,"w") as file:
        json.dump(data, file, indent=4)


def get_id(path):
    json_data=read_json(path)
    return len(json_data)+1


def check_person(name, path):
    json_data = read_json(path)
    for person in json_data:
        if person["name"] == name:
            messagebox.showerror('register faild', "this username is already used")
            return False
    return True       


def sing(s):
    if s =="login":
        def log_in():
            username=sv_username.get()
            password=to_shal(sv_password.get())
            data_json = read_json("register.json")
            for person in data_json:
                if person["name"] == username and person['password']==password:
                   menu(person["id"])

        login=Toplevel()
        Label(login, text="Username").grid(row=0, column=0)
        sv_username=StringVar()
        Entry(login, textvariable=sv_username).grid(row=1,column=0)
        Label(login, text="password").grid(row=2, column=0)
        sv_password=StringVar()
        Entry(login, textvariable=sv_password).grid(row=3,column=0)
        Button(login,text='login',command=log_in).grid(row=4,column=0)
        Button(login, text="Exit", command=login.destroy).grid(row=7,column=0)
    elif s=="register":
        def sign_up():
            is_let = check_person(sv_username.get(), 'register.json')
            if is_let:
                new_obj ={
                    "id":get_id("register.json"),
                    "name":sv_username.get(),
                    "password":to_shal(sv_password.get()),
                    'card_number':sv_card_number.get(),
                    "cash":0
                }
                append_json(new_obj, "register.json")
        register=Toplevel()
        Label(register, text="Username").grid(row=0, column=0)
        sv_username=StringVar()
        Entry(register, textvariable=sv_username).grid(row=1,column=0)
        Label(register,text="password").grid(row=2,column=0)
        sv_password=StringVar()
        Entry(register, textvariable=sv_password).grid(row=3,column=0)
        Label(register,text="card number").grid(row=4,column=0)
        global sv_card_number, e1
        sv_card_number=StringVar()
        sv_card_number.trace("w", check_digit)
        e1 = Entry(register, textvariable=sv_card_number)
        e1.grid(row=5,column=0)
        Button(register,text="sign up",command=sign_up).grid(row=6,column=0)
        Button(register,text="Exit",command=register.destroy).grid(row=7,column=0)


def menu(person_id):
    def balance():
        all_data = read_json('register.json')
        your_balance = 0
        for person in all_data:
            if person["id"] == person_id:
                your_balance = person["cash"]                
        top = Toplevel()
        Label(top, text="Your Balance:").grid(row=0,column=0)
        Label(top, text=your_balance).grid(row=1,column=0)    

    def withdrawal():
        all_data = read_json('register.json')
        for person in all_data:
            if person["id"] == person_id:
                if person["cash"] > withdraw_amount.get():
                    person["cash"] -= withdraw_amount.get()
                    write_json(all_data, 'register.json')
                else:
                    messagebox.showerror('Withdraw Fail', "Not Enough Money!!!")

    def withdraw():
        top = Toplevel()
        Label(top, text="Amount:").grid(row=0,column=0)
        global withdraw_amount
        withdraw_amount = IntVar()
        Entry(top, textvariable=withdraw_amount).grid(row=0,column=1)
        Button(top, text="Withdraw", command=withdrawal).grid(row=1,column=0)

    menu_page = Toplevel()
    Button(menu_page, text="Balance", command=balance).grid(row=0,column=0)
    Button(menu_page, text="Withraw", command=withdraw).grid(row=0,column=1)
    Button(menu_page, text="Transfer").grid(row=1,column=0)
    Button(menu_page, text="ChangePin").grid(row=1,column=1)
    Button(menu_page, text="Cancel", command=menu_page.destroy).grid(row=2,column=0)


main=Tk()
Button(main,text="login",command=lambda:sing("login")).grid(row=0,column=0)
Button(main,text="register",command=lambda:sing("register")).grid(row=1,column=0)
main.mainloop()