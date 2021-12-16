# JAVMovieAgent.bundle
A Plex Metadata Agent for JAV Movies.
This Plugin requires access to an [imgproxy](https://github.com/imgproxy/imgproxy) instance to crop the movie covers properly. It's pretty easy to install a local instance using docker (just make sure it's not accessible from the outside).

Please don't expect too much of this plugin, it might be full of bugs and throw some errors.

## Supported Sites
- R18.com
- JavLibrary.com
- Jav.land
- JavHaven.com

## Filenames
Currently the agent uses the name given by Plex to search for the metadata. My recommendation is to name the files by the JAV Code and nothing more (except for the file extension of course).
If a JAV DVD consists of multiple files you can add "cd1", "cd2" etc. to the filename.
Examples:
`ABC-123.mp4`
`DEF-456 cd1.mp4`
`DEF-456 cd2.mp4`

## Installation
1. Download the latest code from this repository: "Code" -> "Download ZIP"
2. Unzip the downloaded file
3. Rename "JAVMovieAgent.bundle-main" to "JAVMovieAgent.bundle"
4. Drop the folder into your [Plug-ins](https://support.plex.tv/articles/201106098-how-do-i-find-the-plug-ins-folder/) directory

5. Go into the Plugin's settings (Plex Settings -> Agents -> JAVMovie -> Settings Gear)
6. Insert the URL to the imgproxy instance you want to use

## Todo
- Authorization Header support for imgproxy
- Option to disable imgproxy cropping
- Check dimensions of image to prevent cropping an image which might already be the front cover only