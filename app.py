import pandas as pd
import folium
from flask import Flask, render_template

# Import OpenTelemetry components
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize OpenTelemetry Tracer
trace_provider = TracerProvider()
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317"))
trace_provider.add_span_processor(span_processor)

# Create Flask App
app = Flask(__name__, template_folder='templates')

# Attach OpenTelemetry to Flask
FlaskInstrumentor().instrument_app(app)

n = 15
corona_df = pd.read_csv('static/dataset.csv')
by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]

def find_top_confirmed(n=15):
    corona_df = pd.read_csv('static/dataset.csv')
    by_country = corona_df.groupby('Country_Region').sum()[
        ['Confirmed', 'Deaths', 'Recovered', 'Active']
    ]
    cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return cdf

corona_df = pd.read_csv('static/dataset.csv')
corona_df = corona_df.dropna()
m = folium.Map(
    location=[34.223334, -82.461707],
    tiles='Stamen Toner',
    attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL',
    zoom_start=8
)

def circle_maker(x):
    folium.Circle(
        location=[x[0], x[1]],
        radius=float(x[2])*10,
        color="red",
        popup='{}\n confirmed cases:{}'.format(x[3], x[2])
    ).add_to(m)

corona_df[['Lat', 'Long_', 'Confirmed', 'Combined_Key']].apply(
    lambda x: circle_maker(x), axis=1
)
html_map = m._repr_html_()

@app.route('/')
def home():
    return render_template("home.html", table=cdf, cmap=html_map)

if __name__ == "__main__":
    app.run(debug=True)
