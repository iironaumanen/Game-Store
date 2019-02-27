# WSD Project 2018

Project repository for WSD 2018 project

#### Team members
* Lauri Anttila
* Iiro Naumanen 
* Atte Viitanen 

## Project Plan

### Introduction

We're developing an online game store for JavaScript games.
There are two types of users: developers and players.
Players can buy games and play the purchased games online.
Developers can add their games to the service and set a price for it.

The project wil be developed using JavaScript and HTML / CSS for the front-end
and Django for the back-end

### Features and implementation

#### Basic Features

###### Authentication
Django comes with a user authentication system.
It handles user accounts, groups, permissions and cookie-based user sessions.
We will be using Django Auth for user authentication and managing login sessions.
Django auth can handle login, logout and registering. We have two types of users: developers and players.

###### Basic Player Functionalities
Games can be bought. We will be using the mockup payment service provided by the course.
The game can be played if user is authenticated and owns the game. We match the user ID with the owned games in the database.

The games are presented in categories and name based search.

###### Basic Developer Functionalities
A developer view where developers can add games based on URL and set a price.
The games can be modified and removed in the developer view.
Developer view can be accessed if you're logged in as a developer.

Game information and statistics are stored on our server.
These can be exported as reports.
Security is handled by Django auth. Developer view shows relevant content based on user ID.

###### Game / Service Interaction
The game communicates with the back-end for saving the score and updating global highscores. Score is linked to user ID.
The score is sent via postMessage to the parent window which saves the data to the DB. Our front-end communicates with the game.

###### Quality of Work
Code is commented according to our own specified commenting practice:
<blockquote>
- Comments cover the main parts of the functions/blocks <br />
- Comments cover variable explanations <br />
- Comments cover return explanations (if present)
</blockquote>

We will be peer reviewing the code style, commenting and functionality which includes DRY-principle and MVT-separation.
Outside personnel will test the user experience of our application. There will be some unit testing for the code.

###### Non-functional requirements and work practices
We're using version.aalto.fi / git for version control. Shared files and documents are in a shared Google Drive folder.
Trello is used for task management and tracking the progress.

We will be writing the documentation for the project alongside the project when new features are being implemented.

##### Additional features

_We are committed to implementing all the additional features, with an emphasis on the following:_

###### REST API
We will be running a REST API endpoint for the database queries and communication with Django.

###### Save / Load
Game states are saved in the database and communicated using JSON. Games can be saved and loaded this way.
Communication with the database happens with the REST API endpoint.
Communication inside the front-end happens via postMessages and the given message protocol in A+.

###### Social Media Sharing
The app has Twitter sharing feature implemented with Twitter Cards.

## Views
The service has at least the following basic views:
###### Frontpage
- Shows a couple of featured or recently added games. Acts as a central hub that has links to the other views.
###### Game view
- Main view for playing games. Shows the game and hiscores for it. Attempting to access this without having bought the game takes the user to the appropriate purhase view.
###### Purchase view
- The view that comes up when a game purchase is attempted. Shows relevant purchase information.
###### Hiscore view
- A page that enables users to look up hiscore listings for any game. Shows the scores on a table.
###### Developer view
- A game management view for game developers/submitters. Allows adding, deleting and modifying games.
###### About view
- Shows some relevant information about the service and the authors.

## Model layout
![Alt text](misc/graph.jpeg?raw=true "Title") <br />
*Basic model/database layout.*

###### Game
Respresents a single game submitted to the service.
> field title: models.CharField(max_length=30) <br />
> field price: models.IntegerField() <br />
> field submitter: models.ForeignKey(User) <br />

###### Category
Respresents a single game category. Has a many-to-many relation to Game.
> field name: models.CharField(max_length=30) <br />
> field games: models.ManyToManyField(Game) <br />

###### User
Represents a single game category. Uses the [pre-existing Django User model](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/).

###### Score
Respresents a single score entry by a user in a game.
> field score: models.IntegerField() <br />
> field submitter: models.ForeignKey(User) <br />
> field game: models.ForeignKey(Game) <br />

###### Transaction
Respresents a single game purchase made by a user.
> field date: models.DateTimeField() <br />
> field buyer: models.ForeignKey(User) <br />
> field game: models.ForeignKey(Game) <br />

## Work practices
The project will be developed almost exclusively in group sessions. As Django is relatively new to all team members, all issues will be easier to tackle as a group and everyone can learn as they work.

The meetings will take place at least two times a week. They will borrow practices the team members have learned from the Software Project course CS-C2130. Workloads will be divided as equally as possibly while making sure everyone gets to work on all aspects of the project.

Trello is used for task management and tracking the progress and Telegram for more direct communication.

## Project timeline
The overall proposed timeline for implementation order (for now) is as follows:

|  Week  | Objectives                                                       |
|--------|-------------------------------------------------------------|
| Week 1 | Django views and models                                     |
| Week 2 | Basic player functionalities, REST api, and payment service |
| Week 3 | Basic developer functionalities and authentication          |
| Week 4 | Our own game and hiscores                                   |
| Week 5 | Social media sharing and 3rd party login                    |
| Week 6 | Fixing and adding functionalities                           |
| Week 7 | Documenting and styling                                     |
