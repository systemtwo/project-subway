Project Subway
==============
Distributed caching system for unencrypted http-bound network resources such as images and stylesheets.

Introduction
------------
Typically, the connection between an internal network and an external network--such as the internet--is much slower than the connection between computers in the internal network. This project aims to cache resources from the www on the harddrives of internal users, making these resources load faster.

Design
------
Each client is also a server. Servers are contacted by interested clients. After this initial connection, the databases are syncronized. As items are added or updated, this synconization continues.

    Server <---{resource list}---> Client

A proxy is then built on top of the network (which operates separately, on a scheduled basis) which allows web browsers to access the resources. Local files are not retrieved by the network, but by direct proxy access.

Sync Protocol
-------------
Packets look like this: 
This is not right :( 
It changed a lot, so don't use the following for any reference

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
