# -*- coding: utf-8 -*-
from pathlib import Path
from io import BytesIO
import base64
import requests
import os

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from fastai.vision.image import open_image
from fastai.basic_train import load_learner

path = Path(__file__).parent
model_file_url = 'https://storage.googleapis.com/smash-bros-detector/resnet-50-stage-2.pkl'
model_file_name = 'resnet-50-stage-2.pkl'


def download_file(url, dest):
    if dest.exists(): return
    r = requests.get(url)
    with open(dest, 'wb') as f: f.write(r.content)

def setup_learner():
    if not os.path.exists('models'):
        os.mkdir('models')
    download_file(model_file_url, path/'models'/model_file_name)
    learn = load_learner(path/'models', model_file_name)
    return learn

def make_prediction(img_bytes):
    img = open_image(BytesIO(img_bytes))
    pred_class,pred_idx,outputs = learn.predict(img)
    prob = outputs[pred_idx].item()*100.0
    return (str(pred_class),  str(round(prob,1)))

learn = setup_learner()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

server = app.server

# App layout
uploader = dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Click here to upload an image')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    )

jumbotron = dbc.Jumbotron(
    [
        html.H1("Super Smash Bros Image Classifier", className="display-3"),
        html.Hr(),
        html.P(),
        html.P(
            "Upload an image and the model will classify it  "
            "as one of the fighters from the Super Smash Bros Game, shown below"
        )
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(jumbotron),
        dbc.Row(uploader),
        dbc.Container(id='output-with-image')
    ]
)

# App callbacks
@app.callback(Output('output-with-image', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename')])
def update_output(content, filename):
    if content is not None:
        decoded = base64.b64decode(content.split(',')[1]) # === deals with padding issues
        # with open(filename, 'wb') as f:
        #     f.write(decoded)
        pred, prob = make_prediction(decoded)

        return ([dbc.Row(dbc.Alert(pred + ' | ' + prob + '%', color='success')), dbc.Row(html.Img(src=content))])
    else: 
        return dbc.Row(html.Img(src='https://www.ssbwiki.com/images/a/af/SSBU_Character_Select_DLC.jpeg'))



if __name__ == '__main__':
    app.run_server(debug=False)