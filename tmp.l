%{
    #include "stdio.h"
    #include "y.tab.h"
%}


alpha [a-zA-Z]
digit [0-9]

%%

[-]?{digit}+                { printf("number\n"); }
[-]?{digit}+\.{digit}{1,6}  { printf("float_number\n"); }

(color|COLOR)({alpha}|{digit})*     { printf("color\n"); }
nodraw|NODRAW                       { printf("color\n"); }
LINETHICK({alpha}|{digit})*         { printf("color\n"); }

{alpha}({alpha}|{digit})*   { printf("id\n"); }

"(?i)and"                   { return AND; }
"(?i)or"                    { return OR; }


\/\/.*                      { ; }
\/\*(.*\n)*.*\*\/           { ; } 
[ \t]*                      { ; }
[\n]                        { countn++; }
.	                        { return *yytext; }
["].*["]                    { return STR; }
['].[']                     { return CHARACTER; }



%%

