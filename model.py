from pyomo.environ import (
    AbstractModel,
    Binary,
    Constraint,
    Expression,
    minimize,
    Objective,
    Set,
    Var,
)
from pyomo.core.expr.relational_expr import InequalityExpression


def get_abstract_model() -> AbstractModel:
    model = AbstractModel(name='museum-guards')

    # Sets
    model.rooms = Set(
        name='rooms',
        doc='Rooms of the museum',
        dimen=1
    )
    model.doors = Set(
        name='doors',
        doc='Doors between two rooms of the museum.',
        dimen=2,
        within=model.rooms * model.rooms
    )

    # Variables
    model.guard_at_door = Var(
        model.doors,
        name='guard_at_door',
        doc='Binary variable: 1 if guard is placed, 0 otherwise.',
        domain=Binary,
    )

    # Constraints
    model.constraint_at_least_one_guard_per_room = Constraint(
        model.rooms,
        name='constraint_at_least_one_guard_per_room',
        doc=constraint_at_least_one_guard_per_room.__doc__,
        rule=constraint_at_least_one_guard_per_room,
    )

    # Objective function
    model.objective_function = Objective(
        name='objective_function',
        doc='Have the minimum number of doors guarded.',
        rule=number_of_guards,
        sense=minimize,
    )

    return model


# Constraints definition
def constraint_at_least_one_guard_per_room(
        model: AbstractModel,
        room: str,
) -> InequalityExpression:
    """Force that each room is guarded for at least one guard.

     This means that at least in one of the doors of each room, a guard should be placed.
     """
    guards_at_room = (
        sum(model.guard_at_door[door] for door in model.doors if room in door)
    )
    return guards_at_room >= 1


# Objective function definition
def number_of_guards(model: AbstractModel) -> Expression:
    """Return the total number of guards placed in the doors of the museum."""
    return sum(model.guard_at_door[door] for door in model.doors)
