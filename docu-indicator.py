import backtrader as bt
import backtrader.indicators as btind

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

class OverUnderMovAv(bt.Indicator):
    lines = ('overunder',)
    params = dict(period=20, movav=bt.ind.MovAv.Simple)

    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,

        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[1.0, -1.0],

        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[1.0, -1.0])

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(overunder=dict(ls='--'))

    def _plotlabel(self):
        # This method returns a list of labels that will be displayed
        # behind the name of the indicator on the plot

        # The period must always be there
        plabels = [self.p.period]

        # Put only the moving average if it's not the default one
        plabels += [self.p.movav] * self.p.notdefault('movav')

        return plabels

    def __init__(self):
        movav = self.p.movav(self.data, period=self.p.period)
        self.l.overunder = bt.Cmp(movav, self.data)


class TestStrategy(bt.Strategy):
    params = (
        ('exitbars', 8),
        ('maperiod', 15),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=True):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
        
        self.ouma = OverUnderMovAv()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

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
            # if self.dataclose[0] > self.sma[0]:
            if self.ouma[0] == 1:
                # BUY with default parameters
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            # Already in the market ... we might sell if...

            # ignore no-member error for 
            #   pylint doesn't recognize dynamically-created attributes

            if len(self) >= (self.bar_executed + self.params.exitbars): 
            # if self.dataclose[0] < self.ouma[0]:
                # SELL with all possible default parameters
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
    
    # def stop(self):
    #     self.log('(MA Period %2d) Ending Value %.2f' %
    #              (self.params.maperiod, self.broker.getvalue()), doprint=True)



if __name__ == '__main__':
    print('\033[1;36m')  # terminal output colorize
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
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)
    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcash(1000.0)
    # cerebro.broker.setcommission(commission=0.001)  # 0.1%


    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()

    # terminal output colorize
    print('\033[0m')    
