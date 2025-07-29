# MY LXB

## What Is LXB ?

LXB is ~~the initals of **"Legislation Xmas Boy"**(圣诞律法小子)~~ my friend and my classmate. So you can regard this program a trick ~~directly towards LXB and even has his agreement.~~

if you are interested in him, you can click here to visit [LXB's blog](chose-b-log.netlify.app).

And **my *evil* idea** to general this program is that, ***you can regard it as that LXB is a pet on your desktop if you open my project, ~~and waitting for your flirtation~~***.

Back to the topic, this is a program desktop pet called **pyPet**,  ~~or you can told it " My LXB".~~ 

it's programed under new framework `PyQt6`, there may be something new between qt5.

As I know both two framework can easily design a desktop pet. And I truly achieve one ~~(with better art assets but was lost)~~ before.

## How To Use My LXB ?

Well, is quite simple to just run the "main.py" in the program to start. and if you are not satisfied in current images, you can replace them with your file (of course with the same name).

## How I Generate The F**king Assets ?

Of course, I'm sure that no one will be happy when the see my test (and even perfunctory) image pre-setting for my LXB. But there are truly some potential editors who are interested in my drawing progress.

To be honest, I just opened a 256x256 canvas in SAI2 and drew some line on it (even didn't use my Tablet), I didn't use any tool but directly change the .png to .gif. How bad I am !


## Where Will LXB go ?

In fact, there is a long way to go from my (or our) goal. if you are glad to help me, you can read the following content.

Geneally speaking, I'd like to design a GUI for LXB, which could be display as I right-click the pet; Adding some interesting fuction to the poor LXB; Create a music moduels...

The charm of coding is that you can do what ever you want, just as you have enough creativity to do that!

as someone said: ` Talk Is Cheap, Show Me The Code!`. Everyone are welcomed to join us!

I hope one day I could proudly give it to LXB, and saying that "Haha, it's you!" (although my mom may be greeting by him).

### Add new state for LXB

it's easy to add new content for this small pet. Just add new state in `state.py`, and providing a gif with name same as the string you give to the state in `./resource/img/`.

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

and add a 'run.gif' to `./resource/img/`, a new state will be create.The loading process of the new state are automatical, you needn't do anything more except think it will take into effect. 

Of course, we can't use it directly. So we need to add a new trigger logic for the state to enter into force.

As you have decided when you should change into your state, just use fuction `swtich_state(PetState.RUN)` to change. If you have other idea, you can achieve them with the knowledge of `PyQt6`.










