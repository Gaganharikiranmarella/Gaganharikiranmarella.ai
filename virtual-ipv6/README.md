Virtual-IPv6
A simple Java client-server project that simulates sending a secret “virtual IPv6 address” between a client and server. Everything sent is checked for the right secret, and access is denied for anyone who sends the wrong code.

Features
Mini client & server using TCP sockets in Java.

The server only talks to clients that know the secret virtual IPv6 address (token).

If you send the wrong token, you get “Unauthorized Access”.

Includes a sample “attacker” program to demonstrate failed access.

Does not use Maven or Gradle—just the plain Java JDK/tools.

Directory Structure
text
src/
  main/java/com/virtualipv6/
    shared/SharedConfig.java    # constants used everywhere
    server/Server.java         # server app
    client/Client.java         # client app
    attacker/ThirdParty.java   # attacker (wrong token demo)
How To Build And Run (No Maven, No Gradle)
1. Prerequisites
Make sure you have Java (JDK) installed and on your PATH.

Run these in your terminal:

text
java -version
javac -version
If these show a version >= 17, you’re ready.

2. Compile The Code
In your project root (the folder with src/):

Windows:

shell
mkdir out
javac -encoding UTF-8 -d out src\main\java\com\virtualipv6\shared\SharedConfig.java src\main\java\com\virtualipv6\server\Server.java src\main\java\com\virtualipv6\client\Client.java src\main\java\com\virtualipv6\attacker\ThirdParty.java
Linux/Mac/WSL:

shell
mkdir -p out
javac -encoding UTF-8 -d out src/main/java/com/virtualipv6/shared/SharedConfig.java src/main/java/com/virtualipv6/server/Server.java src/main/java/com/virtualipv6/client/Client.java src/main/java/com/virtualipv6/attacker/ThirdParty.java
3. Run The Server
In terminal/tab #1:

shell
java -cp out com.virtualipv6.server.Server
You should see something like:

text
Server listening on 9000
4. Run The Client
In terminal/tab #2:

shell
java -cp out com.virtualipv6.client.Client
You should see:

text
Authorized by server.
Server says: ECHO: Hello secure world
5. Try The Attacker (Fails by Design)
In terminal/tab #3:

shell
java -cp out com.virtualipv6.attacker.ThirdParty
Expected:

text
Server replied: Unauthorized Access
Configuration
You can change the secret token or listening port in SharedConfig.java. Be sure both client and server use the same values.

Troubleshooting
“Could not find or load main class...”
Check that you are using -cp out and the case/package matches.

Port in use?
Change SERVER_PORT in SharedConfig or close other Java processes.

Nothing prints or appears stuck?
Be sure you started the server first, then the client (and attacker last).
Check that out.flush() and out.newLine() are always used after writing.

Author
Designed by Marella Gagan Hari Kiran
For educational use and simple socket/project-based learning.