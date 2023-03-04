# coding=utf-8
"""
@author B1lli
@date 2023年02月02日 14:27:09
@File:logger.py
"""
import os
import logging
import traceback


# class Logger :
#     def __init__(self, log_file_name=None, log_level=logging.DEBUG, log_directory=None) :
#         self.log_file_name = 'errors.log'
#         self.log_level = log_level
#         self.log_directory = "../log/"
#
#         if self.log_directory is not None :
#             if not os.path.exists ( self.log_directory ) :
#                 os.makedirs ( self.log_directory )
#             self.log_file_path = os.path.join ( self.log_directory, self.log_file_name )
#         else :
#             self.log_file_path = self.log_file_name
#
#         logging.basicConfig ( filename=self.log_file_path, level=self.log_level,
#                               format="%(asctime)s %(levelname)s: %(message)s",
#                               datefmt="%Y-%m-%d %H:%M:%S")
#
#     def debug(self, message) :
#         logging.debug ( message )
#
#     def info(self, message) :
#         logging.info ( message )
#
#     def warning(self, message) :
#         logging.warning ( message )
#
#     def critical(self, message) :
#         logging.critical ( message )

log_file_name = 'errors.log'
log_directory = "../log/"

if log_directory is not None :
    if not os.path.exists ( log_directory ) :
        os.makedirs ( log_directory )
    log_file_path = os.path.join ( log_directory, log_file_name )
else :
    log_file_path = log_file_name

logging.basicConfig ( filename=log_file_path,
                      format="%(asctime)s %(levelname)s: %(message)s",
                      datefmt="%Y-%m-%d %H:%M:%S")


def log_error(func) :
    def wrapper(*args, **kwargs) :
        try :
            return func ( *args, **kwargs )
        except Exception as e :
            current_version = "V1.0"
            tb = traceback.format_exc ()
            error_message = f"{current_version}\n{tb}\n{e}"
            logging.error ( error_message )
            # raise
    return wrapper

# @log_error
# def func():
#     raise Exception
#
# if __name__ == '__main__':
#     func()


