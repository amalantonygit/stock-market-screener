"""first templates Flask app"""
import pandas as pd
from datetime import datetime
from flask import Flask, render_template

bse_index_df = pd.read_csv('./data/bse/index.csv',sep=',', index_col=False)
bse_equities_df = pd.read_csv('./data/bse/equities.csv',sep=',', index_col=False)
bse_index_df['datetime'] = bse_index_df['Date'].apply(lambda x : datetime.strptime(x, "%d-%B-%Y"))
nse_index_df = pd.read_csv('./data/nse/index.csv',sep=',', index_col=False)
#nse_equities_df = pd.read_csv('./data/nse/equities.csv',sep=',', index_col=False)
print(nse_index_df.columns)
nse_index_df['datetime'] = nse_index_df['Date '].apply(lambda x : datetime.strptime(x, "%d-%b-%Y"))
app = Flask(__name__)


@app.route('/status')
def hello():
    return "It works!"

@app.route('/markets/bse')
def bse_view():
    index_df = bse_index_df
    print(index_df.to_string())
    last_day_details = index_df.loc[index_df['datetime'].idxmax()]
    date = last_day_details['Date']
    open = last_day_details['Open']
    high = last_day_details['High']
    low = last_day_details['Low']
    close = last_day_details['Close']
    previous_day_details = index_df.drop(index_df[index_df['datetime'] == last_day_details['datetime']].index)
    previous_day_details = previous_day_details.loc[previous_day_details['datetime'].idxmax()]
    previous_close = previous_day_details['Close']
    return render_template('bse.html',
                           date=date,
                           open=open,
                           high=high,
                           low=low,
                           close=close,
                           previous_close=previous_close
                           )

@app.route('/markets/nse')
def nse_view():
    index_df = nse_index_df
    print(index_df.to_string())
    last_day_details = index_df.loc[index_df['datetime'].idxmax()]
    date = last_day_details['Date ']
    open = last_day_details['Open ']
    high = last_day_details['High ']
    low = last_day_details['Low ']
    close = last_day_details['Close ']
    previous_day_details = index_df.drop(index_df[index_df['datetime'] == last_day_details['datetime']].index)
    previous_day_details = previous_day_details.loc[previous_day_details['datetime'].idxmax()]
    previous_close = previous_day_details['Close ']
    return render_template('nse.html',
                           date=date,
                           open=open,
                           high=high,
                           low=low,
                           close=close,
                           previous_close=previous_close
                           )

if __name__ == '__main__':
    app.run(debug=True)
