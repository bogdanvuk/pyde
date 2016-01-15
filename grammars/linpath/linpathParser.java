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
		T__0=1, T__1=2, T__2=3, T__3=4, PATHSEP=5, TOKEN=6, WS=7;
	public static final int
		RULE_main = 0, RULE_path = 1, RULE_absolute_path = 2, RULE_relative_path = 3, 
		RULE_step = 4, RULE_abbreviatedStep = 5, RULE_variableReference = 6;
	public static final String[] ruleNames = {
		"main", "path", "absolute_path", "relative_path", "step", "abbreviatedStep", 
		"variableReference"
	};

	private static final String[] _LITERAL_NAMES = {
		null, "'~/'", "'.'", "'..'", "'$'", "'/'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, null, null, null, null, "PATHSEP", "TOKEN", "WS"
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
			setState(15);
			_la = _input.LA(1);
			if (_la==WS) {
				{
				setState(14);
				match(WS);
				}
			}

			setState(17);
			((MainContext)_localctx).path_ = path();
			setState(19);
			_la = _input.LA(1);
			if (_la==WS) {
				{
				setState(18);
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
		public Relative_pathContext relative_path() {
			return getRuleContext(Relative_pathContext.class,0);
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
			setState(23);
			switch (_input.LA(1)) {
			case T__1:
			case T__2:
			case T__3:
			case TOKEN:
				enterOuterAlt(_localctx, 1);
				{
				setState(21);
				relative_path();
				}
				break;
			case T__0:
			case PATHSEP:
				enterOuterAlt(_localctx, 2);
				{
				setState(22);
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
		public Token root_;
		public Relative_pathContext rel_path_;
		public Relative_pathContext relative_path() {
			return getRuleContext(Relative_pathContext.class,0);
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
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(25);
			((Absolute_pathContext)_localctx).root_ = _input.LT(1);
			_la = _input.LA(1);
			if ( !(_la==T__0 || _la==PATHSEP) ) {
				((Absolute_pathContext)_localctx).root_ = (Token)_errHandler.recoverInline(this);
			} else {
				consume();
			}
			setState(26);
			((Absolute_pathContext)_localctx).rel_path_ = relative_path();
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

	public static class Relative_pathContext extends ParserRuleContext {
		public StepContext step;
		public List<StepContext> step_ = new ArrayList<StepContext>();
		public List<StepContext> step() {
			return getRuleContexts(StepContext.class);
		}
		public StepContext step(int i) {
			return getRuleContext(StepContext.class,i);
		}
		public Relative_pathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relative_path; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterRelative_path(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitRelative_path(this);
		}
	}

	public final Relative_pathContext relative_path() throws RecognitionException {
		Relative_pathContext _localctx = new Relative_pathContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_relative_path);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(28);
			((Relative_pathContext)_localctx).step = step();
			((Relative_pathContext)_localctx).step_.add(((Relative_pathContext)_localctx).step);
			setState(33);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==PATHSEP) {
				{
				{
				setState(29);
				match(PATHSEP);
				setState(30);
				((Relative_pathContext)_localctx).step = step();
				((Relative_pathContext)_localctx).step_.add(((Relative_pathContext)_localctx).step);
				}
				}
				setState(35);
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

	public static class StepContext extends ParserRuleContext {
		public VariableReferenceContext variableReference() {
			return getRuleContext(VariableReferenceContext.class,0);
		}
		public AbbreviatedStepContext abbreviatedStep() {
			return getRuleContext(AbbreviatedStepContext.class,0);
		}
		public TerminalNode TOKEN() { return getToken(linpathParser.TOKEN, 0); }
		public StepContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_step; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterStep(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitStep(this);
		}
	}

	public final StepContext step() throws RecognitionException {
		StepContext _localctx = new StepContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_step);
		try {
			setState(39);
			switch (_input.LA(1)) {
			case T__3:
				enterOuterAlt(_localctx, 1);
				{
				setState(36);
				variableReference();
				}
				break;
			case T__1:
			case T__2:
				enterOuterAlt(_localctx, 2);
				{
				setState(37);
				abbreviatedStep();
				}
				break;
			case TOKEN:
				enterOuterAlt(_localctx, 3);
				{
				setState(38);
				match(TOKEN);
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

	public static class AbbreviatedStepContext extends ParserRuleContext {
		public AbbreviatedStepContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_abbreviatedStep; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterAbbreviatedStep(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitAbbreviatedStep(this);
		}
	}

	public final AbbreviatedStepContext abbreviatedStep() throws RecognitionException {
		AbbreviatedStepContext _localctx = new AbbreviatedStepContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_abbreviatedStep);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(41);
			_la = _input.LA(1);
			if ( !(_la==T__1 || _la==T__2) ) {
			_errHandler.recoverInline(this);
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

	public static class VariableReferenceContext extends ParserRuleContext {
		public TerminalNode TOKEN() { return getToken(linpathParser.TOKEN, 0); }
		public VariableReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_variableReference; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).enterVariableReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof linpathListener ) ((linpathListener)listener).exitVariableReference(this);
		}
	}

	public final VariableReferenceContext variableReference() throws RecognitionException {
		VariableReferenceContext _localctx = new VariableReferenceContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_variableReference);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(43);
			match(T__3);
			setState(44);
			match(TOKEN);
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
		"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\t\61\4\2\t\2\4\3"+
		"\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\3\2\5\2\22\n\2\3\2\3\2\5"+
		"\2\26\n\2\3\3\3\3\5\3\32\n\3\3\4\3\4\3\4\3\5\3\5\3\5\7\5\"\n\5\f\5\16"+
		"\5%\13\5\3\6\3\6\3\6\5\6*\n\6\3\7\3\7\3\b\3\b\3\b\3\b\2\2\t\2\4\6\b\n"+
		"\f\16\2\4\4\2\3\3\7\7\3\2\4\5/\2\21\3\2\2\2\4\31\3\2\2\2\6\33\3\2\2\2"+
		"\b\36\3\2\2\2\n)\3\2\2\2\f+\3\2\2\2\16-\3\2\2\2\20\22\7\t\2\2\21\20\3"+
		"\2\2\2\21\22\3\2\2\2\22\23\3\2\2\2\23\25\5\4\3\2\24\26\7\t\2\2\25\24\3"+
		"\2\2\2\25\26\3\2\2\2\26\3\3\2\2\2\27\32\5\b\5\2\30\32\5\6\4\2\31\27\3"+
		"\2\2\2\31\30\3\2\2\2\32\5\3\2\2\2\33\34\t\2\2\2\34\35\5\b\5\2\35\7\3\2"+
		"\2\2\36#\5\n\6\2\37 \7\7\2\2 \"\5\n\6\2!\37\3\2\2\2\"%\3\2\2\2#!\3\2\2"+
		"\2#$\3\2\2\2$\t\3\2\2\2%#\3\2\2\2&*\5\16\b\2\'*\5\f\7\2(*\7\b\2\2)&\3"+
		"\2\2\2)\'\3\2\2\2)(\3\2\2\2*\13\3\2\2\2+,\t\3\2\2,\r\3\2\2\2-.\7\6\2\2"+
		"./\7\b\2\2/\17\3\2\2\2\7\21\25\31#)";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}