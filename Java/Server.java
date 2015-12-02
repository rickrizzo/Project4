import java.io.*;
import java.net.*;

class Server {
	public static void main(String argv[]) throws Exception {
		String clientSentence;
		ServerSocket socket = new ServerSocket(6789);

		System.out.println("Starting server on port 6789...");

		while(true) {
			Socket connection = socket.accept();
			BufferedReader clientInput = new BufferedReader(new InputStreamReader(connection.getInputStream()));
			DataOutputStream clientOutput = new DataOutputStream(connection.getOutputStream());
			clientSentence = clientInput.readLine();
			System.out.println("Recieved: " + clientSentence);
			clientSentence = clientSentence.toUpperCase() + '\n';
			clientOutput.writeBytes(clientSentence);
		}
	}
}