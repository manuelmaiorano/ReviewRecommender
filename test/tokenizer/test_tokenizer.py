import pytest
from tokenizer import *
from data_retriveal import RepoRetriveal

filename_list = ['file1.py', 'file2.py', 'file3.py']
PATH = 'test/tokenizer/data/'

def get_file_list(filename_list):
    file_list = []
    for filename in filename_list:
        filepath = PATH + filename
        with open(filepath) as file:
            content = file.read()
            file_list.append(RepoRetriveal.RepoFile(filepath, content))

    return file_list

class TestTokenizer:
    file_list = get_file_list(filename_list)

    def test_method_occurrences(self):
        expected_output = {'method1': 3, 'method2': 2, 'method3': 3,
        'strip_target': 1, '__init__': 1, 'strip_file_top_level': 1, 'visit_block': 1,
        'visit_class_def': 1, 'save_implicit_attributes': 1, 'visit_func_def': 1,
        'visit_decorator': 1 , 'visit_overloaded_func_def': 1, 'visit_assignment_stmt': 1,
        'visit_import_from': 1, 'process_lvalue_in_method': 1, 'enter_class': 1, 'enter_method': 1}
        assert Tokenizer.method_occurrences(self.file_list) == expected_output

    def test_class_occurrences(self):
        expected_output = {'Class1': 1, 'Class2': 2, 'Class3': 1, 'NodeStripVisitor': 1}
        assert Tokenizer.class_occurrences(self.file_list) == expected_output

    def test_class_method_occurrences(self):
        expected_output = {'method1': 3, 'method2': 2, 'method3': 3, 
        'strip_target': 1, '__init__': 1, 'strip_file_top_level': 1, 'visit_block': 1,
        'visit_class_def': 1, 'save_implicit_attributes': 1, 'visit_func_def': 1,
        'visit_decorator': 1 , 'visit_overloaded_func_def': 1, 'visit_assignment_stmt': 1,
        'visit_import_from': 1, 'process_lvalue_in_method': 1, 'enter_class': 1, 'enter_method': 1,
        'Class1': 1, 'Class2': 2, 'Class3': 1, 'NodeStripVisitor':1}
        assert Tokenizer.class_method_occurrences(self.file_list) == expected_output
