import json

TAB = "    "

FIRST_CELL = "FIRST"
LAST_CELL = "LAST"
EVERY_CELL = "EVERY"

BEGINNING_OF_CELL = "FRONT"
END_OF_CELL = "BACK"

INJECTED_CODE_START = "#INJECTED CODE START\n"
INJECTED_CODE_END = "#INJECTED CODE END\n"

INJECTED_CELL = "#INJECTED CELL"


class Notebook:


    def __init__(self, notebook_str):
        """ Loads a notebook into a JSON object.
        """

        self.notebook_json = json.loads(notebook_str)
        self.block_template_json = json.loads(
            '{"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],"source":[]}'
        )


    def __str__(self):
        """ Returns a formatted JSON string.
        """

        return str(json.dumps(self.notebook_json, indent=1))


    def get_cells(self, position):
        """ Collecting a list of indices of cells to inject/indent in.
        """

        indices = []
        if position == FIRST_CELL:
            counter = 0
            while self.notebook_json["cells"][counter]["cell_type"] != "code":
                counter += 1
            indices.append(counter)
        elif position == LAST_CELL:
            counter = -1
            while self.notebook_json["cells"][counter]["cell_type"] != "code":
                counter -= 1
            indices.append(counter)
        elif position == EVERY_CELL:
            indices = []
            counter = 0
            for cell in self.notebook_json["cells"]:
                if cell["cell_type"] == "code":
                    indices.append(counter)
                counter += 1
        return indices


    def indent_code(self, cells):
        """ Adds a tab before every line of code.
        """

        for cell in cells:
            counter = 0
            cell_size = len(self.notebook_json["cells"][cell]["source"])
            while counter < cell_size:
                line = self.notebook_json["cells"][cell]["source"][counter]
                line = TAB + line
                self.notebook_json["cells"][cell]["source"][counter] = line
                counter += 1


    def unindent_code(self, cells):
        """ Removes a tab before every line of code from a collection of specified code cells.
        This is not a smart function, and should only be called if indent_code is called first.
        """

        for cell in cells:
            counter = 0
            cell_size = len(self.notebook_json["cells"][cell]["source"])
            while counter < cell_size:
                line = self.notebook_json["cells"][cell]["source"][counter]
                line = line[len(TAB):]
                self.notebook_json["cells"][cell]["source"][counter] = line
                counter += 1


    def inject_code(self, cells, position, code):
        """ Adds a collection of lines of code at the front of back of a collection of specified code cells.
        """

        code = add_carriage_return(code)

        for cell in cells:
            if position == BEGINNING_OF_CELL:
                self.notebook_json["cells"][cell]["source"] = [INJECTED_CODE_START] + code + [INJECTED_CODE_END] + self.notebook_json["cells"][cell]["source"]
            elif position == END_OF_CELL:
                self.notebook_json["cells"][cell]["source"][-1] = self.notebook_json["cells"][cell]["source"][-1] + "\n"
                self.notebook_json["cells"][cell]["source"] = self.notebook_json["cells"][cell]["source"] + [INJECTED_CODE_START] + code + [INJECTED_CODE_END]


    def scrub_code(self, cells):
        """ Removes all lines of code injected by inject_code from a collection of specified code cells.
        """

        inside_injected_code = False

        for cell in cells:
            counter = 0
            cell_size = len(self.notebook_json["cells"][cell]["source"])
            while counter < cell_size:
                if self.notebook_json["cells"][cell]["source"][counter] == INJECTED_CELL:
                    del self.notebook_json["cells"][cell]
                    break
                if self.notebook_json["cells"][cell]["source"][counter] == INJECTED_CODE_START:
                    inside_injected_code = True
                if inside_injected_code: 
                    if self.notebook_json["cells"][cell]["source"][counter] == INJECTED_CODE_END:
                        inside_injected_code = False
                    del self.notebook_json["cells"][cell]["source"][counter]
                    cell_size -= 1
                else:
                    counter += 1
        
        # Check for injected cells as well...
        # ...

    def inject_cell(self, position, code):
        """ Add new code cell for pre- or post-execution scripts.
        """

        code = [INJECTED_CELL] + code
        code = add_carriage_return(code)


        if position == FIRST_CELL:
            self.notebook_json["cells"] = self.block_template_json + self.notebook_json["cells"]
            self.notebook_json["cells"][0]["source"] = code
        elif position == LAST_CELL:
            self.notebook_json["cells"] = self.notebook_json["cells"] + self.block_template_json
            self.notebook_json["cells"][-1]["source"] = code


    def add_carriage_return(code):
        """ Adds carriage returns to each line of code in a given list.
        """

        line = 0
        while line < len(code):
            code[line] += "\n"
            line += 1
        return code