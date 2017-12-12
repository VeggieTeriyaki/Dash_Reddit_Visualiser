# Overview
This is a very simple web app for visualising data on reddit. It uses dash in order to visualise data from reddit. All the user has to do is input their reddit post id, and the application will plot the most frequent words that appear on the reddit post **only in the top level comments.** This has to change and will probably be implemented in the future versions.

# Dependencies
In order to run this app, you have to run:
```
pip install dash==0.19.0  # The core dash backend
pip install dash-renderer==0.11.1  # The dash front-end
pip install dash-html-components==0.8.0  # HTML componentspip install dash-core-components==0.15.2  # Supercharged components
pip install plotly --upgrade # Making sure you have latest version of plotly.
pip install praw #The python reddit wrapper that is used.
```
Feel free to contribute to this code!
