

(the)

# UPSET QUARTET

Ivan, Tahmid, Tyler and Ethan							       [click here\!](https://docs.google.com/document/d/1DxpLeQ4nNpbJn5CAcujtiStITcG6vjjoLYJCf5-QXS0/edit?usp=sharing)  
Project Manager: Ivan  
TNPG: Upset Quartet       
SoftDev  
P00: Full-Quick {PIVOT}  
TARGET SHIP DATE: 2026-11-18  
Time Spent: 4 hrs

---

**Team Roster**

| Name | Email | Primary Role | Secondary Role |
| ----- | ----- | ----- | ----- |
| Ivan Chan | ivanc200@nycstudents.net | Project Manager | Story Engine & Page Handler |
| Tahmid Uddin | tahmidu3@nycstudents.net | Authentication | Sessions |
| Tyler Lin | tylerl154@nycstudents.net | SQLite3 Database Architect | HTML |
| Ethan Chang | ethanc284@nycstudents.net | Documentation | CSS |

---

# 

# **Program Components and Site Map**

***login.html***

- The default page the user is redirected to if not logged in.   
- If not logged in, users can only access this site and signup.html  
- Prompts user to input username and password.  
- Redirects to /user/\[username\].html if successfully logged in.

***signup.html*** 

- Prompts user to input a new username and the same password twice  
- Redirects to /user/\[username\].html if successfully logged up.

***/user/\[username\].html***

- Each user’s unique profile page.   
- Displays username, four contributed stories, and four randomized stories.  
- Users should not be able to view other users’ profile pages (stretch feature).

***/page/\[story\].html***

- Every story is in this format.   
- Users can choose to edit the story here.  
  - Editing confirmation popup (stretch feature).

***edit.html***

- Page to create a story (just an edit page with empty fields).   
- After publishing, create paths */page/\[story\].html* & */edit/\[story\].html*.

***/edit/\[story\].html*** 

- When editing a story, only the most recent contributor’s edit is visible.   
- Once the user stops editing, regardless if they selected *cancel* or *update*, they cannot edit the story again afterwards. 

***index.html***

- Displays all stories with clickable hyperlink & search bar.

---

**Possible Routing:**  
**Logged-Out User**  
login.html \-\> signup.html \-\> /user/\[username\].html  
or login.html \-\> login.html \-\> /user/\[username\].html  
**Logged-In User**  
/user/\[username\].html \-\> index.html \-\> /page/\[story\].html \-\> edit/\[page\].html \-\> /page/\[story\].html \-\> /user/\[username\].html \-\> edit.html (create story) \-\> /page/\[story\].html \-\> /user/\[username\].html \-\> logout.html \-\> login.html

---

# **Component Relationships**

**Scenario I: The user creates a web page**

1) On the local client, the user hits the submit button. This sends a POST request to the Flask web server.   
2) Flask requests the necessary information from a SQLite3 table, like page title. However, since the user is creating a page, this step isn’t needed unlike when the user is updating the page.  
3) The table returns data back to Flask. Thereafter, it renders templates using Jinja, compiles the HTML, attaches the CSS.

**Scenario II: The user creates an account.**

1) On the local client, the user hits submit. This sends a POST request to the Flask web server.  
2) Flask checks the client’s information, primarily by their cookie, to see if they are logged in. If so, then Flask tries to redirect the user to their profile page. Otherwise, Flask requests the necessary information from a SQLite3 table, to check if the account creation is valid. If the username is already taken, a field isn’t filled out, or there are no matching passwords, then an error message is displayed. Then, the Flask server should append the user information to the necessary table.  
3) Once the information has been stored, Flask then creates a cookie, logging the user into their new account. The user is redirected to their profile page.

**Scenario III: The user adds onto an existing story.**

1) Flask reads the data associated with the current page and checks if the user has previous edits  
2) If not, the user can add onto the story. Otherwise, they can only view the story.  
3) Added content will be sanitized of any SQLite3 keywords before being appended to the story content.   
4) The user's username will be added to a list in Flask attached to the story. 

**Scenario IV: The user searches for every page in the index.**  
Beyond reading every page in the SQLite3 table and storing it in a list to be displayed, if the user tries to search for a certain character (“a”), what results should be listed foremost? Should there be customizable ways to sort the pages you read?

**Summary/Generalization of Processes**

1) The user requests an operation to be handled.  
2) Flask confirms that the user has the capability to do so  
3) Flask requests/modifies information from the SQLite3 table.  
4) Flask modifies/redirects/creates a web page.  
5) The user is able to see the changes made.

---

# 

**Database Organization**

| *users* |  |  |
| ----- | :---- | :---- |
| integer | id | PK |
| string | username |  |
| string | password |  |

| *pages* |  |  |
| ----- | :---- | :---- |
| integer | id | PK |
| string | title |  |
| string | text |  |
| integer | creator\_id |  |
| integer | created\_at |  |

| *pages\_history* |  |  |
| ----- | :---- | :---- |
| integer | id |  |
| integer | edit\_id | PK |
| string | last\_editor\_id |  |
| integer | last\_update |  |
| string | text\_added |  |
| integer | created\_at |  |

*\**NOTE*: To prevent multiple people from pushing edits at the same time, compare the original edit\_id to the current edit\_id. If they are the same, nobody pushed changes in the time the edit was made. If they are not the same, then the text displayed being added onto must be updated before anyone else can push their edits to prevent edit conflicts.* 

*A simple*  
*diagram showing*  
*the cardinality*  
*of each table.*

*Please do not*  
*fret over whether*  
*the symbol should*  
*be an asterisk*  
*or the letter N.*

# ---

# 

# **Security**

Queries are parameterised to have SQLite treat the input as pure data rather than code, instead of using Python f-strings.  
Rather than having Flask doing this:  
cursor.execute(f"SELECT \* FROM users WHERE name \= '{user\_input}'")     
Where the entire statement being executed will be treated as valid SQL code, meaning that Flask won’t be able to know what’s server-side SQL code and what’s user-submitted SQL code.

We will do this:  
	cursor.execute("SELECT \* FROM users WHERE name \= ?", (user\_input,))  
Where SQLite takes the SQL statement and compiles it separately and only uses the user\_input at execution time, and thus can never be parsed as SQL code. 

\**NOTE*: SECRET\_KEY should be a randomly generated hex token seeded at the time of the start of server runtime.  
---

# **Task Breakdown/Team Ownership**

# **Person 1:** Lin, Tyler (backup: Uddin, Tahmid)

- SQLite3 Database Architect   
- Responsible for constructing and managing the database

**Person 2:** Uddin, Tahmid (backup: Lin, Tyler)

- Authentication and Session Master \| SQLite3 Database Assistant  
- Responsible for the integrity of the database, as well as helping the Database Architect. 

**Person 3:** Chan, Ivan (backup: Chang, Ethan)

- Story Engine and Page Handler   
- Write the main engine for Flask/Python/Jinja setup and help jumpstart the code for SQLite3 tables and design for each page.

**Person 4:** Chang, Ethan (backup: Chan, Ivan)

- Documentation and Front-End Developer  
- Make sure the repository is up-to-date and work on CSS/front end development.

---

# **Component Relationship Diagram & Routing Diagram**

