['AACG', 'ABST', 'ABSX', 'ACCG', 'ACOM', 'ACST', 'AFCL', 'AFCP', 'AFCX', 'AFIN', 'AHIS', 'AHIX', 'AIHI', 'ANAT', 'ANTH', 'ANTX', 'APFN', 'APPL', 'ARTS', 'ARTX', 'ASBA', 'ASTR', 'BIOL', 'BIOM', 'BIOX', 'BMOL', 'BUSA', 'CAUD', 'CHEM', 'CHEX', 'CHIN', 'CHIR', 'CIVL', 'CLIN', 'COGS', 'COGX', 'COMP', 'CROA', 'ECHE', 'ECHP', 'ECHX', 'ECNM', 'ECON', 'EDIT', 'EDST', 'EDSX', 'EDTE', 'EDUC', 'EESC', 'ELCT', 'ELEC', 'ENGG', 'ENGL', 'ENGX', 'ENVS', 'FOAR', 'FOHS', 'FOSE', 'FOSX', 'FREN', 'GEND', 'GENX', 'GEOP', 'GEOS', 'GEOX', 'GMBA', 'GRMN', 'HLTH', 'HSYP', 'INDG', 'INED', 'INTS', 'ITAL', 'JPNS', 'JPNX', 'LAWS', 'LING', 'LINX', 'LYMP', 'MATH', 'MECH', 'MEDI', 'MGMT', 'MGRK', 'MHIS', 'MHIX', 'MHPG', 'MKTG', 'MMBA', 'MMCC', 'MMCS', 'MOLS', 'MPHR', 'MQBS', 'MRES', 'MTRN', 'PHIL', 'PHIX', 'PHTY', 'PHYS', 'PICT', 'PICX', 'PLSH', 'POIR', 'POIX', 'PROF', 'PSYB', 'PSYC', 'PSYH', 'PSYM', 'PSYN', 'PSYO', 'PSYP', 'PSYU', 'PSYX', 'RUSS', 'SLAS', 'SLAX', 'SOCI', 'SOCX', 'SPED', 'SPHL', 'SPTH', 'SSCI', 'STAT', 'STAX', 'TELE', 'TRAN', 'WACC', 'WACO', 'WACT', 'WART', 'WCIV', 'WCOM', 'WECO', 'WENG', 'WFBG', 'WFEC', 'WFEN', 'WFIT', 'WFMA', 'WFMD', 'WFRS', 'WMAT', 'WMEC', 'WMGM', 'WMKT', 'WMMC', 'WPHL', 'WPHY', 'WSTA']



    public static String traversePreOrder(ParseNode root) {

        if (root == null) {
            return "";
        }
    
        StringBuilder sb = new StringBuilder();
        sb.append(root.getValue());
    
        String pointerRight = "└──";
        String pointerLeft = (root.getRight() != null) ? "├──" : "└──";
    
        traverseNodes(sb, "", pointerLeft, root.getLeft(), root.getRight() != null);
        traverseNodes(sb, "", pointerRight, root.getRight(), false);
    
        return sb.toString();
    }

    public static void traverseNodes(StringBuilder sb, String padding, String pointer, ParseNode node, boolean hasRightSibling) {
        if (node != null) {
            sb.append("\n");
            sb.append(padding);
            sb.append(pointer);
            sb.append(node.getValue());

            StringBuilder paddingBuilder = new StringBuilder(padding);
            if (hasRightSibling) {
                paddingBuilder.append("│  ");
            } else {
                paddingBuilder.append("   ");
            }

            String paddingForBoth = paddingBuilder.toString();
            String pointerRight = "└──";
            String pointerLeft = (node.getRight() != null) ? "├──" : "└──";

            traverseNodes(sb, paddingForBoth, pointerLeft, node.getLeft(), node.getRight() != null);
            traverseNodes(sb, paddingForBoth, pointerRight, node.getRight(), false);
        }   
    }   



    public static String[] infixToReversePolishNotation(String input) {
        final String[] expression = input.trim().split(" ");

        for (String token : expression) {

            final char op = token.charAt(0); // Validated beforehand.

            if (isOperator(op)) { // if token is an operator
                final Operator op1 = Operator.getOperatorByValue(op);

                while (!operatorStack.isEmpty()) {
                    final Operator op2 = operatorStack.peek();

                    final boolean condition1 = (isLeftAssociative(op1) && compareOperators(
                            op1, op2) <= 0);
                    final boolean condition2 = (!isLeftAssociative(op1) && compareOperators(
                            op1, op2) < 0);
                    if (condition1 || condition2) {
                        outputQueue.add(String.valueOf(operatorStack.pop()
                                .getSymbol()));
                        continue;
                    } else {
                        break;
                    }

                }
                operatorStack.push(op1);
            } else if (token.equals("(")) { // if token is an open parenthesis
                operatorStack.push(Operator.OPEN_PARENTHESIS);

            } else if (token.equals(")")) { // if token is a closed parenthesis
                while (!operatorStack.isEmpty()
                        && (operatorStack.peek() != Operator.OPEN_PARENTHESIS)) {
                    outputQueue.add("" + operatorStack.pop().getSymbol());
                }
                operatorStack.pop(); // pop and discard left parenthesis.
            } else if (isNumerical(token)) {
                outputQueue.add(token);
            }

        }

        while (!operatorStack.empty()) { // Empty out remainder.
            outputQueue.add("" + operatorStack.pop().getSymbol());
        }

        return outputQueue.toArray(new String[] {});
    }