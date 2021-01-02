# cleanup_script_python
Never have time to organize your downloads folder? Fear no more, run this script and it'll organize your files for you

*By Jonathan Mancia*

## Application Type

**Command Line Interface**

## Description

> Organizes loose files into directories by file type.

## Requirements

1. The script shall be called from any directory in the filesystem.
2. The script, by default, shall organize files in the directory in which the script was called in.
3. The script shall be capable of overriding the default directory path to organize files in.
4. The script shall confirm the directory path with the user before organizing the files.
5. The script shall, by default, create folders by the file type (extension) in the current working directory or in the directory specified by the user. 
6. The script shall move files to the folders named after their file type.
7. The script shall move files with no particular file extension to a directory named "other".
8. The script shall allow the user to override the output folder names by adding a postfix. Example: pdf_<postfix> or default pdf

### Wish List

- [x]  Have a copy option to copy files into their respective folders instead of moving them

## Syntax Usage

```bash
*******************************************************************************
* Name: cleanup
*
* Syntax: 
*   cleanup [--path </your/path>] [--copy] [--postfix <postfix name>]
* 
*   --path, by default the current working directory will be used
*.  --copy, by default files are moved, this option copies instead
*   --postfix, by default the directories created will follow the naming
*                  convention of the files in current working directory. If
*                  postfix name is provided, the directory names will follow
*                  'png_<postfix>' naming pattern.
***************************************************************************
```

## Interface

```python
cleanup = CleanUp(path='.', postfix='')

cleanup.organize() # ie. png
```
