# mbox_process
mbox_process is a python script to process an mbox email file to save each message as a file in a directory, along with any associated images and attachments.

## Description
[mbox email files](https://en.wikipedia.org/wiki/Mbox) are single text files used to contain collections of email. Email exports, including [Google Takeout](https://en.wikipedia.org/wiki/Google_Takeout) and [Google Vault](https://en.wikipedia.org/wiki/Google_Workspace#Google_Vault), use the mbox format as a choice (along with PST). This utility will take an mbox file as input and save all of the messages in a directory. Each message will be saved within it's own directory along with any images or attachments included in the original message.  

The exported messages will include the sender, recipient, date received, subject, and email body in `.txt` (for plain/text messages) or `.html` (for plain/html messages) format. In addition to the message, any `png` or `jpg` images and attachments included in the email will be saved in the directory with the original message. Additional email metadata can be included by modifying the script.

## Getting Started

### Dependencies

* Tested and run in Python 3.9 an Python 3.10
* Requires `mailbox`, `os`, and `csv` libraries, which are included in the standard Python library

### Executing program

* Navigate in terminal to directory that contains mbox file
* Clone repository to directory or copy script to file named `mbox_process.py`
* Usage:
```
$ python3 mbox_process.py [FILENAME] [DIRECTORY NAME]
```
* The mbox file that will be processed must be in the same directory as the script
* Example final directory structure:
```bash
Directory
|
|---example.mbox
|---example
    |---msg-1
    |   |---msg-1.txt
    |   |---msg-1.html
    |---msg-2
    |   |---msg-2.txt
    |---msg-3
    |   |---msg-3.html
    |---msg-4
    |   |---msg-4.txt
    |   |---msg-4.html
    |   |---image.png
    |---msg-5
        |---msg-5.txt
        |---msg-5.html
        |---attachment.pdf
        |---screenshot.jpg
```
* Notes on above example
  * `msg-1` is a multipart message with both `content_type` of `plain/text` and `plain/html`
  * `msg-2` is a message with only a `content_type` of `plain/text`
  * `msg-3` is a message with only a `content_type` of `plain/html`
  * `msg-4` is a multipart message with both `content_type` of `plain/text` and `plain/html` and a `png` image named `image.png`
  * `msg-5` is a multipart message with both `content_type` of `plain/text` and `plain/html` and a `jpg` image named `screenshot.png` and an attachment call `attachment.pdf`

## Authors

Chris Ovrebo  
[@IMChrisOvrebo](https://twitter.com/imchrisovrebo)

## Version History

* 21.10.21
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [Python Mailbox Documentation](https://docs.python.org/3/library/mailbox.html#)
* [How to Read Emails with Python from PythonCode](https://www.thepythoncode.com/article/reading-emails-in-python)
