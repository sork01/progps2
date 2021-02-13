// Mikael Forsberg <miforsb@kth.se>
// Robin Gunning <rgunning@kth.se>
// Skapad 2015-11-18

/**
 * Represents a single token.
 * 
 * @author Mikael Forsberg
 * @author Robin Gunning
 * @version 2015-11-18
 */
public class Token
{
    /**
     * Enumerates the different types of tokens.
     */
    public enum Type
    {
        KEYWORD_FORW,
        KEYWORD_BACK,
        KEYWORD_LEFT,
        KEYWORD_RIGHT,
        KEYWORD_UP,
        KEYWORD_DOWN,
        KEYWORD_COLOR,
        KEYWORD_REP,
        COLOR_HEX,
        QUOTE,
        END_STATEMENT,
        POSITIVE_INTEGER,
        COMMENT,
        WHITESPACE,
        NONWHITESPACE,
        UNKNOWN,
    };
    
    /**
     * Type of this Token.
     */
    public Type type;
    
    /**
     * Text that matched a specific token.
     */
    public String text;
    
    /**
     * Creates a new Token.
     * 
     * @param type Token type
     * @param text Text that matched this type of token
     */
    public Token(Type type, String text)
    {
        this.type = type;
        this.text = text;
    }
}
