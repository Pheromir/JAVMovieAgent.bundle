# JAVMovieAgent.bundle
A Plex Metadata Agent for JAV Movies.
This Plugin requires access to an [imgproxy](https://github.com/imgproxy/imgproxy) instance to crop the movie covers properly. It's pretty easy to install a local instance using docker (just make sure it's not accessible from the outside).

Please don't expect too much of this plugin, it might be full of bugs and throw some errors.

## Supported Sites
- R18.com
- JavLibrary.com
- Jav.Land
- JavHaven.com

## Installation
1. Download the latest code from this repository: "Code" -> "Download ZIP"
2. Unzip the downloaded file
3. Rename "JAVMovieAgent.bundle-master" to "JAVMovieAgent.bundle"
4. Drop the folder into your [Plug-ins](https://support.plex.tv/articles/201106098-how-do-i-find-the-plug-ins-folder/) directory

5. Go into the Plugin's settings (Plex Settings -> Agents -> JAVMovie -> Settings Gear)
6. Insert the URL to the imgproxy instance you want to use

## Todo
- Authorization Header support for imgproxy
- Option to disable imgproxy cropping
- Check dimensions of image to prevent cropping an image which might already be the front cover only