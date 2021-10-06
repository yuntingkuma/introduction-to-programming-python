#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 23:34:41 2019

@author: BrandonLin
"""

"""

目標:
算出使用者總共領到多少股利
算出使用者2種制度（合併&分開）下的「實際應納稅額」
建議使用者要採用合併還是分離

算出如果「完全不參加除權息」（把股票全賣掉，除權息後再全部買回）要付多少手續費跟證交稅
建議使用者是否參加除權息
"""

"""
累進差額 ＝ progressive_difference
應納稅額 ＝ tax_payable
實際應繳金額 ＝ 應自行繳納稅額 ＝ tax_balance_due
"""

"""
稅法範例請參考 https://is.gd/Xx6Jyk 以及 https://is.gd/lQThCG

"""
#%% #需要匯入的套件

# 爬股價需要匯入的
import datetime
print(datetime.datetime.now())

import twstock

# 爬股利需要匯入的
import urllib
from urllib.request import urlopen
import re
import time 
#%%
# function==================================================================


# 查詢稅率（由綜合所得淨額來判斷級距，而非真實所得收入。）
def tax_rate(net_taxable_income):
    
    if (net_taxable_income <= 540000) :
        return(0.05)
    elif(net_taxable_income <= 1210000):
        return(0.12)
    elif(net_taxable_income <= 2420000):
        return(0.2)
    elif(net_taxable_income <= 4530000):
        return(0.3)
    elif(net_taxable_income >= 4530001):
        return(0.4)

# 查詢累進差額（由綜合所得淨額來判斷級距，而非真實所得收入。）
def progressive_difference(net_taxable_income):
    if (net_taxable_income <= 540000) :
        return(0)
    elif(net_taxable_income <= 1210000):
        return(37800)
    elif(net_taxable_income <= 2420000):
        return(134600)
    elif(net_taxable_income <= 4530000):
        return(376600)
    elif(net_taxable_income >= 4530001):
        return(829600)

# 「together」：算出若股利合併計稅，實際應繳之金額         
def together(net_taxable_income, dividend_income):
    
    if (dividend_income * 0.085 <= 80000):
        tax_payable = net_taxable_income * tax_rate(net_taxable_income) - progressive_difference(net_taxable_income)
        
        # (dividend_income * 0.085) 是股利可抵扣稅額
        tax_balance_due = tax_payable - (dividend_income * 0.085)
        
        return(tax_balance_due)
    
    #合併計稅的8.5%抵扣額度最高只有8萬元，故若股利的8%超過8萬，則以80000元計。
    else:
        tax_payable = net_taxable_income * tax_rate(net_taxable_income) - progressive_difference(net_taxable_income)
        tax_balance_due = tax_payable - 80000
        
        return(tax_balance_due)
        
# 「separate」：算出若股利分離計稅，實際應繳之金額 
def separate(net_income_without_dividend, dividend_income):
    
    ans = net_income_without_dividend * tax_rate(net_income_without_dividend) - progressive_difference(net_income_without_dividend) + (dividend_income * 0.28)
    
    return(ans)

# 「handing_fee」：算出手續費
def handing_fee( price, shares):
    
    return round( price * shares * 0.001425 )

# 「securities transaction tax」：算出證交稅

def securities_transaction_tax( price, shares):
    
    return round( price * shares * 0.003 )

#%% 
# main =====================================================================

# 「net_taxable_income」 代表「含股利之所得淨額」。（等於「不含股利之所得淨額」加上「總股利收入」）
net_taxable_income = int(0)

net_income_without_dividend = int( input("✍請輸入「不含股利」之所得淨額：") )

# 「dividend_income」代表總股利收入
dividend_income = int(0) 



# 儲存每檔股票的現價之陣列
all_current_price_list = [0]
# 儲存每檔股票的股數之陣列
all_shares_list = [0]
# 儲存每檔股票的現金股利之陣列
all_cash_dividend_list = [0]
# 儲存每檔股票的股票股利之陣列
all_stock_dividend_list = [0]
# 儲存每檔股票的合計股利之陣列
all_total_dividend_list = [0]

#讓使用者輸入持股資料（股票代碼/股數）
stock_ID_and_shares = str()

#「counter」代表使用者的持股「檔數」
counter = int(0)

print("\n請輸入持有股票之代碼與股數，輸入完畢後請輸入「done」\n代碼與股數請用「/」隔開。（範例: 2330/500000）")
while( stock_ID_and_shares != "done"):
    
    # 請使用者輸入股票代碼
    stock_ID_and_shares = str(input("✍第 %d 檔股票：" % (counter+1) ))
    
    
    
    # 如果輸入「done」就跳出迴圈
    if (stock_ID_and_shares == "done"):
        break
    
    print("處理中，請稍候5秒⋯⋯")
    counter += 1
    
    # 把輸入的資訊分割成「代碼」與「持有股數」
    stock_ID_and_shares = stock_ID_and_shares.split("/")
    """
    print(stock_ID_and_shares)
    """
  
    #%%  #爬取股價
   

    stock_ID = stock_ID_and_shares[0]
    
    #爬取股價，儲存在「current_price」
    current_price = twstock.Stock(stock_ID)
    
    # current_price.price[-1] 代表最新的收盤價
    """
    print('收盤價：',current_price.price[-1])
    """
    #把這檔股票的收盤價加入「儲存每檔股票的現價之陣列」
    all_current_price_list.append( current_price.price[-1] )
    
    #把這檔股票的你持有的股數加入「儲存每檔股票的股數之陣列」。（stock_ID_and_shares[1]是你輸入的持有股數）
    all_shares_list.append( stock_ID_and_shares[1] )



    #%% #爬取股利
    
    #假裝是正常人使用瀏覽器瀏覽
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1;WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    
    #我要爬取的網站
    req = urllib.request.Request(url ='https://histock.tw/stock/financial.aspx?no='+stock_ID+'&t=2',headers = headers)
    time.sleep(5)
    
    #要暫停五秒，才不會有問題
    res = urlopen(req).read().decode('utf-8')
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(res,features = 'lxml')
    
    
    #尋找現金股利與股票股利的html tag
    stock_dividend = soup.find_all('td','b-b')
    cash_dividend = soup.find_all('td')
    
    #將現金股利與股票股利分別append進分別的list裡面
    stock_dividend_list = []
    cash_dividend_list = []
    for i in range(0,len(stock_dividend)):
            stock_dividend_list.append(stock_dividend[i].text)
    for i in range(0,len(cash_dividend)):
            cash_dividend_list.append(cash_dividend[i].text)
    #while '' in stock_dividend_list:
    #    stock_dividend_list.remove('')
    
    #把有‘-’在list裡面刪除
    while '-' in stock_dividend_list:
        stock_dividend_list.remove('-')
    now_stock_dividend = float(stock_dividend_list[1])
    #本來想把list中含有0與''空白也剔除，但發現如此一來規律就會不對
    
    #while '' in cash_dividend_list:
    #    cash_dividend_list.remove('')
    while '-' in stock_dividend_list:
        cash_dividend_list.remove('-')
    now_cash_dividend = float(cash_dividend_list[6])
    
    #股利總和為現金股利加股票股利
    now_total_dividend = now_cash_dividend + now_stock_dividend
    """
    print(now_total_dividend)
    """
    # 把把這檔股票的現金股利加入「儲存每檔股票的現金股利之陣列」
    all_cash_dividend_list.append(now_cash_dividend)
    
    # 把把這檔股票的股票股利加入「儲存每檔股票的股票股利之陣列」
    all_stock_dividend_list.append(now_stock_dividend)
    
    # 把把這檔股票的合計股利加入「儲存每檔股票的合計股利之陣列」
    all_total_dividend_list.append(now_total_dividend)
    
    # 爬蟲完畢，該存到陣列的也存好了，告訴使用者可以繼續輸入。
    print("請繼續輸入！全部輸入完畢，請輸入「done」")

"""
print("各檔的現價：" , end='')
print(all_current_price_list)
print("各檔的持有股數：" , end='')
print(all_shares_list)
print("各檔的現金股利：" , end='' )
print(all_cash_dividend_list)
print("各檔的股票股利："  , end='')
print(all_stock_dividend_list)
print("各檔的合計股利：" , end='')
print(all_total_dividend_list)
"""

#%%
# 計算若使用者參加除權息，他的股利收入是多少

for i in range(1, counter+1, 1):
    dividend_income = dividend_income + ( float(all_total_dividend_list[i]) * float(all_shares_list[i]) )

print("\n您共有 %d 檔股票，若參加除權息，您的總股利收入為 %d 元" % (counter,dividend_income) )


print("▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣")
net_taxable_income = net_income_without_dividend + dividend_income
print("若您將要參加除權息，您「含股利之所得淨額」為 %d 元" % net_taxable_income)

# 「net_taxable_income」 代表「含股利之所得淨額」。（等於「不含股利之所得淨額」加上「總股利收入」）
 

# 「separate_ans」代表若股利分離計稅，實際應繳之金額 
separate_ans = int( separate(net_income_without_dividend, dividend_income) )

# 「together_ans」代表若股利合併計稅，實際應繳之金額
together_ans = int( together(net_taxable_income, dividend_income) )


# 印出使用者的2種實際應納稅額（合併&分開）
print("採股利所得合併計稅，共需繳 %d 元" % together_ans )
print("採股利所得分離計稅，共需繳 %d 元" % separate_ans )


# 若參加除權息的話，應採用哪一種制度？能因此剩下多少錢？
if (separate_ans < together_ans):
    print("因此，建議您採取股利所得分離計稅，可省下 %d 元" % (together_ans - separate_ans))

else:
    print("因此，建議您採取股利所得合併計稅，可省下 %d 元" % (separate_ans - together_ans))


#%% #若不參加除權息

# 儲存每檔股票的除權息參考價之陣列
all_after_price_list = [0]

# 算出每檔股票的除權息參考價
for i in range(1, counter+1, 1):
    
    #「after_price」代表某檔股票的除權息參考價
    after_price = round(float((all_current_price_list[i] - all_cash_dividend_list[i]) / (1 + all_stock_dividend_list[i]/10) ) , 2)
    
    # 把「某檔股票的除權息參考價」儲存到「儲存每檔股票的除權息參考價之陣列」
    all_after_price_list.append(after_price)
"""    
print(all_after_price_list)
"""


# 執行棄權息之交易成本（把全部股票先賣出再買回）

# 儲存每檔股票的賣出手續費之陣列
all_hf_sell_list = [0]
# 儲存每檔股票的賣出證交稅之陣列
all_stt_list = [0]
# 儲存每檔股票的買進手續費之陣列
all_hf_buy_list = [0]
# 儲存每檔股票的合計交易成本之陣列
all_total_transaction_cost_list = [0]

for i in range(1, counter+1, 1):
    hf_sell = handing_fee( float(all_current_price_list[i]), float(all_shares_list[i]) ) #賣出之手續費
    stt = securities_transaction_tax( float(all_current_price_list[i]), float(all_shares_list[i]) )#賣出之證交稅
    hf_buy = handing_fee( float(all_after_price_list[i]), float(all_shares_list[i]) ) #買進之手續費
    
    total_transaction_cost = hf_sell + stt + hf_buy
    
    all_hf_sell_list.append(hf_sell)
    all_stt_list.append(stt)
    all_hf_buy_list.append(hf_buy)
    
    all_total_transaction_cost_list.append(total_transaction_cost)

"""
print("各檔股票的賣出手續費：", end='')    
print(all_hf_sell_list)
print("各檔股票的證交稅：", end='') 
print(all_stt_list)
print("各檔股票的買回手續費：", end='') 
print(all_hf_buy_list)
print("各檔股票的總交易成本：", end='') 
print(all_total_transaction_cost_list)
"""
print("▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣")
print("若您決定不參加除權息，於除權息前一日將股票賣出，再於隔日買回，會有以下結果：")

"""
print("須繳交：賣出手續費 %.0f 元、買回手續費 %.0f 元、證交稅 %.0f 元" % ( sum(all_hf_sell_list), sum(all_hf_buy_list), sum(all_stt_list) ) )
"""

# 在賣光股票的情況下，須繳交的所得稅
income_tax_after_sell_all_stock = together(net_income_without_dividend, 0)

"""
print("賣光股票後，須繳交的所得稅：%d " % income_tax_after_sell_all_stock)
"""

# 「income_tax_can_save_after_sell_all_stock」代表如果賣光股票，可省下多少所得稅

# 如果原本要用分離計稅，那就用分離計稅去減，賣光股票後的所得稅
if (separate_ans < together_ans):
    income_tax_can_save_after_sell_all_stock = separate_ans - income_tax_after_sell_all_stock
# 如果原本要用合併計稅，那就用合併計稅去減，賣光股票後的所得稅
else:
    income_tax_can_save_after_sell_all_stock = together_ans - income_tax_after_sell_all_stock
    if income_tax_can_save_after_sell_all_stock < 0:
        income_tax_can_save_after_sell_all_stock = 0


#告訴使用者棄權息「要付出的」與「能省下的」

print("要多付的總交易成本：%d 元" % sum(all_total_transaction_cost_list) )
print("可因此省下的所得稅：%d 元" % income_tax_can_save_after_sell_all_stock)
print("-------------------------")

if income_tax_can_save_after_sell_all_stock - sum(all_total_transaction_cost_list) > 0 :
    print("判斷：可合法避稅 %d 元" % (income_tax_can_save_after_sell_all_stock - sum(all_total_transaction_cost_list) ) )
else:
    print("判斷：花費的總交易成本比省下的所得稅還多，划不來。")
print("▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣")

if sum(all_total_transaction_cost_list) >= income_tax_can_save_after_sell_all_stock:
    
    print("★★結論：請不要為了避開所得稅而出清股票！因為先棄權息再買回，對您而言沒有節稅效果。★★")

else:
    
    print("★★結論：請不要參加除權息！可將股票於除權息前一日出清，隔日再以低價買回。★★")















