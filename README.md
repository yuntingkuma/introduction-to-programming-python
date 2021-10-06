# Shareholder Tax Saving Machine
 This is the final project on introduction to programming class (Course code：10720QF100300) at National Tsing Hua University. 
 
 Our teammates include Brandon Lin, Pin-Yu	HUANG,	Rou-Fang Pan, and Yun-Ting Lee.
 
## Feature Design 
  Solve the actual tax issues that shareholders will encounter：
  
  **Question_1：If shareholders receive dividends, which tax system should be more beneficial to them?**
  
  **1. 合併計稅 (Combined Taxation)：**
     
 Combine the "股利所得(dividend income)" with other total income, calculate the tax payable based on the tax rate corresponding to 綜合所得淨額(the net comprehensive income), and then deduct the 股利扣抵額(dividend deduction).
  
  **2. 分離計稅 (Separated Taxation)：**
     
 股利所得(Dividend income ) is not incorporated into total income, and a 28% tax is directly levied on dividend income.
     
  **Question_2：Should shareholders hold stocks to participate in ex-dividends?**
  
  **1. 參加除權息 (Participate in ex-dividend)：**
  
Shareholders do not need to do anything and continue to hold stocks to receive dividends, but dividend income will be subject to income tax.
  
  **2. 不參加除權息 (Do not participate in ex-dividend)：**
  
Shareholders sell the stock the day before the ex-dividend and buy it back at the ex-dividend reference price the next day. "Sell high and buy low" to generate profits. In this way, dividends can avoid being levied income tax, but they have to pay transaction costs.

According to different incomes and different dividend incomes, the best choices will be different. To solve this problem, the shareholders need to know 現金股利(cash dividend), 股票股利(stock dividend), 須負擔多少稅率(tax rate we need to pay), 股利扣抵稅率(dividend tax deduction)...etc.
  
## Methodology
- Web crawler
  - Crawl cash dividend, stock dividend, and stock market price
- Judge the tax rate and the progressive difference based on the comprehensive net income
- Calculate the income tax under the two tax systems (combined or separated taxation)
- Calculate the transaction cost of buying and selling stocks
- Calculate the ex-dividend reference price of each shareholding
