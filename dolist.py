from flask import Flask, flash, request, render_template, redirect
import os

app = Flask(__name__)

lists = []

def write_to_file(filename, data):
    f = open(filename, "a")
    f.writelines(data)
        
def add_listitemtofile(username, listitem):
    write_to_file("data/"+username+".txt", listitem)

def get_listitems_from_file(username):
    listfromfile = []
    if os.path.isfile('./data/'+username+'.txt'):
        f = open("data/"+username+".txt", "r")
        listfromfile = f.readlines()
        return listfromfile
    else:
        f = open("data/"+username+".txt", "x")
        return listfromfile

@app.route("/")
def get_index():
    return render_template("index.html")

@app.route("/login")
def do_login():
    username = request.args['username']
    return redirect(username)

@app.route("/<username>")
def get_userpage(username):
    lists = get_listitems_from_file(username)
    return render_template("list.html", logged_in_as=username, full_list=lists)
    
@app.route("/new", methods=["POST"])
def add_listitem():
    lists = []
    username = request.form['username']
    text = request.form['listitem']
    lists = get_listitems_from_file(username)
    listitem = text +"\n"
    if listitem in lists:
        return redirect(username)
    else:
        lists.append(listitem)
        add_listitemtofile(username,listitem)
        return redirect(username)
   

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))