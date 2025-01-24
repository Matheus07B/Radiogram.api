import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class main {
    public static void main(String[] args) {
        try {
            // URL do endpoint que retorna usuários
            String apiUrl = "http://localhost:5000/listar-usuarios";

            // Configuração da conexão
            URL url = new URL(apiUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET"); // Método GET
            conn.setRequestProperty("Accept", "application/json"); // Aceita JSON como resposta

            // Código de resposta da API
            int responseCode = conn.getResponseCode();
            if (responseCode == 200) { // OK
                // Leitura da resposta
                BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = in.readLine()) != null) {
                    response.append(line);
                }
                in.close();

                // Exibe a resposta (os usuários)
                System.out.println("Lista de usuários do banco de dados:");
		//System.out.print("\n");
                System.out.println(response.toString());
            } else {
                System.out.println("Erro ao conectar com a API. Código HTTP: " + responseCode);
            }

            conn.disconnect(); // Encerra a conexão
        } catch (Exception e) {
            e.printStackTrace(); // Exibe qualquer erro
        }
    }
}
