"""Based on project from Alex Olteanu, content author at dataquest
   link: https://www.dataquest.io/blog/data-science-project-fandango/
   Also, derived from the research done by Walt Hickey in 2015
   Link: https://github.com/fivethirtyeight/data/tree/master/fandango"""

"""Goal: is to determine whether there’s any difference between Fandango’s ratings for popular movies
   in 2015 and Fandango’s ratings for popular movies in 2016. """



""" If you what to use a hard copy of the CSV files you can retireve the files"""
#Retrieve datasets
import urllib.request
# Movie ratings from Walt Hickey
fandango_comparison_file = "https://raw.githubusercontent.com/fivethirtyeight/data/master/fandango/fandango_score_comparison.csv"
# urllib.request.urlretrieve(fandango_comparison_file, "fandango_score_comparison.csv")

# Movie Ratings from 2016 & 2017
movie_ratings = "https://raw.githubusercontent.com/mircealex/Movie_ratings_2016_17/master/movie_ratings_16_17.csv"
# urllib.request.urlretrieve(movie_ratings, "movie_ratings_16_17.csv")


"""Read in files directly from source"""
# Read two samples & view frist 3 films
import pandas as pd
fandango_comparison_url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/fandango/fandango_score_comparison.csv"
movie_ratings_url = "https://raw.githubusercontent.com/mircealex/Movie_ratings_2016_17/master/movie_ratings_16_17.csv"
pd.options.display.max_columns = 100  # Avoid having displayed truncated output
previous = pd.read_csv(fandango_comparison_url)
after = pd.read_csv(movie_ratings_url)
# print(previous.head(3))
# print(after.head(3))


# Isolate Columns only related to Fandago & make a it a copy to avoid 'SettingWithCopyWarning'
fandango_previous = previous[['FILM', 'Fandango_Stars', 'Fandango_Ratingvalue', 'Fandango_votes','Fandango_Difference']].copy()
fandango_after = after[['movie', 'year', 'fandango']].copy()
# print(fandango_previous.head(3))
# print(fandango_after.head(3))


"""Populations of interest include:
   1. All Fandango's ratings for popular movies released in 2015
   2. All Fandango's ratings for popular movies released in 2016

   Popular = 30 or more fan ratings & rating of 3 or higher.

   Although fandango_after dataset does have a popularity column
   it does not show the number of fan ratings used to decided if
   a movie was popular.  We will need to confirm if the dataset
   is representative of of the population (movies w/ over 30 fan
   ratings.

   To test if it is representantve or not we will randomly sample
   10 movies and then check the number of fan ratings.

   ***Important note: as of Febaruary 2017, Fandango acquired
   	  Rotten Tomatoes. In May of 2019 Rotten Tomatoes changed its
   	  score methodology for movies: The site’s standard user rating
   	  will now reflect only moviegoers who can prove they’ve bought
   	  a ticket to see it in a theater. Since, Rotten Tomatoes is owned
   	  by Fandango.  To check the number of fan ratings
   	  and confirm or not confirm that the dataset is representative
   	  in September 2019, the variable "User Ratings" will be used from
   	  the rotten tomatoes website."""

# Print Random same to test for representivity of the after dataset
# print(fandango_after.sample(10, random_state = 1))


# As of September 2019, the foloowing are the user ratings found:
"""
Mechanic - Resurrection: Audiance rating -  25566
Warcarft: Audiance rating - 63226
Max Steel: Audiance rating - 6808
Me Before You: Audiance rating - 30465
Fantastic Beasts and Where to Find Them: Audiance rating - 87439
Cell: Audiance rating - 3774
Genius: Audiance rating - 2871
Sully: Audiance rating - 48287
A Hologram for the King: Audiance rating - 10182
Captain America: Civil War: Audiance rating - 178900
"""

# 100% of the movies are popular according to the criteria thus representiative.

"""Before moving foraward we need to confrim that the previous data set
   does not contain any un-popular movies i.e. < 30 votes.  Zero unpopular
   moive were found.  """
# print(sum(fandango_previous['Fandango_votes'] < 30))



"""For the purposes of the project we need to isolate movies released
in 2015 and 2016. Thais is if any other years are present."""
fandango_previous['Year'] = fandango_previous['FILM'].str[-5:-1]


"""2015"""
# Check to see if there are any years other than 2015
# print(fandango_previous['Year'].value_counts())
# Isolate 2015 year movies
fandango_2015 = fandango_previous[fandango_previous['Year'] == '2015'].copy()
# Confirm isolation completed correctly
# print(fandango_2015['Year'].value_counts())

