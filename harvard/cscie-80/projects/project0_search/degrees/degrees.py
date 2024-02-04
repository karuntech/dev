import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set(),
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set(),
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO
    print("Loaded Data")
    print("==============")
    # view_loaded_data()

    # We will use QueueFronteir as it implemets breadth-first search which is guranteed to find the optimal solution for a search problem

    qf = QueueFrontier()  # Initialize a Queue Frontier

    # In our search problem, nodes (vertices) will be the actors (stars) and the edges (links) will be movies.
    # We have to start from source (first actor), use the movies as 'actions' to get to other actors. The second actor is the target.
    # Here is the algorithm we will use:
    # The node is already defined for us in util
    # Initial node (source)

    sourcenode = Node(source, parent=None, action=None)
    targetnode = Node(target, parent=None, action=None)


    # Add the source node to the frontier
    qf.add(sourcenode)

    # Explored set as we expore the nodes
    explored = set()

    # Keep track of the path
    path = []

    # Keep looping until the target node is found
    while True:
        # If the frontier is empty, there is no solution
        if qf.empty():
            return None  # As per the specification

        # Remove a node from the frontier Queue frontier will remove the first one that was added
        node = qf.remove()

        # If this node is the goal, we have a solution. Return the list containing movie id and actor id
        if node.state == targetnode.state:
            # We found the target node. Trace back to find the full path
            step = ()
            while node.parent is not None:
                # A tuple of two strings is one step in the path
                step = (node.action, node.state)
                path.append(step)
                node = node.parent
            path.reverse()
            return path

        # If we didn't find the solution, add neighors to he fronteir and keep expanding the list to
        # include the movieid and person id.

        # Add this node to the explored set
        explored.add(node.state)
        # degrees_traveled.append

        # Movie is the action and state is the actor
        for action, state in neighbors_for_person(node.state):
            if not qf.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                qf.add(child)

    # raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


# Add helper function to just view the data loaded
def view_loaded_data():
    print(f"names: {names}")
    print(f"people: {people}")
    print(f"movies: {movies}")


if __name__ == "__main__":
    main()
