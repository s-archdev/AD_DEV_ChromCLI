# AD_DEV_ChronCLI

```
                                                                                                    
                                      .                                                             
                                       =                                                            
                                        :                                                           
                                        =                                                           
                                         -                                                          
                                         #                                                          
                                         #                                                          
                                         -                                                          
                                       #                                                            
                                     **                                                             
                                    #                                                               
                                   #                                                                
                                 . %                                                                
                                 - #                                                                
            .                    : #                                                                
             -----.               .                                                                 
         @@########@@-=-          #                                                                 
       #-            .##@--: .     #                                                                
     #:   @@@@@@@     @:.+*@ -  .   #      @@@@@ @@@@@@@*       @@@@@@@@@@+@@@@@:    @@@@@@         
  . #    @@@@@@@@     @@@@@@+#@ -    #.   @@@@@* @@@@@@@@@@@    @@@@@@@@@@@ @@@@@    @@@@@          
    #    @@@@@@@@     @@@@@@@@@ @ --  #@  @@@@@  @@@@@@@@@@@@   @@@@@@@@@@@ @@@@@    @@@@@          
   =     @@@@@@@@.    @@@@@   @@@-#@ - =# @@@@@  @@@@@   @@@@@  @@@@@       @@@@@    @@@@@          
   # .   @@@@@@@@@    @@@@@   @@@@@ #@ -- #@@@*  @@@@@   @@@@@  @@@@@       @@@@@    @@@@+          
   # .  @@@@@-@@@@    @@@@@   @@@@@   #@#-: @@   @@@@@   @@@@@  @@@@@        @@@@   .@@@@           
   .    @@@@@ @@@@    @@@@@   @@@@@      @@ -    @@@@@   @@@@@  @@@@@        @@@@@  @@@@@           
    *   @@@@@ @@@@=   @   #=* @@@@@    @#@-#@ -  @@@@@   @@@@@  @@@@@        @@@@@  @@@@@           
        @@@@@ @@@@@   @@@@@   @ @@@  @# @@@@@#@*:  @@@   @@@@@  @@@@@@@@@@   @@@@@  @@@@@ .         
        @@@@. @@@@@   @@@@@   @@=  @%   @@@@@  #@@ : @   @@@@@  @@@@@@@@@@ . @@@:+                  
       @@@@@  @@@@@   @@@@@   @  @@     @@@@%    ##@ -   @@@@@  @@@@@:...#   +  *#:*@@%@*#@@-       
       @@@@@  @@@@@   @@@@@    =@#@ *  @@@@@     @@@#@ :-             *#* .-. @@@@ .@@@@    #@-     
       @@@@@   @@@@@  @@@@@   @#@@@  # @@@@@          #@@ - %@@@@@@@@=---     @@@@ @@@@@      #     
       @@@@@@@@@@@@@  @@@@@  @@@@@@      @@     @@@##@   #@  -  @@@@@ *#@@--  @@@@ @@@@         @ . 
      @@@@@@@@@@@@@@  @@@@  @ @@@@@   @@    @@@% @@@@@   @@*#@  -  @@     # .  @@@ @@@@     .  @@ . 
      @@@@@@@@@@@@@@  @@@@ #@ @@@@@      @@@.    @@@@@   @@@@@-#@-  -  .    @  @@@@@@@@  .    @#    
      @@@@@    @@@@@  @@@@.  :@@@    :@##@+  #@@ @@@@@@@@@@@@#  @##%@..:--  .  =           @@#      
      @@@@@    @@@@@@ @@@@@*@    %@@#%@@@@     . **     +@@@#   @@@@@.*#@@@@@#-.  .@@@@@%##         
     =@@@@@     @@@@@ @@@@@@@@%##:   @@@@@       @@@@@####*=*@@+.  .@@@##@@ =##%@@@@@@   .          
                                     @@@@@                  ..:-=-:                                 
                                    @@@@@                                                           
                                                                                                    
```

A simple but powerful terminal-based calendar and task scheduler for MacOS.

## Features

- Dual-window interface with task list and calendar view
- Simple text-based UI that runs in the terminal
- Create tasks with start and end times
- Mark tasks as completed
- Navigate through months in the calendar view
- Persistent storage of tasks
- Keyboard shortcuts for all operations

## Requirements

- Python 3.6+
- MacOS (tested on MacOS Monterey 12.0+)
- Terminal with curses support

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/ad_dev_chroncli.git
cd ad_dev_chroncli

# Run the installer
python3 setup.py
```

### Manual Installation

1. Copy `chroncli.py` to a directory in your PATH
2. Make it executable: `chmod +x chroncli.py`
3. Run it: `chroncli.py`

## Usage

After installation, simply run `chroncli` in your terminal.

### Task List Controls

- `↑/↓` - Navigate through tasks
- `a` - Add a new task
- `d` - Delete the selected task
- `Space` - Toggle task completion
- `q` - Quit the application

### Calendar Controls

- `p` - Previous month
- `n` - Next month

### Task Entry Controls

- `Enter` - Move to next field
- `Tab` - Save task
- `Esc` - Cancel and return to task list

## Data Storage

All tasks are stored in `~/.ad_dev_chroncli/tasks.json` and are automatically saved when changes are made.

## Customization

You can customize the appearance by modifying the source code. The curses color pairs are defined in the `ChronCLI` class initialization.

## Uninstallation

To uninstall, simply delete:

1. The installed script: `rm -rf ~/ad_dev_chroncli`
2. The symlink: `rm ~/bin/chroncli`
3. The data directory: `rm -rf ~/.ad_dev_chroncli`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
