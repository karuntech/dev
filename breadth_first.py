# Pseudo code for breadth-first search
# Breadth-first search uses Queue as the data structure in Frontier

class breadth_first:
    def remove(self):
        if self.empty():
            # Fronteir is empty
            raise Exception("Empty Frontier")
        node = self.frontier[0]     #Save the first element 
        # Remove the first element
        self.frontier = self.frontier[1:]
        return node