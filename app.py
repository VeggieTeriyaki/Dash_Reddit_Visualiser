import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from praw.models import MoreComments
import praw #import the reddit wrapper class
from collections import Counter
def redditDataExtractor(postID):
    reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id='MzP2Nwj9ntK6UQ', client_secret="pc7UJvP9yEgrKzJHXDHiBE3rIP4",
                     username='farpista', password='Bratik123') #create a reddit instance
    # Create a submission object that holds details of a specific post
    submission = reddit.submission(id=postID) 
    words ={}
    #Gathering data and cleaning it up
    for i in range(len(submission.comments)):
        if isinstance(submission.comments[i], MoreComments):
            continue
        tmp = submission.comments[i].body.split(" ")
        for k in range(len(tmp)):
            if(tmp[k].replace('\n','') not in words):
                words[tmp[k].replace('\n','')] = 0
            words[tmp[k].replace('\n','')] += 1
    # Making a dictionary that contains the most frequent words
    # PS: The threshold here is contained to be 30. An algorithm could probably be written to optimize ths process,
    # but according to me that is out of the scope of this project.
    words[""] = 0
    highestWords = {}
    words.pop(" ",None)
    words = Counter(words)
    buffer_value = max(words.values())/3
    for k in words:
        if words[k] > buffer_value:
            highestWords[k] = words[k]
    return highestWords

app = dash.Dash() #initializing the dash object

my_css_url = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
app.css.append_css({
"external_url": my_css_url
})

colors = {
    'background': '#111111', #Making JSON to customize the HTML element of the script.
    'text': '#7FDBFF'
}
def updateGraph(id): #Function to graph qith the requested post ID.
    redditData = redditDataExtractor(id)
    return {
            'data': [
                {'x': list(redditData.keys()) , 'y': list(redditData.values()), 'type': 'bar', 'name': 'SF'}
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
app.title = 'Reddit scraper'
app.layout = html.Div(children=[
    html.Title(children="Reddit Scraper"),
    html.Nav(className='navbar navbar-default'),
    html.H1(children='Welcome to a basic reddit scraper!'),
    html.Br(),
    html.Div(children='''
        Hello there! This is a simple graphing applet that will graph for you the words that are most frequently 
        appearing on a reddit post. All you have to do is enter the ID of the reddit post. THE ID is a 6 digit string
        in the URL of any reddit post. For example, in "https://www.reddit.com/r/aww/comments/7j44o0/just_two_best_friends/", the id is 7j44o0.
    ''',className = 'container'),
    html.Br(),
    dcc.Input(id='id-state', type='text', value=''),
    html.P(),
    html.Button(id='submit-button', n_clicks=0, children='Submit post ID', className = 'btn btn-primary'),
    html.Br(),
    html.Br(),
    dcc.Graph(id='output-state')

],className='container')
 #Callbacks work as a part of the dash interface. This is what runs when we want to update the 'state' of the graph.
@app.callback (Output('output-state', 'figure'),
              [Input('submit-button', 'n_clicks')],[State('id-state','value')])
def update_output(n_clicks, id):
    return updateGraph(id)

if __name__ == '__main__':
    app.run_server(debug=True)
