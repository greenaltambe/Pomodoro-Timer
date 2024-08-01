# Pomodoro Timer

#### Video Demo: <[URL HERE](https://youtu.be/lSBIQdK4uIw)>

#### Description: The Pomodoro timer is based on Pomodoro technique where when started, It starts a 25 minute focus session followed by 5 minute rest, then 25 minute focus session and so on. After 4 focus sessions there is a 20 minute break then the process repeats itself. I have implemented Pomodoro technique in my webapp. 
## helper.py

This file contains helper functions. I have imported sqlalchemy and werkzeug.security. It contains two classes User and FocusSession. User class is used for storing user data in database. FocusSession class is used for storing focus session data in database. User class contains id, name, age, set_password method, check_password method and FocusSession class contains user_id, start_time, duration.

## app.py

This is main python file. It contains the code for the webapp. It contains all the routes and the logic for the webapp. I have imported required modules like flask, sqlalchemy, datetime, functools and helper (my own).

### Methods in app.py

<details>
<summary>login</summary>
This method accepts username and password and checks if it is correct or not. If correct, It redirects to index/home page. It renders login.html with /login route.
</details>

<details>
<summary>register</summary>
This method accepts username, password and confirmation and checks if password is equal to confirmation. If it is, then it checks if user is already in the database, If yes then a message appears on top of screen to say that user already exist. If not, then user is successfully registered. After registration, User is redirected to login page. It renders register.html with /register route.
</details>

<details>
<summary>logout</summary>
Logs out the user. It has /logout route.
</details>

<details>
<summary>dashboard</summary>
This method displays data of logged in user in table format. The table contains time of start of focus session and duration of focus session. This method renders dashboard.html with /dashboard route.
</details>

<details>
<summary>login_required</summary>
This method created a decorator to check if user is logged in or not to access a particular part (page) of the webapp.
</details>

<details>
<summary>focus_data</summary>
This is method which adds the data of focus session in the database. It has /focus_data route.
</details>

## templates
This directory contains all the html files for the webapp.

<details>
<summary>layout.html</summary>
This is the layout of the webapp. All the html files inherit this layout. It contains navigation bar in top having login, register, logout and dashboard buttons. It also contains a text with tomato image. 
</details>

<details>
<summary>login.html</summary>
This is login page. It inherits from layout. It contains login form. The form sends data to login route when submitted. The form asks for username and password.
</details>

<details>
<summary>register.html</summary>
This is register page. It inherits from layout. It contains register form. The form sends data to register route when submitted. The form asks for username, password and confirm password.
</details>

<details>
<summary>index.html</summary>
This is index/home page. It inherits form layout. It shows container displaying timer and start/stop button. 
</details>

<details>
<summary>dashboard.html</summary>
This is dashboard page. It inherits from layout. It contains a table. The table contains time of start of focus session and duration of focus session. 
</details>

## static

This directory contains all the image files, javascript files and css files for the webapp.

<details>
<summary>style.css</summary>
This is the css file. It contains all the styling for the webapp. This file is in CSS directory inside static. This is the part of page with is way too long. The code just kept getting messier and messier because I was learning new stuff as I worked on this project. I also used a very weird font at the beginning but then chose a simple font at the end. I was also confused about whether or not to include animations in the webapp but in the end I decided to include them.
</details>

<details>
<summary>script.js</summary>
This is the javascript file. It contains all the logic for the webapp. This file is in JS directory inside static. This is where the timer logic is implemented. I have used json to send data of time and duration of focus session to server.
</details>

<details>
<summary>tomato.png</summary>
It is a tomato image. This file is in Images directory inside static.
</details>

