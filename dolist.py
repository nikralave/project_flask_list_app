from flask import Flask, flash, request, render_template, redirect
import os
import json

app = Flask(__name__)


@app.route("/")
def get_index():
    return render_template("index.html")

@app.route("/login")
def do_login():
    username = request.args["username"]
    return redirect(username)

@app.route("/<username>")
def get_userpage(username):
    task_lists = load_lists(username)
    return render_template("list.html", logged_in_as=username, list_of_keys=task_lists.keys())


@app.route("/new_list", methods=["POST"]) 
def newlist():
    username = request.form['username']
    listname = request.form['namelist']
    
    task_lists = load_lists(username)

    if listname in task_lists:
        return "That list already exists"
        
    task_lists[listname]=[]
    save_lists(task_lists, username)

    return redirect(username)
    

def load_lists(username):
    if os.path.isfile('./data/'+username+'.json'):
        with open("data/"+username+".json") as json_data:
            return json.load(json_data)
    else:
        return {}

    
def save_lists(task_lists, username):
    f = open('data/'+username+'.json', 'w')
    f.write(json.dumps(task_lists))
    f.close()

#-------------------------------------------

@app.route("/new", methods=["POST"])
def add_listitem():
    lists = []
    username = request.form['username']
    text = request.form['listitem']
    
    listitem = text +"\n"
    if listitem in lists:
        return redirect(username)
    else:
        lists.append(listitem)
        return render_template("list_contents.html", logged_in_as=username, full_list=lists)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)