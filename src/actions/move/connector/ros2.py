import logging

from actions.base import ActionConfig, ActionConnector
from actions.move.interface import MoveInput, MovementAction


class MoveUnitreeSDKConnector(ActionConnector[ActionConfig, MoveInput]):
    """
    Connector to link Move action with Unitree SDK via ROS2.
    """

    def __init__(self, config: ActionConfig):
        super().__init__(config)

    async def connect(self, output_interface: MoveInput) -> None:
        """
        Connect the input protocol to the move action via Unitree SDK.

        Parameters
        ----------
        output_interface : MoveInput
            The input protocol containing the action details.
        """
        new_msg = {"move": ""}

        # stub to show how to do this
        if output_interface.action == MovementAction.STAND_STILL:
            new_msg["move"] = "stand still"
        elif output_interface.action == MovementAction.SIT:
            new_msg["move"] = "sit"
        elif output_interface.action == MovementAction.DANCE:
            new_msg["move"] = "dance"
        elif output_interface.action == MovementAction.SHAKE_PAW:
            new_msg["move"] = "shake paw"
        elif output_interface.action == MovementAction.WALK:
            new_msg["move"] = "walk"
        elif output_interface.action == MovementAction.WALK_BACK:
            new_msg["move"] = "walk back"
        elif output_interface.action == MovementAction.RUN:
            new_msg["move"] = "run"
        elif output_interface.action == MovementAction.JUMP:
            new_msg["move"] = "jump"
        elif output_interface.action == MovementAction.WAG_TAIL:
            new_msg["move"] = "wag tail"
        else:
            logging.info(f"Other move type: {output_interface.action}")
            # raise ValueError(f"Unknown move type: {output_interface.action}")

        logging.info(f"SendThisToROS2: {new_msg}")
