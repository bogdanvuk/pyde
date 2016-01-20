java -Xmx500M -cp $CLASSPATH org.antlr.v4.Tool antlr4Parser.g4 antlr4Lexer.g4 -package antlr4
javac *.java

#alias grun='java org.antlr.v4.runtime.misc.TestRig'
