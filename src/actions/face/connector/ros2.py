import logging

from actions.base import ActionConfig, ActionConnector
from actions.face.interface import FaceInput, FaceAction


class FaceRos2Connector(ActionConnector[ActionConfig, FaceInput]):
    """
    Connector to link Face action with ROS2.
    """

    def __init__(self, config: ActionConfig):
        """
        Initialize the FaceRos2Connector with the given configuration.

        Parameters
        ----------
        config : ActionConfig
            Configuration parameters for the connector.
        """
        super().__init__(config)

    async def connect(self, output_interface: FaceInput) -> None:
        """
        Connect to the ROS2 system and send the appropriate face command.

        Parameters
        ----------
        output_interface : FaceInput
            The face input containing the action to be performed.
        """
        new_msg = {"face": ""}

        if output_interface.action == FaceAction.HAPPY:
            new_msg["face"] = "happy"
        elif output_interface.action == FaceAction.CONFUSED:
            new_msg["face"] = "confused"
        elif output_interface.action == FaceAction.CURIOUS:
            new_msg["face"] = "curious"
        elif output_interface.action == FaceAction.EXCITED:
            new_msg["face"] = "excited"
        elif output_interface.action == FaceAction.SAD:
            new_msg["face"] = "sad"
        elif output_interface.action == FaceAction.THINK:
            new_msg["face"] = "think"
        else:
            logging.info(f"Unknown face type: {output_interface.action}")

        logging.info(f"SendThisToROS2: {new_msg}")
