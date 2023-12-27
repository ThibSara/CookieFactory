import math
from collections import defaultdict
from typing import Dict
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Biscuit:
    def __init__(self, biscuit_type: str, size: int, value: int, defect_tolerance: Dict[str, int]):
        """
        Initialize a Biscuit object.
        :param biscuit_type: String representing the type of biscuit.
        :param size: Int representing the length of the biscuit.
        :param value: Numeric value representing the price of the biscuit.
        :param defect_tolerance: Dictionary representing the defect tolerance of the biscuit.
        """
        if not (isinstance(biscuit_type, str) and isinstance(size, int) and isinstance(value, int) and isinstance(
                defect_tolerance, dict)):
            raise ValueError("Invalid input types for Biscuit.")
        if size <= 0 or value <= 0:
            raise ValueError("Size and value must be positive integers.")

        self.biscuit_type = biscuit_type
        self.size = size
        self.value = value
        self.defect_tolerance = defect_tolerance

    def __str__(self) -> str:
        """ String representation of the biscuit. """
        return (f"Biscuit Type: {self.biscuit_type}, Size: {self.size}, Value: {self.value}, Defect Tolerance: "
                f"{self.defect_tolerance}")

    def __repr__(self) -> str:
        """ String representation of the biscuit. """
        return self.__str__()

    def __copy__(self):
        """ Copy the biscuit. """
        return Biscuit(self.biscuit_type, self.size, self.value, self.defect_tolerance)


class Defect:
    """ Represents a defect in the dough roll. """

    def __init__(self, position, defect_class):
        """
        Initialize a Defect object.
        :param position: Numeric value representing the position of the defect.
        :param defect_class: String representing the class or type of the defect.
        """
        if not isinstance(position, float) or not isinstance(defect_class, object):
            raise ValueError("Invalid input types for Defect.")
        if position < 0:
            raise ValueError("Position must be a non-negative integer.")

        self.position = position
        self.defect_class = defect_class

    def __str__(self):
        """ String representation of the defect. """
        return f"Defect Position: {self.position}, Class: {self.defect_class}"

    def __repr__(self) -> str:
        """ String representation of the defect. """
        return self.__str__()


class DoughRoll:
    def __init__(self, length, defect_locations):
        self.length = length
        self.biscuit_placements = []
        self.occupied = [False] * length
        self.defects_at_position = defaultdict(list)  # Dictionary for defects

        # Populate the defects_at_position dictionary
        for defect in defect_locations:
            rounded_position = math.floor(defect.position)
            self.defects_at_position[rounded_position].append(defect)

    def evaluate_cut(self, cut_position: int, biscuit: Biscuit) -> int:
        """
        Evaluate the cut position for a given biscuit.
        :param cut_position: Numeric value representing the position of the cut.
        :param biscuit: Biscuit object to be placed.
        :return: Numeric value representing the defect score.
        """
        defect_score = 0
        defect_tolerance = biscuit.defect_tolerance.copy()

        for position in range(cut_position, cut_position + biscuit.size):
            if position in self.defects_at_position:
                for defect in self.defects_at_position[position]:
                    if defect_tolerance[defect.defect_class] == 0:
                        return -1
                    else:
                        defect_tolerance[defect.defect_class] -= 1
                        defect_score += 1
        return defect_score

    def is_legal_cut(self, cut_position: int, biscuit: Biscuit) -> bool:
        """
        Check if the cut position is legal for a given biscuit.
        :param cut_position: Numeric value representing the position of the cut.
        :param biscuit: Biscuit object to be placed.
        :return: Boolean value representing if the cut is legal or not.
        """
        # Check if the cut position is within the dough roll.
        if cut_position < 0 or cut_position + biscuit.size > self.length:
            return False

        # Check overlap with other biscuits at cut position.
        for i in range(cut_position, cut_position + biscuit.size):
            if self.occupied[i]:
                return False

        # Check defect tolerance.
        return not self.evaluate_cut(cut_position, biscuit) == -1

    def place_biscuit(self, position: int, biscuit: Biscuit) -> None:
        """
        Place a biscuit on the dough roll.
        :param position: Numeric value representing the position of the biscuit.
        :param biscuit: Biscuit object to be placed.
        :return: None
        """

        # Check if the cut position is legal.
        if not self.is_legal_cut(position, biscuit):
            raise ValueError("Illegal cut position.")

        # Evaluate the cut.
        defect_score = self.evaluate_cut(position, biscuit)

        # Add the biscuit to the dough roll.
        self.biscuit_placements.append((position, biscuit, defect_score))

        # Lock the biscuit placement.
        for i in range(position, position + biscuit.size):
            self.occupied[i] = True

    def remove_biscuit(self, position: int) -> None:
        """
        Remove a biscuit from the dough roll.
        :param position: Numeric value representing the position of the biscuit.
        :return: None
        """
        for i, (biscuit_position, biscuit, defect_score) in enumerate(self.biscuit_placements):
            if biscuit_position == position:
                self.biscuit_placements.pop(i)
                for j in range(position, position + biscuit.size):
                    self.occupied[j] = False
                return
        raise ValueError("No biscuit found at the specified position.")

    def evaluate(self) -> int:
        """
        Evaluate the dough roll.
        :return: Numeric value representing the total value of the dough roll.
        """
        total_value = sum(biscuit.value for position, biscuit, defect_score in self.biscuit_placements)
        return total_value

    def visualize(self):
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.set_xlim(0, self.length)
        ax.set_ylim(0, 1)
        ax.set_yticklabels([])
        ax.set_yticks([])

        # Draw biscuits
        for position, biscuit, defect_score in self.biscuit_placements:
            rect = patches.Rectangle((position, 0), biscuit.size, 1, edgecolor='black', facecolor='lightblue',
                                     label=f'Biscuit {biscuit.biscuit_type}')
            ax.add_patch(rect)
            plt.text(position + biscuit.size / 2, 0.5, biscuit.biscuit_type, horizontalalignment='center',
                     verticalalignment='center')

        # Mark defects
        for position, defects in self.defects_at_position.items():
            for defect in defects:
                plt.plot(position, 0.5, marker='x', color='red')
                plt.text(position, 0.6, defect.defect_class, color='red', fontsize=8)

        plt.show()

    def max_value(self, pos, remaining_defects, memo):
        """
        Calculate the maximum value using dynamic programming.
        :param pos: Current position on the roll.
        :param remaining_defects: Remaining defect tolerances.
        :param memo: Dictionary for memoization.
        :return: Maximum value that can be achieved from the current position.
        """
        if pos >= self.length:
            return 0

        # Convert remaining_defects to a hashable type for memoization (e.g., tuple)
        remaining_defects_key = tuple(sorted(remaining_defects.items()))

        if (pos, remaining_defects_key) in memo:
            return memo[(pos, remaining_defects_key)]

        max_val = 0
        # Check placing each biscuit at the current position
        for biscuit in biscuits:  # Assuming 'biscuits' is a list of all biscuit types
            if self.is_legal_cut(pos, biscuit, remaining_defects):
                updated_defects = self.update_defects(remaining_defects, pos, biscuit)
                max_val = max(max_val, biscuit.value + self.max_value(pos + biscuit.size, updated_defects, memo))

        memo[(pos, remaining_defects_key)] = max_val
        return max_val
