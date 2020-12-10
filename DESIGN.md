# 1 Overview
Arenaquiz is, at its core, a Flask web application. On the front end, it uses HTML templates (with templating provided by Jinja), CSS for styling, and JavaScript for interactivity. On the back end, Flask (a Python-based web framework) is used in conjunction with a SQL database to store data.

These tools were chosen for several reasons. One major reason was that these tools were already familiar to me after Problem Set 9: Finance, but I wanted to develop my proficiency in them further, especially with regard to web development. I looked into using React for the front end, but found it difficult to implement. React's data flow model flows from parent element to child element, but I often found myself wanting to have the data flow in the other direction. For this reason, I opted for plain Javascript to fit my needs and maintain interactivity. For the back end, SQL is the premier choice for storing data, and the Flask framework met my needs well.

# 2 Site
## 2.1 Front End
Arenaquiz follows the classic web design model we learned in CS50. If the user needs to submit data to a webpage, a POST request is used, whereas if a user simply needs to view the content of a webpage, a GET request is issued. There are many elements on pages of the site that require modularity: the site needs to display different data and elements depending on the game state and user session. Jinja templates accomplish this goal very well. Finally, the power of Flask allows certain important data to persist between pages through the use of cookies. Data stored in the session cookie includes the user's user_id, the current game_id, and the current tossup_num.

For the game page, the most important page, I had interactivity in mind. I chose to use the UI flow of buttons, rather than simple selections from a dropdown, because I wanted the page to look more interesting and interactive. Using JavaScript to dynamically show/hide/enable/disable the buttons was challenging, but the end result is close to the user experience I wanted: the colorful buttons provide an easy way to visually see the scores being inputted, and let users easily how each click affects the state of the game. An HTML table was the ideal choice for formatting the scoresheet through the use of table rows.

## 2.2 Back End
Arenaquiz uses Flask and SQL to manage its back end. The Flask model provides an easy, modular, efficient way to direct users between pages and handle web requests. Additionally, SQL interacts nicely with Python, and was the natural choice for storing data. The main decision for the back end code came to how to handle and deliver the gamedata to the webpage. My solution was to handle this all on the back end using the function `get_gamedata()`. This function is modular because it does not require any parameters other than the desired game_id and the user's session cookie. I chose to do all the score calculation on the back end using `get_gamedata()` because Python's dictionary/list manipulation is quite good, it would be difficult to perform these calculations on the data after it reaches the front end due to it being separated into table rows, and it allows for the server to maintain a "source of truth". This also allowed me to implement viewing saved games using the existing `get_gamedata()` code.

# 3 Conclusion
I made these design decisions to the best of my ability, and I hope you enjoy the website.
