# AInvestor
AI Hedge Fund

# How to use
Don't

# Ideology
Chicks dig dudes in lamborghinis with large cocks.

# Methodology
There consists two core parts to the program: the Data Manager and the Stock Manager.  
The Data Manager handles the machine learning models and data processing.  On startup it processes a list of Stocks to obtain
the crucial data of each stock.  This will include the currently owned stocks at the top of the pile.  It parses this through different models to generate the feasability of the stock in terms of investment opportunity.  This will send a request to the Stock Manager to purchase the stock, with different attributes, such as purchase when above a certain price, or immediately.  The Stock Manager will interface with the APIs necessary to trade different stocks.  It will send  sell requests to the Data Manager, or just probes to make sure current investments are still healthy for their intended purpose.  Note, the Data Manager will return to the Stock Manager a decision of the Stock Managers question, for example if the Stock Manager asks the Data Manager to make sure Stock A is healthy, the Data Manager will respond with No - Sell that crap ASAP; which the Stock Manager will then sell the stock based on sell properties given.
The Stock Manager will profile stocks based on the intended investment type (long, short) and handle each set differently.  
There will be available statistics to show gains/losses over time, and force commands to buy/sell different stocks, of which the combination of the two managers will look after.  

After proof of concept is established, there may be an opportunity to make this public, where a small percent of gains will be taken (5% for example).  Each user will get different results, as there will be a UI to make their own models, train it on historical data and point at different markets (ForEx, Crypto, Stocks).  
