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
                "movies": set()
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
                "stars": set()
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
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

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
   
	Search Problem Outline:
	
	States: people
	Actions: movies
	Initial State, Goal are defined by the two people we're trying to connect
	We want to implement breadth first search, so lets use the Queue frontier
	 
	"""
    # TODO
    # If source is target
    if source == target:
        return []
    
	# Initialize frontier and explored set
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = list() 
    path = list()

	# Now we need to check the person if they are the goal
    while (True):
        # if there actors have no movies in common, then no path
        if frontier.empty():
            return None
        
        # we want ot remove a node from the frontier, and explore its actions
        expandedNode = frontier.remove()

        # find all the movies that an actor has, in the expanded node
        #actions = list(people[expandedNode.state]['movies'])

        if expandedNode.state == target:
            actions = []; cells = []
            while expandedNode.parent is not None:
                actions.append(expandedNode.action)
                cells.append(expandedNode.state)
                expandedNode = expandedNode.parent
            actions.reverse()
            cells.reverse()
            path = list()
            for i in range(len(actions)):
                path.append((actions[i],cells[i]))
            return path
        
        explored.append(expandedNode.state)

        # Add neighbours to the frontier
        for action, state in neighbors_for_person(expandedNode.state):
            if state not in explored and not frontier.contains_state(state):
                child = Node(state=state,parent=expandedNode,action=action)
                if state == target:
                    actions = []; cells = []
                    while child.parent is not None:
                        actions.append(child.action)
                        cells.append(child.state)
                        child = child.parent
                    actions.reverse()
                    cells.reverse()
                    path = list()
                    for i in range(len(actions)):
                        path.append((actions[i],cells[i]))
                    return path


                else:
                    frontier.add(child)





        # for action in actions:
        #     # map the list of movie stars in each movie
        #     #nodes = [Node(state=i,parent=expandedNode,action=action) for i in list(movies[action]['stars'])]
        #     for node in nodes:
        #         if node in explored:
        #             continue
        #         if node.state == target:
        #             while node.parent is not None:  
        #                 path.append((action, node.state))
        #                 node = node.parent
        #                 action = node.action
        #             path.reverse()  
        #             print(path)
        #             return path
        #         if node == target:
        #             while nodes2[node].parent is not None:  
        #                 path.append((action, nodes2[node].state))
        #                 node = nodes2[node].parent if node.parent is None else node.parent
        #                 action = node.action
        #             #path.reverse() 
        #             print(path)
        #             return path
        #         else:
        #             explored.append(node)
        #             frontier.add(node)
        
        



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


if __name__ == "__main__":
    main()


