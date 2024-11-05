import re

# shunting yard algo
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operators = []
    # splitss into tokens
    tokens = re.findall(r'\d+|\+|\-|\*|\/|\(|\)', expression)

    for token in tokens:
        if token.isdigit():  # Operand
            output.append(token)
        elif token in precedence:  # Operator
            while (operators and operators[-1] != '(' and precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
        elif token == '(':  # Left parenthesis
            operators.append(token)
        elif token == ')':  # Right parenthesis
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Remove '('

    while operators:
        output.append(operators.pop())

    return output

def evaluate_postfix(postfix_tokens):
    stack = []

    for token in postfix_tokens:
        if token.isdigit():  # Operand
            stack.append(float(token))
        else:  # Operator
            operand2 = stack.pop()
            operand1 = stack.pop()
            if token == '+':
                stack.append(operand1 + operand2)
            elif token == '-':
                stack.append(operand1 - operand2)
            elif token == '*':
                stack.append(operand1 * operand2)
            elif token == '/':
                stack.append(operand1 / operand2)
    
    return stack[0] if stack else None

def calculate(expression):
    # Step 1: Convert infix to postfix
    postfix_expr = infix_to_postfix(expression)
    print("Postfix expression:", ' '.join(postfix_expr))  # For debugging
    
    # Step 2: Evaluate postfix expression
    result = evaluate_postfix(postfix_expr)
    return result

# Test cases
print(calculate("1 + 1 * 5"))       # Output: 6.0
print(calculate("(1 + 1) * 5"))     # Output: 10.0
print(calculate("10 / (6 - 1)"))    # Output: 2.0
print(calculate("3 + 4 * 2 / (1 - 5)")) # Output: 1.0
