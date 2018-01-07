# ShadeView
Estimates the street's shade from google street view

This was made in a hackathon, so this is just a back up if I ever want to get back to this. 

# General Idea
The general process I did in the hackathon is as follows:
1. Get all the street names in tel aviv
2. with google location stuff, locate their start, middle and end
3. generate a lot of middle points between them, so I'd have a greed of street locations
4. For each point, take 4 google street photos - one for every direction.
5. For each image, calculate how much sky pixels are they
6. this gives for each point how much sun is exposed to this point
7. make a pretty UI
