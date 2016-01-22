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
		RULE_main = 0, RULE_path = 1, RULE_absolute_path = 2, RULE_rel_path = 3, 
		RULE_part = 4;
	public static final String[] ruleNames = {
		"main", "path", "absolute_path", "rel_path", "part"
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
		public PathContext path() {
			return getRuleContext(PathContext.class,0);
		}
		public List<TerminalNode> WS() { return getTokens(linpathParser.WS); }
		public TerminalNode WS(int i) {
			return getToken(linpathParser.WS, i);
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
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(11);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				{
				setState(10);
				match(WS);
				}
				break;
			}
			setState(13);
			((MainContext)_localctx).path_ = path();
			setState(15);
			_la = _input.LA(1);
			if (_la==WS) {
				{
				setState(14);
				match(WS);
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

	public static class PathContext extends ParserRuleContext {
		public Rel_pathContext rel_path() {
			return getRuleContext(Rel_pathContext.class,0);
		}
		public Absolute_pathContext absolute_path() {
			return getRuleContext(Absolute_pathContext.class,0);
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
		try {
			setState(19);
			switch (_input.LA(1)) {
			case EOF:
			case VARIABLE_REFERENCE:
			case HOME:
			case NAME:
			case WS:
				enterOuterAlt(_localctx, 1);
				{
				setState(17);
				rel_path();
				}
				break;
			case PATHSEP:
				enterOuterAlt(_localctx, 2);
				{
				setState(18);
				absolute_path();
				}
				break;
			default:
				throw new NoViableAltException(this);
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

	public static class Absolute_pathContext extends ParserRuleContext {
		public Rel_pathContext rel_path_;
		public Rel_pathContext rel_path() {
			return getRuleContext(Rel_pathContext.class,0);
		}
		public Absolute_pathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_absolute_path; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterAbsolute_path(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitAbsolute_path(this);
		}
	}

	public final Absolute_pathContext absolute_path() throws RecognitionException {
		Absolute_pathContext _localctx = new Absolute_pathContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_absolute_path);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(21);
			match(PATHSEP);
			setState(22);
			((Absolute_pathContext)_localctx).rel_path_ = rel_path();
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

	public static class Rel_pathContext extends ParserRuleContext {
		public PartContext part;
		public List<PartContext> part_ = new ArrayList<PartContext>();
		public List<PartContext> part() {
			return getRuleContexts(PartContext.class);
		}
		public PartContext part(int i) {
			return getRuleContext(PartContext.class,i);
		}
		public Rel_pathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rel_path; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterRel_path(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitRel_path(this);
		}
	}

	public final Rel_pathContext rel_path() throws RecognitionException {
		Rel_pathContext _localctx = new Rel_pathContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_rel_path);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(27);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << VARIABLE_REFERENCE) | (1L << HOME) | (1L << NAME))) != 0)) {
				{
				{
				setState(24);
				((Rel_pathContext)_localctx).part = part();
				((Rel_pathContext)_localctx).part_.add(((Rel_pathContext)_localctx).part);
				}
				}
				setState(29);
				_errHandler.sync(this);
				_la = _input.LA(1);
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
		public Token folder_;
		public TerminalNode NAME() { return getToken(linpathParser.NAME, 0); }
		public TerminalNode HOME() { return getToken(linpathParser.HOME, 0); }
		public TerminalNode VARIABLE_REFERENCE() { return getToken(linpathParser.VARIABLE_REFERENCE, 0); }
		public TerminalNode PATHSEP() { return getToken(linpathParser.PATHSEP, 0); }
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
		enterRule(_localctx, 8, RULE_part);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(30);
			((PartContext)_localctx).name_ = _input.LT(1);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << VARIABLE_REFERENCE) | (1L << HOME) | (1L << NAME))) != 0)) ) {
				((PartContext)_localctx).name_ = (Token)_errHandler.recoverInline(this);
			} else {
				consume();
			}
			setState(32);
			_la = _input.LA(1);
			if (_la==PATHSEP) {
				{
				setState(31);
				((PartContext)_localctx).folder_ = match(PATHSEP);
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

	public static final String _serializedATN =
		"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\7%\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\5\2\16\n\2\3\2\3\2\5\2\22\n\2\3\3\3\3\5"+
		"\3\26\n\3\3\4\3\4\3\4\3\5\7\5\34\n\5\f\5\16\5\37\13\5\3\6\3\6\5\6#\n\6"+
		"\3\6\2\2\7\2\4\6\b\n\2\3\4\2\3\3\5\6$\2\r\3\2\2\2\4\25\3\2\2\2\6\27\3"+
		"\2\2\2\b\35\3\2\2\2\n \3\2\2\2\f\16\7\7\2\2\r\f\3\2\2\2\r\16\3\2\2\2\16"+
		"\17\3\2\2\2\17\21\5\4\3\2\20\22\7\7\2\2\21\20\3\2\2\2\21\22\3\2\2\2\22"+
		"\3\3\2\2\2\23\26\5\b\5\2\24\26\5\6\4\2\25\23\3\2\2\2\25\24\3\2\2\2\26"+
		"\5\3\2\2\2\27\30\7\4\2\2\30\31\5\b\5\2\31\7\3\2\2\2\32\34\5\n\6\2\33\32"+
		"\3\2\2\2\34\37\3\2\2\2\35\33\3\2\2\2\35\36\3\2\2\2\36\t\3\2\2\2\37\35"+
		"\3\2\2\2 \"\t\2\2\2!#\7\4\2\2\"!\3\2\2\2\"#\3\2\2\2#\13\3\2\2\2\7\r\21"+
		"\25\35\"";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}