"""2016"""
# Check to see if there are any years other than 2016
# print(fandango_after['year'].value_counts())
# Isolate 2016 year movies
fandango_2016 = fandango_after[fandango_after['year'] == 2016].copy()
# Confirm isolation completed correctly
# print(fandango_2016['year'].value_counts())



"""The purpose of this project was to investigate where there was any difference in
   in the ratings from 2015 and 2016. Below we will compare the distibutions for the two samples. """

import matplotlib.pyplot as plt
from numpy import arange
import matplotlib as mpl
plt.style.use('fivethirtyeight')
fandango_2015['Fandango_Stars'].plot.kde(label = '2015', legend = True, figsize = (8,5.5))
fandango_2016['fandango'].plot.kde(label = '2016', legend = True)
plt.title("Comparing distribution shapes for Fandango's ratings\n(2015 vs 2016)", y = 1.07)
# the `y` parameter pads the title upward
plt.xlabel('Stars')
plt.xlim(0,5)
# because ratings start at 0 and end at 5
plt.xticks(arange(0,5.1,.5))
# plt.show()


""" THe kernal density plots reveal two main findings about
	the distribution samples.
	1. Left Skewed
	2. 2016 is slightly less left skewed than 2015.

	We see here the beginnigs of a confirmation that there is
	a difference bwtween the two samples"""


""" Lets Take a look at the number of ratings per a rating
	with a frequency table to further the study.  Also,
	since both datasets have different amount of observations,
	the data will be normalized and show percentages. """
"""2015 Frequency Table"""
# print('2015' + '\n' + '-' * 16)
# print(fandango_2015['Fandango_Stars'].value_counts(normalize = True).sort_index() * 100)

"""2016 Frequency Table"""
# print('2016' + '\n' + '-' * 16)
# print(fandango_2016['fandango'].value_counts(normalize = True).sort_index() * 100)

"""At a first glance we can see that the percentages
   for the  4.5 and 5.0 ratings were higher for 2015
   than they were for 2016. A percentage difference of
   13.4% and 6.5% respectivley. This is a significant
   change.

   It is importatnt also to note that there was a greater
   percentage movies that recieved a 3.5 and 4.0 ratings,
   compared to 2015.  This confirms what we saw in the
   density plot.  But, before we get ahead of ourselves
   lets take a look at a few more metrics (MEAN, MEDIAN, MODE)."""


# Table showing MEAN, MEDIAN, and MODE for both 2016 and 2015
mean_2015 = fandango_2015['Fandango_Stars'].mean()
mean_2016 = fandango_2016['fandango'].mean()

median_2015 = fandango_2015['Fandango_Stars'].median()
median_2016 = fandango_2016['fandango'].median()

mode_2015 = fandango_2015['Fandango_Stars'].mode()[0] # the output of Series.mode() is a bit uncommon
mode_2016 = fandango_2016['fandango'].mode()[0]

summary = pd.DataFrame()
summary['2015'] = [mean_2015, median_2015, mode_2015]
summary['2016'] = [mean_2016, median_2016, mode_2016]
summary.index = ['mean', 'median', 'mode']
# print(summary)


# Bargraph showing MEAN, MEDIAN, and MODE for both 2016 and 2015
plt.style.use('fivethirtyeight')
summary['2015'].plot.bar(color = '#0066FF', align = 'center', label = '2015', width = .25)
summary['2016'].plot.bar(color = '#CC0000', align = 'edge', label = '2016', width = .25,
                         rot = 0, figsize = (8,5))
plt.title('Comparing summary statistics: 2015 vs 2016', y = 1.07)
plt.ylim(0,5.5)
plt.yticks(arange(0,5.1,.5))
plt.ylabel('Stars')
plt.legend(framealpha = 0, loc = 'upper center')
# plt.show()

# Difference in mean from 2015 relative to the mean in 2016
# print((summary.loc['mean'][0] - summary.loc['mean'][1]) / summary.loc['mean'][0])

"""We can see that the mean rating was lower by 0.2 in 2016.
   Or, in other words, the overall mean for 2016 had saw a
   drop of approx. 4.8%. Thus, we can conclude that the movie
   ratings in 2016 were slightly lower than 2015.  Though,
   further investigation would be nesssary, with the recent changes
   Fandango has been making to its score rating system in 2019 to
   its newlyish acquired subsidiary Rotten Tomatoes, that one reason
   for the scoring difference from 2015 to 2016 maybe that Fandango
   fixed the biased rating system hickey's analysis uncovered."""
