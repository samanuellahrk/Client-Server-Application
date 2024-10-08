# **Client-Server File Sharing Application**

## **Introduction**

This document presents the design and implementation of a client-server file sharing application utilizing TCP sockets. The system allows clients to upload and download files from a shared server, with the option to specify if the file is 'open' or 'protected.' A validation mechanism ensures file integrity, where the sender attaches extra validation information, and the receiver checks that the file matches the original.

Key features include:
- **File Upload and Download**: Clients can send and receive files from the server.
- **File Status**: Files can be marked as 'open' or 'protected' during upload.
- **File Validation**: A mechanism verifies that files remain unaltered during transfer.
- **File Listing**: Clients can query the server for a list of available files.
- **Command Line Arguments**: Users can specify server IP and port when connecting.

## **Design and Functionality**

The application is a multithreaded client-server model utilizing TCP sockets for reliable file transfer. TCP guarantees reliable data transmission between devices by managing flow control and congestion, making it ideal for file sharing.

### **Concurrent TCP Server**

The application employs a concurrent TCP server, allowing multiple clients to connect simultaneously using distinct port numbers. The server listens on a specified port and serves multiple clients concurrently via threading.

### **Protocol Design**

The protocol for communication between the client and server is based on TCP. The server uses `bind()` to associate itself with an IP address and `listen()` to wait for incoming connections. When a client attempts to connect using a specific IP address and port, the server responds using `accept()`. The server then returns to the listening state, allowing multiple connections via threading.

Once connected, the client can upload, download, or list available files using the `send()` and `recv()` data transfer functions. The client provides the relevant information (file details, actions), and the server processes the request.

### **Message Structure**

Messages between the client and server follow a structured format to ensure compatibility. The TCP header includes:
- **Source Port**: Port on the client side.
- **Destination Port**: Server port, which is fixed at 5050.
- **Sequence Number**: To ensure ordered delivery.

The application uses a message header (64-byte fixed size) containing metadata such as the filename, file size, and hash value for file validation. The socket type is `SOCK_STREAM`, and the address family is `AF_INET`.

---

## **How To Use**

### 1. **Setting Up the Application**

1. **Extracting the ZIP folder**  
   - Open the provided zip folder and copy **all contents** into a new folder, including the `ServerFiles` and `Client_Files` directories.
   - Use this newly created folder to run and test the files.

### 2. **Contents of the ZIP Folder**

- The ZIP file contains the following:
  - `Server.py` - The main server script.
  - `ServerDetails.py` - Configuration file for server details.
  - `client.py` - Client scripts (3 versions for different client instances).
  - `ServerFiles` - Directory to store files on the server.
  - `Client_Files` - Directory for client-side files.

**Important:** Ensure all the contents from the zip folder are copied into the new folder to avoid issues while running the program.

### 3. **File Handling**

- To simplify the file upload/download process, ensure that the files are located in the **same directory** as the submitted client and server scripts.

### 4. **Running the Application**

1. **Starting the Server**
   - Run the server script to start listening for client connections.
   
2. **Starting the Client**
   - Use the command line to start the client and connect to the server using the following format:

   ```bash
   python client.py <server_ip_address> 5050 <request_type>
   ```

   - Replace `<server_ip_address>` with the server's IP and `<request_type>` with the action (upload/download/list).

---

This setup allows you to use the application effectively while ensuring proper configuration and file handling.
