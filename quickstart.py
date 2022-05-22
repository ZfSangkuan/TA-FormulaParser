from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt

'''# pylint: disable=locally-disabled, no-member'''

def callback_func():
    print("callback")

class TestStrategy(bt.Strategy):
    params = (
        ('exitbars', 8),
        ('maperiod', 20),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=True):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    # def __init__(self, callback = callback_func):
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Alias, for compatibility with formula transfered
        C = self.datas[0].close
        CLOSE = self.datas[0].close
        OPEN = self.datas[0].open
        V = self.datas[0].volume
        VOL = self.datas[0].volume

        # Alias of func, for compatibility with formula transfered
        def REF(line, int):
            return line(-1 * int)

        def EMA(line, period_int):
            return bt.indicators.ExponentialMovingAverage(line, period = period_int)

        def MA(line, period_int):
            return bt.indicators.MovingAverageSimple(line, period = period_int)

        def COUNT(line, period_int):
            cond = line > 0
            return bt.indicators.SumN(cond, period = period_int)

        def STICKLINE(cond, lw, up, width, bool):
            to_plot = bt.If(cond, up-lw, 0)
            bt.LinePlotterIndicator(to_plot, name="")

        ABS = abs


        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        # callback()

        DIF=(EMA(C,12)-EMA(C,26))
        DEA=EMA(DIF,9)
        MACD=2*(DIF-DEA)
        STICKLINE(bt.And(MACD>REF(MACD,1),MACD>=0),MACD,0,2,0)
        STICKLINE(bt.And(MACD>REF(MACD,1),MACD<0),MACD,0,2,1)
        FH1=bt.And(bt.And(REF(MACD,1)<REF(MACD,2),REF(MACD,2)<REF(MACD,3)),REF(MACD,3)<REF(MACD,4))
        FH2=bt.And(MACD>=0,COUNT(MACD>REF(MACD,1),1)==1)
        FH3=bt.And(bt.And(FH1,FH2),EMA(C,13)>REF(EMA(C,13),1))
        FH4=bt.And(bt.And(FH1,FH2),ABS((DIF-DEA)/C)<0.018)
        FH5汉=bt.And(bt.And(FH1,FH2),MACD<0.10)

        # bt.LinePlotterIndicator(FH1, name='fh1')

        # Indicators for the plotting show
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:
                # BUY with default parameters
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            # Already in the market ... we might sell if...
            # ignore no-member error for 
            #   pylint doesn't recognize dynamically-created attributes
            # if len(self) >= (self.bar_executed + self.params.exitbars): 
            if self.dataclose[0] < self.sma[0]:
                # SELL with all possible default parameters
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
    
    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)



if __name__ == '__main__':
    # print('\033[1;36m')  # terminal output colorize
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    modpath = "/Users/zhifanshangguan/Downloads/GitRepo/backtrader-master/"


    cerebro = bt.Cerebro()
    # strats = cerebro.optstrategy(
    #     TestStrategy,
    #     maperiod=range(10, 31))
    cerebro.addstrategy(TestStrategy)
    datapath = os.path.join(modpath, 'datas/orcl-1995-2014.txt')
    print("datapath: " + datapath)
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2013, 1, 1),
        todate=datetime.datetime(2013, 12, 31),
        reverse=False)
    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcash(1000.0)
    # cerebro.broker.setcommission(commission=0.001)  # 0.1%


    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run(maxcpus=1)

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()

    # terminal output colorize
    # print('\033[0m')    
