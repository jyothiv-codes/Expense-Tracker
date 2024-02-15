from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson import ObjectId
from datetime import date

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['expense_tracker']
collection = db['expenses']



@app.route('/')
def index():
    return render_template('main.html')
    

@app.route('/process_form', methods=['POST'])
def process_form():
    redirect_route = request.form.get('submit_action')
    return redirect(redirect_route)


@app.route('/page_to_add_expense')
def page_for_addition():
    return render_template('add_expense.html') 

@app.route('/add_expense', methods=['POST'])
def add_record():
    description = request.form.get('description')
    amount = float(request.form.get('amount'))
    today=str(date.today())
    notes=request.form.get('notes')
        # Process and store the data in MongoDB
    expense_data = {
            'description': description,
            'amount': amount,
            'notes':notes,
            'date':today
        }

    id=collection.insert_one(expense_data)
    print(id)
    return render_template('main.html')
        
    

@app.route('/page_to_delete_expense')
def page_for_deletion():
    records = collection.find()
    return render_template('delete_expense.html', records=records) 

@app.route('/delete/<record_id>', methods=['POST'])
def delete_record(record_id):
    collection.delete_one({'_id': ObjectId(record_id)})
    return redirect(url_for('index'))


@app.route('/edit_expense/<expense_id>', methods=['GET'])
def edit_expense(expense_id):
    expense = collection.find_one({'_id': expense_id})
    return render_template('edit_expense.html', expense=expense)


@app.route('/update_expense/<expense_id>', methods=['POST'])
def update_expense(expense_id):
    # Get updated data from the form
    updated_data = {
        'description': request.form['description'],
        'amount': float(request.form['amount']),
        'category': request.form['category']
    }
    # Update the expense in MongoDB
    collection.update_one({'_id': expense_id}, {'$set': updated_data})

    return render_template('update_expense.html')