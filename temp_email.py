from tempmail import EMail
import time

def main():
    # Create a new temporary email instance
    email = EMail()

    # Display the generated email address
    print(f"Your temporary email address is: {email.address}")

    # Wait for incoming messages
    print("Waiting for new messages...")

    try:
        while True:
            # Retrieve all messages in the inbox
            inbox = email.get_inbox()

            if inbox:
                for msg_info in inbox:
                    msg = msg_info.message
                    print(f"\nFrom: {msg.from_addr}")
                    print(f"Subject: {msg.subject}")
                    print(f"Body:\n{msg.body}")

                    # Check for attachments
                    if msg.attachments:
                        for attachment in msg.attachments:
                            data = attachment.download()
                            # Save the attachment to a file
                            with open(attachment.filename, 'wb') as f:
                                f.write(data)
                            print(f"Attachment '{attachment.filename}' saved.")
            else:
                print("No new messages.")

            # Wait before checking again
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
