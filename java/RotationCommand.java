// Mikael Forsberg <miforsb@kth.se>
// Robin Gunning <rgunning@kth.se>
// Skapad 2015-11-18

/**
 * Represents a LEFT or a RIGHT instruction. Why not just
 * use signed numbers for the direction?
 * 
 * @author Mikael Forsberg
 * @author Robin Gunning
 * @version 2015-11-18
 */
public class RotationCommand implements Command
{
    /**
     * Enumerates the directions.
     */
    public enum Direction
    {
        LEFT, RIGHT
    };
    
    /**
     * Creates a new rotation command.
     * 
     * @param dir Direction of rotation
     * @param angle Angle of rotation
     */
    public RotationCommand(Direction dir, int angle)
    {
        direction = dir;
        this.angle = angle;
    }
    
    /**
     * Direction of rotation.
     */
    public Direction direction;
    
    /**
     * Angle of rotation.
     */
    public int angle;
}
