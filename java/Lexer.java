// Mikael Forsberg <miforsb@kth.se>
// Robin Gunning <rgunning@kth.se>
// Skapad 2015-11-18

import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * Lexer takes a text and chops it up into smaller chunks
 * called tokens.
 *
 * @author Mikael Forsberg
 * @author Robin Gunning
 * @version 2015-11-18
 */
public class Lexer
{
    /**
     * Creates a new Lexer.
     * 
     * @param data Source data (source code) to tokenize.
     */
    public Lexer(String data)
    {
        this.data = data.toUpperCase();
        length = this.data.length();
        pos = 0;
    }
    
    /**
     * Computes and returns the next token.
     */
    public Token next()
    {
        if (pos == length)
        {
            return null;
        }
        
        if (data.startsWith("REP", pos))
        {
            pos += 3;
            return new Token(Token.Type.KEYWORD_REP, "REP");
        }
        else if (data.startsWith("FORW", pos))
        {
            pos += 4;
            return new Token(Token.Type.KEYWORD_FORW, "FORW");
        }
        else if (data.startsWith("BACK", pos))
        {
            pos += 4;
            return new Token(Token.Type.KEYWORD_BACK, "BACK");
        }
        else if (data.startsWith("LEFT", pos))
        {
            pos += 4;
            return new Token(Token.Type.KEYWORD_LEFT, "LEFT");
        }
        else if (data.startsWith("RIGHT", pos))
        {
            pos += 5;
            return new Token(Token.Type.KEYWORD_RIGHT, "RIGHT");
        }
        else if (data.startsWith("UP", pos))
        {
            pos += 2;
            return new Token(Token.Type.KEYWORD_UP, "UP");
        }
        else if (data.startsWith("DOWN", pos))
        {
            pos += 4;
            return new Token(Token.Type.KEYWORD_DOWN, "DOWN");
        }
        else if (data.startsWith("COLOR", pos))
        {
            pos += 5;
            return new Token(Token.Type.KEYWORD_COLOR, "COLOR");
        }
        else if (data.startsWith(".", pos))
        {
            pos += 1;
            return new Token(Token.Type.END_STATEMENT, ".");
        }
        else if (data.startsWith("\"", pos))
        {
            pos += 1;
            return new Token(Token.Type.QUOTE, "\"");
        }
        else
        {
            Matcher match;
            match = colorhex.matcher(data).region(pos, length);
            
            if (match.lookingAt())
            {
                pos += 7;
                return new Token(Token.Type.COLOR_HEX, match.group());
            }
            
            match = positive_int.matcher(data).region(pos, length);
            
            if (match.lookingAt())
            {
                pos += match.group().length();
                return new Token(Token.Type.POSITIVE_INTEGER, match.group());
            }
            
            match = comment.matcher(data).region(pos, length);
            
            if (match.lookingAt())
            {
                pos += match.group().length();
                return new Token(Token.Type.COMMENT, match.group());
            }
            
            match = whitespace.matcher(data).region(pos, length);
            
            if (match.lookingAt())
            {
                pos += match.group().length();
                return new Token(Token.Type.WHITESPACE, match.group());
            }
            
            match = nonwhitespace.matcher(data).region(pos, length);
            
            if (match.lookingAt())
            {
                pos += match.group().length();
                return new Token(Token.Type.NONWHITESPACE, match.group());
            }
            
            pos = length;
            return new Token(Token.Type.UNKNOWN, "");
        }
    }
    
    /**
     * If there are more tokens available, returns true, otherwise returns false.
     */
    public boolean hasNext()
    {
        return (pos != length);
    }
    
    /**
     * Rewind source data n characters.
     */
    public void putBack(int n)
    {
        pos -= n;
    }
    
    /**
     * Rewind source data by the length of a given string.
     */
    public void putBack(String s)
    {
        pos -= s.length();
    }
    
    /**
     * Computes and returns the last line number containing
     * instructional data.
     */
    public int line()
    {
        int line_seen = 1;
        int line_reached = 1;
        
        Lexer L = new Lexer(data);
        
        while (L.pos < pos)
        {
            Token tok = L.next();
            
            line_seen += countNewlines(tok.text);
            
            if (tok.type != Token.Type.COMMENT && tok.type != Token.Type.WHITESPACE)
            {
                line_reached = line_seen;
            }
        }
        
        return line_reached;
    }
    
    /**
     * Computes and returns the number of new lines in a given string.
     */
    private int countNewlines(String s)
    {
        int last = 0;
        int count = 0;
        
        while (last < pos)
        {
            last = s.indexOf("\n", last);
            
            if (last != -1)
            {
                count++;
                last += 1;
            }
            else
            {
                break;
            }
        }
        
        return count;
    }
    
    /**
     * The regex pattern for colorhex.
     */
    private Pattern colorhex = Pattern.compile("#[a-fA-F0-9]{6}");
    
    /**
     * The regex pattern for positive integers.
     */
    private Pattern positive_int = Pattern.compile("[1-9](\\d+)?");
    
    /**
     * The regex pattern for comments.
     */
    private Pattern comment = Pattern.compile("%[^\\n]*");
    
    /**
     * The regex pattern for whitespace.
     */
    private Pattern whitespace = Pattern.compile("\\s+");
    
    /**
     * The regex pattern for non-whitespace.
     */
    private Pattern nonwhitespace = Pattern.compile("[^\\s]+");
    
    /**
     * Source data to tokenize.
     */
    private String data;
    
    /**
     * Current position in source data.
     */
    private int pos;
    
    /**
     * Length of source data.
     */
    private int length;
}
