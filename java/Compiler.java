// Mikael Forsberg <miforsb@kth.se>
// Robin Gunning <rgunning@kth.se>
// Skapad 2015-11-18

import java.util.LinkedList;
import java.lang.Math;
import java.util.Scanner;
import java.lang.StringBuilder;

/**
 * Compiler takes a parsetree and outputs the line segments generated
 * by the program.
 *
 * @author Mikael Forsberg
 * @author Robin Gunning
 * @version 2015-11-18
 */
public class Compiler
{
    /**
     * Creates a new compiler.
     * 
     * @param parsetree Parse tree to compile
     */
    public Compiler(LinkedList<Command> parsetree)
    {
        this.parsetree = parsetree;
    }
    
    /**
     * Main method for directly lexing, parsing and compiling
     * a program given on standard input.
     */
    public static void main(String[] args)
    {
        Scanner sc = new Scanner(System.in);
        StringBuilder data = new StringBuilder();
        
        // read everything off standard input
        while (sc.hasNext())
        {
            data.append(sc.nextLine());
            data.append("\n");
        }
        
        // this handles "the empty program"
        if (data.length() == 0)
        {
            System.out.println();
            System.exit(0);
        }
        
        Parser p = new Parser(new Lexer(data.toString()));
        LinkedList<Command> parsetree = p.parse();
        
        if (parsetree != null)
        {
            Compiler c = new Compiler(parsetree);
            c.compile();
        }
    }
    
    /**
     * Compile the parsetree.
     */
    public void compile()
    {
        execute(parsetree);
    }
    
    /**
     * Executes a parse tree, printing any generated line segments.
     *
     * @param commands Parse tree to execute
     */
    public void execute(LinkedList<Command> commands)
    {
        for (Command c : commands)
        {
            if (c instanceof MovementCommand)
            {
                MovementCommand cc = (MovementCommand) c;
                
                double oldx = x;
                double oldy = y;
                
                if (cc.direction == MovementCommand.Direction.FORWARD)
                {
                    x = x + cc.magnitude * Math.cos(angle);
                    y = y + cc.magnitude * Math.sin(angle);
                }
                else
                {
                    x = x - cc.magnitude * Math.cos(angle);
                    y = y - cc.magnitude * Math.sin(angle);
                }
                
                if (pen_down)
                {
                    System.out.format("%s %.4f %.4f %.4f %.4f\n", color, oldx, oldy, x, y);
                }
            }
            else if (c instanceof RotationCommand)
            {
                RotationCommand cc = (RotationCommand) c;
                
                if (cc.direction == RotationCommand.Direction.LEFT)
                {
                    angle = angle + cc.angle * Math.PI / 180.0;
                }
                else
                {
                    angle = angle - cc.angle * Math.PI / 180.0;
                }
            }
            else if (c instanceof PenCommand)
            {
                pen_down = (((PenCommand) c).state == PenCommand.State.DOWN);
            }
            else if (c instanceof ColorCommand)
            {
                ColorCommand cc = (ColorCommand) c;
                
                color = cc.color;
            }
            else if (c instanceof RepeatCommand)
            {
                RepeatCommand cc = (RepeatCommand) c;
                
                for (int i = 0; i < cc.count; ++i)
                {
                    execute(cc.commands);
                }
            }
        }
    }
    
    /**
     * Current X position of pen.
     */
    private double x = 0;
    
    /**
     * Current Y position of pen.
     */
    private double y = 0;
    
    /**
     * Current angle for moving the pen forwards / backwards.
     */
    private double angle = 0;
    
    /**
     * Current color of pen.
     */
    private String color = "#0000FF";
    
    /**
     * Is the pen touching the canvas?
     */
    private boolean pen_down = false;
    
    /**
     * Parse tree to compile.
     */
    private LinkedList<Command> parsetree;
}
