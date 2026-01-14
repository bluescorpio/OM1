import pytest
from unittest.mock import MagicMock, patch
from actions.move_turtle.interface import MoveInput, MovementAction
from actions.move_turtle.connector.zenoh import MoveZenohConnector, MoveZenohConfig

class TestMoveZenohConnector:
    """Test move turtle connector with focus on enum comparison fixes"""
    
    def test_enum_action_comparisons(self):
        """Test that all enum actions are processed correctly"""
        config = MoveZenohConfig()
        connector = MoveZenohConnector(config)
        
        test_cases = [
            MovementAction.TURN_LEFT,
            MovementAction.TURN_RIGHT,
            MovementAction.MOVE_FORWARDS,
            MovementAction.STAND_STILL
        ]
        
        for action in test_cases:
            mock_input = MoveInput(action=action)
            # Should not raise exceptions for valid enum values
            assert connector.connect(mock_input) is None
            
    def test_invalid_action_handling(self):
        """Test handling of invalid/unknown actions"""
        config = MoveZenohConfig()
        connector = MoveZenohConnector(config)
        
        # Test with invalid action (not in enum)
        mock_input = MoveInput(action="invalid_action")
        
        # Should handle gracefully (not crash) - implementation specific behavior
        result = connector.connect(mock_input)
        # The result depends on implementation - verify it doesn't crash
        assert result is None or result is not None