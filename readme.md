# GLHF

This web application was intentionally built with security flaws commonly found in real-world systems.

Your task is to find and understand these issues using everything you've learned so far.

For each vulnerability, take note of:

• Name of the vulnerability  
• Affected component  
• Description of what happens  
• Steps to reproduce the issue  
• Screenshot or any technical evidence  
• What the impact would be if exploited  
• How the issue could be fixed

Keep your notes organized. You'll need them to write your report later.



## Installation

### Requirements

- **Docker** installed on your system.

### Running Locally

1. Pull the image directly from Docker Hub:  
   ```bash
   docker pull coriscope/glhf:v0.1-beta
   ```

2. Run the container *(mapping port 1337)*:  
   ```bash
   docker run -p 1337:1337 coriscope/glhf:v0.1-beta
   ```

3. Access the app in your browser:  
   - [http://localhost:1337](http://localhost:1337)

```
      ___                         ___           ___   
     /  /\                       /__/\         /  /\  
    /  /:/_                      \  \:\       /  /:/_ 
   /  /:/ /\    ___     ___       \__\:\     /  /:/ /\
  /  /:/_/::\  /__/\   /  /\  ___ /  /::\   /  /:/ /:/
 /__/:/__\/\:\ \  \:\ /  /:/ /__/\  /:/\:\ /__/:/ /:/ 
 \  \:\ /~~/:/  \  \:\  /:/  \  \:\/:/__\/ \  \:\/:/  
  \  \:\  /:/    \  \:\/:/    \  \::/       \  \::/   
   \  \:\/:/      \  \::/      \  \:\        \  \:\   
    \  \::/        \__\/        \  \:\        \  \:\  
     \__\/                       \__\/         \__\/  
```
