# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 16:42:09 2021

@author: ngues
"""

#================================= Import packages==============================#
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st




#=============================== Download data ETFs===============================#

start = '2014-01-02'
end = '2015-01-01'
EEM = yf.download("EEM", start=start, end = end)
EFA = yf.download("EFA", start=start, end = end)
TIP = yf.download("TIP", start=start, end = end)
TLT = yf.download("TLT", start=start, end = end)
VNQ = yf.download("VNQ", start=start, end = end)
VTI = yf.download("VTI", start=start, end = end)



#=============================Application Title==================================#
st.title('Bollinger Bands Strategy')
st.markdown('')
st.write('Select Your Portfolio')
if st.button('CryptoPortfolio'):
    st.write('Not Available !')
    T = False
if st.button('E-commercePortfolio'):
    st.write('Not Available !')
    T = False
if st.button('CurrenciesPortfolio'):
    st.write('Not Available !')
    T = False
if st.button('EtfsPortfolio'):
    st.write('Available !')
    T = True

  

#st.write(VTI.head(2))

st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
# Create buttons to select an ETF
list_of_etfs = [EEM, EFA, TIP, TLT, VNQ, VTI]
ETFs_names = ['EEM', 'EFA', 'TIP', 'TLT', 'VNQ', 'VTI']
genre = st.radio("Select an ETF to display Close Price evolution", 
                 ('EEM', 'EFA', 'TIP', 'TLT', 'VNQ', 'VTI', 'All'))

for Etf, etf_name in zip(list_of_etfs, ETFs_names):
    Etf = Etf[['Adj Close']].dropna()
    if genre == etf_name:
        fig, axes = plt.subplots(figsize=(10,6))
        axes.plot(Etf)
        axes.set_title(f'Close Price Evolution on {etf_name} asset \n')
        st.pyplot(fig)
if genre == 'All':
        fig, axes = plt.subplots(figsize=(10,6))
        axes.plot(EEM['Adj Close'], label='EEM')
        axes.plot(EFA['Adj Close'], label='EFA')
        axes.plot(TIP['Adj Close'], label='TIP')
        axes.plot(TLT['Adj Close'], label='TLT')
        axes.plot(VNQ['Adj Close'], label='VNQ')
        axes.plot(VTI['Adj Close'], label='VTI')
        axes.set_title('Close Price Evolution on ETFs assets \n')
        axes.legend(bbox_to_anchor=(1,1), loc="upper left")
        st.pyplot(fig)




#========================================== Sharpe Ratio Strategy on ETFs=========================================#

st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.subheader('\n\n\n Sharpe Ratio')

agree = st.checkbox('Check Box to Calculate Sharpe Ratio')
if agree:
#if st.button('Calculate Sharpe Ratio'):
    start = '2014-01-02'
    end = '2015-01-01'
    ETF = yf.download("VTI EFA EEM TLT TIP VNQ" ,start=start, end_date= end)
    ETF = ETF['Adj Close'].dropna()
    ETF = ETF.loc[start:end]
    #ETF.tail(2)
    
    
    # Daily return Calculation
    
    list_close_price = ETF.columns
    for close_price in list_close_price:
        ETF[close_price + '_daily_return_%'] = (ETF[close_price].pct_change(periods=1))
    ETF = ETF.dropna()
    
    # Let's create a dataframe with only daily returns
    ETF_dr = ETF.iloc[:, 6:12]
    
    
    # Let's create an array of random ratios and bring it to 100 %
    num_iter = 15000
    all_ratios = np.zeros((num_iter, len(ETF_dr.columns)))
    exp_returns = np.zeros((num_iter))
    exp_vololatilities = np.zeros((num_iter))
    SR = np.zeros((num_iter))
    
    for each_iter in range(num_iter):
        # Ratios
        ratios = np.random.random(6)
        ratios = ratios / np.sum(ratios)
        
        # Assign the value of each ratio to each line of tha matrix all_ratios  
        all_ratios[each_iter,:] = ratios
    
        # Annual Expected Return for every iteration : Here we use the period mean daily return
        exp_returns[each_iter] = np.sum(ETF_dr.mean() * ratios * 252)
    
        # Annual Expected Volatility for every iteration
        # exp_vol = np.sqrt(np.dot(ratios.T, ((stocks_dr.cov() * 252).dot(ratios))))
        exp_vololatilities[each_iter] = np.sqrt(((ETF_dr.cov() * 252).dot(ratios)).dot(ratios)) #cal cov btw the stocks x 252 days
    
        # Ratio de Sharpe
        SR[each_iter] = exp_returns[each_iter] / exp_vololatilities[each_iter]
    
    if SR.max() > 3:
        st.markdown(f'The Sharp Ratio is an excelent ratio : {SR.max()}.')    
    elif SR.max() > 2:
        st.markdown(f'The Sharp Ratio is a very good ratio : {SR.max()}.')
    elif (SR.max() > 1) :
        st.markdown(f'The Sharp Ratio is a good ratio : {SR.max()}.')
    elif SR.max() < 1:
        st.markdown(f'The Sharp Ratio is a bad ratio : {SR.max()}. But is better than a zero risk investment.')
    else: 
        st.markdown(f'The Sharp Ratio is a very bad ratio : {SR.max()}. It is poorer than a zero risk investment.')
    
    # SR > 1  : good ratio
    # SR > 2  : very good
    # SR > 3  : excellent
        
    
    st.markdown('')
    st.markdown('\n Allocation Ratio')
    x = all_ratios[SR.argmax()]
    y = ETF.columns[0:6]
    st.write(pd.DataFrame(data = x, index = y, columns=['Allocations']))
    
        #==================== Pie Chart =======================#
    sizes = all_ratios[SR.argmax()]
    labels = ['EEM', 'EFA', 'TIP', 'TLT', 'VNQ', 'VTI']
    fig_pie, ax = plt.subplots(figsize=(10,6))
    ax.pie(sizes, labels = ['']*6, startangle=90, normalize=True)
    ax.axis('equal')
    ax.legend(labels=labels, bbox_to_anchor=(1,1), loc="best")
    ax.set_title('ETF Allocation')
    st.pyplot(fig_pie)




# Apply Sharpe Ratio on the ETFs Portfolio






st.markdown('')
st.markdown('')
st.markdown('')


# Create buttons to select an ETF Bollinger Bands
     
st.subheader('\n\n\n Bollinger Bands')
agree = st.checkbox('Check Box to run Bollinger Bands Strategy')
if agree:
#if st.button('Run Bollinger Bands Strategy'):        
    list_of_etfs = [EEM, EFA, TIP, TLT, VNQ, VTI]
    ETFs_names = ['EEM', 'EFA', 'TIP', 'TLT', 'VNQ', 'VTI']
    genre = st.radio("Select an ETF to display it's Bollinger Bands Graph", 
                     ('EEM', 'EFA', 'TIP', 'TLT', 'VNQ', 'VTI'))
    List_of_annualized_return = []

    for Etf, name in zip(list_of_etfs, ETFs_names):
        Etf = Etf[['Adj Close']].dropna()
        if genre == name:
            Etf['SMA_20'] = Etf['Adj Close'].rolling(window=20).mean()
            Etf['Sdt_20'] = Etf['Adj Close'].rolling(window=20).std()
            Etf['Upper_band'] = Etf['SMA_20'] + 2*Etf['Sdt_20']
            Etf['Lower_band'] = Etf['SMA_20'] - 2*Etf['Sdt_20']
            Etf['Sell_signal'] = np.where(Etf['Upper_band'] < Etf['Adj Close'], True, False)
            Etf['Buy_signal'] = np.where(Etf['Lower_band'] > Etf['Adj Close'], True, False)
            Etf = Etf.dropna()
        
            # Let's reduce the number of signals so that we donnot have consecutive buyings or sellings
            buys = []
            sells = []
            position = True
        
            for pos in range(len(Etf)):
                if Etf['Lower_band'][pos] > Etf['Adj Close'][pos]:
                    if position == True:
                        buys.append(pos)
                        position = False
                elif Etf['Upper_band'][pos] < Etf['Adj Close'][pos]:
                    if position == False:
                        sells.append(pos)
                        position = True    
        
            # Let's plot Bollinger Bands strategy
            figs, axe = plt.subplots(figsize=(16,10))
            axe.plot(Etf['Upper_band'], label = 'Upper_band')
            axe.plot(Etf['Lower_band'], label = 'Lower_band')
            axe.plot(Etf['Adj Close'], label = 'Adj Close')
            axe.scatter(Etf.iloc[sells].index, Etf['Adj Close'].iloc[sells], color='m', marker='^', s=100, label= 'Sell_signal')
            axe.scatter(Etf.iloc[buys].index, Etf['Adj Close'].iloc[buys], color='k', marker='v', s=100, label= 'Buy_signal')
            axe.fill_between(Etf.index, Etf['Upper_band'],Etf['Lower_band'], color='k', alpha=0.08)
            axe.legend()
            axe.set_title(f'Bollinger Bands Strategy on {name} asset \n')
            st.pyplot(figs);
            
            # Let's calculate the annualized return
            X = pd.concat([Etf['Adj Close'].iloc[buys], Etf['Adj Close'].iloc[sells]], axis=1)
            X.columns = ['Buys', 'Sells']
            Annualized_return = (X.Sells.shift(periods=-1) - X.Buys) / X.Buys
            Annualized_return_pct = round(Annualized_return.mean(skipna=True)*100, 2)
            List_of_annualized_return.append(Annualized_return_pct)


st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')


st.subheader('\n\n\n Investment')
st.markdown('')
st.markdown('')
st.markdown('')
agree = st.checkbox('Check Box to invest ($)')
if agree:
#if st.button('Click here to invest ($)'):
    user_investment = st.number_input('Please enter the amount to invest in USD:')
    if user_investment > 0:
        st.markdown(f'You invested  {user_investment} $  in your EtfsPortfolio !')


st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
agree = st.checkbox('Calculate Return')
if agree:
#if st.button('Calculate Return'):
    if user_investment > 0:
        position_values = all_ratios[SR.argmax()] * user_investment * List_of_annualized_return
        st.write(pd.DataFrame(data=position_values, index=ETFs_names, columns = ['Returns ($)']))
        st.write(f'Total profit : {position_values.sum()} $')
        


    
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('*Disclaimer, do you agree that all your investment can be loss and this is not of our responsability ?*')
agree = st.checkbox('Yes, i agree')
if agree:
    st.write('Thanks !')




































