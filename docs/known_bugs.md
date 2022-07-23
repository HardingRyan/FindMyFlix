# **FindMyFlix - Known Bugs**

This document contains a collection of issues and glitches which are known by the developer. If you encounter a bug which is not already listed here, please report it <a href="mailto: rn.hardingg@utexas.edu">here.</a>

<strong> Last updated: July 22, 2022</strong>

- Scrolling in the results window only works when physically using the scrollbar, instead of working anywhere within the window.

- Clicking & holding while dragging the scroll bar can cause images to temporarily load incorrectly. The images are immediately fixed once the scrollbar is released and the screen lands in a definite position; this issue is a minor cosmetic one.

- Resizing the application can be laggy. This is due to the fact that the background image is recreated each time the screen size is changed. The resizing does not experience lag when the background image is removed.

- The application appears to "not respond" when loading a large amount of search results. This is not indicative of the app crashing; the results are still loading as normal in the background, and waiting through this period will result in the correct behavior.

- Scrolling through the streaming sources in a detailed view card causes the sources to partially extend outside of the allocated space for them.

- For streaming sources with a long title, the title extends beyond the allocated title display box. The link is still functional regardless, and the logo should aid in deciphering the title of the source.