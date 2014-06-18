Movie Recommendations
=====================

Web applications for showing movie recommendations to users based on Collaborative Filtering Algorithm. 
The project was done in just couple of days for Student Programming competition Best Code Challenge. 
We coded our custom algorithm for suggesting movies to users, script for calculating accuracy of algorithm and web app for showing movies list, 
movie details and movie suggestions on website.

The project consists of two "main" parts:
Web application
Other scripts (management commands)

Management commands folder consists of:
movies.csv
prefs.csv (list of user_id, movie_id, rating for testing purposes)
populate_movies.py and populate_prefs.py for populating tables with values from .csv files
algorithm_tester.py script for calculating accuracy of implemented algorithm (uses training set from prefs.csv)

Besides usual django files, web application uses script recommendation_algorithm.py.
recommendation_algorithm.py returns 10 recommended movies for specific user.



