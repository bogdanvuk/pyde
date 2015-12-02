grammar linpath;

main  :  path
  ;

path
  :  relative_path
  |  absolute_path
  ;

absolute_path
  :  '/' relative_path
  |  '~/' relative_path
  ;

relative_path
  :  step ('/' step)*
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
