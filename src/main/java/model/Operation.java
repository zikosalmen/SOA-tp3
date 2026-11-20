package model;

import java.io.Serializable;

public class Operation implements Serializable {

    private double a;
    private double b;
    private String operation;
    private double resultat;
    private String statut;

    public Operation() {
    }

    public Operation(double a, double b, String operation, double resultat, String statut) {
        this.a = a;
        this.b = b;
        this.operation = operation;
        this.resultat = resultat;
        this.statut = statut;
    }

    public double getA() {
        return a;
    }

    public void setA(double a) {
        this.a = a;
    }

    public double getB() {
        return b;
    }

    public void setB(double b) {
        this.b = b;
    }

    public String getOperation() {
        return operation;
    }

    public void setOperation(String operation) {
        this.operation = operation;
    }

    public double getResultat() {
        return resultat;
    }

    public void setResultat(double resultat) {
        this.resultat = resultat;
    }

    public String getStatut() {
        return statut;
    }

    public void setStatut(String statut) {
        this.statut = statut;
    }
}
