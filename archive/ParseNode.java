import java.util.ArrayList;

public class ParseNode {
    
    ArrayList<ParseNode> children;
    String data;

    public ParseNode(ArrayList<ParseNode> children, String data) {
        this.children = children;
        this.data = data;
    }

    public ArrayList<ParseNode> getChildren() {
        return children;
    }

    public String getValue() {
        return data;
    }

}