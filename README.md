# Store
#### Video Demo:  https://youtu.be/2B2UqkMH4oo
#### Description: I am going to start with html files calling each one then with app.py file and call every function in it.

## how to run
> cd the project and execute:
>
> Flask run

## accounts
> username: admin
>
> password: admin
>
> username: osamah
>
> password: 12345

# Html Files

## layout.html
>in the beginning of the file I am configuring bootstrap in the head,
> and setting icon for the website which is a cart emoji from favicon website,
> then configuring my own style sheet, then setting a title which is a store then
> creating a block with jinja, so I can call the page what ever I want next.
> 
> in the body I am creating a nav and putting the store name in it, then if the user
> is logged in using jinja I show logged in as username then bought page then
> cash history and after that if the user is admin which id is 1 I show add products
> button, so only the admin can add products to the store then change password and logout
> . and if the user is not logged in I am showing a register and log in button only.
>
> next I am configuring where the flash message will show.
> 
> and next I am creating a main and putting in it a block using jinja, so I can put
> my page content there when I use the layout page.
> 
> next I am creating a footer writing in copyright the copyright sign and my name and
> here is where my layout page end.

## register.html
> in the register page I am starting by extending the layout and give the page title
> then starting the page in main.
> 
> in main, I am starting by creating a form that will send user inputs to /register
> using post method.
>
> inputs using bootstrap form control and putting it in the middle of page:
> 
> 1. first is username giving name and placeholder and id the name username, turning off 
> autocomplete and giving it type text.
> 2. second is password giving name and placeholder and id the name password, and type password, so it shows stars instead of text.
> 3. third is just confirming password to make sure user didn't miss type anything.
> 
> and between inputs I am putting a div, so it makes gap between them.
> 
> then a register button that will submit the form using bootstrap button style.

## login.html
> in the login page I am starting by extending the layout and give then page title
> then starting the page in main.
> 
> in main, I am starting by creating a form that will send user inputs to /login
> using post method.
>
> inputs using bootstrap form control and putting it in the middle of page:
> 
> 1. first is username giving name and placeholder and id the name username, turning off 
> autocomplete and giving it type text.
> 2. second is password giving name and placeholder and id the name password, and type password, so it shows stars instead of text.
> 
>  and between inputs I am putting a div, so it makes gap between them.
> 
> then a login button that will submit the form using bootstrap button style.

## change.html
> in the change page I am starting by extending the layout and give the page title
> then starting the page in main.
> 
> change page is the page that change user password
> 
> in main, I am starting by creating a form that will send user inputs to /change_password
> using post method.
>
> inputs using bootstrap form control and putting it in the middle of page:
> 
> 1. first is old password giving it name password and placeholder password and type password, so it shows stars instead of text
> 2. second is new password giving name new_password and placeholder new password, and type password, so it shows stars instead of text.
> 3. third is just confirming new password to make sure user didn't miss type anything.
> 
> and between inputs I am putting a div, so it makes gap between them.
> 
> then a change button that will submit the form using bootstrap button style.

## error.html
> in the error page I am starting by extending the layout and give then page title
> then starting the page in main.
> 
> error page is the page will show for the user when he makes any error.
> 
> in main, I am putting image and text in it using memegen.

## index.html
> in the index page I am starting by extending the layout and give the page title then starting the page in main.
> 
> index page is the home page for store that will show products and filters and cart and cash and add cash and add to cart.
> 
> starting home page with filters: filter for type and filter for price, and cart below it cash and add cash.
> 
> creating a container using bootstrap creating one row have 2 columns:
> one for the filter nad one for cart and cash and add cash.
> 
> in filter colum I am creating a form submit to "/" using method post that have a select giving it name type and my own style for width and height,
> and 2 options one called and valued filter, and second one called and valued all,
> then I am starting loop using jinja to loop through all types in store using option and valued with that type.
> and after that there is another select called price and my own style for width and height this select have 3 options:
> first one called and valued price, second one called and valued bigger-smalled, third one called and valued smaller-bigger.
> 
> then there is button to submit to "/" using post with bootstrap style.
> 
> after that there is another form that submit to "/" using get and have one button called remove filters
> named and valued r, and it's red button bootstrap style
> 
> and here is the second colum that have the cart and cash and add cash.
> I start in this colum by creating redirect to /cart inside it there is button and cart image and a span for displaying
> how many products there is in cart using jinja and the cart created using bootstrap.
> 
> next it shows cash with filter usd.
> 
> next there is form that submit to /cash using post method inside it there is input
> for how many cash name cash placeholder add cash and type number and setting minimum to 1 turning autocomplete off and styling it
> with my own width and height and putting it in center, then another hiding input named a and valued 1,
> so I can redirect user to index after he adds cash more on that later.
> and at the end is add button that submit to /cash style with bootstrap colored green.
> 
>
> next is container with one row and loop through columns, in the colum there is first
> a form submit to /page using get method that have 2 inputs first one is hidden for product id second one
> is product image that submits the form, then the name and price of product, 
> 
>then another form that add the product to the cart submit to /cart
> using post method, and it has 2 inputs one is hidden for product id and second one is for how many one of that product to add to cart,
> then a button submit to /cart.
> 
> and here where index ends after all products looped through them.

