%{
    #include "lex.yy.c"
    #include "stdio.h"
    
    void yyerror(const char *s) {
        fprintf( stderr, "%s\n", s );
    }

    #define YYDEBUG 1

%}


%start lines

%token ASSIGN ID
%token COLOR STICKLINE

%left AND OR
%nonassoc '>' '<' '=' LE GE
%left '-' '+'
%left '*' '/'

%token NUMBER FLOAT_NUM 


%%

lines       : /* empty */
            | lines line 
            ;

line        : line_body line_tail ';' ;

line_tail   : /* empty */
            | line_tail color_state
            ;

color_state : ',' COLOR 
            ;

line_body   : statement
            | plotment
            ;

statement   : ID ASSIGN expr 
            ;

/* assign_plot */

plotment    : STICKLINE '(' expr ')'
            ;

expr        : '(' expr ')'
            | expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr '>' expr
            | expr '<' expr
            | expr '=' expr
            | expr LE expr
            | expr GE expr
            | expr AND expr
            | expr OR expr
            | func
            | ID
            | NUMBER
            | FLOAT_NUM
            ;

func        : ID '(' params ')'
            ;

params      : expr
            | params ',' expr
            ;

%%

int main() {
    yydebug = 1;
    return yyparse();
}
