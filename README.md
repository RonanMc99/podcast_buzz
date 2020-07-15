# PodcastBuzz

![PCbuzz-screenshot1](https://user-images.githubusercontent.com/51950969/87582896-fbe8ef00-c6d2-11ea-91b7-cefc38646c32.png)

## Introduction

PodcastBuzz allows users to search for and comment on their favourite podcast episodes.

I am a big podcast listener and wanted to create an app that would allow me to listen to podcasts and make notes as I go.  While listening, I often come across great ideas, concepts and links that I might like to follow up on later.  Thus, the idea for PodcastBuzz was born.

I then realised that by adding some simple user management, different users could add their own notes, links, comments and reviews, and so share their ideas and insights with others.

The app is based on Python with Flask, integrates with an external API to get podcast data, and uses a MongoDB (NoSQL) database to persist the data.   To read more about my process for developing the app, see the design section below.

### Technologies

Backend: Python, Flask, MongoDB. REST API. 

Frontend: HTML / CSS / Jquery / Bootstrap 4

Deployment: Heroku

## Prerequisites

* Python 3.8.2.
* Flask version 1.1.2
* MongoDB 3.6 or above.  Either a local installation or a cloud-based instance of MongoDB Atlas is suitable
* Additional package requirements are provided in the requirements.txt file.  See below for installation
* The application uses the ListenNotes API to get podcast information.  You must [request your own API key here](https://www.listennotes.com/api/) 

## Installation

1. Clone the repositary to your installation location

2. Create a virtual environment for Python using virtualenv 

    ```
    pip install virtualenv

    virtualenv myvenv --python=python3.8
    ```

3. Activate the virtualenv using the command:

    ```
    source myvenv/bin/activate
    ```

4. Install requirements using the command:

    ```
    pip3 install -r requirements.txt
    ```

5.  Configure variables required by the application (example below)

	```
	SECRET_KEY="afjdhafds758efdskj38srfdafda9f2er2qh" 	# required by flask to cryptographically sign cookies
	MONGO_URI="mongodb://localhost:27017/podcastdb" 	# location of your MongoDB database
	X_LISTENAPI_KEY="thisismysecretkeyfromListenNotes" 	# ListenNotes API key
	```
6. Run the server
	```
	flask run # execute run.py
	```

7. Navigate to [http://localhost:5000](http://localhost:5000)

### Deployment on Heroku

1. Signup for [Heroku](https://signup.heroku.com/)

2. Sign in

3. Download the [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true)

4. Launch the CLI using the command ```heroku login```

5. Log in by following the prompts and entering your Heroku credentials as required

6. Prepare a local git repository which will be delpoyed to Heroku using the command:
	```
	git clone https://github.com/RonanMc99/podcast_buzz.git
	```
7. Change into this directory.  Your local git repository contains a runtime.txt file which specifies the python version that Heroku will use.  There is also a requirements.txt which will be used to install the Python dependancies.  Finally, the 'procfile' will tell Heroku how to launch the application

8. Create your Heroku app ```heroku create <your-app-name-here>```  This creates a git remote called 'Heroku' which is associated with the local git repository

9. Push your code to the Heroku remote ```git push heroku master```

10. Configure the configuration variables by opening Heroku in the browser, finding your app, and opening the 'settings' tab.  Expand the 'config vars' section and add your variables as shown:

![heroku_config](https://user-images.githubusercontent.com/51950969/87567338-16639e00-c6bc-11ea-932e-bda2f0dbf076.png)

11. Open your app by clicking the 'Open app' button.  Your app should look similar to the below:

![CleanShot 2020-07-15 at 10 57 49](https://user-images.githubusercontent.com/51950969/87567544-46ab3c80-c6bc-11ea-8b89-ad3535c33563.png)

12. If you have issues, begin by checking the heroku logs:

![CleanShot 2020-07-15 at 16 58 15](https://user-images.githubusercontent.com/51950969/87567669-7a866200-c6bc-11ea-9b5f-2530a320ec5e.png)

### Directory Structure

``` 
# tree
.
├── .flaskenv
├── Procfile
├── README.md
├── config.py
├── podcastbuzz
│   ├── forms.py
│   ├── listen_notes.py
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   ├── img
│   │   │   ├── favicon.ico
│   │   │   └── podcast-buzz.png
│   │   ├── js
│   │   │   └── main.js
│   │   └── vendor
│   │       ├── bootstrap
│   │       │   ├── css
│   │       │   │   ├── bootstrap.min.css
│   │       │   │   └── bootstrap.min.css.map
│   │       │   └── js
│   │       │       ├── bootstrap.bundle.min.js
│   │       │       ├── bootstrap.bundle.min.js.map
│   │       │       └── popper.min.js
│   │       └── jquery
│   │           └── jquery.min.js
│   └── templates
│       ├── base.html
│       ├── home.html
│       ├── logon.html
│       ├── podcast.html
│       └── register.html
├── requirements.txt
├── run.py
├── runtime.txt
├── tests.py
```

## Design

### User Stories
Initial design considerations were based around some simple user stories outlining the functionality required:

* Users should be able to logon to the app with unique credentials, so that their data persists between sessions

* The user registration process should be as simple as possible

* The user should be presented with a form which they can use to search for their favourite podcasts, podcast episodes or by keyword

* From search results, the user should be able to access further information about the podcast, such as the podcast's title, description, an image thumbnail, and a link to listen to the podcast audio

* On the podcast page, the user should be able to add a comment or note.  This comment must persist between sessions

* The user should be able to edit or delete previously added comments

* Users cannot edit or delete the comments of other users

* The user interface must be fully functional and suitable for use on mobile, tablet and desktop devices

Based on these considerations, some high-level principles were followed for this initial release:

1. The design will follow a mobile-first principle to ensure a good UX on all devices, with a priority on the mobile experience
2. Strong or complex authentication is not necessary, and a simple email address / hashed-password combination is sufficient
3. For this first release, a very simple, 'no-frills' UI design will be created in Bootstrap
4. An external API will provide podcast data, but to optimise database writes, a given podcast will only be persisted after it has been selected (as opposed to writing all podcasts matching search criteria)

### Database Design Considerations:
1. The database schema will be as simple as possible without complex relationships or data constraints.  For ease of use, a simple NoSQL database (MongoDB) will be used. This maximises performance and provides flexibilty for future development
2. There will be three collections - one each for users, podcasts and comments.  User documents have a one-to-many relationship with comments, as each user may have commented on multiple podcasts.  By placing the comments in a separate collection, the details may be accessed as stand-alone entities, providing most flexibility for adding new application features later

### Database Schema
![database_schema 001](https://user-images.githubusercontent.com/51950969/87563214-dfd75480-c6b6-11ea-94b3-8ab196f94efc.jpeg)

### Front-End Design

As stated previously, the main focus for this release is to create a simple, functional design with minimal F.E. interactions.  Using the user stories and design considerations above, a simple mockup was created using Figma:

![PCbuzz_design](https://user-images.githubusercontent.com/51950969/87568538-b66df700-c6bd-11ea-8071-1bdd15541296.png)

Additionally, a colour palette was chosen to provide consistency throughout the application.  This palette was converted to CSS variables for use within the app (podcastbuzz/static/css/style.css)

![pcbuzz_colors](https://user-images.githubusercontent.com/51950969/87568893-4318b500-c6be-11ea-9b22-600c508efb58.png)

The design focussed on readability, making good use of whitespace, visual hierarchy, alignment, contrast and scale in order that the (considerable amount of) information related to the podcasts could be effectively conveyed and provide a good user experience.

![PCBuzz-Screenshot 2](https://user-images.githubusercontent.com/51950969/87582971-276bd980-c6d3-11ea-95d4-295f7e582a77.png)

## Testing
Testing for this app is by means of a combination of simple automated tests and manual QA.  The automated tests allow for quick identification of errors, while the manual QA provided confidence of extended application functionality which was problematical to automate given the use of an external API and Jquery-based search.  Future releases will aim to provide fully automated testing with complete coverage.

[Manual QA tests and results can be viewed here](https://docs.google.com/spreadsheets/d/1zzRLS54mid4wzM7i52V12LIKrbLTku_aVzcovMD8ph0/edit?usp=sharing)

## Future Improvements

Next steps for this application will be to add some additional features:

1. Add a list of the 'most commented' podcasts to be presented beneath the search box for logged in users.  The information may be obtained using a search query similar to the following:

```
recent_comments = db.comments.find({}, {podcast_id:1, _id:0}).limit(1).sort({$natural:1}).limit(5)
```

2. Further develop the front-end design to make it more visually appealing, perhaps adding some social sharing buttons

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to provide tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)