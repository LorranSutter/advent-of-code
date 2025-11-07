import unittest
from main import part1

class TestPart1(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
def test_part1_read_and_parse_input(self):
    # Mock the read_file function to return predefined wires and gates
    mock_wires = {'x': 123, 'y': 456}
    mock_gates = [Gate('x', 'AND', 'y', 'z')]
    with unittest.mock.patch('main.read_file', return_value=(mock_wires, mock_gates)):
        # Mock the simulate and get_z_output functions
        with unittest.mock.patch('main.simulate') as mock_simulate:
            with unittest.mock.patch('main.get_z_output', return_value=789) as mock_get_z_output:
                # Capture the print output
                with unittest.mock.patch('builtins.print') as mock_print:
                    part1()
                    
                    # Assert that read_file was called
                    self.assertTrue(mock_simulate.called)
                    # Assert that simulate was called with the correct arguments
                    mock_simulate.assert_called_once_with(mock_wires, mock_gates)
                    # Assert that get_z_output was called with the correct argument
                    mock_get_z_output.assert_called_once_with(mock_wires)
                    # Assert that the correct output was printed
                    mock_print.assert_called_once_with("Output:", 789)