import mailbox
import os

# set the message index
msg_num = 1

# get filename from user
file_name = input("What is the filename: ")

# get directory to store messages in from user
dir_name = input("What is the directory name: ")

# check if the directory exists
if not os.path.isdir(dir_name):
    # make a folder for this email (named after the subject)
    os.mkdir(dir_name)

# iterate over messages
for idx, message in enumerate(mailbox.mbox(file_name)):
    # create a folder for the message
    folder_name = f"{dir_name}/msg-{idx + 1}"
    prev_folder = f"{dir_name}/msg-{idx}"
    if not os.path.isdir(folder_name):
        # make a folder for this email (named after the subject)
        os.mkdir(folder_name)

    # add header info to full message
    full_message = f'''### ### ### Start Message {idx + 1} from {file_name} ### ### ###
TO: {message['to']}
FROM: {message['from']}
DATE: {message['date']}
SUBJECT: {message['subject']}

CONTENT:
    '''

    # iterate through each message
    if message.is_multipart():
        # iterate over the message parts
        for part in message.walk():
            # get email content
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            # print(f"Msg: {idx +1}")
            # print(content_type)
            # print(content_disposition)
            try:
                # get the email body
                body = part.get_payload(decode=True).decode()
            except:
                pass

            # save plain text of email
            if content_type == "text/plain":
                # add the body of the message
                full_message_text = full_message + f"{body}" + "<-- -- END MESSAGE -- --> \n"

                # write the message to a file
                # name the file
                filename = f"msg-{idx + 1}.txt"
                filepath = os.path.join(folder_name, filename)
                # write the file
                open(filepath, "a+").write(full_message_text)

            # save html text of email
            elif content_type == "text/html":
                # add the body of the message
                full_message_html = full_message + f"CONTENT: \n{body}" + "<-- -- END MESSAGE -- --> \n"

                # write the message to a file
                # name the file
                filename = f"msg-{idx + 1}.html"
                filepath = os.path.join(folder_name, filename)
                # write the file
                open(filepath, "a+").write(full_message_html)

            # multipart/mixed messages
            # BUG writes to wrong folder and wrong file name (+1)
            elif content_type == "multipart/mixed":
                # add the body of the message
                full_message_mixed = full_message + f"CONTENT: \n{body}" + "<-- -- END MESSAGE -- --> \n"

                # write the message to a file
                # name the file
                filename = f"msg-{idx}-mxd.html"
                filepath = os.path.join(prev_folder, filename)
                # write the file
                open(filepath, "w").write(full_message_mixed)

            # save png attachments
            elif content_type == "image/png":
                # download attachment
                attachment_name = part.get_filename()
                if attachment_name:
                    filepath = os.path.join(folder_name, attachment_name)
                    # download attachment and save it
                    open(filepath, "wb").write(part.get_payload(decode=True))

            # save jpg attachments
            elif content_type == "image/jpeg":
                # download attachment
                attachment_name = part.get_filename()
                if attachment_name:
                    filepath = os.path.join(folder_name, attachment_name)
                    # download attachment and save it
                    open(filepath, "wb").write(part.get_payload(decode=True))

            # save email attachment
            elif "attachment" in content_disposition:
                # download attachment
                attachment_name = part.get_filename()
                if attachment_name:
                    filepath = os.path.join(folder_name, attachment_name)
                    # download attachment and save it
                    open(filepath, "wb").write(part.get_payload(decode=True))

    else:
        if message.get_content_type() == "text/plain":
            for part in message.walk():
                # add the body of the message
                try:
                    # get the email body
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                full_message_text = full_message + f"{body}" + "<-- -- END MESSAGE -- --> \n"

                # write the message to a file
                # name the file
                filename = f"msg-{idx + 1}.txt"
                filepath = os.path.join(folder_name, filename)
                # write the file
                open(filepath, "a+").write(full_message_text)
        elif message.get_content_type() == "text/html":
            for part in message.walk():
                # add the body of the message
                try:
                    # get the email body
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                full_message_text = full_message + f"{body}" + "<-- -- END MESSAGE -- --> \n"

                # write the message to a file
                # name the file
                filename = f"msg-{idx + 1}.html"
                filepath = os.path.join(folder_name, filename)
                # write the file
                open(filepath, "a+").write(full_message_text)
        else:
            print(f"MESSAGE SKIPPED {idx + 1}")