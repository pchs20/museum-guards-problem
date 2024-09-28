from typing import Any, Dict, Optional


def get_problem_data() -> Dict[Optional[str], Any]:
    """Build and return input data for the problem."""
    return {
        None: {
            'rooms': {None: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']},
            'doors': {
                None: [
                    ('A', 'B'), ('B', 'H'), ('H', 'I'), ('I', 'J'),
                    ('A', 'C'), ('A', 'D'), ('D', 'E'),
                    ('A', 'G'), ('G', 'I'),
                    ('A', 'F'), ('F', 'D'),
                ]
            }
        }
    }
