## Game Concept
You play as a robot hand deep in the darkness of space.
With only two minutes worth of power left your objective is to smash as many asteroids as you can.
Good luck!  
![Robot Hand Asteroid Smasher GIF](docs/gameplay.gif "Basic gameplay of RHAS")
## List of Technologies Used
- [Python 3.9.7](https://www.python.org/downloads/release/python-397/ "Python 3.9.7")
- [Pygame 2.0.1](https://www.pygame.org/docs/ "Pygame Documentation")
- [Visual Studio Code](https://code.visualstudio.com/ "VS Code")
- Microsoft Paint
- [BeepBox](beepbox.co/ "BeepBox")

## Motivation Behind the Game
I was inspired by the games made by YouTuber [DaFluffyPotato](https://www.youtube.com/c/DaFluffyPotato "DaFluffyPotato's YouTube Channel")
using [Pygame](https://www.pygame.org/docs/) and started going through the [Pygame tutorials](https://www.pygame.org/docs/#tutorials "Pygame Documentation Tutorials")
available in the documentation. After completing the [Line By Line Chimp](https://www.pygame.org/docs/tut/ChimpLineByLine.html "Line By Line Chimp Tutorial") I got a grasp
of the basics like blitting an image onto the screen and detecting mouse movement and wanted to make a game which would enable me to practice these concepts and expand on them.
Thus, [Robot Hand Asteroid Smasher](https://github.com/tonypham04/Robot-Hand-Asteroid-Smasher "RHAS Repo") was born.

## References
- [Line by Line Chimp](https://www.pygame.org/docs/tut/ChimpLineByLine.html "Line by Link Chimp Tutorial from Pygame docs")
- [pygame.Surface.set_colorkey](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.set_colorkey "set_colorkey method from Pygame docs")
- [Pixeltype.ttf](https://github.com/clear-code-projects/UltimatePygameIntro/tree/main/font "Source of the Pixeltype.tff file used in this project")
- [pygame.mixer.Sound.play](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.play "play method from Pygame docs")

## Developer Notes
### Thursday, November 25, 2021
Attempted to create an executable file using [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html "Install Pyinstaller") with the following commands:
```
pyinstaller game.py --onefile --noconsole
pyinstaller --onefile -w game.py
```
The problem is Windows 10 flags the generated executable as a virus and then deletes it :frowning:.
Lessons learned here are:
- [Pyinstaller](https://www.pyinstaller.org/ "Pyinstaller Quickstart") creates the executable in the "dist" directory
- The resulting filename.spec file, and contents in the build directory are not needed
- Even without Windows 10 flagging the executable, the .exe file needs access to the assets, files, etc it would have needed running as a Python file