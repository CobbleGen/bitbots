from os import abort
from my_server import app, dbhandler
from flask import jsonify, render_template, url_for, request


@app.route('/')
@app.route('/index')
def start():
    tot_bots = len(dbhandler.get_bots())
    return render_template('index.html', tot_bots = tot_bots)

@app.route('/bots')
def bots():
    bots = []
    for bot in dbhandler.get_bots():
        bots.append(bot.serialize)
    return jsonify(bots)

@app.route('/combine')
def combine():
    return render_template('combine.html')

@app.route('/botinfo/<bot_id>')
def botinfo(bot_id = None):
    if bot_id == None:
        abort(404)
    bot = dbhandler.get_bot(bot_id)
    history_tree = None
    if len(bot.made_from) > 0:
        history_tree = bot.made_from[0].serialize()
    return render_template('botinfo.html', bot=bot.serialize, history_tree=history_tree)

@app.route('/bot/<bot_id>')
def bot(bot_id = None):
    if bot_id == None:
        return jsonify({"error"})
    bot = dbhandler.get_bot(bot_id)
    return jsonify(bot.toMetadata)

@app.route('/wallet')
@app.route('/wallet/<address>')
def wallet(address = 0):
    return render_template('wallet.html', address=address)
    




@app.route('/_new_bot', methods=['GET', 'POST'])
def new_bot():
    id    = request.form['id']
    level = request.form['level']
    head = request.form['head']
    body = request.form['body']
    l_arm = request.form['l_arm']
    r_arm = request.form['r_arm']
    l_leg = request.form['l_leg']
    r_leg = request.form['r_leg']
    created  = dbhandler.add_bot(int(id), level, head, body, r_arm, l_arm, l_leg, r_leg)
    return jsonify(created.serialize)

@app.route('/_bot_serial/<id>')
def bot_serial(id = None):
    if id == None:
        return ''
    return jsonify(dbhandler.get_bot(id).serialize)


@app.route('/_contract_metadata')
def metadata():
    return jsonify({
        "name": "BitBots",
        "description": "BitBots is a collection of robots that have been constructed by mismatched bits of other robots. Collect them and then combine two Bots with your favourite parts from each to make a new one!",
        "image": "http://localhost:8070/static/bots-images/8.PNG",
        "external_link": "http://localhost:8070/",
        "seller_fee_basis_points": 500, # Indicates a 5% seller fee.
        "fee_recipient": "0xE0666cAC0C2267209Ba3Da4Db00c03315Fe64fA8"
    })