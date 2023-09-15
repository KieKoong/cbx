import gspread
from flask import Flask, render_template, redirect, url_for, request, flash

sa = gspread.service_account('mysheets.json')
sh = sa.open_by_key('1CXKnkbHDQkMuTug2Y5vb5lx-fQwiLlDPJijmq9LABJk')
F_acc = sh.worksheet('F_accounting')

app = Flask(__name__)
app.secret_key = 'key_555666'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['GET', 'POST'])
def save():
    date = request.form['date'] #Date (DD/MM/YYYY)
    if date == "":
        date = "--/--/----"

    ec = request.form['ec'] #Exchange cash
    if ec == "":
        ec = '0'

    pc = request.form['pc'] #Pocket cash
    if pc == "":
        pc = '0'

    Ftr = request.form['Ftr'] #F_total revenue
    if Ftr == "":
        Ftr = '0'

    pee = request.form['pee'] #pocket etc exp
    if pee == "":
        pee = '0'

    sr = request.form['sr'] #sticky rice
    if sr == "":
        sr = '0'

    cl = request.form['cl'] #cola
    if cl == "":
        cl = '0'

    wt = request.form['wt'] #water
    if wt == "":
        wt = '0'

    fu = request.form['fu'] #fuel
    if fu == "":
        fu = '0'

    ot = request.form['ot'] #others
    if ot == "":
        ot = '0'

    total_exp = int(sr)+int(cl)+int(wt)+int(fu)+int(ot)
    pocket_balance = int(pee)-int(total_exp)
    
    if pocket_balance > 0:
        cash_borrowed = 0
    else:
        cash_borrowed = pocket_balance*-1

    cash_rvn = (int(pc)-int(ec))+cash_borrowed
    transfer_rvn = int(Ftr)-cash_rvn

    return redirect(url_for("check", **locals()))
        
@app.route('/check')
def check():
    date = request.args.get('date') 
    ec = request.args.get('ec')
    pc = request.args.get('pc')
    Ftr = request.args.get('Ftr')
    pee = request.args.get('pee')
    sr = request.args.get('sr')
    cl = request.args.get('cl')
    wt = request.args.get('wt')
    fu = request.args.get('fu')
    ot = request.args.get('ot')
    total_exp = request.args.get('total_exp')
    pocket_balance = request.args.get('pocket_balance')
    cash_borrowed = request.args.get('cash_borrowed')
    cash_rvn = request.args.get('cash_rvn')
    transfer_rvn = request.args.get('transfer_rvn')
    
    return render_template("check.html", **locals())

@app.route('/add', methods=['POST', 'GET'])
def add():
    date = request.form['date']
    ec = request.form['ec'] 
    pc = request.form['pc'] 
    Ftr = request.form['Ftr'] 
    pee = request.form['pee'] 
    sr = request.form['sr'] 
    cl = request.form['cl'] 
    wt = request.form['wt'] 
    fu = request.form['fu'] 
    ot = request.form['ot'] 
    total_exp = request.form['total_exp']
    pocket_balance = request.form['pocket_balance']
    cash_borrowed = request.form['cash_borrowed']
    cash_rvn = request.form['cash_rvn']
    transfer_rvn = request.form['transfer_rvn']

    rows = [date,ec,pc,cash_borrowed,Ftr,cash_rvn,transfer_rvn,pee,total_exp,sr,cl,wt,fu,ot,pocket_balance]
    F_acc.append_rows([rows])
    return render_template('added.html', **locals())

if __name__ == '__main__':
    app.run(debug=True)