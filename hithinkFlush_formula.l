%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "hithinkFlush_formula.tab.h"

    char* dup4val(char* yytext) {
        int len = strlen(yytext);
        char* yylval = (char*) malloc(++len * sizeof(char));
        strcpy(yylval, yytext);
        return yylval;
    }
%}

alpha [a-zA-Z]
digit [0-9]
han [\xE4-\xE9][\x80-\xBF][\x80-\xBF]

%%

{digit}+                { printf("flex:%s\n", yytext); yylval.sval = dup4val(yytext); return NUMBER; }
{digit}+\.{digit}+      { printf("flex:%s\n", yytext); yylval.sval = dup4val(yytext); return FLOAT_NUM; }

(color|COLOR)({alpha}|{digit})*     { printf("flex:%s\n", yytext); yylval.sval = dup4val(yytext); return COLOR; }
nodraw|NODRAW                       { printf("flex:%s\n", yytext); yylval.sval = dup4val(yytext); return COLOR; }
LINETHICK({alpha}|{digit})*         { printf("flex:%s\n", yytext); yylval.sval = dup4val(yytext); return COLOR; }
STICKLINE                           { printf("flex:%s\n", yytext); yylval.sval = dup4val(yytext); return STICKLINE; }

"AND"                   { printf("and\n"); yylval.sval = dup4val(yytext); return AND; }
"OR"                    { printf("or\n"); yylval.sval = dup4val(yytext); return OR; }

({han}|{alpha})({han}|{alpha}|{digit})*   { printf("flex:%s\n", yytext); yylval.sval = dup4val(yytext); return ID; }

"<="                        { printf("le\n"); yylval.sval = dup4val(yytext); return LE; }
">="                        { printf("ge\n"); yylval.sval = dup4val(yytext); return GE; }
":="                    { printf("assign\n"); yylval.sval = dup4val(yytext); return ASSIGN; }
":"                     { printf("assignplot\n"); yylval.sval = dup4val(yytext); return ASSIGNPLOT; }

[ \t]                   { ; }
.	                        { printf("lex:%c\n", *yytext); yylval.sval = dup4val(yytext); return *yytext; }

%%

int yywrap() {
    return 1;
}