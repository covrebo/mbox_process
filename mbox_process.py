import mailbox
import os
import csv
import argparse

############################
### PARSE CLI ARGUEMENTS ###
############################

# Create the parser
my_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
my_parser.add_argument('file_name',
                       action='store',
                       help='Name of file to be processed.')

my_parser.add_argument('dir_name',
                       action='store',
                       help='Name of directory to store messages.')

# Execute the parse_args() method
args = my_parser.parse_args()

###################################
### PREPARE FOR FILE PROCESSING ###
###################################

# set the message index
msg_num = 1

# get filename from user
file_name = args.file_name

# get directory to store messages in from user
dir_name = args.dir_name

# check if the directory exists
if not os.path.isdir(dir_name):
    # make a folder for this email (named after the subject)
    os.mkdir(dir_name)

# create a list to store information on each message to be written to csv
csv_headers = ['Message', 'From', 'To', 'Date', 'Subject', 'Attachment', 'PNG', 'JPG']
email_list = []

# create a complete list of all the email in one text string to create a file later
all_messages_text = f'### ###  ALL MESSAGES  ### ### \n'

#########################
### PROCESS MBOX FILE ###
#########################

# iterate over messages
for idx, message in enumerate(mailbox.mbox(file_name)):
    # create a folder for the message
    folder_name = f"{dir_name}/msg-{idx + 1}"
    prev_folder = f"{dir_name}/msg-{idx}"
    if not os.path.isdir(folder_name):
        # make a folder for this email (named after the subject)
        os.mkdir(folder_name)

    # add message to summary list for csv
    msg_dict_temp = {
        'Message': idx + 1,
        'From': message['from'],
        'To': message['to'],
        'Date': message['date'],
        'Subject': message['subject'],
        'Attachment': "N",
        'PNG': "N",
        'JPG': "N"
    }


    # add header info to full message
    full_message = f'''\n### ### ### Start Message {idx + 1}  ### ### ### \n
TO: {message['to']}
FROM: {message['from']}
DATE: {message['date']}
SUBJECT: {message['subject']}

CONTENT:
    '''

# add html header info to full message
    html_header = f'''\n### ### ### Start Message {idx + 1}  ### ### ### \n </br>
TO: {message['to']}</br>
FROM: {message['from']}</br>
DATE: {message['date']}</br>
SUBJECT: {message['subject']}</br>
</br>
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
                full_message_text = full_message + f"{body}"

                # add the body of the message to the full emails variable
                all_messages_text += full_message + f"{body}"

                # write the message to a file
                # name the file
                filename = f"msg-{idx + 1}.txt"
                filepath = os.path.join(folder_name, filename)
                # check if file exists to append
                if os.path.exists(filepath):
                    # append additional text to existing file
                    open(filepath, "a").write(body)
                else:
                    # write the file
                    open(filepath, "w").write(full_message_text)

            # save html text of email
            elif content_type == "text/html":
                # add the body of the message
                full_message_html = html_header + f"CONTENT: \n{body}"

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
                full_message_mixed = full_message + f"CONTENT: \n{body}"

                # write the message to a file
                # name the file
                filename = f"msg-{idx}-mxd.html"
                filepath = os.path.join(prev_folder, filename)
                # write the file
                open(filepath, "w").write(full_message_mixed)

            # save png attachments
            elif content_type == "image/png":
                # update email summary list
                msg_dict_temp['PNG'] = "Y"
                # download attachment
                attachment_name = part.get_filename()
                if attachment_name:
                    filepath = os.path.join(folder_name, attachment_name)
                    # download attachment and save it
                    open(filepath, "wb").write(part.get_payload(decode=True))

            # save jpg attachments
            elif content_type == "image/jpeg":
                # update email summary list
                msg_dict_temp['JPG'] = "Y"
                # download attachment
                attachment_name = part.get_filename()
                if attachment_name:
                    filepath = os.path.join(folder_name, attachment_name)
                    # download attachment and save it
                    open(filepath, "wb").write(part.get_payload(decode=True))

            # save email attachment
            elif "attachment" in content_disposition:
                # update email summary list
                msg_dict_temp['Attachment'] = "Y"
                # download attachment
                attachment_name = part.get_filename()
                if attachment_name:
                    filepath = os.path.join(folder_name, attachment_name)
                    # download attachment and save it
                    open(filepath, "wb").write(part.get_payload(decode=True))

        # append final message dict to email summary list
        email_list.append(msg_dict_temp)

    else:
        if message.get_content_type() == "text/plain":
            for part in message.walk():
                # add the body of the message
                try:
                    # get the email body
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                full_message_text = full_message + f"{body}"

                # add the body of the message to the full emails variable
                all_messages_text += full_message + f"{body}"

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
                full_message_text = html_header + f"CONTENT: \n{body}"

                # add the body of the message to the full emails variable
                all_messages_text += full_message + f"{body}"

                # write the message to a file
                # name the file
                filename = f"msg-{idx + 1}.html"
                filepath = os.path.join(folder_name, filename)
                # write the file
                open(filepath, "a+").write(full_message_text)
        else:
            print(f"MESSAGE SKIPPED {idx + 1}")

# write the full emails variable to a text file
# name the file
filename = f"ALL-{dir_name}.txt"
filepath = os.path.join(dir_name, filename)
# write the file
open(filepath, "w").write(all_messages_text)

# write email summary to csv
with open(f'{dir_name}/{dir_name}.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(email_list)