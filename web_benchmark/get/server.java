import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;


public class server {
    
    static class GetHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String method = exchange.getRequestMethod();
            String path = exchange.getRequestURI().getPath();
            String response ;
            
            if (!method.equals("GET")) {
                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.sendResponseHeaders(405, 0);
                try (OutputStream os = exchange.getResponseBody()) {
                    
                    String error = "{\"error\": \"Method Not Allowed\"}";
                    os.write(error.getBytes(StandardCharsets.UTF_8));
                }
                return;
            }
            
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            
            
            if (path.equals("/")) {
                response = "{\"status\": \"success\", \"message\": \"Hello Benchmark\", \"language\": \"Java\"}";
                
                
                exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);
            } else if (path.equals("/health")) {
                response = "{\"status\": \"healthy\"}";
                exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);
            } else if (path.startsWith("/api/data")) {
                
                response = "{\"data\": \"benchmark_data\", \"timestamp\": 1234567890, \"value\": 42}";
                exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);
            } else {
                String error = "{\"error\": \"Not found\"}";
                response = error;
                exchange.sendResponseHeaders(404, response.getBytes(StandardCharsets.UTF_8).length);
            }
            
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(response.getBytes(StandardCharsets.UTF_8));
            }
        }
    }
    
    public static void main(String[] args) throws IOException {
        String portStr = System.getenv("PORT");
        int port = portStr != null ? Integer.parseInt(portStr) : 8005;
        
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 0);
        server.createContext("/", new GetHandler());
        server.createContext("/health", new GetHandler());
        server.createContext("/api/data", new GetHandler());
        server.setExecutor(null);
        
        System.err.println("Java GET Server running on port " + port);
        server.start();
    }
}
