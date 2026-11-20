package serveur;

import org.glassfish.grizzly.http.server.HttpServer;
import org.glassfish.jersey.grizzly2.httpserver.GrizzlyHttpServerFactory;
import rest.RestApplication;

import java.io.IOException;
import java.net.URI;

public class ServeurREST {

    public static final String BASE_URI = "http://localhost:8080/CalculatriceREST/";

    public static HttpServer startServer() {
        RestApplication config = new RestApplication();
        return GrizzlyHttpServerFactory.createHttpServer(URI.create(BASE_URI), config);
    }

    public static void main(String[] args) throws IOException {
        final HttpServer server = startServer();
        System.out.println("Serveur REST demarre sur : " + BASE_URI + "api/");
        System.out.println("Endpoints disponibles :");
        System.out.println(" - " + BASE_URI + "api/calculatrice/addition?a=10&b=5");
        System.out.println(" - " + BASE_URI + "api/calculatrice/soustraction?a=10&b=5");
        System.out.println(" - " + BASE_URI + "api/calculatrice/multiplication?a=10&b=5");
        System.out.println(" - " + BASE_URI + "api/calculatrice/division?a=10&b=5");
        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            server.shutdownNow();
        }
    }
}
