%{
    #include "lex.yy.c"
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    
    void yyerror(const char *s) {
        fprintf( stderr, "%s\n", s );
    }

    #define YYDEBUG 1

    char py_repr[1024];

    char* strmrg(char** s, int* free_bits) {
        char* ss = (char*) malloc(1 * sizeof(char));
        return ss;
    }

    char* strmrg1(char* s1) {
        int len = strlen(s1);
        char* ss = (char*) malloc(++len * sizeof(char));
        strcpy(ss, s1);

        return ss;
    }

    char* strmrg2(char* s0, char* s1, int free_bit) {
        int len = strlen(s0) + strlen(s1);
        char* ss = (char*) malloc(++len * sizeof(char));
        strcpy(ss, s0);
        strcat(ss, s1);

        switch(free_bit) {
            case 0:
                free(s0);
                break;
            case 1:
                free(s1);
                break;
            case 2:
                free(s0);
                free(s1);
                break;
        }

        return ss;
    }

    char* strmrg3(char* s1, char* s2, char* s3, int free_bit) {
        int len = strlen(s1) + strlen(s2) + strlen(s3);
        char* ss = (char*) malloc(++len * sizeof(char));
        strcpy(ss, s1);
        strcat(ss, s2);
        strcat(ss, s3);

        if(free_bit == 1) {
            free(s1); free(s3);
        }else if(free_bit == 0) {
            free(s2);
        }else if(free_bit == 2) {
            free(s1); free(s2);
        }else if(free_bit == 3) {
            free(s3);
        }
        
        return ss;
    }

    char* strmrg4(char* s0, char* s1, char* s2, char* s3) {
        int len = strlen(s0) + strlen(s1) + strlen(s2) + strlen(s3);
        char* ss = (char*) malloc(++len * sizeof(char));
        strcpy(ss, s0);
        strcat(ss, s1);
        strcat(ss, s2);
        strcat(ss, s3);
        // free(s0); 
        free(s2);

        return ss;
    }

    char* strmrg5(char* s0, char* s1, char* s2, char* s3, char* s4) {
        int len = strlen(s0) + strlen(s1) + strlen(s2) + strlen(s3) + strlen(s4);
        char* ss = (char*) malloc(++len * sizeof(char));
        strcpy(ss, s0);
        strcat(ss, s1);
        strcat(ss, s2);
        strcat(ss, s3);
        strcat(ss, s4);
        free(s1); free(s3);

        return ss;
    }

    char* strmrg8(char* s0, char* s1, char* s2, char* s3, char* s4, char* s5, char* s6, char* s7) {
        int len = strlen(s0) + strlen(s1) + strlen(s2) + strlen(s3) + strlen(s4) + strlen(s5) + strlen(s6) + strlen(s7);
        char* ss = (char*) malloc(++len * sizeof(char));
        strcpy(ss, s0);
        strcat(ss, s1);
        strcat(ss, s2);
        strcat(ss, s3);
        strcat(ss, s4);
        strcat(ss, s5);
        strcat(ss, s6);
        strcat(ss, s7);
        free(s0); free(s2);

        return ss;
    }

%}


%start lines

%union {
    int ival;
    double dval;
    char* sval;
}

%type <sval> lines line line_body expr statement plotment func params string

%token <sval> COLOR STICKLINE ID
%token <sval> NUMBER FLOAT_NUM 

%printer { fprintf (yyo, "\"%s\"", $$); } <sval>;

%nonassoc ASSIGN ASSIGNPLOT
%left AND OR
%nonassoc '>' '<' '=' LE GE
%left '-' '+'
%left '*' '/'
%precedence NEG


%%

lines       : /* empty */       { $$ = strmrg1(""); }
            | lines line        {
                                    $$ = strmrg2($1, $2, 2);
                                    strcpy(py_repr, $$);
                                    printf("\nPY_REPR:\n%s\n\n", py_repr);
                                }
            ;

line        : line_body line_tail ';'   {
                                            $$ = strmrg2($1, "\n", 0);  
                                        }
            ;

line_tail   : /* empty */
            | line_tail color_state
            ;

color_state : ',' COLOR 
            ;

line_body   : statement         { $$ = strmrg1($1); }
            | plotment          { $$ = strmrg1($1); } 
            ;

statement   : ID ASSIGN expr    {
                                    $$ = strmrg3($1, "=", $3, 3);
                                }
            | ID ASSIGNPLOT expr {
                                    $$ = strmrg8($1, "=", $3, "\nPLOT(", $1, ",\"", $1, "\")");
                                }
            ;

/* assign_plot */

plotment    : STICKLINE '(' params ')' {
                                    $$ = strmrg3("STICKLINE(", $3, ")", 0);
                                }
            | func              { $$ = strmrg1($1); }
            ;

expr        : '(' expr ')'      {
                                    $$ = strmrg3("(", $2, ")", 0);
                                }
            | expr '+' expr     {
                                    $$ = strmrg3($1, "+", $3, 1);
                                }
            | expr '-' expr     {
                                    $$ = strmrg3($1, "-", $3, 1);
                                }
            | '-' expr %prec NEG{
                                    $$ = strmrg2("-", $2, 1);
                                }
            | expr '*' expr     {
                                    $$ = strmrg3($1, "*", $3, 1);
                                }
            | expr '/' expr     {
                                    $$ = strmrg3($1, "/", $3, 1);
                                }
            | expr '>' expr     {
                                    $$ = strmrg3($1, ">", $3, 1);
                                }
            | expr '<' expr     {
                                    $$ = strmrg3($1, "<", $3, 1);
                                }
            | expr '=' expr     {
                                    $$ = strmrg3($1, "==", $3, 1);
                                }
            | expr LE expr      {
                                    $$ = strmrg3($1, "<=", $3, 1);
                                }
            | expr GE expr      {
                                    $$ = strmrg3($1, ">=", $3, 1);
                                }
            | expr AND expr     {
                                    $$ = strmrg5("bt.And(", $1, ",", $3, ")");
                                }
            | expr OR expr      {
                                    $$ = strmrg5("bt.Or(", $1, ",", $3, ")");
                                }
            | func              {   $$ = strmrg1($1); }
            | ID                {   $$ = strmrg1($1); }
            | ID '[' NUMBER ']' {   
                                    $$ = strmrg5("REF(", $1, ",", $3, ")"); 
                                }
            | NUMBER            {   $$ = strmrg1($1); }
            | FLOAT_NUM         {   $$ = strmrg1($1); }
            ;

func        : ID '(' params ')' {
                                    $$ = strmrg4($1, "(", $3, ")");
                                }
            ;

string      : '\'' ID '\''      {   $$ = strmrg3("\"", $2, "\"", 0); }

params      : expr              { $$ = strmrg1($1); }
            | params ',' expr   { $$ = strmrg3($1, ",", $3, 1); }
            | params ',' string { $$ = strmrg3($1, ",", $3, 1); }
            ;

%%

int main() {
    yydebug = 1;
    return yyparse();
}
