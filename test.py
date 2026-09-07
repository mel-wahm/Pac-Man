from Src.views.leaderboard_view import Board

import arcade
view = arcade.Window()
Board(view).update_json("notme", 100)
print(Board(view).board)