"""
Family Tree Creator - Create a class called Person which will have a name, when they were born and when (and if)
they died. Allow the user to create these Person classes and put them into a family tree structure.
Print out the tree to the screen.
"""
from datetime import datetime

from dateutil import parser


class Person:
    def __init__(self, name, birth_day='', birth_location='', death_day='', **children):
        """
        Class constructor

        name:           String      - The first name
        birth_day:      String      - The birth day in string format
        birth_location: String      - location of birth
        death_day:      String      - The death day in string format
        children:       Dictionary  - List of children (person.name: person)
        """
        self.name = name
        self.birth_day = birth_day
        self.birth_location = birth_location
        self.death_day = death_day
        self._children = {}
        self.parent = None

        # Add children using the add_child method
        for child in children.values():
            self.add_child(child)

    def add_child(self, person):
        """
        Add a child to the current person

        person: Person - An instance of another person object
        """
        # Set the parent of the child
        person.parent = self
        # Add the child
        self._children[person.name] = person

    def has_children(self):
        """
        Whether or not the current person has children
        """
        return len(self._children) > 0

    @property
    def children(self):
        """
        Property to access the children of the person

        returns: Dictionary - Children of the person
        """
        return self._children

    def age(self):
        """
        Calculate the person age

        returns:    Integer  - The age of the person
        """
        year_now = datetime.now().year

        # Person age up to this year
        birth_day_object = parser.parse(self.birth_day)
        years = year_now - birth_day_object.year

        # On death, person age is up to his/her death
        if self.death_day is not None:
            death_day_object = parser.parse(self.death_day)
            years -= year_now - death_day_object.year

        return years


class FamilyTree:
    def __init__(self, root):
        """
        Class constructor

        root: Person - The root person to display his/her family tree
        """
        self.root = root

    def display(self):
        """
        Display the family tree starting from the root children
        """
        self.display_children(self.root, 0)

    def display_children(self, person, level=0, name_with=0, last_child=False):
        """
        Display the children of a Person

        person:     Person  - The person object to display its children
        level:      Integer - The hierarchy level of the person in the current family tree
        name_with:  Integer - The width size of the longest child name in the Person object. This used for padding
        last_child: Boolean - Whether or not this person is the last item in children list
        returns:    This method prints out the tree structure. No returns.
        """
        # Init variables
        next_level = level  # Current level
        left_arrow = '  |-- ' if last_child is False else '  `-- '  # The left arrow for person name
        person_name = left_arrow + person.name  # The person name with the left arrow

        # Left padding with continues lines for each parent
        print '   |' * next_level,

        # Person name with right padding based on the longest child name
        print person_name.ljust(name_with),

        # Person info
        print '\t(%s - %s: %s years old)\t%s' % (
            person.birth_day,
            person.death_day,
            person.age(),
            person.birth_location
        )

        # Display children if any
        if person.has_children():
            # The index of the last child in the current person
            last_child_index = len(person.children) - 1

            # Next level for the children
            next_level += 1

            # Get longest child name + the length of the left arrow
            next_name_with = len(max(person.children.keys(), key=len)) + len(left_arrow)

            # Display children
            for i, child in enumerate(person.children.values()):
                is_last = True if last_child_index == i else False
                self.display_children(child, level=next_level, name_with=next_name_with, last_child=is_last)


if __name__ == '__main__':
    # Root
    lucas = Person('Lucas', birth_day='1920-10-10', birth_location='UK', death_day='2010-01-10')

    # Children
    mary = Person('Mary', birth_day='1956-04-23', birth_location='New Zealand')
    jason = Person('Jason', birth_day='1944-10-05', birth_location='New Zealand', death_day="2011-01-13")
    peter = Person('Peter', birth_day='1960-05-10', birth_location='New Zealand')
    lucas.add_child(mary)
    lucas.add_child(jason)
    lucas.add_child(peter)

    # Children of children
    fred = Person('Fred', birth_day='1982-11-11', birth_location='New Zealand')
    jane = Person('Jane', birth_day='1985-06-07', birth_location='New Zealand')
    mary.add_child(fred)
    mary.add_child(jane)

    # Children of children
    sean = Person('Sean', birth_day='1983-01-01', birth_location='Australia')
    jessica = Person('jessica', birth_day='1984-08-12', birth_location='Australia')
    hannah = Person('Hannah', birth_day='1986-09-22', birth_location='New Zealand')
    jason.add_child(sean)
    jason.add_child(jessica)
    jason.add_child(hannah)

    # Children of children of children
    joseph = Person('Joseph', birth_day='2000-04-10', birth_location='New Zealand')
    john = Person('John', birth_day='2003-12-12', birth_location='New Zealand')
    laura = Person('Laura', birth_day='2005-03-27', birth_location='New Zealand')
    jessica.add_child(joseph)
    jessica.add_child(john)
    jessica.add_child(laura)

    # Display family tree for faisal
    print 'Family tree: (%s)' % lucas.name
    FamilyTree(lucas).display()
