package com.virtualipv6.attacker;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

import com.virtualipv6.shared.SharedConfig;

public class ThirdParty {
    public static void main(String[] args) {
        // Connect without sending the correct token to see Unauthorized Access
        try (Socket sock = new Socket("127.0.0.1", SharedConfig.SERVER_PORT);
             BufferedReader in = new BufferedReader(
                 new InputStreamReader(sock.getInputStream(), StandardCharsets.UTF_8))) {

            // Intentionally do not send token; just read server's expectation result.
            String line = in.readLine();
            System.out.println("Server replied: " + line);
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
