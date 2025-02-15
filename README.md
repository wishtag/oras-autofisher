# ORAS AutoFisher
A python program for Omega Ruby and Alpha Sapphire playing on Citra that automatically fishes for you until it finds a shiny  

This is a project I was really proud of at the time, but now that I'm uploading my stuff to GitHub I realize how not user-friendly this is.  

I don't have any plans to update this, or even write instructions on how to set this up for yourself. This repository was really only created as a way to archive and showcase a project I was proud of.  
# Features
## Automatic Fishing
Through the `pydirectinput` library, the program is able to send inputs to the game. After sending the input to send your fishing rod out, the program will monitor the screen until the exclamation mark bubble appears. Once that shows up, it sends the input to reel it in.  
## Logging
Tracks the current chain, elapsed time, encounters, elapsed time since last shiny, and encounters since last shiny.
## Shiny Detection
In ORAS, shiny pokémon have a special animation that plays when they are encountered. This animation delays the appearance of the UI. So by monitoring the screen and seeing how long it takes for the UI to appear, we can tell if the pokémon encountered is a shiny or not. That's exactly what the program does.  

If the pokémon is shiny, then the program will stop. If the pokémon is not shiny, the program will send the inputs to run away from the encounter. After that, it starts fishing again.  
## Discord Notifying
Through the use of a discord webhook, the program will notify you when it finds a shiny.  
<img src="readme_img/Webhookoutput.png" alt="Webhook">
# Showcase
Here's a little video showing off the program in action  
https://github.com/user-attachments/assets/e70163cd-f107-4e91-9837-0fb4a49f178e


Ill move this later but for now i gotta write it somewhere

# Setup
I designed this program with a specific window position, size, and resolution. So if you're set up isn't the exact same as mine then you'll have some extra work to do.  
## My Setup
I have my setup organized like this:  
<img src="readme_img/setup.png" alt="Setup" style="width:100%;">  
I'm on a `1080p` display, with my windows split so VS Code takes up the left half and the Citra emulator takes up the right half. In Citra, I have `Screen Layout` set to `Default` along with `Show Status Bar` enabled. If you replicate this setup, you get to skip to here(but like some html i dont even know but just make it where when you click "here" it takes them to the next step they need to do). Otherwise, keep following these steps.  
## Getting Bounding Boxes