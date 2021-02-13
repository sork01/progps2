// Mikael Forsberg <miforsb@kth.se>
// Robin Gunning <rgunning@kth.se>
// Skapad 2015-11-18

/**
 * Represents an UP or DOWN instruction.
 * 
 * @author Mikael Forsberg
 * @author Robin Gunning
 * @version 2015-11-18
 */
public class PenCommand implements Command
{
    /**
     * Enumerates the available pen states.
     */
    public enum State
    {
        UP, DOWN
    };
    
    /**
     * Create a new pen command.
     * 
     * @param st Pen state
     */
    public PenCommand(State st)
    {
        state = st;
    }
    
    /**
     * Pen state.
     */
    public State state;
}
