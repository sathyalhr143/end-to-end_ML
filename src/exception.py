import sys
import logging

def handle_exception(exc_type, exc_value, exc_traceback):
    """Custom exception handler that prints exceptions in a readable format."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    print("Uncaught exception:", exc_value)
    
    
def error_message_detail(error, error_detail: sys):
    """Generates a detailed error message including file name and line number."""
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Error occurred in file: {file_name} at line: {line_number} with message: {str(error)}"

class CustomException(Exception):
    """Custom exception class that includes detailed error information."""
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message   
    
    
# if __name__ == "__main__":
    
#     try:
#         a = 1 / 0
#     except Exception as e:
#         logging.info("Exception occurred")
#         raise CustomException(e, sys)