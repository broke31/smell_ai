import ast
import re


def Chain_Indexing(libraries, filename, node):
    if "pandas" in libraries:
        function_name = node.name
        function_body = ast.unparse(node.body).strip()
        pattern = r'\b\w[a-zA-Z0-9]*\[[a-zA-Z0-9]*\]\b'
        matches = re.findall(pattern, function_body)
        message = " Using chain indexing may cause performance issues."
        num_matches = len(matches)
        if num_matches > 0:
            return [f"{filename}", f"{function_name}", num_matches, message]
        return []
    return []


def dataframe_conversion_api_misused(libraries, filename, node):
    if "pandas" in libraries:
        function_name = node.name
        function_body = ast.unparse(node.body).strip()
        number_of_apply = function_body.count(".values(")
        message = "Please consider to use numpy instead values to convert dataframe. The function 'values' is deprecated." \
                  "The value return of this function is unclear."
        if number_of_apply > 0:
            to_return = [filename, function_name, number_of_apply, message]
            return to_return
        return None
    return None


def matrix_multiplication_api_misused(libraries, filename, node):
    if "numpy" in libraries:
        function_name = node.name
        function_body = ast.unparse(node.body).strip()
        number_of_dot = function_body.count(".dot(")
        message = "Please consider to use np.matmul to multiply matrix. The function dot() not return a scalar value, " \
              "but a matrix. "
        if number_of_dot > 0:
            to_return = [filename, function_name, number_of_dot, message]
            return to_return
        return None
    return None


def gradients_not_cleared_before_backward_propagation(libraries, filename, node):
    if "pytorch" in libraries:
        function_name = node.name
        function_body = ast.unparse(node.body).strip()
        lines = function_body.split('\n')
        zero_grad_called = False
        gradients_not_cleared = 0
        backward_called = False
        for line in lines:
            if "optimizer.zero_grad" in line:
                zero_grad_called = True
                if backward_called:
                    gradients_not_cleared = 1
            elif 'loss_fn.backward()' in line:
                backward_called = True
                if not zero_grad_called:
                    gradients_not_cleared = 1
            elif 'optimizer.step()' in line:
                if not backward_called:
                    gradients_not_cleared = 1
            zero_grad_called = False
            backward_called = False
        message = "If optimizer.zero_grad() is not used before loss_- fn.backward(), the gradients will be accumulated" \
              " from all loss_- fn.backward() calls and it will lead to the gradient explosion," \
              " which fails the training."
        if gradients_not_cleared > 0:
            to_return = [filename, function_name, gradients_not_cleared, message]
            return to_return
        return None
    return None
