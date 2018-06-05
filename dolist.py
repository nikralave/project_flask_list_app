from flask import Flask, flash, request, render_template, redirect, url_for
import os
import json

app = Flask(__name__)

#------Functions to load and add list names-----------------------
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

#------Functions to load and add list items-----------------------

def load_list_items_by_list_name(username, list_name):
    if os.path.isfile('./data/'+username+'.json'):
        with open("data/"+username+".json", "r" ) as json_data:
            listdata = json_data.read()
            items = json.loads(listdata)
            filtered_list = []
            for key, value in items.items():
                if(key==list_name):
                    filtered_list.append(value)
            return filtered_list
                   
    else:
        items = []  
        
def add_bit_to_full(username, pair_name, item_entered):
    if os.path.isfile('./data/'+username+'.json'):
        with open("data/"+username+".json", "r" ) as json_data:
            listdata = json_data.read()
            items = json.loads(listdata)
            items[pair_name].append(item_entered)
            return items
                   
    else:
        items = [] 
        
def add_list_item(username, list_name, item_entered, list_contents):
     with open('data/'+username+'.json', "w") as f:
        data = json.dumps(list_contents)
        f.write(data)
    
   

#-----------------------------------------------------------------

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
    # list_name = get_selected(task_lists)
    return render_template("list.html", logged_in_as=username, list_of_keys=task_lists.keys())
    

@app.route("/<username>/<list_name>")
def get_list(username,list_name):
    list_contents = load_list_items_by_list_name(username, list_name)
    return render_template("list_contents.html", logged_in_as=username, list_of_items=list_contents, list_name_selected=list_name)

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

@app.route("/show_items", methods=["GET","POST"]) 
def showItems():
    username = request.form['username']
    listname = request.form['list_name']
    page = username + "/" + listname    
    
    return redirect(page)  



#-------------------------------------------

@app.route("/new_item", methods=["POST"])
def add_listitem():
    list_contents = []
    username = request.form['username']
    list_item_entered = request.form['list_item']
    list_name = request.form['list_name']
    page = username + "/" + list_name    
    


    if list_item_entered in list_contents:
        return redirect(page)
        
    
    else:
        full_dict = add_bit_to_full(username, list_name,list_item_entered)
        add_list_item(username, list_name, list_item_entered, full_dict)
        return redirect(page)





if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)