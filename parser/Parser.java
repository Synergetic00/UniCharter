import java.io.*;
import java.util.*;

public class Parser {

    public static String unitCode;
    public static String hasUnit;
    public static String justCredits;

    public static void main(String[] args) {

        System.out.println();

        unitCode = "^[A-Z]{3,4}[0-9]{3,4}$";
        hasUnit = "^.*[A-Z]{3,4}[0-9]{3,4}.*$";
        justCredits = "^[0-9]{2,3}cp at [0-9]{4} level or above$";

        //String input = "(ABST1000 or ABST100) and (ABST2020 or ABST202 or ABST2060 or ABST2035)";
        //String[] postfix = infixToPostfix(input);
        //String[] test = new String[] {"ABST1000", "ABST100", "or", "ABST2020", "ABST202", "or", "ABST2060", "or", "ABST2035", "or", "and"};
        //ParseNode root = createTree(test);
        //for (ParseNode child : root.getChildren()) {
            //System.out.println(child.data);
        //}

        readFile();
    }

    public static void readFile() {
        BufferedReader br;
        try {
            br = new BufferedReader(new FileReader("data/codes.csv"));
            for(String line; (line = br.readLine()) != null; ) {
                String[] arr = line.split("\\|");
                System.out.println(arr[1]);
            }
            br.close();
        } catch (IOException e) {
        }
    }

    public static ParseNode createTree(String[] inputs) {
        Stack<ParseNode> nodes = new Stack<ParseNode>();
        for (int i = 0; i < inputs.length; i++) {
            String input = inputs[i];
            if (input.equals("and") || input.equals("or")) {
                ArrayList<ParseNode> children = new ArrayList<ParseNode>();
                for (ParseNode node : nodes) {
                    children.add(node);
                }
                nodes.push(new ParseNode(children, input));
            } else {
                nodes.add(new ParseNode(null, input));
            }
        }
        return nodes.pop();
    }

    public static void traversePreOrder(ParseNode root) {
        Stack<ParseNode> nodes = new Stack<ParseNode>();
        nodes.push(root);
        while (!nodes.isEmpty()) {
            ParseNode curr = nodes.pop();
            if (curr != null) {
                System.out.print(curr.data + " ");
                for(int i = curr.getChildren().size() - 1; i >= 0; i--)
                {
                    nodes.add(curr.getChildren().get(i));
                }
            }
        }
    }

    public static String[] infixToPostfix(String exp) {
        String parsed = exp.replaceAll(" ", "");
        String[] replace = new String[]{"\\(", "\\)", "and", "or"};
        parsed = massReplace(parsed, replace);
        parsed = parsed.replaceAll("  ", " ");
        parsed = parsed.trim();
        String[] arr = parsed.split(" ");

        Deque<String> stack  = new LinkedList<>();
        ArrayList<String> output = new ArrayList<String>();

        for (String str : arr) {
            if (str.equals("and") || str.equals("or")) {
                while(!stack.isEmpty()) {
                    output.add(stack.pop());
                }
                stack.push(str);
            } else if (str.equals("(")) {
                stack.push(str);
            } else if (str.equals("}")) {
                while(!stack.isEmpty()) {
                    output.add(stack.pop());
                }
                stack.pop();
            } else {
                output.add(str);
            }
        }

        while(!stack.isEmpty()) {
            output.add(stack.pop());
        }

        //System.out.println(output);

        String[] postfix = new String[output.size()];
        for (int i = 0; i < postfix.length; i++) {
            postfix[i] = output.get(i);
        }

        return arr;
    }

    public static String massReplace(String str, String[] args) {
        for (String arg : args) {
            str = str.replaceAll(arg, ' '+arg+' ');
        }
        return str;
    }
}
