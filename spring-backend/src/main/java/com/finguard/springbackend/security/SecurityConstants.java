package com.finguard.springbackend.security;

public final class SecurityConstants {

    private SecurityConstants() {
    }

    public static final String JWT_ALGORITHM = "HmacSHA256";

    public static final long JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60;

    public static final String JWT_SECRET_KEY_ENV = "JWT_SECRET_KEY";
}