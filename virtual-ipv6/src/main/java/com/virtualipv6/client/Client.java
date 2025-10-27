package com.virtualipv6.client;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

import com.virtualipv6.shared.SharedConfig;

public class Client {
    public static void main(String[] args) {
        String host = "127.0.0.1";
        int port = SharedConfig.SERVER_PORT;

        try (Socket sock = new Socket(host, port);
             BufferedReader in = new BufferedReader(
                 new InputStreamReader(sock.getInputStream(), StandardCharsets.UTF_8));
             BufferedWriter out = new BufferedWriter(
                 new OutputStreamWriter(sock.getOutputStream(), StandardCharsets.UTF_8))) {

            out.write(SharedConfig.SECRET_IPV6_TOKEN);
            out.newLine();
            out.flush();

            String resp = in.readLine();
            if (!"OK".equals(resp)) {
                System.out.println("Handshake failed: " + resp);
                return;
            }

            out.write("Hello secure world");
            out.newLine();
            out.flush();

            String echo = in.readLine();
            if (echo != null) System.out.println("Server says: " + echo);

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
