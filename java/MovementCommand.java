// Mikael Forsberg <miforsb@kth.se>
// Robin Gunning <rgunning@kth.se>
// Skapad 2015-11-18

/**
 * Represents a FORW or a BACK instruction.
 * 
 * @author Mikael Forsberg
 * @author Robin Gunning
 * @version 2015-11-18
 */
public class MovementCommand implements Command
{
    /**
     * Enumerates the available directions.
     */
    public enum Direction
    {
        FORWARD, BACK
    };
    
    /**
     * Creates a new movement command.
     *
     * @param dir Direction of movement
     * @param magn Length of movement
     */
    public MovementCommand(Direction dir, int magn)
    {
        direction = dir;
        magnitude = magn;
    }
    
    /**
     * Direction of movement.
     */
    public Direction direction;
    
    /**
     * Length of movement.
     */
    public int magnitude;
}
