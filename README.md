# arenaquiz
Quizbowl Scorekeeping

Arenaquiz is a web application that allows its users to keep track of the scores of quizbowl games. On the front end, it uses HTML/CSS/Javascript, while on the back end it uses Flask and SQL.

## 1. Installation Instructions
### 1.1 Using the CS50 IDE
Arenaquiz is run just like any other Flask app from the CS50 IDE. The CS50 IDE already has all the necessary modules installed, so all that is needed is to download the code as a .zip file, upload it to CS50 IDE, unzip it, and navigate to the directory containing the code. There is one caveat, however: the Flask driver file is named `app.py`, as this is the default setting for non-CS50-IDE environments, so you will need to run the following command:
`$ export FLASK_APP=app.py`
Once inside the `/arenaquiz` directory, simply run the following command:
`$ flask run`
and the application will start.

To visit the website, simply follow the link outputted by the CS50 IDE.

### 1.2 Command Line
Download the Arenaquiz code and unzip it. In your command line, navigate to the Arenaquiz directory.
#### 1.2.1 (Optional) Virtual Environment
Instructions adapted from [Flask's website](https://flask.palletsprojects.com/en/1.1.x/installation/).
Once in the Arenaquiz directory, you may wish to create a virtual environment to run Arenaquiz. Python versions 3 and above automatically include the `venv` module. To create the virtual environment, simply execute the following (for Unix-based systems):
`$ python3 -m venv venv`

To activate the virtual environment, execute:
`$ . venv/bin/activate`

#### 1.2.2 Install Modules
Ensure that you have the required modules installed, as listed in `requirements.txt`. To install, execute
```
$ pip install flask
$ pip install flask-session
$ pip install cs50
$ pip install requests
```

Once these modules are installed, you are ready! Simply execute
`$ flask run`.

By default, the website is viewable in your browser at localhost:5000.

## 2 Quizbowl Overview

The following information may be helpful to someone who has never played quizbowl before:

Quizbowl is a fast-paced, buzzer-based knowledge competition played by teams throughout the world. Students are read questions on a variety of academic subjects including history, literature, science, fine arts, and more, and buzz in to score points for their team.

A typical round of quizbowl consists of tossups and bonuses.

*Tossup*
A question read to both teams. Each tossup has multiple clues, ordered from hardest to easiest. A player can buzz in whenever they think they know the answer. If a player answers a tossup correctly, their team is awarded a bonus.
Bonus
Each bonus consists of three parts worth 10 points each. After each part is read, the team answering the bonus has 5 seconds to come up with an answer.

There are some additional terms for buzzing in on a tossup:

*Power*
If a player correctly buzzes in sufficiently early during a tossup (i.e. while the harder clues are being read), they will earn 15 points as opposed to the usual 10.
*Neg*
If a player buzzes in incorrectly while a tossup is being read, their team loses 5 points and is locked out for the rest of the tossup. Note that there is no penalty for buzzing in after the tossup has been read in full, or if the other team has already negged.

Finally, some common terms used in quizbowl statistics:

*PPG*
Points Per Game. Used to keep track of the number of (tossup) points a player scored in a game. Can be used to compare players of a team when averaged over several games.
*PPB*
Points Per Bonus. Keeps track of the average number of points a team recieves on a given bonus. Used to compare the strengths of teams, since bonuses are less variable than tossups.

## 3 Site Overview
Users require an account to view the site. If a user tries to view the site without being logged in they will be redirected to the login page. If a user does not have an account, they can visit the "Register" page to create one. Once they create an account by entering a username and password, they can view the site and will be redirected to the index page.

For information on quizbowl terminology such as tossups and bonuses, as well as the exact rules of scoring, please see the information on the index page (`/`).

##### Features common to every page: 
Every page has the navbar visible, which contains links to several of the site's pages. Additionally, the site also makes use of Flask's "flash" messages to display errors and alerts to the user.

### 3.1 Pages
* Home (`/`): The index page. Contains a greeting, welcoming the user to the site. Additionally, contains an overview of what quizbowl is and how it is scored. If a game is in progress, a link at the top of the page will prompt the user to return to their game in progress.
* Register (`/register`): Register a new user as described above.
* Login (`/login`): Log an existing user in.
* Logout (`/logout`): Log the current user out.
* Change Password (`/change_password`): Changes the user's password to a new password, so long as they supply their existing password.
* Teams (`/teams`): A page where a user can choose a team from their saved teams to view that team's roster, or add a new team. A team can have between 1 and 8 players. Once a team is selected, the user is redirected to `view_team`.
* `/view_team`: A page that displays the team name and roster of a given team_id, supplied via the GET request argument of a URL. A team can only be viewed by the user that created it.
* `/add_team`: A page where the user can create a new team. To create a new team, the user must supply a team name and between 1 and 8 player names.
* New Game (`/new_game`): A page where the user can set up a new game. The user must have at least 2 saved teams to create a game. The user cannot select the same team for both teams. Once the game is created, the user is redirected to `/game`.

#### 3.1.1 Game
* Game (`/game`): This page is where most of the action happens. Here, the user is presented with a game scoring interface. At the top, the game's title is presented, containing the game's title, "X vs. Y", where X and Y are the team names. The current tossup (question) number is also displayed. Below is 2 sets of buttons containing the names of the players on each team. Each set of buttons is labeled with the team's name and its score. Below these are buttons to Submit the tossup and Reset the tossup, and finally, a scoresheet containing the current scores of the match.
* The score of a tossup is inputted by the buttons. To input the score for a player, simply click on their name. Buttons with values "15", "10", and "-5" will appear under the player's name, indicating the possible point values that the player can score. (For more information on the scoring rules of quizbowl, see section 2.) To indicate the player's score, whether they power, ten, or neg the tossup, simply click on the corresponding button. The webpage will dynamically update to reflect what states are and are not possible atfer this, according to some rules:
  * Once a player is clicked, the rest of their team becomes disabled. This is because only one player per team can buzz in per tossup.
  * Once a player's score is selected, their other score buttons become disabled, to better indicate what score is being entered.
  * If a player negs, the neg buttons of the other team become disabled. This is because there is no score penalty for buzzing incorrectly if the other team has already negged.
  * If a player powers or tens, the other team becomes disabled. Only one player can power or ten any given tossup.
* If a player powers or tens the tossup, three bonus buttons will appear. These buttons can be toggled to indicate how many of the three bonus parts the player's team answered correctly.
* Once the user hits Submit and enters the score, the scoresheet is updated immediately to reflect the new score. The teams' scores, PPGs, PPBs, and subtotals are all calculated and appear in the scoresheet.
* The site will prompt the user to stop once 20 tossups have been read and there is not a tie, but scores can continue to be entered afterwards (this is to allow for situations like scrimmages or nonstandard games.)

Additional pages:
* Games (`/games`): A page where a user can choose a game from their saved games to view that game's scoresheet. Once a game is selected, the user is redirected to `view_game`. There is also a button to create a new game.
* `view_game`: A page that displays the game name, scores, and scoresheet of a given game_id, supplied via the GET request argument of a URL. A game can only be viewed by the user that created it.

## 4 Conclusion

This site was made for CS50's final project. I hope it may someday find use within the quizbowl community. Thank your for using my site!

