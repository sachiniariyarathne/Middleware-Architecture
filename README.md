# 📡 Middleware Architectures: Publish/Subscribe System

**Course:** IS3108 / SCS3203  
**Assignment 01 — UCSC 2025**  
**Language:** Python  

---

## Objective

This project implements a **simple Publish/Subscribe (Pub/Sub) middleware** using **Client-Server socket programming** in Python. It simulates asynchronous messaging where clients act as publishers or subscribers and communicate via topics.

---

## Assignment Tasks Overview

### Task 1: Basic Client-Server Communication
- Build a simple client-server system using TCP sockets.
- Server listens on a given port.
- Client connects with IP and port.
- Messages typed by client are printed on the server terminal.
- Typing `terminate` disconnects the client.

### Task 2: Publishers and Subscribers
- Server handles multiple concurrent clients.
- Clients specify if they are `PUBLISHER` or `SUBSCRIBER`.
- Messages from publishers are **broadcasted only to subscribers**.
- Multiple publishers and subscribers can run simultaneously.

### Task 3: Topic-Based Filtering
- Each client provides a **topic/subject** as an additional argument.
- Server forwards messages only to **subscribers of the same topic**.
- Subscribers to unknown topics are rejected.

---

## How to Run the Project (Terminal Instructions)

### Prerequisites
- Python 3 installed
- Use separate terminal tabs/windows for each client and server

---

### Start the Server and then client

```bash
python server.py <PORT>

python client.py <SERVER_IP> <PORT> <ROLE> <TOPIC>


