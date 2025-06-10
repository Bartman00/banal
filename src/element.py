import math
import numpy as np
from .node import Node
from .material import Material
from .section import Section


"""
TODO:
- Add truss, beam-column (frame) elements
- Add parent class for all 2D elements with common properties including
  - Index
  - Material
  - Section
  - Nodes (as a list. Ok to store as variables for beam elements)
  - Local stiffness matrix (use unit matix for parent)
"""

class Element():
    """2D beam element with 2 local DOFs per node (translation and rotation)
    When transformed to global coordinates, each node has 3 DOFs (x-trans, y-trans, rotation)
    """

    def __init__(self, index: int, material: Material, section: Section, node1: Node, node2: Node):
        """Constructor

        Args:
            index (int): Element index in the model
            material (Material): Material properties
            section (Section): Section properties
            node1 (Node): First node
            node2 (Node): Second node

        Raises:
            ValueError: If element has zero length
        """
        self.index = index
        self.material = material
        self.section = section
        self.node1 = node1
        self.node2 = node2
        
        # Calculate length and orientation
        self.dx = self.node2.x - self.node1.x
        self.dy = self.node2.y - self.node1.y
        self.length = math.sqrt(self.dx**2 + self.dy**2)
        
        if self.node1.index == self.node2.index:
            raise ValueError(f"Element {index} needs to connect to two different nodes")

        if self.length < 1e-10:
            raise ValueError(f"Element {index} has zero length")
        
        # Calculate direction cosines
        self.cos_theta = self.dx / self.length
        self.sin_theta = self.dy / self.length

        self.local_stiffness_matrix = self.local_stiffness()

    def local_stiffness(self) -> np.ndarray:
        """Calculate the local stiffness matrix [4x4] for the element
        Local DOFs are: [v1, θ1, v2, θ2] where v is transverse displacement and θ is rotation

        Returns:
            np.ndarray: 4x4 local stiffness matrix
        """
        E = self.material.E
        I = self.section.I
        L = self.length
        
        # Basic beam stiffness terms
        k = E * I / (L**3)
        
        # Local stiffness matrix
        K_local = np.array([
            [ 12,    -6*L,    -12,     -6*L],
            [-6*L,   4*L**2,   6*L,   2*L**2],
            [-12,    6*L,     12,    6*L],
            [-6*L,   2*L**2,  6*L,   4*L**2]
        ]) * k
        
        return K_local

    def global_stiffness(self) -> np.ndarray:
        """Calculate the global stiffness matrix [6x6] for the element
        Global DOFs are: [u1, v1, θ1, u2, v2, θ2] where u is x-translation,
        v is y-translation, and θ is rotation

        Returns:
            np.ndarray: 6x6 global stiffness matrix
        """

        """TODO:
        - Need to return submatrix of global stiffness matrix 
        linked to the element's node's DOFs
        """
        c = self.cos_theta
        s = self.sin_theta
        
        # Transformation matrix from local to global coordinates
        T = np.array([
            [ 0,  -1,   0,   0,   0,   0],
            [ c,   s,   0,  -c,  -s,   0],
            [ 0,   0,   1,   0,   0,   0],
            [ 0,   0,   0,   0,  -1,   0],
            [ c,   s,   0,  -c,  -s,   0],
            [ 0,   0,   0,   0,   0,   1]
        ])
        
        # Get local stiffness
        K_local = self.local_stiffness()
        
        # Expand local stiffness to include axial terms (which are zero for pure bending)
        K_local_expanded = np.zeros((6, 6))
        # Insert bending terms
        for i, ii in enumerate([1, 2, 4, 5]):
            for j, jj in enumerate([1, 2, 4, 5]):
                K_local_expanded[ii, jj] = K_local[i, j]
        
        # Add axial stiffness terms
        EA = self.material.E * self.section.A
        K_local_expanded[0, 0] = EA / self.length
        K_local_expanded[3, 3] = EA / self.length
        K_local_expanded[0, 3] = -EA / self.length
        K_local_expanded[3, 0] = -EA / self.length
        
        # Transform to global coordinates
        K_global = T.T @ K_local_expanded @ T
        
        return K_global 