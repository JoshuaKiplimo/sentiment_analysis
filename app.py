import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import twitter
import tweepy
import json
import re
import requests
from textblob import TextBlob
import os

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server

app.title = 'Sentiment Analysis'

app.layout = html.Div([
    html.Div([

      html.H2(' Twitter Sentiment Analysis')

        ], className='banner'),
    html.Div([

        html.Div([# tag1
            dcc.Tab(label='Description', value='tab-1', children = [
                html.Div(className='myparagraph', children=[

                    html.H4('About'),
                    html.P('To make this possible, most subjective data retrieved from Twitter API is analysed for keywords that express sentiments from texts.'
                    ' Data is returned as positive, negative or neutral.'
                    ' This is for experimental purposes and may not be 100 percent accurate'),
                    html.P('To try it out, type in data followed by an asterisk, for example Joshua*.'
                        ' This to prevent throttling of API requests.'),
                    
                    html.H5('Type in name of person or company'),
                    dcc.Input(id='my-id',

                 type='text', 
                 placeholder='Enter Name'
                 )
                ])
            ])
        ],className='four columns',style={'border':'0.5px solid #FFFFFF','marginLeft':'30px','marginTop':'30px','padding':'30px',
         'border-radius':'6px','height':'75vh','backgroundColor':'#FFFFFF','overflow':'scroll'}),

        html.Div([ #tag2
            html.Div(id='output',)

            ],className = 'seven columns',style={'margin':'10px','padding':'10px','height':'75vh'})

                ],className= 'row')

                 ],style={ 'height':'100vh','backgroundColor':'#F6F6F6'}) #My graph goes back to this output which makes the mashed together inside the tab),
@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
    )
def update_output_div(input_value):
    if input_value is None or input_value == '':
        return "Enter an input to see the graph"
    else:

        if input_value[-1] == '*':
            input_value = input_value.split('*')[0]
            
            
        
            api_key = os.environ.get('API_KEY')
            
            api_secret_key = os.environ.get('API_SECRET_KEY')

            access_token =os.environ.get('ACECSS_TOKEN') 


            access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

            r = requests.post('https://api.twitter.com/oauth2/token',
                              auth=(api_key, api_secret_key),
                              headers={'Content-Type':
                                  'application/x-www-form-urlencoded;charset=UTF-8'},
                              data='grant_type=client_credentials')
            assert r.json()['token_type'] == 'bearer'
            bearer = r.json()['access_token']

            url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23'+input_value+'&result_type=mixed&count=100&include_entities=false'
            r = requests.get(url, headers={'Authorization': 'Bearer ' + bearer})
            r = r.json()
            print(len(r['statuses']))
            tweets = []
            for num in range(len(r['statuses'])):
                tweets.append(r['statuses'][num]['text'])
            
            #subjectivity ranges from 0 to 1 where 0 is very objective and 1 is very subjective 
            #polarity
            #greater than 0 is positive
            # less than 0 is negative 
            #and 0 is neutral 
            positive_count = 0.0000001 #for now, I will use 1 as a place holder, Needs major update as it skews returned data
            negative_count = 0.0000001
            neutral_count = 0.00000001
            total = positive_count + negative_count + neutral_count
            texts = 0 # to find out how many texts were actually used in the survey.
            # tweets = twitterdata.get_twitter_data()
            for t in tweets:
                texts +=1 
                analysis = TextBlob(t)
                if analysis.sentiment.polarity > 0.1:

                    if analysis.sentiment.polarity > 0 and analysis.sentiment.subjectivity < 0.7: #increase subjectivity 
                        positive_count += 1
                elif analysis.sentiment.polarity < 0.1:
                    if analysis.sentiment.polarity < 0 and analysis.sentiment.subjectivity < 0.7:
                        negative_count += 1 
                else:
                    neutral_count += 1
            
            positive_count = (positive_count/total)*100
            negative_count = (negative_count/total)*100
            neutral_count = (neutral_count/total)*100
            #total = positive_count + negative_count + neutral_count
            print(positive_count, negative_count, neutral_count)
            return dcc.Graph(
                        id ='graph',
                        figure = {
                        'data' : [
                         {'x': ['Positive', 'Negative', 'Neutral'], 'y':[positive_count, negative_count, neutral_count], 'type':'bar', 'name': 'twitter','marker':dict(color=“MediumPurple”)}


                        ],
                        'layout': {

                        'title': 'CURRENT TWITTER SENTIMENTS FOR {}'.format(input_value.upper()),
                        'xaxis':{
                        'title':'Sentiment'
                                },
                        'yaxis':{
                             'title':'Percentage Of Sentiment'
                                }
                        



                        }

                        }
                            )
        else:
            return 'Have you added a * at the end of text?'


if __name__ == '__main__':
    app.run_server(debug=True)