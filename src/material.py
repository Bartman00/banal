class Material():
    """Material class containing basic mechanical properties
    """

    def __init__(self, index: int, name: str, E: float, p: float, v: float):
        """Constructor

        Args:
            index (int): Index within the model
            name (str): Material name/identifier
            E (float): Young's modulus of elasticity
            p (float): Material density (ρ)
            v (float): Poisson's ratio (ν)
        """
        self.index = index
        self.name = name
        self.E = E
        self.p = p
        self.v = v

    def shear_modulus(self) -> float:
        """Calculate the shear modulus (G) using the relationship G = E/2(1+ν)

        Returns:
            float: Shear modulus
        """
        return self.E / (2 * (1 + self.v))

    def bulk_modulus(self) -> float:
        """Calculate the bulk modulus (K) using the relationship K = E/3(1-2ν)

        Returns:
            float: Bulk modulus
        """
        return self.E / (3 * (1 - 2 * self.v)) 