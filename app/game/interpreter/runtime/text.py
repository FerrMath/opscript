from app.game.interpreter.utils.variables import interpolate_variables_in_text_line


def get_interpolated_text_line(expr:str, variables) -> str:
    return interpolate_variables_in_text_line(expr, variables)