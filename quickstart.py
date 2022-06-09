from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt

'''# pylint: disable=locally-disabled, no-member'''

def callback_func():
    print("callback")

class UnitLineInd(bt.Indicator):
    lines = ('unitline',)

    params = (('value', 1),)

    plotinfo = dict(plot=False)

    def __init__(self):
        self.lines.unitline = bt.Max(0.0, self.params.value)


# class FindLastNoneZeroIndex(bt.indicators.FindLastIndex):
#     params = (('_evalfunc', lambda x: x != 0),)


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
        OPEN = self.datas[0].open
        O = OPEN
        HIGH = self.datas[0].high
        LOW = self.datas[0].low
        CLOSE = self.datas[0].close
        C = CLOSE
        VOL = self.datas[0].volume
        V = VOL

        unitline = UnitLineInd()

        # Alias of func, for compatibility with formula transfered
        # reference func
        def REF(line, period_int):
            return line(-1 * period_int)
        
        # def BARSLAST(line):
        #     return bt.indicators.FindLastNoneZeroIndex(line)

        # arithmetic func
        def EMA(line, period_int):
            return bt.indicators.ExponentialMovingAverage(line, period = period_int)

        def MA(line, period_int):
            return bt.indicators.MovingAverageSimple(line, period = period_int)

        def WMA(line, period_int):
            return bt.indicators.WeightedMovingAverage(line, period = period_int)

        def DMA(line, smoothfactor_float):
            return bt.indicators.SmoothedMovingAverage(line, period = int(1.0/smoothfactor_float))

        def SUM(line, period_int):
            return bt.indicators.SumN(line, period = period_int)

        def COUNT(line, period_int):
            cond = line > 0
            return bt.indicators.SumN(cond, period = period_int)

        def HHV(line, period_int):
            return bt.indicators.MaxN(line, period = period_int, plot=False)

        def LLV(line, period_int):
            return bt.indicators.MinN(line, period = period_int, plot=False)

        def MAX(line_1, line_2):
            return bt.Max(line_1, line_2)

        def MIN(line_1, line_2):
            return bt.Min(line_1, line_2)


        def CROSS(line_1, line_2):
            return bt.indicators.CrossDown(line_1, line_2)

        def LONGCROSS(line_1, line_2, period_int):
            pass

        def REVERSE(line):
            return line * -1

        def SQRT(line):
            return bt.talib.SQRT(line)

        def POW(base_line, exponent_int):
            exponentiation = base_line
            for i in range(exponent_int-1):
                exponentiation = bt.talib.MULT(exponentiation, base_line)
            return exponentiation

        def COS(line):
            return bt.talib.COS(line)
        
        def SIN(line):
            return bt.talib.SIN(line)
        
        def RANGE(line, lower_line, upper_line):
            is_lower = lower_line < line
            is_upper = upper_line > line
            return bt.And(is_lower, is_upper)

        BETWEEN = RANGE
        
        # logic func
        def IF(cond, line_1, line_2):
            return bt.If(cond, line_1, line_2)

        # ploting func
        def STICKLINE(cond, lw, up, width, bool):
            to_plot = bt.If(cond, up-lw, 0)
            bt.LinePlotterIndicator(to_plot, name="")

        def PLOT(line, name_str):
            if isinstance(line, int):
                bt.LinePlotterIndicator(unitline * line)
            else:
                bt.LinePlotterIndicator(line*1, name=name_str)

        def DRAWTEXT(cond, y_axis, text_str):
            pass

        ABS = abs

        DRAWNULL = unitline * 0


        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        # callback()

        # Paste here TA-FormulaParser output
        # DIF=(EMA(C,12)-EMA(C,26))
        # PLOT(DIF,"DIF")
        # DEA=EMA(DIF,9)
        # PLOT(DEA,"DEA")
        # MACD=2*(DIF-DEA)
        # PLOT(MACD,"MACD")
        # STICKLINE(bt.And(MACD>REF(MACD,1),MACD>=0),MACD,0,2,0)
        # STICKLINE(bt.And(MACD>REF(MACD,1),MACD<0),MACD,0,2,1)
        # FH1=bt.And(bt.And(REF(MACD,1)<REF(MACD,2),REF(MACD,2)<REF(MACD,3)),REF(MACD,3)<REF(MACD,4))
        # FH2=bt.And(MACD>=0,COUNT(MACD>REF(MACD,1),1)==1)
        # FH3=bt.And(bt.And(FH1,FH2),EMA(C,13)>REF(EMA(C,13),1))
        # FH4=bt.And(bt.And(FH1,FH2),ABS((DIF-DEA)/C)<0.018)
        # FH5=bt.And(bt.And(FH1,FH2),MACD<0.10)
        # STICKLINE(bt.Or(bt.Or(FH3,FH4),FH5),0,MACD,2,0)
        # STICKLINE(bt.And(MACD<=REF(MACD,1),MACD<0),0,MACD,2,0)
        # STICKLINE(bt.And(MACD<REF(MACD,1),MACD>0),0,MACD,2,1)

        # N=9
        # M1=3
        # M2=3
        # RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
        # PLOT(RSV,"RSV")
        # K=EMA(RSV,(M1*2-1))
        # PLOT(K,"K")
        # D=EMA(K,(M2*2-1))
        # PLOT(D,"D")
        # J=K*3-D*2
        # PLOT(J,"J")

        操盘线=20
        MID=MA(C,操盘线)
        VART1=POW((C-MID),2)
        VART2=MA(VART1,操盘线)
        VART3=SQRT(VART2)
        UPPER=MID+2*VART3
        LOWER=MID-2*VART3
        # bt.indicators.FindLastIndex(C>5)
        
        主力操盘线=REF(MID,1)
        PLOT(主力操盘线,"主力操盘线")
        # 涨=IF(主力操盘线>REF(主力操盘线,1),主力操盘线,DRAWNULL)
        # PLOT(涨,"涨")
        # 跌=IF(主力操盘线<REF(主力操盘线,1),主力操盘线,DRAWNULL)
        # PLOT(跌,"跌")

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
