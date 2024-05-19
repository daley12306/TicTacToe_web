import streamlit as st
from easyAI import TwoPlayerGame
from easyAI.Player import Human_Player
from easyAI import AI_Player, Negamax
import numpy as np

class TicTacToe(TwoPlayerGame):
    """The board positions are numbered as follows:
    1 2 3
    4 5 6
    7 8 9
    """

    def __init__(self, players, first_player):
        self.players = players
        self.board = [0 for i in range(9)]
        self.current_player = first_player  # Set the current player based on user choice.

    def possible_moves(self):
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.current_player

    def unmake_move(self, move):  # optional method (speeds up the AI)
        self.board[int(move) - 1] = 0

    def lose(self):
        """ Has the opponent "three in line ?" """
        return any(
            [
                all([(self.board[c - 1] == self.opponent_index) for c in line])
                for line in [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],  # horiz.
                    [1, 4, 7],
                    [2, 5, 8],
                    [3, 6, 9],  # vertical
                    [1, 5, 9],
                    [3, 5, 7],
                ]
            ]
        )  # diagonal

    def is_over(self):
        return (self.possible_moves() == []) or self.lose()

    def show(self):
        board_str = "\n".join(
            [
                " ".join([[".", "O", "X"][self.board[3 * j + i]] for i in range(3)])
                for j in range(3)
            ]
        )
        return board_str

    def scoring(self):
        return -100 if self.lose() else 0


# Initialize Streamlit app
st.set_page_config(page_title="Tic Tac Toe", page_icon=":game_die:", layout="centered")

st.title("❌ Tic Tac Toe ⭕")

# Custom CSS for background and buttons
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i.pinimg.com/564x/2e/66/bd/2e66bd296f6acb84258310f45c0e39ee.jpg");
        background-size: cover;
    }
    .stButton>button {
        font-size: 30px;
        height: 100px;
        width: 100px;
        margin: 10px;
        font-weight: bold;  /* Make the font bold */
        border: 2px solid #000;  /* Add a solid border */
        opacity: 1;
    }
    .stButton>button:hover {
        color: white !important;
        background-color: #80c883 !important;
    }
    .stHeader, .stMarkdown {
        text-align: center;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# HTML to embed background music
st.markdown(
    """
    <audio autoplay loop>
        <source src="https://joeybabcock.me/blog/wp-content/uploads/2019/05/lobby-classic-game-halloween.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    """,
    unsafe_allow_html=True
)

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.session_state.first_player = st.selectbox("Who goes first?", options=["Human", "AI"])
    if st.button("Start Game"):
        first_player = 1 if st.session_state.first_player == "Human" else 2
        ai_algo = Negamax(6)
        st.session_state.game = TicTacToe([Human_Player(), AI_Player(ai_algo)], first_player)
        st.session_state.started = True

        if first_player == 2:  # If AI goes first
            ai_move = st.session_state.game.get_move()
            st.session_state.game.make_move(ai_move)
            st.session_state.game.switch_player()
else:
    game = st.session_state.game

    # Define the move function
    def make_move(row, column):
        move = 3 * row + column + 1
        if move in game.possible_moves() and not game.is_over():
            game.make_move(move)
            game.switch_player()
            if not game.is_over():
                ai_move = game.get_move()
                game.make_move(ai_move)
                game.switch_player()

    # Display the board
    board_array = np.array(game.board).reshape(3, 3)
    board_display = board_array.tolist()

    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            if board_display[i][j] == 0:
                cols[j].button(" ", key=f"{i}-{j}", on_click=lambda i=i, j=j: make_move(i, j))
            elif board_display[i][j] == 1:
                cols[j].button("⭕", key=f"{i}-{j}", disabled=True)
            elif board_display[i][j] == 2:
                cols[j].button("❌", key=f"{i}-{j}", disabled=True)

    if game.is_over():
        if game.lose():
            st.header("You lose!")
        else:
            st.header("It's a draw!")
        if st.button("Restart"):
            st.session_state.started = False
            st.experimental_rerun()
    else:
        st.markdown("### Your turn! Play by clicking a button.")

    st.markdown(
        """
        <style>
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )
