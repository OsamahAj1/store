import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from flask_session import Session
from helpers import error, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///store.db")

# Configure files
app.config['UPLOAD_FOLDER'] = r"C:\Users\Osama\PycharmProjects\Store\store\static"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Allowed files
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """show all products on index page"""

    # if method POST render templet with filter
    if request.method == "POST":

        # getting filter from user
        type_name = request.form.get("type")
        price = request.form.get("price")

        if (type_name == "filter" or type_name == "All") and price == "price":
            flash("Filter removed")
            return redirect("/")

        # if user choose all we show all products
        if (type_name == "All" or type_name == "filter") and price == "Smaller-Bigger":
            products = db.execute(
                "SELECT name, price, image, products.id FROM products ORDER BY price")

        elif (type_name == "All" or type_name == "filter") and price == "Bigger-Smaller":
            products = db.execute(
                "SELECT name, price, image, products.id FROM products ORDER BY price DESC")

        elif (type_name != "All" or type_name != "filter") and price == "Smaller-Bigger":
            products = db.execute("SELECT name, price, image, products.id FROM products JOIN types WHERE "
                                  "products.type_id = types.id AND type = ? ORDER BY price", type_name)

        elif (type_name != "All" or type_name != "filter") and price == "Bigger-Smaller":
            products = db.execute("SELECT name, price, image, products.id FROM products JOIN types WHERE "
                                  "products.type_id = types.id AND type = ? ORDER BY price DESC", type_name)

        elif (type_name != "All" or type_name != "filter") and price == "price":
            products = db.execute("SELECT name, price, image, products.id FROM products JOIN types WHERE "
                                  "products.type_id = types.id AND type = ?", type_name)

        # query to get types
        typess = db.execute("SELECT type FROM types")

        # get user_cash
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        # render templet with filter
        flash("Filter applied")
        return render_template("index.html", products=products, typess=typess, cash=cash)

    # if method GET render templet without filter
    else:
        # query to get products
        products = db.execute(
            "SELECT name, price, image, products.id FROM products")

        # query to get types
        typess = db.execute("SELECT type FROM types")

        # query to get sum of items in cart
        i = db.execute(
            "SELECT sum(n) AS sum FROM cart WHERE user_id = ?", session["user_id"])

        # if there is no items return 0
        if i[0]["sum"] is None:
            i = 0

        # if there is items return the number of items
        else:
            i = i[0]["sum"]

        # get user_cash
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        # render the page and pass the products
        if request.args.get("r") == "r":
            flash("Filter removed")
        return render_template("index.html", products=products, typess=typess, i=i, cash=cash)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["name"] = request.form.get("username")

        # Redirect user to home page
        flash("Logged in")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("logged out")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # POST
    if request.method == "POST":

        # define variables for inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        # make sure no blanks
        if not username or not password or not confirm:
            return error("Must fill all fields", 400)

        # make sure password = confirm
        if password != confirm:
            return error("Password and confirmation do not match", 400)

        # make sure username not taken
        users = db.execute(
            "select username from users where username = ?", username)
        if len(users) == 1:
            return error("username already taken", 400)

        # adding data to database
        hashp = generate_password_hash(password)
        db.execute(
            "insert into users (username, hash) values (?, ?)", username, hashp)

        # log user in
        uid = db.execute("select id from users where username = ?", username)
        session["user_id"] = uid[0]["id"]
        session["name"] = username
        flash("Registered")
        return redirect("/")

    # GET
    else:
        return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """change password of user"""

    # POST
    if request.method == "POST":

        # get input from user
        password = request.form.get("password")
        new_password = request.form.get("new_password")
        re_password = request.form.get("re_password")

        # make sure input not empty
        if not password or not new_password or not re_password:
            return error("Must fill all fields", 400)

        # get user password
        user_password = db.execute(
            "SELECT hash FROM users WHERE id = ?", session["user_id"])

        # make sure user password = input password
        if not check_password_hash(user_password[0]["hash"], password):
            return error("Invalid old password", 400)

        # make sure new_password == re_password
        if new_password != re_password:
            return error("Password and confirmation do not match", 400)

        # update user password
        hashp = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   hashp, session["user_id"])

        # redirect
        flash("Changed")
        return redirect("/")

    # GET
    else:
        return render_template("change.html")


