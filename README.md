# Augury

Ryan Siu and Terry Guan

## Inspiration

A [study](https://blogs.wsj.com/venturecapital/2014/03/19/study-crowdsourced-stock-opinions-beat-analysts-news/) from 2014 found that crowdsourced stock opinions on investor forum seekingalpha.com regularly beat the opinions of analysts. We wanted to replicate this effect by using Twitter as our crowdsourced opinions, in addition to taking mainstream investor data into account, to provide recommendations for beginning investors.

Our goal in creating Augury is to create a different investment model that's both more powerful and easier to use. 

## What it does

Using tweets from Twitter, our app aims to provide accurate recommendations for trading stocks to users. These recommendations are buy/sell stock ratings that are calculated by our application.

See What's Next section for our future plans for Augury.

## How we built it

There are three components to our project: the natural language processing and machine learning algorithm used to calculate recommendations; getting the data needed to perform NLP and machine learning; and creating the application to display our recommendations.

We used Google Cloud Platform's Natural Language Processing to perform sentiment analysis of companies on tweets. The sentiment analysis returned a score and magnitude detailing the sentiment the article portrayed of the entity and how positive or negative it portrayed it in. Using that information along with quantitative research measures we trained an unsupervised learning algorithm using K-means to determine whether a stock is worth investing in or not. 

Using the Twitter API, we pulled the most popular and recent tweets relating to a company and stored that in Firebase and local SQL databases. We also pulled data from the IEX Trading API, which provided key statistics about a company, such as revenue, earnings per share, etc.

The application that displays the recommendations is a Jekyll static site, hosted on a DigitalOcean droplet. Each recommendation is a "post" in Jekyll.

A script that runs continuously in the background continuously updates the databases, looks for possible recommendations, and updates the website when a new recommendation is found.

## Challenges we ran into
- Firebase refusing to cooperate (or maybe we set up the database structure incorrectly)
- Researching how people invest in stocks
- Researching machine learning algorithms (k-means clustering)

## Accomplishments that we're proud of & what we learned

- Incorporating NLP and machine learning into our project
- Learning about how stocks are traded/evaluated
- Successfully using Google Cloud Platform and APIs
- Learning about Firebase, and integrating it into our project
- ...managing to not sleep for most of the hackathon...

## What's next for Augury

- Use MD&A to perform qualitative research
- Use more quantitative indicators for machine learning
- Use news articles in the data we're analyzing
- Give specific reasons why an investor should invest in a company
- Improve UI/UX of website
- Train our own model for GCP
- **Evaluate the performance of our application over a longer period of time**
