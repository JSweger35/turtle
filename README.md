# Turtle
#### Video Demo:  https://youtu.be/gR5MClh24WQ
#### Description:

### For this project I decided to create a web app that I call "Turtle". The inspiration for this was to create a twitter like  application as twitter news seems to be all over the place at the moment.

### This app gives you the ability to create a profile with a user picture and username specific to you. From there you can post to the main feed page, chat with anyone else on the website, or view your specific posts. I wanted the ability to post regardless of what page you were on. I also made it so that once you were chatting with one person, it would stay on that page.

### This project splits the web app into a few different sections. It first allows you to create a profile with the registration html template and then logs you in with the login template. Your username and password are saved into a users database with the password using a password hash function. It will also reject duplicate usernames when registering as well as incorrect username/password combinations when logging in.

### Once logged in, there are three main pages, "Feed", "Chat", and "Profile".

### The Feed page is the main page that shows everything that every user has posted. This is pulled from the "posts" database. I wanted the ability to post from any page, so the post dropdown is in the navigation bar and will redirect you to the feed page when a post is submitted.

### The chat page gives you the ability to have a conversation with other specific users in the database. You can select whatever user you would like to have a conversation with and it will direct you to the "chatting" html template where it will you show a conversation between you and that other user. It will also pul the users specific profile picture at the top. These conversations are also posted in the "posts" database and are filtered slightly different to avoid the same information on the feed page.

### The profile page is the last page that uses the profile.html template to show you your current user picture as well as all of your specific posts.

### Going into the different files and folders: within the static folder, it included three profile pictures for the three different users within the users databased. It also included the turtle logo for the web app. Lastly it included the css styles sheet for the site to work with bootstrap.

### Under the templates there were a few different html layouts:
### - apology.html shows when something is not entered correctly within the the web app.
### - chat.html is the layout for the the chat tab for two different users to have a conversation
### - chatting.html is the layout for when you are already in a conversation with a certain user.
### - index.html is the feed page that shows all of the posts from all users in the posts database.
### - layout.html is the base layout for almost all the other html files
### - login.html is the login page
### - post.html was initially going to be a page to be able to post from, however was later decided to be part of the layout.html.
### - profile.html is the profile tab of the web app that shows all posts by the user that is currently logged in.
### - register.html is the tab where you can create a new user in the users database.

### app.py is the main code of how the web app actually functions. This pulls and inserts in different data from the project.db database and also decides what template to load based on the users input.

### poject.db stores all the data within two tables, the users and posts tables. The users table stores all of the user information including the username, id, the hash password, and the profile picture. The profile picture is something that is not currently complete in the ability to add it directly from the site. This is something I would like to add moving forward. The posts table include the id, feed text, chat text, datetime, user_id, and chat_id. The feed text is the text that is pulled just for the posts page and the profile page. The chat text is used just for the chat page. This is how those different pages can separate what is actually being shown. The chat_id gives the id of whoever you select to chat with on the chat page, and the user_id is whoever is logged in at that time.

### I wanted the web app to be simple to use. I also created a little logo on the top left to go with the name of the web app.