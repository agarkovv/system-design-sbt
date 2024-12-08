import allure
import pytest
from app.main import main, print_menu


@allure.epic("Main Application")
class TestMain:

    @allure.feature("Menu")
    @allure.story("Menu Display")
    def test_print_menu(self, capsys):
        """Test menu printing"""
        with allure.step("Print menu"):
            print_menu()
            captured = capsys.readouterr()
            assert "Graph Operations:" in captured.out
            assert all(str(i) in captured.out for i in range(9))

    @allure.feature("Main Function")
    @allure.story("Demo Mode")
    def test_main_demo_mode(self, capsys):
        """Test main function in demo mode"""
        with allure.step("Run main in demo mode"):
            main(True)
            captured = capsys.readouterr()
            assert "Running demo graph operations..." in captured.out
            assert "Creating vertices A, B, C..." in captured.out
            assert "Demo completed. Exiting..." in captured.out

    @allure.feature("Main Function")
    @allure.story("Graph Operations")
    def test_main_graph_operations(self, capsys):
        """Test main function graph operations"""
        with allure.step("Verify graph operations"):
            main(True)
            captured = capsys.readouterr()
            output = captured.out

            # Verify vertex creation
            assert "Creating vertices A, B, C..." in output

            # Verify edge creation
            assert "Adding edges: A->B (weight 1.0), B->C (weight 2.0)..." in output

            # Verify path analysis
            assert "Path from A to C:" in output
            assert "Is graph cyclic:" in output
