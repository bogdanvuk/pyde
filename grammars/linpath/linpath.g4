grammar linpath;

main : path_ = path EOF;

path
  :  PATHSEP? part_ += part (PATHSEP part_ += part)* (folder_=PATHSEP)?
  ;

part  :  name_=(NAME | HOME | VARIABLE_REFERENCE)
  ;

VARIABLE_REFERENCE
  :  '$' NAME
  ;

PATHSEP
       :'/';
HOME   :'~';

NAME : [0-9a-zA-Z_*.\-?]+ ;
WS : [ \t\r\n]+;
