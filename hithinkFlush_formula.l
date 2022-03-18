%{
    #include "stdio.h"
    #include "y.tab.h"
%}

alpha [a-zA-Z]
digit [0-9]

%%

[-]?{digit}+                { printf("number\n"); return NUMBER; }
[-]?{digit}+\.{digit}{1,6}  { printf("float_number\n"); return FLOAT_NUM; }

(color|COLOR)({alpha}|{digit})*     { printf("flex:color\n"); return COLOR; }
nodraw|NODRAW                       { printf("flex:color\n"); return COLOR; }
LINETHICK({alpha}|{digit})*         { printf("flex:color\n"); return COLOR; }
STICKLINE                           { printf("stickline\n"); return STICKLINE; }

"AND"                   { printf("and\n"); return AND; }
"OR"                    { printf("or\n"); return OR; }

{alpha}({alpha}|{digit})*   { printf("flex:id\n"); return ID; }

"<="                        { printf("le\n"); return LE; }
">="                        { printf("ge\n"); return GE; }
":="                    { printf("flex:assign\n"); return ASSIGN; }

[ \t]                   { ; }
.	                        { printf("flex:%c\n", *yytext); return *yytext; }

%%

int yywrap() {
    return 1;
}