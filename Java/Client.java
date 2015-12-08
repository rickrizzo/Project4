import java.io.*;
import java.net.*;

class Client{
	public static void main(String argv[]) throws Exception{
		String sentence;
		BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in));
		Socket clientSocket = new Socket("localhost", 8765);
		DataOutputStream toServer = new DataOutputStream(clientSocket.getOutputStream());
		BufferedReader serverInput = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
		sentence = userInput.readLine();
		toServer.writeBytes(sentence + '\n');
		sentence = serverInput.readLine();
		System.out.println("FROM SERVER: " + sentence);
		clientSocket.close();
	}
}