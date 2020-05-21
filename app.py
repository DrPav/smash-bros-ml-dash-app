# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

uploader = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
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
            "as one of 72 fighers of the Super Smash Bros Game"
        )
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(jumbotron),
        dbc.Row(uploader),
        dbc.Row(
            id='output-with-image', 
            children=html.Img(src='https://www.ssbwiki.com/images/a/af/SSBU_Character_Select_DLC.jpeg')
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)