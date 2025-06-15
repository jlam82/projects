class Surveilled:
    """
    Class module for setting destroyer and observer tkinter variables.
    
    Meant to be used for inheritance.
    """
    destroyer, observer = None, None

    @classmethod
    def set_destroyer(cls, destroyer_instance):
        cls.destroyer = destroyer_instance

    @classmethod
    def set_observer(cls, observer_instance):
        cls.observer = observer_instance

    def __init__(self):
        if not Surveilled.destroyer:
            raise ValueError("destroyer instance in the form of a tk.IntVar() has not been set.")
        if not Surveilled.observer:
            raise ValueError("observer instance in the form of a tk.BooleanVar() has not been set.")