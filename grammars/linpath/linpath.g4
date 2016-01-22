grammar linpath;

main  :  WS? path_ = path WS?
  ;

path
  :  rel_path
  |  absolute_path
  ;

absolute_path
  :  '/' rel_path_=rel_path
  ;

rel_path
  :  part_ += part (PATHSEP part_ += part)* (folder_=PATHSEP)?
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
