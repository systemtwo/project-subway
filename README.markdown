Project Subway
==============
Distributed caching system for unencrypted http-bound network resources such as images and stylesheets.

Introduction
------------
Typically, the connection between an internal network and an external network--such as the internet--is much slower than the connection between computers in the internal network. This project aims to cache resources from the www on the harddrives of internal users, making these resources load faster.

Design
------
Each client is also a server. Servers broadcast their precense, and are then contacted by interested clients. After this initial connection, the databases are syncronized. As items are added or updated, this synconization continues.

    Server <---{resource list}---> Client

Sync Protocol
-------------
Packets look like this: 
 - Header: single byte
 - Length: short (2 bytes)
 - Data: varies (up to 255*2 bytes)

Handshake:
 - Header: 0x01
 - Data:
  - Version: 2 bytes
  - More tpd

Resource:
 - Header: 0x02
 - Data:
  - Name Hash (sha1): 128 bytes
  - Last-modified (unix time): 4 bytes