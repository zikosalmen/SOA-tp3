package rest;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import model.Operation;
import service.Calculatrice;

@Path("/calculatrice")
public class CalculRest {

    private final Calculatrice calculatrice = new Calculatrice();

    @GET
    @Path("/addition")
    @Produces(MediaType.APPLICATION_JSON)
    public Response addition(@QueryParam("a") double a, @QueryParam("b") double b) {
        double resultat = calculatrice.addition(a, b);
        Operation op = new Operation(a, b, "addition", resultat, "SUCCESS");
        return Response.ok(op).build();
    }

    @GET
    @Path("/soustraction")
    @Produces(MediaType.APPLICATION_JSON)
    public Response soustraction(@QueryParam("a") double a, @QueryParam("b") double b) {
        double resultat = calculatrice.soustraction(a, b);
        Operation op = new Operation(a, b, "soustraction", resultat, "SUCCESS");
        return Response.ok(op).build();
    }

    @GET
    @Path("/multiplication")
    @Produces(MediaType.APPLICATION_JSON)
    public Response multiplication(@QueryParam("a") double a, @QueryParam("b") double b) {
        double resultat = calculatrice.multiplication(a, b);
        Operation op = new Operation(a, b, "multiplication", resultat, "SUCCESS");
        return Response.ok(op).build();
    }

    @GET
    @Path("/division")
    @Produces(MediaType.APPLICATION_JSON)
    public Response division(@QueryParam("a") double a, @QueryParam("b") double b) {
        if (b == 0.0) {
            Operation op = new Operation(a, b, "division", 0.0, "ERREUR: Division par zero impossible");
            return Response.status(Response.Status.BAD_REQUEST).entity(op).build();
        }
        double resultat = calculatrice.division(a, b);
        Operation op = new Operation(a, b, "division", resultat, "SUCCESS");
        return Response.ok(op).build();
    }
}
