package com.virtualipv6.server;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

import com.virtualipv6.shared.SharedConfig;

public class Server {
    public static void main(String[] args) {
        System.out.println("Starting server on port " + SharedConfig.SERVER_PORT);
        try (ServerSocket ss = new ServerSocket(SharedConfig.SERVER_PORT)) {
            System.out.println("Server listening on " + SharedConfig.SERVER_PORT);
            while (true) {
                try (Socket sock = ss.accept();
                     BufferedReader in = new BufferedReader(
                         new InputStreamReader(sock.getInputStream(), StandardCharsets.UTF_8));
                     BufferedWriter out = new BufferedWriter(
                         new OutputStreamWriter(sock.getOutputStream(), StandardCharsets.UTF_8))) {

                    String token = in.readLine();
                    if (token == null || !SharedConfig.SECRET_IPV6_TOKEN.equals(token)) {
                        out.write("Unauthorized Access");
                        out.newLine();
                        out.flush();
                        continue;
                    }

                    out.write("OK");
                    out.newLine();
                    out.flush();

                    String msg = in.readLine();
                    if (msg != null) {
                        out.write("ECHO: " + msg);
                        out.newLine();
                        out.flush();
                    }
                } catch (IOException e) {
                    System.out.println("Connection error: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            throw new RuntimeException("Failed to bind server socket", e);
        }
    }
}