## items.html
> in the items page I am starting by extending the layout and give the page title then starting the page in main.
> 
> items page is the page that will show details about the products and more images and comments and rate.
> 
> starting by creating a container 2 columns one is for slide images I took that from
> bootstrap document, and I insert in it the 3 images using jinja,
> 
> second colum is a loop through name and price and rate and description and add to cart button,
> first is a bunch of divs for: name, price, rate that shows how many rates there is and the average rate, description.
> then a form which is the same in index.html that add the product to the cart submit to /cart
> using post method, and it has 2 inputs one is hidden for product id and second one is for how many one of that product to add to cart,
> then a button submit to /cart.
> 
> next after the container I show comments and how many comments there is, then a loop
> so I can add product id to it, so I start by a form submit to /comments using post method
> that have 3 inputs one for user comment and one for user rate out of 10 and is hidden for product id.
> 
> next there is all comments using loop and section, so I loop through all comments and display the name of the person who commented
> then the date then the rate then the comment, and inside this loop there is form for
> admin that will remove the comment, so the form submit to /page using post method and there is 2 inputs inside it
> one is the user comment and one is the username then a button called remove colored red by bootstrap submit to /page.

## cart.html
> in the cart page I am starting by extending the layout and give the page title then starting the page in main.
> 
> this page is for displaying the cart and user can add cash from here too.
> 
> I start in this page by creating redirect to /cart that is the same in index.html inside it there is button and cart image and a span for displaying
> how many products there is in cart using jinja and the cart created using bootstrap.
> 
> next it shows cash with filter usd.
> 
> next there is form that submit to /cash using post method inside it there is input
> for how many cash name cash placeholder add cash and type number and setting minimum to 1 turning autocomplete off and styling it
> with my own width and height and putting it in center, but here I don't have the hiding input named a and valued 1,
> so I can redirect user to cart after he adds cash more on that later.
> and at the end is add button that submit to /cash style with bootstrap colored green.
> 
> next is container have a loop through rows and 6 colum and the rows is cart items,
> so first colum is the image then, name of product then, price of product with usd filter then, 
> a form to update how many one of product submit to /update using get and it has 1 input hidden for
> product id and a button submit to /update styled with bootstrap then, the total of all products price with usd filter
> then, another form submit to update too but now using post and it has hidden input too for id and a remove button colored red with bootstrap.
> 
> next is the second row in container that have the sum of all products prices in cart using usd filter.
> 
> next is the third row in container that have a form to buy the products submit to /bought using post method, and it has only one button
> styled with bootstrap submit to /bought.

## bought.html
> in the bought page I am starting by extending the layout and give the page title then starting the page in main.
> 
> in the start of page  I show user cash with usd filter.
> 
> then basically a container have a loop through 1 row and 6 columns to show all products user have bought,
> first colum is name, then price with float and usd, then how many one of this product, then total price of product with float and usd,
> then the date of buying.

## history.html
> in the history page I am starting by extending the layout and give the page title then starting the page in main.
> 
> history is a table that shows the history of money spending and adding.
> 
> the table head is cash and date.
> 
> the table body is a loop through cash with usd, and the date.

## admin.html
> in the cart page I am starting by extending the layout and give the page title then starting the page in main.
> 
> admin is basically a big form have 5 inputs and 1 select to let admin add a new product to the store.
> 
> the form submits to /admin using post method.
> first it asks for name of product, then price, then description, then it asks for type that
> already in store with select and loop through options or to add a new type, then it asks for image that will show in index page
> , then it asks for 3 images that will show in the product page, then there is the button to submit the form
> to /admin styled with bootstrap.

# data base

## bought
> save user bought products with user_id, product_id, number of products, total price, date.

## cart
> save user cart with total price, number of products, user_id, product_id.

## comments
> save the comments with user_id, product_id, comment, rate, date.

## history
> save user cash history with cash, user_id, date.

## images
> save the 3 images in product page with product_id, image.

