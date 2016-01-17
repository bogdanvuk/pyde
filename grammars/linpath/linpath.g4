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
  :  (part_ += part)*
  ;

part  :  name_=(NAME | HOME | VARIABLE_REFERENCE) (folder_='/')?
  ;

VARIABLE_REFERENCE
  :  '$' NAME
  ;

PATHSEP
       :'/';
HOME   :'~';

NAME : [0-9a-zA-Z_*.\-?]+ ;
WS : [ \t\r\n]+;
