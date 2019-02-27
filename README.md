# Game Store

[Link to our initial project plan](project_plan.md)

#### This project was done with the help of these guys
[Iiro Naumanen (Me)](https://github.com/iironaumanen)<br />
[Lauri Anttila](https://github.com/teekkari)<br />
[Atte Viitanen](https://github.com/AttK0)

## Description of the software

This is a school project done as a part of the web software development course.
Game Store is a website where a user can buy and and play games. User can also become a developer and then publish his own games on the site. Buying of games is handled by a mockup payment system (provided by the course). User can save and load his current game states. Game and the game service communicate using window.postMessage. User can view his top scores in the hiscores page. Using Tweet button user can share his favourite games in Twitter, since it fills out a tweet template with an appropriate text, a game link and a hashtag. Google OAuth implementation allows user to login and register with his google account credentials.

Game Store is built using Django and its frameworks. RESTful API is implemented with Django REST framework. Game Store is using Bootstrap as a CSS library. There is also some JavaScript code that is used mostly in the About Us page. Website is very mobile friendly.

## Instructions

The project can be run in a local developments environment just like any typical django project with manage.py runserver. Required packages must first be installed from the requirements.txt file:
```bash
 pip install -r requirements.txt
 ```

However, the social authorization API keys in settings.py use environment variable hooks in order to hide them and obey Google’s guidelines.

## Screenshot
#### More screenshots are found in the [screenshots folder](https://github.com/iironaumanen/Game-Store/tree/master/screenshots)

![Image of the home page](https://github.com/iironaumanen/Game-Store/blob/master/screenshots/Screenshot%202019-02-27%20at%2012.37.54.png)

