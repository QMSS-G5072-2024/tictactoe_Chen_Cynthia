from tictactoe_yc4336.tictactoe_yc4336 import make_move, initialize_board, check_winner, reset_game
import pytest

# Fixture to create a fresh board for each test
@pytest.fixture
def fresh_board():
    return initialize_board()

def test_initialize_board():
    board = initialize_board()
    assert len(board) == 3  # Check if it's a 3x3 board
    assert all(len(row) == 3 for row in board)  # Ensure each row has 3 columns
    assert all(cell == ' ' for row in board for cell in row)  # Ensure all cells are empty

def test_make_move_empty_board(fresh_board):
    assert make_move(fresh_board, 0, 0, 'X')  # Move should be successful
    assert fresh_board[0][0] == 'X'  # Cell should be updated

def test_make_move_occupied_cell(fresh_board):
    make_move(fresh_board, 0, 0, 'X')
    assert not make_move(fresh_board, 0, 0, 'O')  # Move should fail since cell is occupied

def test_make_move_out_of_bounds(fresh_board):
    with pytest.raises(IndexError):
        make_move(fresh_board, 3, 3, 'X')  # This should raise an IndexError as it's out of bounds

def test_check_winner_x_wins():
    board = [['X', 'X', 'X'],
             [' ', 'O', 'O'],
             [' ', ' ', ' ']]
    assert check_winner(board) == 'X'  # X should win

def test_check_winner_o_wins():
    board = [['X', 'X', 'O'],
             ['O', 'O', 'O'],
             ['X', ' ', ' ']]
    assert check_winner(board) == 'O'  # O should win

def test_check_winner_draw():
    board = [['X', 'O', 'X'],
             ['X', 'O', 'O'],
             ['O', 'X', 'X']]
    assert check_winner(board) == 'Draw'  # It should be a draw

def test_reset_game(fresh_board):
    make_move(fresh_board, 0, 0, 'X')
    new_board = reset_game()
    assert new_board == [[' ' for _ in range(3)] for _ in range(3)]  # Board should be reset to empty

@pytest.mark.parametrize(
    "initial_board, row, col, player, expected_result", [
        # Case 1: Valid move on an empty board
        ([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], 0, 0, 'X', True),
        
        # Case 2: Invalid move (occupied cell)
        ([['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], 0, 0, 'O', False),
        
        # Case 3: Out of bounds (negative row index)
        ([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], -1, 0, 'X', False),  # Will raise IndexError
        
        # Case 4: Out of bounds (row index too large)
        ([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], 3, 0, 'O', False),  # Will raise IndexError
        
        # Case 5: Valid move in middle of board
        ([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], 1, 1, 'X', True)
    ]
)
def test_make_move_param(initial_board, row, col, player, expected_result):
    """
    Parametrized test for make_move function to handle different scenarios:
    - Valid move
    - Invalid move (cell already occupied)
    - Out of bounds (negative index, index too large)
    """
    try:
        result = make_move(initial_board, row, col, player)
        assert result == expected_result
    except IndexError:
        # If the test expects an out of bounds error, it should fail gracefully
        assert not expected_result
