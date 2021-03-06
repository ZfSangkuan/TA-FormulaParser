# TA-FormulaParser

(Ongoing) A Stock Technical Analysis Formula Parser for Backtesting.

Implement the analysis, transformation and backtesting of formulas written based on traditional technical analyze indicators.  
Allows more convenient inheritance and understanding of traditional technical analysis ideas, furthurmore, combined with the rigorous logic of modern quantitative investment.

![flow.png](./flow.png)

## Directories

Regular for Lexer ```./hithinkFlush_formula.l```  
Grammar for Parser ```./hithinkFlush_formula.y```

DFA in Parser, generated by Bison ```./hithinkFlush_formula.output```  
DFA in Parser, generated by Yacc ```./y.output```  

TA-FormulaParser, the executable ```./a.out```

## Quickstart

0. Requirements

Python 2.7 / 3.2 / 3.3 / 3.4 / 3.5 / 3.7  
&nbsp; &nbsp; &nbsp; &nbsp;backtrader >= 1.9  
&nbsp; &nbsp; &nbsp; &nbsp;matplotlib >= 1.4.1  
&nbsp; &nbsp; &nbsp; &nbsp;requests >= 2.25  
Flex 2.5.35 Apple(flex-32)  
Bison (GNU Bison) 3.8.2  

1. Compile

```shell
>bison hithinkFlush_formula.y -d -t -v
>flex hithinkFlush_formula.l
>cc hithinkFlush_formula.tab.c -DYYDEBUG=1
>echo "DIF:=(EMA(C,12)-EMA(C,26)),COLORF0F0F0;" | ./a.out
```  

Results are listed by the end of debug info.  
Copy results to quickstart.py backtrader \_\_init\_\_() function for backtesting:

2. Backtest

```shell
>python3 quickstart.py
```

## Reference

Flex: Lexical analyzer generator  
GNU Bison: Yacc-compatible parser generator  
Backtrader: A feature-rich Python framework for backtesting and trading
