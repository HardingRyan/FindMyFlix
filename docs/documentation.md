# **FindMyFlix - Documentation**

This document contains more detailed information about FindMyFlix, technical explanations, primary use cases, and references for developers who wish to use this code. Please consult the known_bugs document for information about application issues and troubleshooting.

## General

FindMyFlix is a streaming service availability and media information platform. This service has only been tested on Windows systems. By searching all or part of a title, the service will automatically generate results of every relevant show stored in the database, providing as much information as possible. The backbone of this application is built with the [Watchmode](https://www.watchmode.com/) platform. Watchmode's information is consistently updated to include past, present, and even near future releases.

On first launch, if your computer has a firewall or security software, it might prompt saying that FindMyFlix.exe does not have a valid digital signature, and it will block the program from running and mark it as potentially dangerous. To get around this, select the option which is most equivalent to "always allow," and then restart the application in order to allow it to work. There is no dangerous or malicious component of this application; the code is open source in this repository, and please reach out to me by email if you have any related questions.

## For Developers

The following is a breakdown of unique files/folders, as well as their usage/significance:

| Name | Explanation |
| ------ | ------|
|`__main__.py` | The main driver file of the application. This file contains the main Tkinter window for the application, as well as functionality related to searches, displaying results, and formatting. A majority of the actual code is located here. Only one instance of the application can be active at a time.|
| `resultcard.py` | A file containing the `ResultCard` class, which is used to organize results from an individual result in a general search.|
| `showcard.py` | A file containing the `Showcard` class, which is used to organize more detailed information about a show which is generated and presented upon user request to view details. Additionally within this file is the `Source` class, a helper class which is used to organize information about an individual streaming source for a particular show. This class is only present upon user request to view details. |
| `tkHyperlinkManager.py` | A helper class meant to organize hyperlink insertion within a Text element in Tkinter. This file is not of my creation. The original can be found [here](https://github.com/GregDMeyer/PWman/blob/master/tkHyperlinkManager.py). |
| `/tests/` | Static JSON files used to debugging and testing. The files are results from actual calls to the API, and they can be manually plugged in for offline development purposes. One file of interest within this folder is sources.json, a static list of all supported sources from the platform. The purpose of this file is to retrieve logo information for display purposes. |

The main issue which developers might run into if they choose to utilize this code is in communicating with the API. Watchmode requires a unique key. For me, this key was stored in an untracked file called `config.py`, and the key was used by calling `config.key`. In order to use this application independently, the developer must sign up for a key [here.](https://api.watchmode.com/). The free version has a limit of 1,000 API calls per month. Watchmode has a very friendly documentation, FAQ section, and live support chat to answer any questions which developers might have.

This project was also created in a virtual Python environment, so those who wish to clone this repository would need to use `pip` to install certain modules if they aren't already within the local Python environment. Please reach out to me <a href="mailto:rn.hardingg@utexas.edu">here</a> if you have any more questions!


