# FileIndexer

File indexing tools.


Functionalities will be:

- finding duplicated files
- associating tags to files
- detect changes in directory content
- searching for PDFs by author, title, keyword, content


## notes

During this phase of the project everything should be a CLI tool, as this allows for easy integration with unix utilities.

For example:

```.sh
python updateDirlisting.py docs
cat docs.fhl | sort -n -k4 | tail | cut -f4,5,6
```
will show 10 biggest files inside `docs` folder or its sub-folders.
