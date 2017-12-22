# Genrec - Discover Yourself
This is a hackathon project submitted as a part of SDHacks 2017

# Inspiration
Most modern Recommender engines use features like user age-group, user location, sex, etc. But these parameters are not personal. For example, my taste in music can differ from my friends', even though we live in the same city, are of similar age-group and sex. We need to build Recommender systems that is personal to each and every user. What better way to define a user than his/her gene data?

# What it does
GeneRec uses an individual's genetic information to recommend personalized products like movies, songs, books. etc.

According to many recent studies [1][2], genetic information is closely tied with an individual's personality traits, nutrition deficiency, learning challenges as well as many physical traits. We leveraged this information along with GenomeLink's API and datasets, we managed to create a unsupervised-learning powered Recommender engine that provides personal recommendations to users.

# How we built it
We mainly developed in Python Django Framework, with the backend clustering algorithms developed in pure Python. We also integrated many APIs to enrich our user experience.

Some of the APIs we used: 
GenomeLink API: We extensively used this API to gather genome information about our users \
Youtube API: We leverage Google Youtube API to provide Youtube video links for the songs we recommend \
Google Books API: We leverage Google Books API to fetch book URL from its ISBN number \
Google Translate API: We use this to make our web pages available throughout the world in many supportable languages \

Some of the Datasets we used:
GenomeLink Private Dataset: This was provided to us by GenomeLink during the hackathon. It contains the traits defined by genetic information for 1140 users \
Kaggle Songs DB: We included this dataset to procure the corpus of songs and the corresponding artists \
Kaggle Movies DB: We included this as a corpus for our Movies

# Challenges we ran into
The data was initially unseeded. Meaning, initially, we did not have information about users' movie/song preferences. We tackled this problem by seeding the data manually and then working on it. In a real world scenario, we can overcome this by merging APIs like Netflix, Spotify, Youtube which already aggregate user preferences over time.

# Accomplishments that we're proud of
We built a unsupervised-learning algorithm and generalized it for different kinds of products and services. This is something we, personally, have never achieved in such a short time. Also, our algorithm is completely scalable and evolves over time.

# What we learned
Genome tracking is awesome! It provides a lot of information about an individual and his/her personal traits.

# What's next for GeneRec
Andoid and IOs apps \
Real-time integration for Netflix, Spotify/Youtube \


# References
[1] https://works.bepress.com/timothy_thomason/108/download/
[2] https://en.wikipedia.org/wiki/Big_Five_personality_traits
[3] https://medium.com/@awakens/genome-link-api-challenge-sd-hacks-2017-cee5fe079a5b
