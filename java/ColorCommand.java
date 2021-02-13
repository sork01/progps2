// Mikael Forsberg <miforsb@kth.se>
// Robin Gunning <rgunning@kth.se>
// Skapad 2015-11-18

/**
 * Represents a COLOR instruction.
 * 
 * @author Mikael Forsberg
 * @author Robin Gunning
 * @version 2015-11-18
 */
public class ColorCommand implements Command
{
    /**
     *  Creates a new color command.
     * 
     * @param color Hexadecimal color value
     */
    public ColorCommand(String color)
    {
        this.color = color;
    }
    
    /**
     * Hexadecimal color value.
     */
    public String color;
}
