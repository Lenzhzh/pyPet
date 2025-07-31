[ENGLISH README](README.md)
[中文README](README_cn_zh.md)

---

# My LXB

## What Is LXB?

LXB is ~~the initials of **"Legislation Xmas Boy"** (圣诞律法小子)~~ my friend and my classmate. So you can regard this program as a trick ~~directed towards LXB, and he has even agreed to it~~.

If you are interested in him, you can click here to visit [LXB's blog](chose-b-log.netlify.app).

And **my *evil* idea** behind this program is that ***you can think of it as having LXB as a pet on your desktop if you open my project, ~~and waiting for your flirtation~~***.

Back to the topic, this is a desktop pet program called **pyPet**~~, or you can call it "My LXB"~~.

It's programmed using the new framework `PyQt6`, so there may be some differences from Qt5.

As far as I know, both frameworks can be used to easily design a desktop pet. And I actually made one before ~~(with better art assets, but they were lost)~~.

## How To Use My LXB?

Well, it's quite simple. Just run `main.py` to start the program. If you are not satisfied with the current images, you can replace them with your own files (using the same filenames).

## How Did I Generate The F**king Assets?

Of course, I'm sure that no one will be happy when they see my test (and even perfunctory) image presets for my LXB. But there might be some potential contributors who are interested in my drawing process.

To be honest, I just opened a 256x256 canvas in SAI2 and drew some lines on it (without even using my tablet). I didn't use any animation tools and just directly converted the `.png` to a `.gif`. I know, it's pretty bad!

## Where Will LXB Go?

In fact, there is a long way to go to reach my (or our) goal. If you would like to help, you can read the following content.

Generally speaking, I'd like to design a GUI for LXB that would display when I right-click the pet, add some interesting functions for the poor LXB, create a music module, and more.

The charm of coding is that you can do whatever you want, as long as you have enough creativity!

As someone said: `Talk Is Cheap, Show Me The Code!`. Everyone is welcome to join us!

I hope one day I can proudly give it to LXB and say, "Haha, it's you!" (although my mom might be greeted by him).

### Add a New State for LXB

It's easy to add new content to this small pet. Just add a new state in `state.py` and provide a GIF with the same name as the string you assigned to the state in the `./resource/img/` directory.

For example, if you want to add a "Run" state, you just change the file to:
```python
# state.py
import enum

class PetState(enum.Enum):
    STANDBY = 'standby'
    DRAG = 'drag'
    MOVE = 'move'

    # add a run state
    RUN = 'run'
```
Then, add a `run.gif` to `./resource/img/`, and a new state will be created. The new state will be loaded automatically; you don't need to do anything else for it to be recognized by the program.

Of course, we can't use it directly yet. We need to add trigger logic for the state to take effect.

Once you have decided when the pet should change to your new state, just use the function `switch_state(PetState.RUN)` to change it. If you have other ideas, you can implement them using your knowledge of `PyQt6`.