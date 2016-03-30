java -Xmx500M -cp $CLASSPATH org.antlr.v4.Tool linpath.g4 -package linpath
javac *.java
cd ..
java pyinterface.GrammarJsonDump linpath linpath/linpathAST.js
