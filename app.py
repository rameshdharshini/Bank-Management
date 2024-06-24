from flask import Flask, render_template, request, redirect, url_for
import pickle
import os
import pathlib

app = Flask(__name__)

class Account:
    accNo = 0
    name = ''
    deposit = 0
    type = ''

    def createAccount(self, accNo, name, type, deposit):
        self.accNo = accNo
        self.name = name
        self.type = type
        self.deposit = deposit

    def showAccount(self):
        return {
            'accNo': self.accNo,
            'name': self.name,
            'type': self.type,
            'deposit': self.deposit
        }

    def modifyAccount(self, name, type, deposit):
        self.name = name
        self.type = type
        self.deposit = deposit

    def depositAmount(self, amount):
        self.deposit += amount

    def withdrawAmount(self, amount):
        self.deposit -= amount

    def report(self):
        return self.accNo, self.name, self.type, self.deposit

def get_accounts():
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            accounts = pickle.load(infile)
    else:
        accounts = []
    return accounts

def save_accounts(accounts):
    with open('accounts.data', 'wb') as outfile:
        pickle.dump(accounts, outfile)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        accNo = int(request.form['accNo'])
        name = request.form['name']
        type = request.form['type']
        deposit = int(request.form['deposit'])
        account = Account()
        account.createAccount(accNo, name, type, deposit)
        accounts = get_accounts()
        accounts.append(account)
        save_accounts(accounts)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/accounts')
def accounts():
    accounts = get_accounts()
    return render_template('accounts.html', accounts=accounts)

@app.route('/account/<int:accNo>')
def account(accNo):
    accounts = get_accounts()
    for account in accounts:
        if account.accNo == accNo:
            return render_template('account.html', account=account)
    return 'Account not found', 404

if __name__ == '__main__':
    app.run(debug=True)
