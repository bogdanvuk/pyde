grammar linpath;

main  :  WS? path_ = path WS?
  ;

path
  :  relative_path
  |  absolute_path
  ;

absolute_path
  :  root_=('/' | '~/') rel_path_=relative_path
  ;

relative_path
  :  step_ += step ('/' step_ += step)*
  ;

step  :  variableReference
  |  abbreviatedStep
  |  TOKEN
  ;

abbreviatedStep
  :  '.'
  |  '..'
  ;

variableReference
  :  '$' TOKEN
  ;

PATHSEP
       :'/';

TOKEN : [0-9a-zA-Z_*.\-?]+ ;
WS : [ \t\r\n]+;
