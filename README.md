# spotifyPlaylistGenerator
This generates a playlist for you based on your preferred genre, most recently listened music, top listened to artists, top tracks, top albums. 


Copyright © 2022 AirDeb

This playlist generator works more efficiently when you choose a genre that you listen to frequently based on the algorithm. 
To access this, the client secret must be obtained by the developer for proper authorization of the API.

Around 67%-82% of the songs will be from new artists that are similar to the ones you previously listened to.

The spotipy library must be installed on your computer to use this program.
On your terminal, type "pip install spotipy" (without the quotes) to download the library.


IMPORTANT: Make sure you enter the username that is under your account overview under Spotify. Your username should be located here under your profile:
![image](https://user-images.githubusercontent.com/97564205/171031982-5efb53e6-6e93-480d-aa7a-54b6b839c81a.png)



To run the program, go into the work directory by setting the directory on your terminal as the downloaded folder from the respository.
After setting the directory on your terminal, type into the terminal "python frontend.py" (without the quotation marks)
If you have done that properly, you should be on the application. It will look something like this:

![image](https://user-images.githubusercontent.com/97564205/171032519-267f7d62-1a61-41f5-998d-ce55b52f8918.png)

NOTE: The maximum number of songs you can enter is 100 because that is the maximum that Spotify's API allows. Otherwise, you will get an error message.
The privacy tab is for whether you want your playlist public or private.

Spotify periodically changes it's authorization into it's API, so if there's any issues feel free to let me know and I'll update the app. 

Enjoy and happy listening!
