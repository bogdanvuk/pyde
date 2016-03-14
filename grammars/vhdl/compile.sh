java -Xmx500M -cp $CLASSPATH org.antlr.v4.Tool vhdl.g4 -package vhdl
javac *.java
cd ..
java pyinterface.GrammarJsonDump vhdl vhdl/vhdlAST.js

#alias grun='java org.antlr.v4.runtime.misc.TestRig'
