import re
import sys

# This class will represent the interpreter for the Flo language
class FloInterpreter:
    def __init__(self):
        self.variables = {}

    def parse_line(self, line):
        # Remove comments
        line = line.strip()
        if line.startswith("#") or line == "":
            return None

        # Variable assignment
        if line.startswith("let"):
            return self.handle_variable_assignment(line)

        # Print statement
        if line.startswith("print"):
            return self.handle_print_statement(line)

        # Conditional statement
        if line.startswith("if"):
            return self.handle_if_statement(line)

        # Else statement
        if line.startswith("else"):
            return self.handle_else_statement(line)

        return line

    def handle_variable_assignment(self, line):
        # Matches `let x = 10`
        match = re.match(r"let (\w+) = (.+)", line)
        if match:
            var_name = match.group(1)
            value = self.evaluate_expression(match.group(2))
            self.variables[var_name] = value

    def handle_print_statement(self, line):
        # Matches `print expression`
        match = re.match(r"print (.+)", line)
        if match:
            expr = match.group(1)
            value = self.evaluate_expression(expr)
            print(value)

    def handle_if_statement(self, line):
        # Matches `if condition`
        match = re.match(r"if (.+):", line)
        if match:
            condition = self.evaluate_expression(match.group(1))
            return condition

    def handle_else_statement(self, line):
        return True

    def evaluate_expression(self, expr):
        try:
            # Substitute variables with their values in the expression
            for var in self.variables:
                expr = expr.replace(var, str(self.variables[var]))
            # Evaluate the expression (basic math support)
            return eval(expr)
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {expr}. {str(e)}")

    def run(self, filepath):
        with open(filepath, "r") as file:
            lines = file.readlines()

        in_if_block = False
        condition_result = False
        for line in lines:
            parsed = self.parse_line(line)

            # Handle conditional blocks
            if isinstance(parsed, bool):
                condition_result = parsed
                in_if_block = True
            elif parsed == "else" and in_if_block:
                condition_result = not condition_result
            elif in_if_block:
                # Only run code inside if block if condition is true
                if condition_result:
                    self.parse_line(line)
                # Reset after the block ends (a simple approach for 1-level blocks)
                if not line.startswith(" "):
                    in_if_block = False
            else:
                if parsed:
                    self.parse_line(line)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python flo_interpreter.py <file.flo>")
        sys.exit(1)

    filepath = sys.argv[1]
    interpreter = FloInterpreter()
    interpreter.run(filepath)
