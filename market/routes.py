from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import item, user
from market.forms import register_form, login_form, purchase_item, sell_item
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/market", methods = ["GET", "POST"])
@login_required
def market_page():

    purchase_form = purchase_item()
    sell_form = sell_item()
    if request.method == 'POST':
        purchased_item = request.form.get("purchased_item")
        p_item_obj = item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.buy(current_user)
                flash(f"Congratulation, you purchased {p_item_obj.name} for {p_item_obj.price}$", category="success")
            else:
                flash("You don't have enough money", category="danger")
        
        sold_item = request.form.get("sold_item")
        s_item_obj = item.query.filter_by(name=sold_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f"Congratulation, you sold {s_item_obj.name} to market", category="success")
            else:
                flash(f"Something went wrong while selling {s_item_obj.name}", category="danger")

        return redirect(url_for("market_page"))
    
    if request.method == "GET":
        items = item.query.filter_by(owner=None)
        owned_items = item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)

@app.route("/register", methods = ["GET", "POST"])
def register_page():
    form = register_form()
    if form.validate_on_submit():
        create_user = user(username = form.username.data, email = form.email.data, password_hash = form.password1.data)
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        flash(f"Account created successfully! You are logged in as {create_user.username}", category="success")    
        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error with creating an account : {err_msg}", category="danger")
    return render_template("register.html", form=form)

@app.route("/login", methods = ["GET", "POST"])
def login_page():
    form = login_form()
    if form.validate_on_submit():
        attempted_user = user.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as {attempted_user.username}", category="success")
            return redirect(url_for("market_page"))
        else:
            flash("Username or password not match", category="danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out", category= "info")
    return redirect(url_for("home_page") )