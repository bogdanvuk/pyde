// Generated from linpath.g4 by ANTLR 4.5.1
package linpath;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class linpathParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.5.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		VARIABLE_REFERENCE=1, PATHSEP=2, HOME=3, NAME=4, WS=5;
	public static final int
		RULE_main = 0, RULE_path = 1, RULE_part = 2;
	public static final String[] ruleNames = {
		"main", "path", "part"
	};

	private static final String[] _LITERAL_NAMES = {
		null, null, "'/'", "'~'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, "VARIABLE_REFERENCE", "PATHSEP", "HOME", "NAME", "WS"
	};
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "linpath.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public linpathParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class MainContext extends ParserRuleContext {
		public PathContext path_;
		public TerminalNode EOF() { return getToken(linpathParser.EOF, 0); }
		public PathContext path() {
			return getRuleContext(PathContext.class,0);
		}
		public MainContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_main; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterMain(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitMain(this);
		}
	}

	public final MainContext main() throws RecognitionException {
		MainContext _localctx = new MainContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_main);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(6);
			((MainContext)_localctx).path_ = path();
			setState(7);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class PathContext extends ParserRuleContext {
		public PartContext part;
		public List<PartContext> part_ = new ArrayList<PartContext>();
		public Token folder_;
		public List<PartContext> part() {
			return getRuleContexts(PartContext.class);
		}
		public PartContext part(int i) {
			return getRuleContext(PartContext.class,i);
		}
		public List<TerminalNode> PATHSEP() { return getTokens(linpathParser.PATHSEP); }
		public TerminalNode PATHSEP(int i) {
			return getToken(linpathParser.PATHSEP, i);
		}
		public PathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_path; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterPath(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitPath(this);
		}
	}

	public final PathContext path() throws RecognitionException {
		PathContext _localctx = new PathContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_path);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(10);
			_la = _input.LA(1);
			if (_la==PATHSEP) {
				{
				setState(9);
				match(PATHSEP);
				}
			}

			setState(12);
			((PathContext)_localctx).part = part();
			((PathContext)_localctx).part_.add(((PathContext)_localctx).part);
			setState(17);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(13);
					match(PATHSEP);
					setState(14);
					((PathContext)_localctx).part = part();
					((PathContext)_localctx).part_.add(((PathContext)_localctx).part);
					}
					} 
				}
				setState(19);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			}
			setState(21);
			_la = _input.LA(1);
			if (_la==PATHSEP) {
				{
				setState(20);
				((PathContext)_localctx).folder_ = match(PATHSEP);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class PartContext extends ParserRuleContext {
		public Token name_;
		public TerminalNode NAME() { return getToken(linpathParser.NAME, 0); }
		public TerminalNode HOME() { return getToken(linpathParser.HOME, 0); }
		public TerminalNode VARIABLE_REFERENCE() { return getToken(linpathParser.VARIABLE_REFERENCE, 0); }
		public PartContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_part; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterPart(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitPart(this);
		}
	}

	public final PartContext part() throws RecognitionException {
		PartContext _localctx = new PartContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_part);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(23);
			((PartContext)_localctx).name_ = _input.LT(1);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << VARIABLE_REFERENCE) | (1L << HOME) | (1L << NAME))) != 0)) ) {
				((PartContext)_localctx).name_ = (Token)_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\7\34\4\2\t\2\4\3"+
		"\t\3\4\4\t\4\3\2\3\2\3\2\3\3\5\3\r\n\3\3\3\3\3\3\3\7\3\22\n\3\f\3\16\3"+
		"\25\13\3\3\3\5\3\30\n\3\3\4\3\4\3\4\2\2\5\2\4\6\2\3\4\2\3\3\5\6\33\2\b"+
		"\3\2\2\2\4\f\3\2\2\2\6\31\3\2\2\2\b\t\5\4\3\2\t\n\7\2\2\3\n\3\3\2\2\2"+
		"\13\r\7\4\2\2\f\13\3\2\2\2\f\r\3\2\2\2\r\16\3\2\2\2\16\23\5\6\4\2\17\20"+
		"\7\4\2\2\20\22\5\6\4\2\21\17\3\2\2\2\22\25\3\2\2\2\23\21\3\2\2\2\23\24"+
		"\3\2\2\2\24\27\3\2\2\2\25\23\3\2\2\2\26\30\7\4\2\2\27\26\3\2\2\2\27\30"+
		"\3\2\2\2\30\5\3\2\2\2\31\32\t\2\2\2\32\7\3\2\2\2\5\f\23\27";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}