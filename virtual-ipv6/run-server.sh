#!/usr/bin/env bash
# Run server from project root
mvn -q compile exec:java -Dexec.mainClass="com.virtualipv6.server.Server"