@app.route("/bought", methods=["GET", "POST"])
@login_required
def buy():
    """buy products and display bought products"""

    # if POST buy the products
    if request.method == "POST":

        # get cart products
        products = db.execute("SELECT products_id, n, total FROM cart JOIN products WHERE cart.products_id = "
                              "products.id AND user_id = ?", session["user_id"])

        # check if cart empty
        if len(products) == 0:
            return error("cart is empty", 400)

        # query to get user cash and cart cash
        cart_cash = db.execute(
            "SELECT sum(total) AS sum FROM cart WHERE user_id = ?", session["user_id"])
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])

        # update user cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash[0]["cash"] - cart_cash[0]["sum"],
                   session["user_id"])

        # getting date and time
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")

        # insert to history
        db.execute("INSERT into history (cash, user_id, date) VALUES (?, ?, ?)",
                   cart_cash[0]["sum"] * -1, session["user_id"], date)

        # loop to move products from cart to bought
        for i in products:
            db.execute("INSERT INTO bought (user_id, products_id, n, total, date) VALUES (?, ?, ?, ?, ?)",
                       session["user_id"], i["products_id"], i["n"], i["total"], date)

        # empty the cart
        db.execute("DELETE FROM cart WHERE user_id = ?", session["user_id"])

        # redirect
        flash("Bought")
        return redirect("/bought")

    # if GET display the bought page with data
    else:
        # query to get data
        bought = db.execute("SELECT image, name, price, n, total, date, products_id FROM bought JOIN products JOIN "
                            "users WHERE users.id = bought.user_id AND products.id = bought.products_id AND user_id = "
                            "?", session["user_id"])

        # get user_cash
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        # return template with data
        return render_template("bought.html", bought=bought, cash=cash)


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    """shopping cart"""

    # if method POST we add items to cart
    if request.method == "POST":

        # get the product id and how many products from user
        idd = request.form.get("id")
        n = request.form.get("n")

        # check if n is digit
        if str(n).isdigit() is False:
            return error("number must be positive digit")
        idd = int(idd)
        n = int(n)

        # get the price of product to calculate total
        price = db.execute("SELECT price FROM products WHERE id = ?", idd)
        price = float(price[0]["price"])

        # calculate total
        total = price * n

        # if product not already on cart insert it
        # else update n and total

        # get the cart products to check
        cart_items = db.execute("SELECT products_id FROM cart WHERE products_id = ? AND user_id = ?",
                                idd, session["user_id"])

        # check by checking if the variable empty
        if len(cart_items) == 0:

            # insert
            db.execute("INSERT INTO cart (total, n, products_id, user_id) VALUES (?, ?, ?, ?)", total, n, idd,
                       session["user_id"])

        else:

            # get current n to update new n
            old_n = db.execute(
                "SELECT n FROM cart WHERE products_id = ? AND user_id = ?", idd, session["user_id"])
            old_n = old_n[0]["n"]
            new_n = old_n + n
            new_total = new_n * price

            # update
            db.execute("UPDATE cart SET total = ?, n = ? WHERE products_id = ? AND user_id = ?",
                       new_total, new_n, idd, session["user_id"])

        # redirect to index
        flash("added")
        return redirect("/")

    # if GET show cart
    else:

        # query to get cart items
        items = db.execute("SELECT image, name, price, n, total, products_id FROM products JOIN cart JOIN users WHERE "
                           "cart.products_id = products.id AND users.id = cart.user_id AND user_id = ?",
                           session["user_id"])

        # query to get sum of cart
        sum_cart = db.execute("SELECT sum(total) AS sum FROM products JOIN cart JOIN users WHERE cart.products_id = "
                              "products.id AND users.id = cart.user_id AND user_id = ?", session["user_id"])

        # query to get sum of items in cart
        i = db.execute(
            "SELECT sum(n) AS sum FROM cart WHERE user_id = ?", session["user_id"])

        # if there is no items return 0
        if i[0]["sum"] is None:
            i = 0

        # if there is items return the number of items
        else:
            i = i[0]["sum"]

        # get user_cash
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        # render template with values
        return render_template("cart.html", items=items, sum_cart=sum_cart, i=i, cash=cash)


@app.route("/page", methods=["GET", "POST"])
@login_required
def page():
    """page"""

    # if GET display item
    if request.method == "GET":

        # get id
        idd = request.args.get("id")

        # query to get data
        data = db.execute(
            "SELECT id, name, price, rate, des FROM products WHERE id = ?", idd)

        # query to get images
        image = db.execute(
            "SELECT image FROM images WHERE products_id = ?", idd)

        # query to get comments
        com = db.execute("SELECT username, comment, rate, date FROM comments JOIN users WHERE users.id = "
                         "comments.user_id AND products_id = ?", idd)

        # query to get avg rate
        rate = db.execute(
            "SELECT avg(rate) AS rate FROM comments WHERE products_id = ?", idd)

        if rate[0]["rate"] is None:
            rate = "No rate"

        else:
            rate = f'{rate[0]["rate"]:.1f}'

        # query to get how many user rate it
        c = db.execute(
            "SELECT count(rate) AS count FROM comments WHERE products_id = ?", idd)
        c = c[0]["count"]

        # render template with data
        return render_template("items.html", data=data, image=image, com=com, rate=rate, c=c)

    # if POST remove comment
    else:

        # get comment and username
        comment = request.form.get("comment")
        name = request.form.get("name")

        # get user id
        idd = db.execute("SELECT id FROM users WHERE username = ?", name)
        idd = idd[0]["id"]

        # delete comment
        db.execute(
            "DELETE FROM comments WHERE user_id = ? AND comment = ?", idd, comment)

        # return page
        return redirect("/")


@app.route("/update", methods=["POST", "GET"])
@login_required
def update():
    """update item from cart"""

    # if method POST remove item from cart
    if request.method == "POST":
        # get the id of the item user want to remove
        idd = request.form.get("id")
        idd = int(idd)

        # query to remove item from cart
        db.execute("DELETE FROM cart WHERE products_id = ? AND user_id = ?",
                   idd, session["user_id"])

        # redirect
        flash("Removed")
        return redirect("/cart")

    # if method GET update total
    if request.method == "GET":
        # get n and id
        idd = request.args.get("id")
        n = request.args.get("n")

        # check if n is digit
        if str(n).isdigit() is False:
            return error("number must be positive digit")
        idd = int(idd)
        n = int(n)

        # to get price
        price = db.execute("SELECT price FROM products WHERE id = ?", idd)
        price = float(price[0]["price"])

        # calculate new total
        total = n * price

        # update total and n in db
        db.execute("UPDATE cart SET total = ?, n = ? WHERE products_id = ? AND user_id = ?", total, n, idd,
                   session["user_id"])

        # return template with total
        flash("Updated")
        return redirect("/cart")


@app.route("/comments", methods=["POST"])
@login_required
def comments():
    """Add comments to products"""

    # check if rate is digit
    if str(request.form.get("rate")).isdigit() is False:
        return error("number must be positive digit")

    # check if user give comment and rate
    if not request.form.get("rate") or not request.form.get("comment"):
        return error("must provide comment and rate")

    # get inputs from user
    comment = request.form.get("comment")
    rate = request.form.get("rate")
    rate = float(rate)
    idd = request.form.get("id")
    idd = int(idd)

    # getting date and time
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")

    # add comment to db
    db.execute("INSERT INTO comments (user_id, products_id, rate, comment, date) VALUES (?, ?, ?, ?, ?)",
               session["user_id"], idd, rate, comment, date)

    idd = str(idd)

    flash("Commented")
    return redirect("/page?id=" + idd)


@app.route("/admin", methods=["POST", "GET"])
@login_required
def admin():
    """add products to store"""

    # if POST add product to store
    if request.method == "POST":

        # error checking
        if not request.form.get("name") or not request.form.get("des") or not request.form.get("price") or not request.files["image1"] or not request.files.getlist("image3"):
            return error("must fill all fields and images except type choose one")

        if not request.form.get("new_type") and not request.form.get("in_type"):
            return error("must fill one of type")
        if not allowed_file(request.files["image1"].filename):
            return error("image must be .png or .jpg or .jpeg")

        for i in request.files.getlist("image3"):
            if not allowed_file(i.filename):
                return error("image must be .png or .jpg or .jpeg")

        # 1- type

        # check if it's new
        new_type = request.form.get("new_type")

        # if type already in db
        if not new_type:

            # get the type
            in_type = request.form.get("in_type")

            # get type id
            type_id = db.execute(
                "SELECT id FROM types WHERE type = ?", in_type)
            type_id = type_id[0]["id"]

        # if new type
        elif new_type:

            # get the new type
            new_type = request.form.get("new_type")

            # insert new type into db
            db.execute("INSERT INTO types (type) VALUES (?)", new_type)

            # get id of new type
            type_id = db.execute(
                "SELECT id FROM types WHERE type = ?", new_type)
            type_id = type_id[0]["id"]

        # 2- name, price, des

        # get name, price,des from user
        name = request.form.get("name")
        price = request.form.get("price")
        des = request.form.get("des")

        # 3- display image1

        # get image from user
        image1 = request.files["image1"]

        # insert image to pc and name of image to db
        if image1 and allowed_file(image1.filename):
            image1_name = secure_filename(image1.filename)
            image1.save(os.path.join(app.config["UPLOAD_FOLDER"], image1_name))
            db.execute("INSERT INTO products (name, price, des, type_id, image) VALUES (?, ?, ?, ?, ?)",
                       name, float(price), des, int(type_id), "/static/" + image1_name)

        # 4- display image3

        # get id of product
        product_id = db.execute("SELECT id FROM products WHERE name = ?", name)
        product_id = product_id[0]["id"]

        # get images from user
        image3 = request.files.getlist("image3")

        # insert images to pc and name of images to db with product id
        for image in image3:
            if image and allowed_file(image.filename):
                image_name = secure_filename(image.filename)
                image.save(os.path.join(
                    app.config["UPLOAD_FOLDER"], image_name))
                db.execute("INSERT INTO images (image, products_id) VALUES (?, ?)",
                           "/static/" + image_name, int(product_id))

        # redirect to index
        flash("product added")
        return redirect("/")

    # if GET show admin page
    else:

        # get types
        typess = db.execute("SELECT type FROM types")

        # render template with types
        return render_template("admin.html", typess=typess)


@app.route("/cash", methods=["POST", "GET"])
@login_required
def update_cash():
    """update cash"""

    # if POST add cash
    if request.method == "POST":

        # get cash from user
        cash = request.form.get("cash")

        # check if user provide cash
        if str(cash).isdigit() is False:
            return error("number must be positive digit")
        cash = float(cash)

        # get user current cash from db
        old_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        old_cash = float(old_cash[0]["cash"])

        # getting date and time
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")

        # insert into history
        db.execute("INSERT into history (cash, user_id, date) VALUES (?, ?, ?)",
                   cash, session["user_id"], date)

        # update cash in db
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   cash + old_cash, session["user_id"])

        # from index back to index
        if request.form.get("a") == "1":
            return redirect("/")

        # from cart back to cart
        else:
            return redirect("/cart")

    # if GET display page
    else:

        # get history from db
        cash = db.execute(
            "SELECT cash, date FROM history WHERE user_id = ?;", session["user_id"])

        # render template with history
        return render_template("history.html", cash=cash)

