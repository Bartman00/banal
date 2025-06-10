import math

class Node():
    """2D Node with some basic utilities
    """

    def __init__(self, index: int, x: float, y: float):
        """Constructor

        Args:
            index (int): Index within the model
            x (float): X Coordinate
            y (float): Y Coordinate
        """
        self.index = index
        self.x = x
        self.y = y

    def distance(self, anode: 'Node') -> float:
        """Distance to another node

        Args:
            anode (Node): Other node

        Returns:
            float: Distance
        """
        return math.sqrt((self.x - anode.x)**2 + (self.y - anode.y)**2)
    
    def is_same_location(self, anode: 'Node') -> bool:
        """Return true if the other node is at the same location
        uses a hard-coded tolerance.

        Args:
            anode (Node): Other node

        Returns:
            bool: True if at the same location
        """
        return self.distance(anode) < 1e-6
    
    def dofs(self) -> list[int]:
        """Return the DOFs for the node

        Returns:
            list[int]: DOFs
        """
        return [self.index * 3, self.index * 3 + 1, self.index * 3 + 2]



    