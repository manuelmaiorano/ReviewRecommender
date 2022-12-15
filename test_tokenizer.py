import unittest
from tokenizer import *

class TestTokenizer(unittest.TestCase):
    def test_method_occurrences(self):
        file_list = ['file1.py', 'file2.py', 'file3.py']
        expected_output = {'method1': 3, 'method2': 2, 'method3': 3,
        'strip_target': 1, '__init__': 1, 'strip_file_top_level': 1, 'visit_block': 1,
        'visit_class_def': 1, 'save_implicit_attributes': 1, 'visit_func_def': 1,
        'visit_decorator': 1 , 'visit_overloaded_func_def': 1, 'visit_assignment_stmt': 1,
        'visit_import_from': 1, 'process_lvalue_in_method': 1, 'enter_class': 1, 'enter_method': 1}
        self.assertEqual(Tokenizer.method_occurrences(file_list), expected_output)

    def test_class_occurrences(self):
        file_list = ['file1.py', 'file2.py', 'file3.py']
        expected_output = {'Class1': 1, 'Class2': 2, 'Class3': 1, 'NodeStripVisitor': 1}
        self.assertEqual(Tokenizer.class_occurrences(file_list), expected_output)

    def test_class_method_occurrences(self):
        file_list = ['file1.py', 'file2.py', 'file3.py']
        expected_output = {'method1': 3, 'method2': 2, 'method3': 3, 
        'strip_target': 1, '__init__': 1, 'strip_file_top_level': 1, 'visit_block': 1,
        'visit_class_def': 1, 'save_implicit_attributes': 1, 'visit_func_def': 1,
        'visit_decorator': 1 , 'visit_overloaded_func_def': 1, 'visit_assignment_stmt': 1,
        'visit_import_from': 1, 'process_lvalue_in_method': 1, 'enter_class': 1, 'enter_method': 1,
        'Class1': 1, 'Class2': 2, 'Class3': 1, 'NodeStripVisitor':1}
        self.assertEqual(Tokenizer.class_method_occurrences(file_list), expected_output)

if __name__ == '__main__':
    unittest.main()