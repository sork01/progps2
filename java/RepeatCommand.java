// Mikael Forsberg <miforsb@kth.se>
// Robin Gunning <rgunning@kth.se>
// Skapad 2015-11-18

import java.util.LinkedList;

/**
 * Represents a REP instruction.
 * 
 * @author Mikael Forsberg
 * @author Robin Gunning
 * @version 2015-11-18
 */
public class RepeatCommand implements Command
{
    /**
     *  Creates a new repeat command.
     * 
     * @param n Number of repetitions
     */
    public RepeatCommand(int n)
    {
        count = n;
    }
    
    /**
     * Number of repetitions.
     */
    public int count;
    
    /**
     * Inner parse tree (instructions to be repeated).
     */
    public LinkedList<Command> commands = new LinkedList<Command>();
}
