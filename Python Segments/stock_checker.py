# pip install yfinance - for data
# pip install plotly - for graph

# data source
import yfinance as yf
# raw package
import numpy
import pandas
# data visualization
import plotly.graph_objs as go


data = yf.download(tickers="GME", period="1d", interval="1m")
print(data)

# #declare figure
# fig = go.Figure()

# #Candlestick
# fig.add_trace(go.Candlestick(x=data.index,
#                 open=data['Open'],
#                 high=data['High'],
#                 low=data['Low'],
#                 close=data['Close'], name = 'market data'))

# # Add titles
# fig.update_layout(
#     title='GME',
#     yaxis_title='Stock Price (USD per Shares)')

# # X-Axes
# fig.update_xaxes(
#     rangeslider_visible=True,
#     rangeselector=dict(
#         buttons=list([
#             dict(count=15, label="15m", step="minute", stepmode="backward"),
#             dict(count=45, label="45m", step="minute", stepmode="backward"),
#             dict(count=1, label="HTD", step="hour", stepmode="todate"),
#             dict(count=3, label="3h", step="hour", stepmode="backward"),
#             dict(step="all")
#         ])
#     )
# )

# #Show
# fig.show()



# define ticker
tickerSymbol = 'GME'
# get ticker data
tickerData = yf.Ticker(tickerSymbol)
getTicker = []
getTicker = tickerData.history(period="1m")
print(tickerData.option_chain())
