import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import org.json.JSONObject;

public class server {
    
    static class GetHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String method = exchange.getRequestMethod();
            String path = exchange.getRequestURI().getPath();
            
            if (!method.equals("GET")) {
                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.sendResponseHeaders(405, 0);
                try (OutputStream os = exchange.getResponseBody()) {
                    JSONObject error = new JSONObject();
                    error.put("error", "Method Not Allowed");
                    os.write(error.toString().getBytes(StandardCharsets.UTF_8));
                }
                return;
            }
            
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            byte[] response;
            
            if (path.equals("/")) {
                JSONObject json = new JSONObject();
                json.put("status", "ok");
                json.put("message", "Hello from Java GET Server");
                json.put("language", "Java");
                response = json.toString().getBytes(StandardCharsets.UTF_8);
                exchange.sendResponseHeaders(200, response.length);
            } else if (path.equals("/health")) {
                JSONObject json = new JSONObject();
                json.put("status", "healthy");
                response = json.toString().getBytes(StandardCharsets.UTF_8);
                exchange.sendResponseHeaders(200, response.length);
            } else if (path.startsWith("/api/data")) {
                JSONObject json = new JSONObject();
                json.put("data", "benchmark_data");
                json.put("timestamp", 1234567890);
                json.put("value", 42);
                response = json.toString().getBytes(StandardCharsets.UTF_8);
                exchange.sendResponseHeaders(200, response.length);
            } else {
                JSONObject json = new JSONObject();
                json.put("error", "Not found");
                response = json.toString().getBytes(StandardCharsets.UTF_8);
                exchange.sendResponseHeaders(404, response.length);
            }
            
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(response);
            }
        }
    }
    
    public static void main(String[] args) throws IOException {
        String portStr = System.getenv("PORT");
        int port = portStr != null ? Integer.parseInt(portStr) : 8080;
        
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 0);
        server.createContext("/", new GetHandler());
        server.createContext("/health", new GetHandler());
        server.createContext("/api/data", new GetHandler());
        server.setExecutor(null);
        
        System.err.println("Java GET Server running on port " + port);
        server.start();
    }
}
