import os

class Test:
    """This class stores a test"""
    
    def __init__(self, Input, Output, points = 1, feedback = None, show = None):
        """
        Parameters
        ----------
        Input: str
            The test input
        Output: str
            The test output
        points: int, optional
            The number of points awarded for succeeding this test
        feedback: str, optional
            The feedback for this test
            If there is a feedback, then this test is public (i.e., Show will be yes)
        """

        self._input = Input
        self._output = Output
        self.points = points
        self.feedback = '{}'
        self.show = '{}'
        if feedback is not None:
            self.feedback = f'{{{feedback}}}'
        if show is not None:
            self.show = 'yes'
            
    def class_tcl(self):
        return "return Test"
    def data_tcl(self):
        return f"""set        Fatal {{}}
set      Warning {{}}
set         args {{}}
set        input input
set       output output
set      context context
set       Points {self.points}
set     Feedback {self.feedback}
set         Show {self.show}
"""
    def input(self):
        return self._input
    def output(self):
        return self._output
    
class Problem:
    def __init__(self, name, letter = 'A', solver = None, description = None, input_to_string = None):
        """
        Parameters
        ----------
        name: str
            The problem name
        letter: char, optional
            The problem's letter (MOOshak specific)
        solver: function, optional
            This function takes one test and generates the corresponding output
        input_to_string: function, optional
            This function takes one test and generates the corresponding input
        """

        self.name = name
        self.letter = letter
        if solver is not None and not callable(solver):
            raise Exception('solver is not callable')
        self.solver = solver
        self.description = lambda: description if description is not None else ""
        self.input_to_string = input_to_string if input_to_string is not None else str
        self.points = 100
        self.folder = letter
        self.tests = []

    def __repr__(self):
        return f"""Name: {self.name}
Folder: {self.letter}
{self.debug_info}
"""
    def add_tests(self, inputs, points = None, feedback = None, show = None):
        """Add several tests

        Parameters
        ----------
        inputs: list
            List of inputs
        points: list
            List of points
        """
        if True or points is None:
            points = [1] * len(inputs)
            
        assert len(inputs) == len(points), f"Wrong number of points {len(inputs)} != {len(points)}"
        if feedback is None or type(feedback) is str:
                feedback = [feedback] * len(points)
        if show is not None:
            show = True
            
        assert type(feedback) is list, "Wrong type of feedback" + str(type(feedback))
        assert len(feedback) == len(inputs), "Wrong number of feedback"
        
        for I, pts, feed in zip(inputs, points, feedback):
            self.add_test(I, points = pts, feedback = feed, show = show)
            
    def add_test(self, Input, Output = None, points = 1, feedback = None, show = None):
        """Add one test

        Parameters
        ----------
        Input:
            The input
        Output: optional
            The output, if it was not provided, the solver will be used to generate it
        points: int, optional
            The number of points for this test
        feedback: str, optional
            The feedback in case the test is wrong
        """

        if Output is None:
            if self.solver is None:
                raise(Exception('No solver found'))
            Output = self.solver(Input)
        self.tests.append(Test(Input, Output, points = points, feedback = feedback, show = show))
    def class_tcl(self):
        return "return Problem"
    def data_tcl(self):
        return f"""set        Fatal {{}}
set      Warning {{}}
set         Name {self.letter}
set        Color red
set        Title {{{self.name}}}
set   Difficulty Medium
set         Type ad-hoc
set  Description description.html
set          PDF {{}}
set      Program {{}}
set  Environment Environment
set      Timeout 1
set Static_corrector {{}}
set Dynamic_corrector {{}}
set       images {{}}
set        tests tests
"""
    def assign_points(self, total = 100):
        self.points = total
        default_points = lambda n: [total // n + (1 if i < total % n else 0) for i in range(n)]
        points = default_points(len(self.tests))
        for t, p in zip(self.tests, points):
            t.points = p
        
    def create_files(self):
        """Creates the folder and all the corresponding files needed to create the MOOshak problem

        Parameters
        ----------
        folder: str
            The path for the folder that will be generated
        """
        
        def create_file(file, fun):
            """Creates the file and calls the function that will be used to populate it

            Parameters
            ----------
            file: str
                The pathname of the file
            fun: function
                The function that will generate the text for the file
            """
            
            with open(file, 'w', newline = '\n', encoding = "utf-8") as f:
                result = fun()
                result = str(result).rstrip()
                print(result, file = f)
            return result
        def show(fname, field):
            if field != "{}":
                return f"\n{fname} {field}"
            else:
                return ""
        folder = self.folder
        import shutil
        if os.path.exists(f'{folder}'):
            shutil.rmtree(f'{folder}')
        os.makedirs(f'{folder}', exist_ok = True)
        create_file(f'{folder}/.data.tcl', self.data_tcl)
        create_file(f'{folder}/.class.tcl', self.class_tcl)
        create_file(f'{folder}/description.html', self.description)
        os.makedirs(f'{folder}/tests', exist_ok = True)
        create_file(f'{folder}/tests/.data.tcl', lambda: f"""set        Fatal {{}}
set      Warning {{}}
set   Definition Definition
set         Test {len(self.tests)}
""")
        create_file(f'{folder}/tests/.class.tcl', lambda: """return Tests
""")
        self.debug_info = ""
        for num, test in enumerate(self.tests):
            tst_dir = f'{folder}/tests/T{num + 1:03d}'
            os.makedirs(tst_dir, exist_ok = True)
            create_file(f'{tst_dir}/.data.tcl', test.data_tcl)
            create_file(f'{tst_dir}/.class.tcl', test.class_tcl)
            input_file = f'{tst_dir}/input'
            output_file = f'{tst_dir}/output'
            inp_txt = create_file(input_file, lambda: self.input_to_string(test.input()))
            out_txt = create_file(output_file, test.output)

            # Debugging information about each test
            
            self.debug_info += f"""Test {num + 1:03d}{show("Feedback", test.feedback)}{show("Show", test.show)}
Input: {inp_txt}
Output: {out_txt}

"""