## products
> save the products data with id, name, price, description, type_id, image will show in index page.

## types
> save the types of products that is in store with id, type.

## users
> save users information with id, username, password, cash.

# app.py
note: I am going to refer to comments between braces()

## configuring
>app, session, sql, files, allowed_extensions files that allowed, allowed_file check if the file allowed.

## index
> this route handle the products to page from sql and, accept 2 methods.
> 
> (if method POST render templet with filter):
>> when it's post.
>>I get the type and price from user filters then assign products to the query depends on what user choose.
>
> if user didn't choose anything or just choosed all and price redirect to "/".
>
> (query to get types):
>> here I get the products types from db.
> 
> (get user_cash):
>> here I get user cash from session.
> 
> (render templet with filter):
>> here I flash filter applied first then I render index.html with the products that filtered and types and user cash.
> 
> (if method get render templet without filter):
>> here I just get the products without filters
> 
> (query to get products).
> (query to get types).
> 
> (query to get sum of products in cart):
>> here I am using sql command sum to get how many products in the cart.
> 
> (if here is no products return 0):
>> if the cart is empty return 0.
>>
>> else return the sum.
>
> (get user_cash):
>> here I get user cash from session.
>
> if there's something called r it's mean user pressed the remove all filters button, so I flash filter removed.
> 
> I render index.html without filters

## login
> first clear session to make sure user logged out.
> 
> when it's post first I check errors.
> 
> then I check if the username in db and check password and if every thing okay log in the user and redirect to "/".
> 
> when it's get just display the login.html.

## logout
> just clear session and flash logged out and redirect to "/".

## register
> when it's post first error checking.
> 
> make sure password and confirm all equals.
> 
> make sure username not already in db
> 
> then hash the password for security and insert username and hashed password to db.
> 
> then log user in and flash registered and redirect to "/"
> 
> when it's get just show register.html


## change_password
> when it's post first error checking.
> 
> then make sure old password and the password user entered are equals
> 
> make sure new password and confirm are equals
> 
> update password in db where name in session
> 
> flash changed and redirect to "/"
> 
> when it's get just show change.html


## buy
> when it's post I buy products.
> 
> get cart from db
> 
> make sure cart is not empty.
> 
> then update user cash, then get the date and time and insert to history with cash spend.
> 
> then move cart to bought but add date and time too.
> 
> then make the cart empty.
> 
> flash bought and redirect to /bought.
> 
> when it's get, get the bought and cash from db and show bought.html with data.


# cart
> when it's post we add product to cart.
> 
> first get product id and how many product user want.
> 
> make sure number is digit then convert it.
> 
> get price of product from db and calculate the total.
> 
> if product not already in the cart just add it, but when it's in cart increase how many product in cart.
> 
> flask added and redirect to "/"
> 
> when it's get, get the cart from db and sum of cart and user cash and how many products in cart, and show cart.html with data.


## page
> when it's get I get the id of product the user want to see from hidden input
> 
> then I get the data of that product and comments of that product and avg of rates of that product (and when there is no rate just return no rate) from db.
> 
> then show items.html with data.
> 
> when it's post mean admin want to remove comment.
> 
> get the name and comment admin want to remove and remove it from data.
> 
> redirect to "/"

# update:
> when post remove the product user want to remove from cart.
> 
> get id of product user want to remove from hidden input.
> 
> then delete the product from db.
> 
> flask removed and redirect to /cart.
> 
> when get update how many one of that product.
> 
> get the number from user and make sure it's digit
> 
> calculate the new total
> 
> then update the number and total in cart in db
> 
> flash updated and redirect /cart.

## comments
> comments only accept post, and it adds comment to product.
> 
> make sure rate is digit and error check.
> 
> get user comment and rate and date and time, then insert them to db.
> 
> flash commented and redirect user to page he was seeing.

##admin
> when post add product to store.
> 
> error checking first.
> 
> then check if it's new type or already type.
> 
> then get name, price, description.
> 
> then get the index image and save it to pc and add it name plus the folder to db.
> 
> then get the 3 images and save it to pc and add it names plus folder to db.
> 
> flash product added and redirect to "/".
> 
> when get, get the types from db, then show admin.html with data.

##cash
>when post add cash.
> 
> get the cash from user and make sure it's digit.
> 
> get the current user cash from db and add it to the new cash.
> 
> get the date and time and insert the cash and date and time in history.
> 
> then update user cash in db.
> 
> if the user added cash from index i will get the a hidden input, so I will redirect to "/".
> 
> and if I didn't get the hidden value i will redirect to /cart.
> 
> when get, get history from db and show history.html with data.





