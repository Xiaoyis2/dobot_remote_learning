# dobot_remote_learning

### Setting Up the Dynamic Link Library (DLL)

#### **Windows**

Add the directory containing the dynamic link library to the system `Path` environment variable:

1. Open the **System Properties** dialog by pressing `Win + S`, searching for "Environment Variables," and clicking on  **Edit the system environment variables** .
2. In the **System Properties** window, click  **Environment Variables** .
3. Under  **System Variables** , locate and edit the `Path` variable.
4. Add the full path to the directory containing the dynamic link library (`DobotDll.dll`).

#### **Linux**

Add the directory containing the shared library (`libDobotDll.so`) to the `LD_LIBRARY_PATH` environment variable:

1. Open the `~/.bash_profile` file in a text editor.
2. Append the following line to the file:
   ```bash
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/DobotDll
   ```
3. Save the file and restart your computer or run `source ~/.bash_profile` to apply the changes immediately.

#### **Mac**

Add the directory containing the shared library (`libDobotDll.dylib`) to the `DYLD_LIBRARY_PATH` environment variable:

1. Open the `~/.bash_profile` file in a text editor.
2. Append the following line to the file:
   ```bash
   export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/path/to/DobotDll
   ```
3. Save the file and restart your computer or run `source ~/.bash_profile` to apply the changes immediately.

---
