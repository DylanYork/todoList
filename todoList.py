from flask import Flask, jsonify, request
import sqlite3
import json

dbcon = sqlite3.connect('todoList.db', check_same_thread=False)

dbcon.execute('''CREATE TABLE IF NOT EXISTS todoList
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 task TEXT, complete INTEGER);''')

def addTask(task):
    dbcon.execute("INSERT INTO todoList (task, complete) VALUES(?,?)", (task,0))
    dbcon.commit

def deleteTask(id):
    dbcon.execute("DELETE FROM todoList WHERE id =?", (id,))
    dbcon.commit

def markTaskComplete(id):
    dbcon.execute("UPDATE todoList SET complete = 1 WHERE id = ?", (id,))
    dbcon.commit

def removeComplete(id):
    dbcon.execute("UPDATE todoList SET complete = 0 WHERE id = ?", (id,))
    dbcon.commit     

def getTodoList():
    selector = dbcon.execute("SELECT * FROM todoList")
    rows = selector.fetchall()
    taskArray = []
    for row in rows:
        task = {'id':row[0], 'task':row[1], 'complete':bool(row[2])}
        taskArray.append(task)
    return taskArray

app = Flask(__name__)

@app.route('/api/todoList/getTodoList', methods=['GET'])
def getAllTodoTasks():
    allTodoTasks = getTodoList()
    return jsonify(allTodoTasks)

@app.route('/api/todoList/deleteTodoTask/<int:id>', methods=['DELETE'])
def deleteTodoListTask(id):
    deleteTask(id)
    return jsonify({'success': True})

@app.route('/api/todoList/addTodoTask', methods=['POST'])
def addTodoListTask():
    taskData = request.get_json()
    tasks=taskData['task']
    addTask(tasks)
    return jsonify({'success': True})

@app.route('/api/todoList/completeTodoTask/<int:id>', methods=['PUT'])
def completeTodoTask(id):
    markTaskComplete(id)
    return jsonify({'success':True})

@app.route('/api/todoList/markTaskAsIncomplete/<int:id>', methods=['PUT'])
def removeTaskAsComplete(id):
    removeComplete(id)
    return jsonify({'success':True})

def main():
    app.run()

if __name__ == '__main__':
    main()

dbcon.close            
        
