from os import read
from tkinter import *
from tkinter import messagebox
import json
import hashlib


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


def get_id(path):
    json_data=read_json(path)
    return len(json_data)+1


def check_person(name, path):
    json_data = read_json(path)
    for person in json_data:
        if person["name"]==name:
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
                    messagebox.showerror("tada",'tada')

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
            is_let = True
            sv_card_number=StringVar()
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
        sv_card_number=StringVar()
        Entry(register, textvariable=sv_card_number).grid(row=5,column=0)
        Button(register,text="sign up",command=sign_up).grid(row=6,column=0)
        Button(register,text="Exit",command=register.destroy).grid(row=7,column=0)


def menu():
    Label()


main=Tk()
Button(main,text="login",command=lambda:sing("login")).grid(row=0,column=0)
Button(main,text="register",command=lambda:sing("register")).grid(row=1,column=0)
main.mainloop()