class Section():
    """Cross-section properties for structural elements
    """

    def __init__(self, index: int, name: str, A: float, I: float):
        """Constructor

        Args:
            index (int): Index within the model
            name (str): Section name/identifier
            A (float): Cross-sectional area
            I (float): In-plane moment of inertia
        """
        self.index = index
        self.name = name
        self.A = A
        self.I = I

    def radius_of_gyration(self) -> float:
        """Calculate the radius of gyration (r) using r = √(I/A)

        Returns:
            float: Radius of gyration
        """
        return (self.I / self.A) ** 0.5 