

## Installation


3. **Clone the repository**:

```
git clone 
```

2. **Create and activate a virtual environment (optional but recommended)**:

```
conda create -n env python=3.10 -y
```

```
conda activate env
```

3. **add depencencies**
```
pip install .
```

1. **Install claude desktop**:

Download and install from this [link](https://claude.ai/download)

2. **Google App password verification**:
myaccount.google.com/security -> 2 step verification -> enable it

myaccount.google.com/apppasswords -> enter app name -> create -> copy paste the generated password





5. **Add Claude config file**
open cluade desktop > menu > file > settings... > Developer > Edit config > claude_desktop_config.json > add the following file
```
{
  "mcpServers": {
    "hr-assist": {
      "command": "C:\\Users\\linto\\anaconda3\\Scripts\\uv",  # add location of uv.exe in your system
      "args": [
        "--directory",
        "C:\\Users\\linto\\code\\hr-ai-agent",  # location of project file. where your code is
        "run",
        "server.py"
      ],
      "env": {
        "CB_EMAIL": <enter here>,
        "CB_EMAIL_PWD": <enter here>
      }
    }
  }
}
```

4. **Run**

claude -> + -> add from hr assistant -> run prompt -> give details
Note: if changes are not reflecting. then close claude desktop app and kill the task in task manager and reopen.



## Installation Guide
Follow these steps to set up and run the project on your system

### **1. Clone the Repository**
```
git clone https://github.com/lintosunny/hr-ai-agent.git
```

### **2. Create and Activate a Virtual Environment (Recommended)**
Using Conda:
```
conda create -n env python=3.10 -y
conda activate env
```

### **3. Install Dependencies**
Install project dependencies with ```pyproject.toml```
```
pip install .
```

### **4. Install Claude Desktop**
Download and install Claude Desktop from *[here](https://claude.ai/download)*

### **5. Configure Google App Password**
1. Go to: *[Google Account Security](myaccount.google.com/security)*
2. Enable 2-Step Verification
3. Create an App Password at *[Google App Passwords](myaccount.google.com/apppasswords)*
4. Enter an app name → click Create → copy and save the generated password

### **6. Add Claude Config File**

Open Claude Desktop and navigate: *Menu → File → Settings → Developer → Edit config*

Locate ```claude_desktop_config.json``` and add the following:

```
{
  "mcpServers": {
    "hr-assist": {
      "command": "C:\\Users\\linto\\.local\\bin\\uv",  // replace uv.exe location specific to your system
      "args": [
        "--directory",
        "C:\\Users\\linto\\code\\hr-ai-agent",  // replace project folder location specific to your system
        "server.py"
      ],
      "env": {
        "CB_EMAIL": "<enter your email here>",
        "CB_EMAIL_PWD": "<enter your generated app password here>"
      }
    }
  }
}
```

### **7. Run the AI agent**
1. Open Claude Desktop
2. Click + → select Add from hr assistant
3. Run a prompt and provide required details

If changes do not reflect:
* Close Claude Desktop
* Kill the task from Task Manager
* Reopen the app