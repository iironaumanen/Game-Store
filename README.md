# WSD Project 2018

Project repository for WSD 2018 project

[Link to our initial project plan](project_plan.md)

#### Team members
* Lauri Anttila #665869
* Iiro Naumanen #605890
* Atte Viitanen #598088

## Project Documentation

#### Minimum functional requirements

All the projects minimum functional are met. A user can register to the site as a player and effortlessly change the account type to a developer in the developer panel. Player can buy games then play them. Player cannot play games that he doesn’t own. Player can also see his best scores from separate hi-scores page. Hi-scores can have many scores from one player. Hi-scores highlight players top scores (if any). If a players score is not in the hiscores it will show in the bottom. Player can also set himself as a developer from the developer page. As a developer, user can add games of his own. Developer can see sales records for his own games. Developer has a option to modify his games and change the price and the title of the game and even delete the game.

#### Authentication
Our evaluation: 200pts

We’re using Django’s own authentication system with a custom user model for the authentication. Django’s own authentication system ensures that the passwords provided by the user match and are secure enough, it also checks that username does not match with any existing ones. Users can have a player or developer account which have the same permissions, except developer can access developer area (adding, modifying games etc). A player account can convert to a developer account but not vice versa (intendedly, why would you want to “downgrade” your account). There is email authentication which uses the django console email backend. 

#### Basic player functionalities
Our evaluation: 300pts
		
Basic player functionalities are fulfilled. Players can buy and play games and the payments are secured using a checksum (generated in the backend) with the critical variables. Payment is handled by the given mockup payment service.  Players can only play games they have on their account (which they have purchased). User can find games in two different ways. There is a search functionality and also category system where games can be found easily. 
		
#### Basic developer functionalities
Our evaluation: 200pts

Developers have a developer view where they can add new games, see their existing games and modify or remove them. Anytime a game is added or modified the backend checks that the game belongs to the developer and that the input fields contain correctly formatted data. We’re using Django’s own model field validators as well as some regular expression whitelists. All of the security logic is in the back end so it should not be able to be bypassed.

#### Game/service interaction
Our evaluation: 200pts

Communication between the service and games has been implemented using postMessage (jquery/ajax). It is possible to save and load game states, submit your scores to high score lists and scale the iframe correctly. The service has full support for the messaging protocol specified in Game Developer Information section of the project assignment.

#### Quality of Work
Our evaluation: 100pts

We have consistent code styling guidelines set for the project. We are using pylint, eslint and validators for html / css to achieve a good consistent quality of code. We also properly utilize the MVT. We have mostly focused on black box style of testing which focuses on the functionality of elements rather than what’s inside. We’re using the site from the end user’s point of view to make sure the user experience is smooth and intuitive and simultaneously test all kinds of inputs to weed out any bugs in the service. We have also had a session with fellow students to test the site out.

#### Non-functional requirements
Our evaluation: 200pts

We have written proper and extensive project plans and final reports. However, our projects does not include documentation for the actual code aside from inline commentation. Teamwork has been excellent and an a significant majority of the code has been written in coding sessions with the entire team present. We had proper branching in the project. However, towards the end of the project we felt extensive branching was not necessary as the team had excellent communication due to working together physically.
 
#### Save/load and resolution feature
Our evaluation: 100pts

The game has full support for saving and loading as well as the whole protocol described in Game Developer Information.

#### 3rd party login
Our evaluation: 100pts

We have implemented OAuth (Gmail / Google account) signup / login which works as intended.

#### RESTful API
Our evaluation: 60pts

There is a REST API implemented, which is written around Django REST API framework but with our own serializers. The API supports listing games.

#### Own game
Our evaluation: 100pts

We implemented a simple box game that works nicely with all the service-game interaction methods described in the project description.

#### Mobile Friendly
Our evaluation: 50pts

The service has support for mobile / tablets. All of the functionality can be used with a touch screen. The support for multiple viewports was quite effortless to implement thanks to bootstrap.

#### Social media sharing
Our evaluation: 35pts

We implemented twitter sharing for games. It automatically fills out a tweet template with an appropriate text, a game link and a hashtag.

#### How did you divide the work between the team members - who did what?

Most of the time we worked together as a group in a meeting room so communication and task splitting was easy. This had a small caveat of reducing branching in the git repository. As we could communicate effectively together, there was no inherent need for specific branching as we made sure the areas we worked on wouldn’t cause merge conflicts. Programming wise we tried distributing tasks evenly where everyone had areas of responsibility such as the developer page or high score page.

At the start of the project we established a Trello board and used it quire effectively. But as we moved towards a more coding session -based approach to the project we deemed it unnecessary.

#### Additional features

As a fun extra side project, we implemented an about page for the project. It was mainly for playing around with javascript and testing things out. Feel free to check it out from the link in the page footer. Beware, it includes sound and itsn’t something you’d show to your grandma!

#### Overall impressions

The project was quite taxing but also really rewarding. Django offered many simple solutions to some initially hard problems. Doing this project with anything else than Django would have been really hard and would have required much more skill and man hours.

The most difficult things during the course of the project was getting our custom user model to function properly with django.

We felt that we were most successful in getting the whole website to feel consistent to the user and look like a decent game store. We got things looking and working in a very consistent-looking manner by properly utilizing the MVT. All in all iIt was a fun ride and we feel like we exceeded even our own expectations.

## Instructions

The project can be run in a local developments environment just like any typical django project with manage.py runserver. Required packages must first be installed from the requirements.txt file:
```bash
 pip install -r requirements.txt
 ```

However, the social authorization API keys in settings.py use environment variable hooks in order to hide them and obey Google’s guidelines.

The project is up on heroku at:
[Link to the page](http://boiling-woodland-71071.herokuapp.com)

To aid in assessment of the instance running in Heroku, we have prepared the following normal and administrator users:
> testuser1:testpassword <br />
> testuser2:testpassword <br />
> testadmin1:testpassword <br />
> testadmin2:testpassword <br />